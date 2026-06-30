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
a banana on the left side of the table and an apple on the right side
```

我们生成的应该是一个 RoboTwin 中可加载、可验证的桌面场景：

```text
table
+ banana placed on the left side
+ apple placed on the right side
+ physically valid poses
+ usable asset metadata
```

这个场景以后可以被下游机器人任务使用。例如，在这个场景上再定义或执行：

```text
pick the banana from the left side and move it to the right side
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
  "a banana on the left side of the table and an apple on the right side"

Output placement:
  banana asset on left tabletop area
  apple asset on right tabletop area
  no collisions
  stable on table
  visible to camera
  reachable enough for a later pick-and-place task

Possible downstream task:
  "pick banana from the left side to the right side"
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
- 新路线的自然语言可以是 placement-oriented，例如 banana left, apple right, breakfast tabletop, cluttered toolbench。
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
  a banana on the left side of the table and an apple on the right side

Designer output:
  banana: left tabletop region
  apple: right tabletop region
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
"banana" -> choose a banana asset
"apple" -> choose an apple asset
"left side of table" -> convert to tabletop pose region
"right side of table" -> convert to tabletop pose region
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
  "placement_name": "banana_left_apple_right_v0",
  "language_prompt": "a banana on the left side of the table and an apple on the right side",
  "workspace": {
    "surface": "table",
    "bounds": {
      "x": [-0.45, 0.45],
      "y": [-0.35, 0.25],
      "z": [0.74, 1.10]
    },
    "spatial_regions": {
      "left_side": {
        "x": [-0.35, -0.10],
        "y": [-0.20, 0.15]
      },
      "right_side": {
        "x": [0.10, 0.35],
        "y": [-0.20, 0.15]
      }
    }
  },
  "objects": [
    {
      "id": "banana_1",
      "semantic": "banana",
      "asset_id": "banana_asset_01",
      "role": "manipuland_candidate",
      "pose": {
        "region": "left_side",
        "xyz": [-0.22, -0.02, 0.75],
        "qpos": [1, 0, 0, 0]
      },
      "physical": {
        "is_static": false,
        "collision": true,
        "stable_on_table": true
      }
    },
    {
      "id": "apple_1",
      "semantic": "apple",
      "asset_id": "apple_asset_01",
      "role": "target_or_distractor",
      "pose": {
        "region": "right_side",
        "xyz": [0.22, -0.02, 0.75],
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
    "satisfy_left_right_relation",
    "keep_robot_reachable"
  ],
  "downstream_task_hints": [
    "pick banana from left side to right side"
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
scene = banana_left_apple_right_v0
task = pick banana and place near apple
policy = external pick-and-place policy
```

---

## 8. What To Do

### 8.1 必须完成

- [ ] 定义 TabletopPlacementSpec v0。
- [ ] 定义 asset catalog entry format。
- [ ] 选一个简单 placement prompt：banana left, apple right。
- [ ] 准备或指定 banana / apple assets。
- [ ] 写 Designer / Critic / Orchestrator prompts。
- [ ] 写一个人工 TabletopPlacementSpec reference。
- [ ] 写 PlacementSpec validator。
- [ ] 写 RoboTwin placement loader helper。
- [ ] 在 RoboTwin 中加载该 scene。
- [ ] 跑 load / stability / camera smoke。
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
3. Designer / Critic / Orchestrator prompt draft
4. banana-left apple-right placement spec
5. RoboTwin placement loader helper
6. RoboTwin load/stability smoke result
7. explanation of how a downstream RoboTwin task can consume the scene
```

---

## 9. How To Do

### Step 1: 选第一个 placement prompt

建议从最简单开始：

```text
a banana on the left side of the table and an apple on the right side
```

这个 prompt 好处：

- 语义清晰。
- 空间关系清晰。
- 只需要两个物体。
- 后续能自然接 pick-and-place task。
- 容易通过视觉和 simulator state 验证。

### Step 2: 建 asset catalog 小样例

先不接大资产库，做一个小 catalog：

```json
[
  {
    "asset_id": "banana_asset_01",
    "category": "banana",
    "tags": ["banana", "fruit", "yellow", "elongated"],
    "size_m": [0.16, 0.04, 0.04],
    "stable_on_table": true,
    "graspable": true,
    "robotwin_path": "~/RoboTwin/assets/objects/banana_asset_01"
  },
  {
    "asset_id": "apple_asset_01",
    "category": "apple",
    "tags": ["apple", "fruit", "red", "round"],
    "size_m": [0.08, 0.08, 0.08],
    "stable_on_table": true,
    "graspable": true,
    "robotwin_path": "~/RoboTwin/assets/objects/apple_asset_01"
  }
]
```

### Step 3: 让 Designer 生成初始 PlacementSpec

Designer prompt 应要求：

- 识别场景里需要的 objects。
- 找到合适 asset。
- 将 left/right 映射成桌面坐标区域。
- 生成 pose。
- 保证不碰撞、不越界。
- 给出下游 task hints。

### Step 4: 让 Critic 检查 PlacementSpec

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

Orchestrator 根据 Designer 和 Critic 输出：

```text
final_placement_spec.json
validation_plan.json
```

### Step 6: RoboTwin placement loader

实现一个 helper，不要生成新 task：

```text
scripts/load_tabletop_placement.py
```

或者先在 RoboTwin 内写：

```text
envs/utils/load_tabletop_placement.py
```

目标是把 PlacementSpec 里的物体实例化到 RoboTwin scene。

### Step 7: validation / smoke

验证分两层：

静态 validation：

- asset id exists。
- pose in bounds。
- no bbox overlap。
- left/right relation correct。

RoboTwin validation：

- scene loads。
- objects stable。
- video/camera can see objects。
- simple downstream policy/task can reference scene objects。

---

## 10. 后续如何接 RoboTwin task

Placement 生成后，下游 task 可以有两种方式使用：

### 10.1 外部 policy 直接使用 scene

类似 SceneSmith 的 external policy demo：

```text
generated placed scene
+ language-conditioned policy
-> policy executes: pick banana and place it near apple
```

这要求 policy 本身能理解 scene observations 和 language command。

### 10.2 RoboTwin task 消费 scene

后续可以写一个 RoboTwin task，但这是 scene 之后的下游模块：

```text
placement_spec = banana_left_apple_right_v0
task = pick_banana_left_to_right
```

task 不需要重新决定 banana/apple 怎么摆；它读取 scene 里的 object id 和 pose。

也就是说：

```text
placement generation first
task definition second
policy/data/eval third
```

---

## 11. 当前 TODO

### High priority

- [ ] 定义 TabletopPlacementSpec v0。
- [ ] 定义 asset catalog sample。
- [ ] 确认 RoboTwin / rich asset library 中是否有 banana 和 apple。
- [ ] 写 banana-left apple-right reference PlacementSpec。
- [ ] 写三个 agent prompts：Designer、Critic、Orchestrator。
- [ ] 写 PlacementSpec validator。

### Medium priority

- [ ] 写 RoboTwin placement loader helper。
- [ ] 跑 banana/apple scene load smoke。
- [ ] 保存 validation report 和视频。
- [ ] 写下游 task 消费 scene 的接口说明。

### Lower priority

- [ ] 接入 VLM / embedding 做 asset retrieval。
- [ ] 生成多种 placement prompt。
- [ ] 接入 external policy eval。
- [ ] 做 success/failure evaluator。

---

## 12. 风险和判断

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

---

## 13. 远程环境状态

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

## 14. References

- SceneSmith project page: https://scenesmith.github.io/
- SceneSmith repo: https://github.com/nepfaff/scenesmith
- RoboTwin project page: https://robotwin-platform.github.io/
- RoboTwin official repo: https://github.com/robotwin-Platform/robotwin
- RoboTwin documentation: https://robotwin-platform.github.io/doc/index.html
