# RoboTwin Tabletop Placement Agent Plan

更新时间：2026-06-30
所属大任务：Self-Improving Agents for Physical AI
当前项目方向：SceneSmith-style tabletop placement agent for downstream RoboTwin robot tasks

---

## 0. 再次明确方向

这次要更精确地区分三件事：

```text
Placement generation != task generation != policy training
```

我们现在要做的是 **placement agent**：根据自然语言和资产库决定桌面资产应该如何摆放。

也就是说，输入一句自然语言：

```text
an apple and a plate on the table
```

我们生成的应该是一个 RoboTwin 中可加载、可验证的桌面场景：

```text
table
+ apple placed on a reachable tabletop pose
+ plate placed on a reachable tabletop pose
+ physically valid poses
+ usable asset metadata
```

这个场景以后可以被下游机器人任务使用。例如，在这个场景上再定义或执行：

```text
pick the apple and place it on the plate
```

所以本项目的直接输出不是 `play_once()`、`check_success()` 或新的 RoboTwin task program，而是：

```text
simulation-ready tabletop placement / placed scene
```

这个理解更接近 SceneSmith 页面里的 **Zero-Shot External Policy in Generated Scenes**：先生成物理可用场景，再让一个外部/下游 robot policy 在这些场景里执行任务。

博士生给我的要求可以概括为：**做一个 placement agent，通过 agentic 的方式解决桌面场景里资产如何摆放的问题。** 资产生成、完整任务生成和 policy 训练都不是当前主线。

---

## 1. 一句话目标

学习 SceneSmith 的 agentic scene construction 思路，专注做 RoboTwin tabletop placement agent：把自然语言里的空间语义转成资产选择和桌面 pose，使生成的 placed scene 可以被后续 RoboTwin task、外部 policy 或 evaluation pipeline 使用。

最小例子：

```text
Input placement prompt:
  "an apple and a plate on the table"

Output placement:
  apple asset on a reachable tabletop area
  plate asset on a reachable tabletop area
  no collisions
  stable on table
  visible to camera
  reachable enough for a later pick-and-place task

Possible downstream task:
  "pick the apple and place it on the plate"
```

---

## 2. 和旧路线的区别

旧路线：

```text
Natural language task
-> Text2Env JSON
-> generate RoboTwin task program
-> collect data / train / eval
```

新路线：

```text
Natural language placement prompt
-> TabletopPlacementSpec
-> instantiate placed scene in RoboTwin
-> downstream task / external policy runs in generated placed scene
```

关键变化：

- 旧路线关注“生成任务代码”。
- 新路线关注“资产选择与桌面摆放”，也就是 placement。
- 旧路线的自然语言通常是 action-oriented，例如 move / pick / place。
- 新路线的自然语言可以是 placement-oriented，例如 apple and plate on table, cup near plate, breakfast tabletop, cluttered toolbench。
- 下游 task 可以在 scene 生成之后再定义。

---

## 3. SceneSmith 给我们的参考

SceneSmith 是从自然语言生成 simulation-ready indoor scenes 的 agentic framework。它的页面里强调：

- VLM agents 共同生成 simulation-ready scene。
- 场景直接可用于 physics simulator。
- 生成场景可以支持外部 robot policy 的 zero-shot interaction。
- 场景也可以用于 scalable policy evaluation。

我们不复刻完整 room / house scene generation，只取 tabletop 版本：

```text
tabletop placement prompt
-> object selection
-> object placement
-> physical validation
-> RoboTwin scene loading
-> downstream robot task compatibility
```

---

## 4. 三个 placement agents 的分工

### 4.1 Designer agent

Designer 负责把自然语言 placement prompt 变成初始桌面资产摆放方案。

输入：

- placement prompt。
- tabletop bounds。
- asset catalog。
- optional downstream task hint。
- optional robot/camera constraints。

输出：

- 需要哪些 objects。
- 每个 object 的语义角色。
- 每个 object 对应的 asset candidates。
- 物体之间的空间关系。
- 初始 pose proposal。
- 可能的 keep-out / interaction zones。

例子：

```text
Prompt:
  an apple and a plate on the table

Designer output:
  apple: reachable tabletop region
  plate: reachable tabletop region
  table center kept mostly free if downstream pick-and-place is expected
```

### 4.2 Critic agent

Critic 负责评估这个 placement 是否语义正确、物理可行、机器人可用。

检查范围：

- 语义是否匹配 prompt。
- asset 是否存在，是否类别正确。
- left / right / near / inside / on top 等 spatial relation 是否满足。
- pose 是否在桌面边界内。
- asset 是否互相碰撞。
- asset 是否稳定放在桌上。
- 是否保留了机器人可达空间。
- 是否会遮挡相机或挡住下游 policy。

Critic 不负责生成 task code，也不负责训练 policy。

### 4.3 Orchestrator agent

Orchestrator 负责沟通 Designer 和 Critic。

它决定：

- 接受 placement spec。
- 要求 Designer 换 asset。
- 要求 Designer 调整 pose。
- 要求减少 clutter。
- 触发 simulator validation。
- 根据 RoboTwin logs 让 Designer 修复。

最终输出：

```text
final TabletopPlacementSpec
validation report
RoboTwin scene adapter command
```

---

## 5. 资产库的新边界

资产生成本身不是当前重点。后续会有人负责更丰富的资产来源。

本项目假设会有一个 asset library，提供：

```text
asset_id
category
natural-language tags
thumbnail / preview
visual mesh
collision mesh
dimensions
stable pose
physical metadata
optional affordance / functional points
```

RoboTwin 最终安装路径仍然是：

```text
~/RoboTwin/assets/objects/<asset_id>/
/data/sdb/zhengye/RoboTwin/assets/objects/<asset_id>/
```

普通刚体资产推荐结构：

```text
~/RoboTwin/assets/objects/<asset_id>/
  visual/base0.glb
  collision/base0.glb
  model_data0.json
  points_info.json
  asset_manifest.json
```

我们需要解决的是 **asset grounding**：

```text
"apple" -> choose `035_apple` or another apple asset
"plate" -> choose `003_plate` or another plate asset
"on the table" -> convert to stable tabletop poses
"and" -> ensure both objects are present, visible, non-overlapping, and reachable
```

可用方法：

- LLM 读 asset catalog tags。
- CLIP / SigLIP / VLM 对 thumbnails 做 image-text matching。
- 规则约束：category 必须匹配，尺寸必须合理，stable_on_table 必须为 true。

---

## 6. 新的中间表示：TabletopPlacementSpec

旧 Text2Env 是为了描述任务。现在需要的是 `TabletopPlacementSpec`，用于描述资产选择、空间关系和桌面 pose。

建议 v0：

```json
{
  "schema_version": "robotwin.tabletop_placement.v0",
  "placement_name": "apple_plate_table_v0",
  "language_prompt": "an apple and a plate on the table",
  "workspace": {
    "surface": "table",
    "bounds": {
      "x": [-0.45, 0.45],
      "y": [-0.35, 0.25],
      "z": [0.74, 1.10]
    },
    "spatial_regions": {
      "apple_start_area": {
        "x": [-0.25, -0.05],
        "y": [-0.20, 0.15]
      },
      "plate_area": {
        "x": [0.05, 0.30],
        "y": [-0.20, 0.15]
      }
    }
  },
  "objects": [
    {
      "id": "apple_1",
      "semantic": "apple",
      "asset_id": "035_apple",
      "role": "manipuland_candidate",
      "pose": {
        "region": "apple_start_area",
        "xyz": [-0.15, -0.02, 0.75],
        "qpos": [1, 0, 0, 0]
      },
      "physical": {
        "is_static": false,
        "collision": true,
        "stable_on_table": true
      }
    },
    {
      "id": "plate_1",
      "semantic": "plate",
      "asset_id": "003_plate",
      "role": "support_or_target_candidate",
      "pose": {
        "region": "plate_area",
        "xyz": [0.16, -0.02, 0.75],
        "qpos": [1, 0, 0, 0]
      },
      "physical": {
        "is_static": false,
        "collision": true,
        "stable_on_table": true
      }
    }
  ],
  "constraints": [
    "objects_on_table",
    "no_initial_collision",
    "satisfy_prompt_object_presence",
    "keep_robot_reachable"
  ],
  "downstream_task_hints": [
    "pick the apple and place it on the plate"
  ],
  "validation": {
    "semantic_check": "pending",
    "asset_check": "pending",
    "collision_check": "pending",
    "stability_check": "pending",
    "robotwin_load_check": "pending"
  }
}
```

注意：这里没有 `play_once()`，没有 `check_success()`。它描述的是 placement，不是任务。

---

## 7. RoboTwin 里的落点

我们要把 TabletopPlacementSpec 实例化到 RoboTwin。

可能实现方式：

```text
Option A: 写一个通用 placement loader/helper
Option B: 写一个 base tabletop scene task，只负责加载场景
Option C: 写一个 wrapper，在下游 task reset 前加载指定 scene
```

推荐从 Option A 开始：

```python
def load_tabletop_placement(task, placement_spec):
    task.placement_objects = {}
    for obj in placement_spec["objects"]:
        actor = create_actor(
            scene=task,
            pose=sapien.Pose(obj["pose"]["xyz"], obj["pose"]["qpos"]),
            modelname=obj["asset_id"],
            convex=True,
            is_static=obj["physical"].get("is_static", False),
            model_id=obj.get("model_id", 0),
        )
        task.placement_objects[obj["id"]] = actor
```

后续下游 task 可以引用这个场景：

```text
scene = apple_plate_table_v0
task = pick apple and place on plate
policy = external pick-and-place policy
```

---

## 8. What To Do

### 8.1 必须完成

- [x] 定义 TabletopPlacementSpec v0：`harness/schemas.py`。
- [x] 定义 asset catalog entry format，并建立 MVP 小样例：`asset_catalogs/robotwin_tabletop_assets_sample.json`。
- [x] 选一个简单 placement prompt：an apple and a plate on the table。
- [x] 准备或指定 apple / plate assets：`035_apple`、`003_plate`。
- [x] 写 Designer prompt：`prompts/designer_prompt.md`。
- [x] 写 Designer 初始 PlacementSpec：`placements/apple_plate_table/designer_initial_placement.json`。
- [x] 写 Critic prompt：`prompts/critic_prompt.md`。
- [x] 写 Critic 静态 review：`placements/apple_plate_table/critic_review.json`。
- [x] 写 Orchestrator prompt：`prompts/orchestrator_prompt.md`。
- [x] 输出 final static placement：`placements/apple_plate_table/final_placement.json`。
- [x] 输出 validation plan：`placements/apple_plate_table/validation_plan.json`。
- [x] 写 PlacementSpec validator：`harness/schemas.py`。
- [x] 写 RoboTwin placement loader / smoke runner：`scripts/run_robotwin_placement_smoke.py`。
- [x] 在 RoboTwin 中加载该 scene。
- [x] 跑 load / stability / camera smoke。
- [x] 保存 smoke result、图片、视频和人工 visual review。
- [ ] 记录该 scene 可供下游 task 使用的方式。

### 8.2 暂不做

- [ ] 不以生成新 task program 为主目标。
- [ ] 不训练 3D asset generator。
- [ ] 不复刻完整房间/住宅 SceneSmith。
- [ ] 不要求一开始完成 policy training。
- [ ] 不要求一开始自动生成 success predicate。

### 8.3 MVP 交付物

```text
1. TabletopPlacementSpec schema draft
2. asset catalog sample
3. Designer prompt draft
4. apple-and-plate Designer initial placement spec
5. Critic prompt and static review
6. Orchestrator prompt, final static placement, and validation plan
7. RoboTwin placement loader helper
8. RoboTwin load/stability smoke result
9. render image/video and visual review result
10. explanation of how a downstream RoboTwin task can consume the scene
```

---

## 9. How To Do

### Step 1: 选第一个 placement prompt

已选第一个 MVP placement prompt：

```text
an apple and a plate on the table
```

这个 prompt 好处：

- 语义清晰。
- 当前 RoboTwin 基础资产库已有 `035_apple` 和 `003_plate`。
- 只要求两个物体都在桌面上，避免一开始引入复杂空间关系。
- 只需要两个物体。
- 后续能自然接 pick-and-place task。
- 容易通过视觉和 simulator state 验证 object presence、on-table、no-collision、stability。

### Step 2: 建 asset catalog 小样例

已建立第一个 MVP asset catalog：

```text
asset_catalogs/robotwin_tabletop_assets_sample.json
```

先不接大资产库，当前 catalog 只覆盖 apple / plate 两个资产，用于验证 agent 能完成最小 asset grounding：

```json
[
  {
    "asset_id": "035_apple",
    "category": "apple",
    "tags": ["apple", "fruit", "round", "tabletop"],
    "models": 2,
    "size_m": null,
    "stable_on_table": true,
    "graspable": true,
    "robotwin_path": "~/RoboTwin/assets/objects/035_apple"
  },
  {
    "asset_id": "003_plate",
    "category": "plate",
    "tags": ["plate", "tableware", "flat", "support_surface", "tabletop"],
    "models": 1,
    "size_m": null,
    "stable_on_table": true,
    "graspable": false,
    "support_surface_candidate": true,
    "robotwin_path": "~/RoboTwin/assets/objects/003_plate"
  }
]
```

### Step 3: 让 Designer 生成初始 PlacementSpec

已完成两个输出：

```text
prompts/designer_prompt.md
placements/apple_plate_table/designer_initial_placement.json
```

Designer prompt 应要求：

- 识别场景里需要的 objects。
- 找到合适 asset。
- 将 "on the table" 映射成桌面坐标区域。
- 生成 pose。
- 保证不碰撞、不越界。
- 给出下游 task hints。

### Step 4: 让 Critic 检查 PlacementSpec

已完成两个输出：

```text
prompts/critic_prompt.md
placements/apple_plate_table/critic_review.json
```

本次 Critic 静态 review 结论：

```text
verdict = accept_for_next_stage
```

含义是：语义、资产、model id、bounds、粗略 collision、稳定性 metadata 和下游可用性在静态层面通过；但 RoboTwin load、真实物理稳定性、camera/render 可见性仍需后续 smoke 验证。

Critic prompt 应限制在：

- semantic match。
- asset availability。
- spatial relation。
- tabletop bounds。
- collision / stability。
- downstream robot usability。

Critic 输出：

```json
{
  "verdict": "accept_or_repair",
  "issues": [],
  "repair_suggestions": []
}
```

### Step 5: Orchestrator 输出 final placement

已完成三个输出：

```text
prompts/orchestrator_prompt.md
placements/apple_plate_table/final_placement.json
placements/apple_plate_table/validation_plan.json
```

本次 Orchestrator 决策：

```text
decision = accept_for_smoke
stage = final_static_for_smoke
```

含义是：Designer 初稿通过了 Static Critic，Orchestrator 不要求 repair，直接整理成下一步 RoboTwin smoke 使用的 final static placement。但它还不是视觉/仿真验证后的 final scene；`exact_table_contact`、`render_visibility`、`simulator_stability` 仍然 pending。

### Step 6: RoboTwin placement loader

已实现一个 helper / smoke runner，不生成新 task program：

```text
scripts/run_robotwin_placement_smoke.py
```

运行命令：

```text
python scripts/run_robotwin_placement_smoke.py \
  --robotwin-root /data/sdb/zhengye/RoboTwin \
  --placement placements/apple_plate_table/final_placement.json \
  --out-dir runs/apple_plate_table_smoke \
  --task-config demo_smoke \
  --seed 0 \
  --settle-steps 240 \
  --video-frames 60 \
  --fps 15
```

目标是把 PlacementSpec 里的物体实例化到 RoboTwin scene，并保存图片、视频和 pose log。

### Step 7: validation / smoke

验证分两层：

静态 validation：

- asset id exists。
- pose in bounds。
- no bbox overlap。
- required objects are on the tabletop and match the prompt。

RoboTwin validation：

- scene loads。
- objects stable。
- video/camera can see objects。
- simple downstream policy/task can reference scene objects。

本次 smoke 已完成：

```text
placements/apple_plate_table/smoke_result.json
placements/apple_plate_table/visual_review.json
previews/apple_plate_table/head_camera.png
previews/apple_plate_table/observer_camera.png
previews/apple_plate_table/observer_camera.mp4
```

结论：

```text
robotwin_load = pass
settling_stability = pass
render_evidence = pass
human_visual_review = pass
```

---

## 10. 后续如何接 RoboTwin task

Placement 生成后，下游 task 可以有两种方式使用：

### 10.1 外部 policy 直接使用 scene

类似 SceneSmith 的 external policy demo：

```text
generated placed scene
+ language-conditioned policy
-> policy executes: pick the apple and place it on the plate
```

这要求 policy 本身能理解 scene observations 和 language command。

### 10.2 RoboTwin task 消费 scene

后续可以写一个 RoboTwin task，但这是 scene 之后的下游模块：

```text
placement_spec = apple_plate_table_v0
task = pick_apple_to_plate
```

task 不需要重新决定 apple/plate 怎么摆；它读取 scene 里的 object id 和 pose。

也就是说：

```text
placement generation first
task definition second
policy/data/eval third
```

---

## 11. MCP + Skill + Harness 系统化方向

博士生提出的方向是：把当前 demo 做成一个 **MCP + skill + harness** 系统。这个方向是合理的，因为我们现在已经有了 prompt、PlacementSpec、RoboTwin smoke runner、图片/视频结果；下一步应该把它们从“手工串联 demo”升级成“可复现 agentic placement harness”。

### 11.1 三层设计

```text
Skill = 教 agent 怎么做
MCP = 给 agent 稳定可调用的 RoboTwin 工具
Harness = 把完整流程固定成可复现 pipeline
```

### 11.2 MCP tools 层

目标是做一个 `robotwin-placement-mcp`，把 RoboTwin 相关能力封装成工具，避免 agent 直接乱翻目录或手写临时 shell。

建议工具：

```text
list_assets()
get_asset_metadata(asset_id)
validate_placement_spec(spec)
run_robotwin_smoke(spec)
render_scene(spec)
get_smoke_artifacts(run_id)
visual_review(image_or_video, prompt)
```

当前已有的 `scripts/run_robotwin_placement_smoke.py` 可以作为 `run_robotwin_smoke(spec)` 的原型。

### 11.3 Skill 层

Skill 负责固定 agent 的行为规范，不绑定具体模型。

当前采用一个顶层 handoff skill 加多个 focused skill 的结构。顶层 skill 用来给另一个 Codex / agent 复现完整流程，focused skill 负责具体能力。

顶层 skill：

```text
generate-robotwin-tabletop-scene
  输入新的 placement prompt + asset catalog / RoboTwin path
  调度 asset grounding、Designer、Critic、Orchestrator、smoke、visual review、repair、lesson 回写
  输出可验收的 RoboTwin tabletop scene preview 或明确 blocker
```

focused skills：

```text
design-tabletop-placement
  输入 placement prompt + asset catalog
  输出 initial PlacementSpec

critique-tabletop-placement
  检查 semantic match、asset availability、bounds、collision/stability、render evidence

orchestrate-placement-pipeline
  根据 critic 结果决定 accept / repair / rerun

ground-objects-to-robotwin-assets
  把自然语言 object 映射到 RoboTwin 或 rich asset library asset_id

review-robotwin-smoke-preview
  跑 smoke，保存图片/视频，写 visual review
```

当前顶层入口已经放在 `skills/generate-robotwin-tabletop-scene/`。另一个 agent 不需要复现我们手工探索过的每一步，只需要拿到 repo、确认 RoboTwin 在 `~/RoboTwin`，然后从这个 skill 开始处理新的自然语言 prompt。

现有的 `prompts/designer_prompt.md`、`prompts/critic_prompt.md`、`prompts/orchestrator_prompt.md` 已迁移成 focused skill 初版，并保留中文版 `SKILL.zh-CN.md` 方便中文协作。

### 11.4 Harness 层

Harness 是端到端 runner，目标是一条命令从自然语言跑到 scene preview：

```bash
python harness/run_placement_pipeline.py \
  --prompt "an apple and a plate on the table" \
  --asset-catalog asset_catalogs/robotwin_tabletop_assets_sample.json \
  --robotwin-root ~/RoboTwin \
  --model-provider codex_reference \
  --out-dir runs/apple_plate_table
```

固定流程：

```text
1. asset grounding
2. Designer 生成 initial PlacementSpec
3. schema/static validation
4. Critic review
5. Orchestrator 输出 final placement
6. RoboTwin smoke render
7. visual critic / human review
8. 生成 report
```

### 11.5 推荐目录结构

```text
mcp/
  robotwin_placement_server.py
  tools/
    assets.py
    validation.py
    smoke.py
    render.py

skills/
  generate-robotwin-tabletop-scene/SKILL.md
  generate-robotwin-tabletop-scene/SKILL.zh-CN.md
  generate-robotwin-tabletop-scene/references/
  design-tabletop-placement/SKILL.md
  design-tabletop-placement/SKILL.zh-CN.md
  critique-tabletop-placement/SKILL.md
  critique-tabletop-placement/SKILL.zh-CN.md
  orchestrate-placement-pipeline/SKILL.md
  orchestrate-placement-pipeline/SKILL.zh-CN.md
  ground-objects-to-robotwin-assets/SKILL.md
  ground-objects-to-robotwin-assets/SKILL.zh-CN.md
  review-robotwin-smoke-preview/SKILL.md
  review-robotwin-smoke-preview/SKILL.zh-CN.md

harness/
  run_placement_pipeline.py
  model_providers.py
  schemas.py

asset_catalogs/
placements/
previews/
reports/
```

### 11.6 最小交付顺序

第一阶段不要一口气做全 MCP server。先做 MCP-lite / CLI harness：

```text
1. 抽出 PlacementSpec validator。
2. 把 run_robotwin_placement_smoke.py 封装成可复用 smoke tool。
3. 写 Designer / Critic / Orchestrator / Smoke Review skill 初版。
4. 写 harness/run_placement_pipeline.py，一条命令复现 apple/plate。
5. 写 `generate-robotwin-tabletop-scene` 顶层 handoff skill，让另一个 agent 能从新 prompt 跑完整流程。
6. 再把 CLI tools 包成 MCP tools。
```

模型后端要保持可替换：

```text
codex_reference
openai_api
qwen_api
claude_api
local_vllm
local_vlm
```

这样别人复现时可以先用 `codex_reference` 或 mock/reference artifact，不需要马上配置模型 API；之后再替换成 Qwen、OpenAI、Claude 或本地 VLM。

### 11.7 Skill lessons 回写规则

每次跑新的 placement prompt 后，如果发现任何新坑，都必须回写到 skill，不只是修代码：

```text
1. prompt 语义坑 -> skills/design-tabletop-placement
2. asset / loader / qpos / scale 坑 -> skills/ground-objects-to-robotwin-assets
3. static validator 漏检 -> skills/critique-tabletop-placement
4. visual/VLM 判别坑 -> skills/review-robotwin-smoke-preview
5. pipeline 状态、repair、rerun 规则 -> skills/orchestrate-placement-pipeline
6. 新 prompt 的端到端经验 -> skills/generate-robotwin-tabletop-scene/references/known-pitfalls.md
```

一次 run 的完整收尾标准：

```text
code/catalog 修复
smoke 或 pending visual gate 验证
visual review 记录
preview 小文件保存
相关 skill lessons 更新
GitHub 同步
```

---

## 12. 当前 TODO

### High priority

- [x] 定义 TabletopPlacementSpec v0：`harness/schemas.py`。
- [x] 定义 asset catalog sample：`asset_catalogs/robotwin_tabletop_assets_sample.json`。
- [x] 选定第一个 placement prompt：an apple and a plate on the table。
- [x] 确认 RoboTwin 基础资产库中有 apple / plate：`035_apple`、`003_plate`。
- [x] 写 Designer prompt：`prompts/designer_prompt.md`。
- [x] 写 apple-and-plate Designer initial PlacementSpec：`placements/apple_plate_table/designer_initial_placement.json`。
- [x] 写 Critic prompt：`prompts/critic_prompt.md`。
- [x] 写 apple-and-plate Critic static review：`placements/apple_plate_table/critic_review.json`。
- [x] 写 Orchestrator prompt：`prompts/orchestrator_prompt.md`。
- [x] 输出 final static placement：`placements/apple_plate_table/final_placement.json`。
- [x] 输出 validation plan：`placements/apple_plate_table/validation_plan.json`。
- [x] 写 PlacementSpec validator：`harness/schemas.py`。
- [x] 设计 MCP-lite / CLI tool interface：`mcp_lite/tools.py`，包含 asset、validation、smoke、render artifact、visual review。
- [x] 把 Designer / Critic / Orchestrator prompts 迁移成 skill 初版：`skills/design-tabletop-placement`、`skills/critique-tabletop-placement`、`skills/orchestrate-placement-pipeline`。
- [x] 写 harness/run_placement_pipeline.py，一条命令从 prompt 跑到 preview：`harness/run_placement_pipeline.py`。
- [x] 写顶层 handoff skill：`skills/generate-robotwin-tabletop-scene`，用于让另一个 agent 从新 prompt 跑完整 scene generation 流程。

### Medium priority

- [x] 写 RoboTwin placement loader / smoke runner：`scripts/run_robotwin_placement_smoke.py`。
- [x] 跑 apple/plate scene load smoke。
- [x] 保存 validation report、图片和视频。
- [ ] 写下游 task 消费 scene 的接口说明。

### Lower priority

- [ ] 接入 VLM / embedding 做 asset retrieval。
- [ ] 生成多种 placement prompt。
- [ ] 接入 external policy eval。
- [ ] 做 success/failure evaluator。
- [ ] 把 CLI harness 包装成正式 MCP server。
- [ ] 接入 Qwen / OpenAI / Claude / local vLLM backend。

---

## 13. 风险和判断

### Risk 1: 又滑回 task generation

处理方式：

- 文档和 README 明确：项目主输出是 placement spec / placed scene。
- PlacementSpec 不包含 `play_once()` / `check_success()`。
- RoboTwin task 是下游消费者，不是当前主目标。

### Risk 2: asset 语义匹配不准

处理方式：

- asset catalog 必须包含 category、tags、thumbnail。
- Critic 检查 asset 是否满足 prompt。
- 后续用 VLM/embedding 辅助 retrieval。

### Risk 3: pose 语义不准

处理方式：

- 明确 tabletop coordinate convention。
- left/right/front/back 映射到 workspace regions。
- validator 检查 spatial relation。

### Risk 4: 生成 scene 物理不可用

处理方式：

- static bbox validation。
- RoboTwin load check。
- stability check。
- collision check。

### Risk 5: 场景可用但对机器人任务没有价值

处理方式：

- PlacementSpec 加 `downstream_task_hints`。
- 生成时保留 reachability。
- 用简单 pick-and-place task 做 sanity check。

### Risk 6: MCP / skill / harness 过早复杂化

处理方式：

- 先做 CLI harness，再包 MCP。
- 先用 reference artifacts / mock provider，再接真实模型 API。
- 每个 tool 都要求有输入 schema、输出 schema 和最小测试。
- 不把 RoboTwin 大资产、data、logs、HDF5 纳入 repo。

### Risk 7: Static Critic 误把视觉失败当作通过

2026-07-01 的 vegetable/basket 测试暴露了这个问题：static validation 和 RoboTwin smoke 都可能通过，但 basket 在 preview 里仍然可能出现朝向错误或穿模。这个问题不能只靠 JSON validator 解决。

处理方式：

- Critic 必须分成 static Critic 和 visual Critic / VLM Critic。
- `smoke pass` 只表示 RoboTwin 能加载、能渲染，不等于 scene visually valid。
- pipeline 默认状态改为 `pending_visual_review`，直到 human / VLM / Codex visual reference 明确给出 pass。
- visual Critic 必须检查 object identity、orientation、table contact、penetration、floating、occlusion 和 prompt match。
- 对资产库中坐标系特殊的资产，必须把 `placement_defaults.qpos` 等 pose hint 写进 asset catalog，而不是靠 Designer 临场猜。

---

## 14. 远程环境状态

默认远程路径：

```text
zhengye = /data/sdb/zhengye
RoboTwin = /data/sdb/zhengye/RoboTwin
project repo = /data/sdb/zhengye/robotwin-text2env-demo
```

VS Code Remote 注意：

- 不要打开 `/data/sdb` 这种超大根目录。
- 只打开项目子目录或 RoboTwin 子目录。
- 排除 `.git`、`assets`、`data`、`outputs`、`checkpoints`、`logs`、`wandb` 等目录，避免 CPU 占用过高。

---

## 15. References

- SceneSmith project page: https://scenesmith.github.io/
- SceneSmith repo: https://github.com/nepfaff/scenesmith
- RoboTwin project page: https://robotwin-platform.github.io/
- RoboTwin official repo: https://github.com/robotwin-Platform/robotwin
- RoboTwin documentation: https://robotwin-platform.github.io/doc/index.html
