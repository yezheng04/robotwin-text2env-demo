# RoboTwin Tabletop Scene Generation Plan

更新时间：2026-07-02
所属大任务：Self-Improving Agents for Physical AI
当前项目方向：模仿 RoboTwin `code_gen` 的 agentic 思路，做自然语言到 RoboTwin tabletop scene/background 的生成系统。

---

## 0. 重新明确方向

我们现在的目标不是生成 RoboTwin task 的 `play_once()`，也不是直接训练 policy，而是生成一个可被 RoboTwin 下游任务或外部 policy 使用的桌面场景。

核心区别：

```text
RoboTwin code_gen:
  task description
  -> generate envs_gen/gpt_<task>.py::play_once()
  -> run simulator
  -> error / visual feedback
  -> repair task code

我们的项目:
  scene description
  -> asset grounding
  -> generate PlacementSpec
  -> generate reusable scene/background Python module
  -> run RoboTwin smoke / preview
  -> visual/VLM feedback
  -> repair scene placement / catalog defaults
```

一句话目标：

```text
把自然语言桌面场景描述转换成 RoboTwin 可加载、可渲染、可复用、可被视觉审核的 generated scene/background。
```

例子：

```text
Input:
  "an apple and a plate on the table"

Output:
  generated_scenes/apple_plate_scene.py
  + PlacementSpec JSON
  + prompt case catalog
  + smoke preview image/video
  + visual/VLM review report

Possible downstream task:
  "pick the apple and place it on the plate"
```

---

## 1. 新的端到端流程

重构后的主流程：

```text
Natural-language scene prompt
-> Asset Grounding Agent
-> Prompt Case Catalog
-> Designer Agent creates TabletopPlacementSpec
-> Critic validates semantic / physics / robot usability
-> Scene Code Generator writes a RoboTwin scene/background Python module
-> RoboTwin smoke render
-> Visual/VLM Critic reviews preview
-> Orchestrator repairs placement/catalog/code
-> Final generated scene artifact for downstream task/policy
```

对应文件流：

```text
prompt
-> runs/<case>/asset_grounding.json
-> asset_catalogs/prompt_cases/<case>.json
-> runs/<case>/final_placement.json
-> generated_scenes/<case>_scene.py
-> runs/<case>/smoke/
-> runs/<case>/visual_review.json
-> runs/<case>/scene_generation_summary.json
```

最终交付不应该只停在 JSON。`PlacementSpec` 是中间表示，真正给 RoboTwin 下游使用的产物应该是一个 Python scene/background loader。

---

## 2. 和 RoboTwin code_gen 的对应关系

我们借鉴 `RoboTwin/code_gen` 的机制，但不照搬目标。

| RoboTwin code_gen | 我们的 scene generation |
| --- | --- |
| `task_info.py` | `scene_info.json` / `asset_grounding.json` / prompt case |
| `prompt.py` | scene prompt + coordinate/API/asset rules |
| `task_generation_mm.py` | `scene_generation_mm.py` / harness scene loop |
| `envs_gen/gpt_<task>.py` | `generated_scenes/<scene_name>_scene.py` |
| `test_gen_code.py` | scene smoke / placement validator / visual review |
| `observation_agent.py` | scene visual/VLM critic |
| repair `play_once()` | repair pose / qpos / loader / static / catalog defaults / scene loader |

关键原则：

```text
借鉴 code_gen 的结构化输入、仿真测试、视觉反馈、迭代 repair。
不要把项目重新变成 task code generation。
```

---

## 3. 分层架构

### 3.1 Asset Grounding Layer

第一步先解决自然语言里的 objects/assets 是什么，并对应到 master asset catalog 中的哪个 RoboTwin asset。

输入：

```text
scene prompt
robotwin_tabletop_assets_master.json
```

输出：

```text
asset_grounding.json
asset_catalogs/prompt_cases/<case>.json
```

建议 schema：

```json
{
  "schema_version": "robotwin.tabletop_asset_grounding.v0",
  "prompt": "an apple and a plate on the table",
  "direction_frame": "robot_or_dual_arm_first_person",
  "matched_assets": [
    {
      "mention": "apple",
      "asset_id": "035_apple",
      "semantic_name": "apple",
      "match_type": "exact_alias",
      "confidence": 1.0,
      "reason": "Prompt mention 'apple' exactly matches alias 'apple'."
    }
  ],
  "unmatched_mentions": [],
  "spatial_relations": [
    {
      "subject_mention": "apple",
      "relation": "on_surface",
      "reference": "table"
    }
  ],
  "warnings": []
}
```

实现策略：

```text
1. deterministic exact alias / semantic_name / tag match
2. LLM ranking over available catalog entries
3. optional embedding / VLM retrieval for large asset library
4. if uncertain, mark unmatched; do not invent asset_id
```

### 3.2 Prompt Case Catalog Layer

资产库采用 master + prompt case。

```text
asset_catalogs/
  robotwin_tabletop_assets_master.json
  prompt_cases/
    apple_plate.json
    vegetable_basket.json
    laptop_knife.json
```

`robotwin_tabletop_assets_master.json` 保存可复用资产信息：

```text
asset_id
semantic_name
aliases
tags
asset_type
available_model_ids
default_model_id
scale / extents / stable
placement_defaults
affordances
points metadata
```

`prompt_cases/<case>.json` 只保存本 prompt 选了哪些资产：

```json
{
  "catalog_version": "robotwin.tabletop_asset_catalog_case.v0",
  "base_catalog": "../robotwin_tabletop_assets_master.json",
  "mvp_prompt": "an apple and a plate on the table",
  "selected_asset_ids": ["035_apple", "003_plate"],
  "entry_overrides": {}
}
```

### 3.3 PlacementSpec Layer

`TabletopPlacementSpec` 是中间表示，描述资产、空间关系、桌面 pose、物理属性和验证状态。

它回答：

```text
场景里有哪些物体？
每个物体用哪个 asset？
每个物体放在哪里？
物体之间有什么空间关系？
是否满足机器人第一视角方位？
是否可达、稳定、无碰撞？
```

注意：`PlacementSpec` 不包含 `play_once()`，不包含 `check_success()`，不描述机器人动作程序。

### 3.4 Scene Python Module Layer

为了让下游 RoboTwin task 使用，最终应该生成一个 Python scene/background module。

推荐目录：

```text
generated_scenes/
  apple_plate_scene.py
  laptop_knife_scene.py
```

建议接口：

```python
def load_scene(task, placement_spec=None):
    """Load generated tabletop scene into a RoboTwin task instance."""
    ...
    return {
        "apple_1": apple_actor,
        "plate_1": plate_actor,
    }
```

或者：

```python
class ApplePlateScene:
    scene_name = "apple_plate_scene"

    def load(self, task):
        ...
        return task.generated_scene_objects
```

下游 task 的使用方式：

```python
from generated_scenes.apple_plate_scene import load_scene

class pick_apple_to_plate(Base_Task):
    def setup_demo(self, **kwargs):
        super().setup_demo(**kwargs)
        self.generated_scene_objects = load_scene(self)
        self.apple = self.generated_scene_objects["apple_1"]
        self.plate = self.generated_scene_objects["plate_1"]
```

这一步是我们相对旧版本最大的重构：从“生成 JSON preview”升级为“生成可被 RoboTwin task import 的 scene module”。

### 3.5 Smoke / Visual / Repair Layer

生成 scene module 后，需要像 `task_generation_mm.py` 一样做闭环：

```text
generate scene
-> run smoke
-> save observer/head camera
-> visual/VLM review
-> if fail, repair placement/catalog/scene code
-> rerun
```

Visual/VLM Critic 检查：

```text
object presence
object identity
robot-centric left/right/front/back
table contact
penetration
floating
orientation
occlusion
prompt match
```

失败记录建议：

```json
{
  "attempt": 1,
  "failure_source": "visual_review",
  "failure_summary": "basket penetrates the table and appears sideways",
  "repair_target": "asset_catalogs/robotwin_tabletop_assets_master.json",
  "repair_action": "update 110_basket placement_defaults.qpos",
  "rerun_status": "pending"
}
```

---

## 4. 坐标系和方位规则

这是必须固定的约束。

RoboTwin `code_gen/prompt.py` 里写到：

```text
world x positive = right
world y positive = front
world z positive = up
```

我们项目的自然语言方位规则：

```text
left / right / front / back 默认以机器人或双臂第一视角为准。
除非 prompt 明确指定 camera view、observer view、user view 或 object-local frame。
```

这意味着：

```text
"a laptop is on the right side of a knife"
-> laptop 应放在机器人第一视角的 knife 右侧
```

不能再只看 `observer_camera.png` 的屏幕左右来决定语义是否正确，因为 observer camera 可能镜像或旋转。

---

## 5. Agents 分工

### 5.1 Asset Grounding Agent

负责从自然语言中抽取资产 mention，并匹配到 master catalog。

输出：

```text
asset_grounding.json
prompt_cases/<case>.json
```

### 5.2 Designer Agent

负责从 prompt case 和 spatial relations 生成初始 `TabletopPlacementSpec`。

输出：

```text
designer_initial_placement.json
```

### 5.3 Static Critic

负责检查：

```text
schema
asset exists
model_id exists
pose bounds
approx collision
stable_on_table metadata
robot-centric spatial relation
```

### 5.4 Scene Code Generator

负责把 `final_placement.json` 转成 Python scene/background module。

输出：

```text
generated_scenes/<case>_scene.py
```

它只生成 scene loader，不生成 task `play_once()`。

### 5.5 Visual/VLM Critic

负责读取 smoke preview，判断场景是否真的符合 prompt 和物理直觉。

输出：

```text
visual_review.json
```

### 5.6 Orchestrator

负责调度整个闭环：

```text
asset grounding
-> placement design
-> static validation
-> scene code generation
-> smoke
-> visual review
-> repair / rerun / pass / blocker
```

---

## 6. 推荐代码结构

重构后推荐目录：

```text
asset_catalogs/
  robotwin_tabletop_assets_master.json
  prompt_cases/
    apple_plate.json

generate_scene/
  asset_catalog.py
  asset_grounding.py
  model_providers.py
  schemas.py
  scene_codegen.py
  run_scene_generation_pipeline.py
  run_placement_pipeline.py              # legacy-compatible, can remain for now
  run_robotwin_placement_smoke.py
  tools.py

harness/                                # compatibility wrappers

generated_scenes/
  apple_plate_scene.py

scripts/                                # compatibility wrappers

skills/
  generate-robotwin-tabletop-scene/
  ground-objects-to-robotwin-assets/
  design-tabletop-placement/
  critique-tabletop-placement/
  orchestrate-placement-pipeline/
  review-robotwin-smoke-preview/
```

推荐新主入口：

```bash
python generate_scene/run_scene_generation_pipeline.py \
  --prompt "an apple and a plate on the table" \
  --master-catalog asset_catalogs/robotwin_tabletop_assets_master.json \
  --robotwin-root ~/RoboTwin \
  --out-dir runs/apple_plate_scene \
  --run-smoke
```

pipeline 输出：

```text
runs/apple_plate_scene/
  asset_grounding.json
  prompt_case.json
  designer_initial_placement.json
  static_validation_initial.json
  final_placement.json
  generated_scene.py
  smoke/
  visual_review.json
  scene_generation_summary.json
```

---

## 7. 当前已经完成的基础

已经完成：

- [x] RoboTwin2 环境配置在 5090：`/data/sdb/zhengye/RoboTwin`。
- [x] 项目仓库在 5090：`/data/sdb/zhengye/robotwin-text2env-demo`。
- [x] GitHub repo：`https://github.com/yezheng04/robotwin-text2env-demo`。
- [x] `TabletopPlacementSpec v0`：`generate_scene/schemas.py`。
- [x] master + prompt case asset catalog：
  - `asset_catalogs/robotwin_tabletop_assets_master.json`
  - `asset_catalogs/prompt_cases/apple_plate.json`
  - `asset_catalogs/prompt_cases/vegetable_basket.json`
  - `asset_catalogs/prompt_cases/laptop_knife.json`
- [x] prompt case loader：`generate_scene/asset_catalog.py`。
- [x] deterministic reference provider：`generate_scene/model_providers.py`。
- [x] RoboTwin placement smoke runner：`generate_scene/run_robotwin_placement_smoke.py`。
- [x] tool-style helpers：`generate_scene/tools.py`。
- [x] 顶层 handoff skill：`skills/generate-robotwin-tabletop-scene/`。
- [x] skill 中记录了 RoboTwin `code_gen` 可借鉴模式：
  - `skills/generate-robotwin-tabletop-scene/references/robotwin-code-gen-patterns.md`。
- [x] 已验证 prompt cases 可静态通过：
  - apple/plate
  - vegetable/basket
  - laptop/knife
- [x] 已明确方位判断采用机器人/双臂第一视角。
- [x] 已生成并 smoke 验证第一个 scene module：
  - `generated_scenes/apple_plate_scene.py`
  - smoke evidence: `previews/apple_plate_scene_module_smoke/`
  - result: RoboTwin smoke pass, pipeline status `pending_visual_review`

---

## 8. 下一步 TODO

### High Priority

- [x] 写 `generate_scene/asset_grounding.py`：
  - 输入自然语言 prompt + master catalog。
  - 输出 `asset_grounding.json`。
  - 自动创建 prompt case JSON。
  - 先支持 exact alias / semantic / tag match，再预留 LLM backend。

- [x] 定义 `AssetGroundingResult v0` schema。

- [x] 写 `generate_scene/scene_codegen.py`：
  - 输入 `final_placement.json`。
  - 输出 `generated_scenes/<case>_scene.py`。
  - 只生成 `load_scene(task)` 或 scene class，不生成 task `play_once()`。

- [x] 写 `generate_scene/run_scene_generation_pipeline.py`：
  - 串起 asset grounding、prompt case、placement、scene codegen、smoke、visual review。
  - 逐步替代当前 `run_placement_pipeline.py`。

- [x] 写第一个 generated scene module：
  - `generated_scenes/apple_plate_scene.py`。

- [x] 更新 smoke runner，让它能直接测试 generated scene module，而不只测试 `PlacementSpec`。

### Medium Priority

- [ ] 设计 visual/VLM review JSON schema。
- [ ] 写 repair record schema。
- [ ] 接入一个可替换 VLM backend：
  - human/Codex visual reference
  - OpenAI API
  - Qwen-VL
  - local VLM
- [ ] 把 visual feedback 接回 Orchestrator repair loop。
- [ ] 为 `apple_plate` 做一次完整 scene module smoke。

### Lower Priority

- [ ] 把 CLI harness 包成正式 MCP server。
- [ ] 支持 larger asset library / thumbnail retrieval。
- [ ] 接入 embedding / CLIP / SigLIP / VLM retrieval。
- [ ] 接下游 task 消费 scene 的示例。
- [ ] 接 external policy evaluation。

---

## 9. 最小交付物定义

重构后的最小可交付物：

```text
1. prompt:
   "an apple and a plate on the table"

2. asset grounding:
   runs/apple_plate_scene/asset_grounding.json

3. prompt case:
   asset_catalogs/prompt_cases/apple_plate.json

4. placement:
   runs/apple_plate_scene/final_placement.json

5. generated scene module:
   generated_scenes/apple_plate_scene.py

6. RoboTwin smoke:
   runs/apple_plate_scene/smoke/smoke_report.json
   runs/apple_plate_scene/smoke/observer_camera.png
   runs/apple_plate_scene/smoke/head_camera.png

7. visual review:
   runs/apple_plate_scene/visual_review.json

8. summary:
   runs/apple_plate_scene/scene_generation_summary.json
```

验收标准：

```text
static validation pass
scene module imports successfully
RoboTwin smoke pass
preview contains requested objects
robot-centric spatial relation correct
no obvious penetration/floating/orientation failure
visual/VLM review pass
```

---

## 10. 风险和处理

### Risk 1: 又滑回 task generation

处理：

- scene code generator 只允许生成 `load_scene(task)`。
- 禁止生成 `play_once()`。
- 下游 task 可以消费 scene，但不是本项目主输出。

### Risk 2: asset grounding 错误

处理：

- 先 exact alias / semantic_name / tag match。
- LLM 只能从 catalog asset_id 中选择。
- 不确定就输出 `unmatched_mentions`。
- 不允许编造 asset_id。

### Risk 3: 方位坐标混乱

处理：

- 自然语言方位默认机器人/双臂第一视角。
- RoboTwin world frame 写入 prompt 和 schema。
- visual review 不能只按 observer screen left/right 判断。

### Risk 4: JSON 通过但视觉失败

处理：

- smoke pass 不等于 visual pass。
- 必须有 human/VLM/Codex visual reference review。
- 失败原因进入 repair record。

### Risk 5: scene module 和 RoboTwin API 不兼容

处理：

- scene codegen 应该复用现有 smoke runner 中已经验证过的 loader 逻辑。
- 先生成最小 `load_scene(task)`，不要生成复杂 class hierarchy。
- 每个 generated scene module 必须 import test。

---

## 11. 远程环境和同步规则

默认远程路径：

```text
zhengye = /data/sdb/zhengye
RoboTwin = /data/sdb/zhengye/RoboTwin
project repo = /data/sdb/zhengye/robotwin-text2env-demo
```

GitHub：

```text
https://github.com/yezheng04/robotwin-text2env-demo
branch: main
```

远程连接注意事项：

```text
不要打开 /data/sdb 这种大根目录。
只打开具体项目目录。
搜索时排除 data、datasets、outputs、checkpoints、logs、wandb、venv、node_modules、__pycache__。
中间测试 runs 用完要删除。
不要提交 HDF5、完整 runs、大视频、大资产文件。
```

---

## 12. 现在最应该做的第一步

从重构角度，下一步最应该做：

```text
Step 1: Asset Grounding Agent
```

具体任务：

```text
1. 写 AssetGroundingResult v0 schema。
2. 写 deterministic asset grounding：
   prompt mention -> master catalog alias/tag match。
3. 生成 runs/<case>/asset_grounding.json。
4. 自动生成 asset_catalogs/prompt_cases/<case>.json。
5. 把这个步骤接到新的 run_scene_generation_pipeline.py 开头。
```

这一步完成后，整个系统才真正从“自然语言”开始，而不是手写 prompt case。
