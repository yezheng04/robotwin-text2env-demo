# RoboTwin Tabletop Background Scene Generation Plan

更新时间：2026-06-30  
所属大任务：Self-Improving Agents for Physical AI  
当前项目方向：SceneSmith-style tabletop background generation for existing RoboTwin tasks

---

## 0. 方向重置

之前的路线是：

```text
Natural language task
-> Text2Env JSON
-> generate a new RoboTwin task program
-> data collection / train / eval
```

这个方向现在需要重构。新的理解是：

> 我们不是要从自然语言生成一个新的 RoboTwin task，而是要学习 SceneSmith 的场景生成方式，为一个已经存在的 RoboTwin task 生成桌面级 background scene。

也就是说，RoboTwin 里的 core task 已经存在，例如 `place_empty_cup`、`beat_block_hammer`、`place_object_basket`。我们要做的是给这个 task 自动生成更丰富、更语义一致、更物理可行的桌面背景环境：

```text
Existing RoboTwin task
+ natural-language scene/background request
+ asset library
-> tabletop scene spec
-> background asset placement
-> simulator validation
-> data/eval variants
```

---

## 1. 一句话目标

为已有 RoboTwin tabletop manipulation task 自动生成可执行、可验证的桌面背景场景。

最小目标：

```text
Input:
  task_name = "place_empty_cup"
  scene request = "a tidy breakfast tabletop with a plate, spoon, napkin, and fruit around the task area"
  asset catalog = available tabletop assets

Output:
  a RoboTwin-compatible background scene
  placed assets that match the request
  no collision with task-critical objects
  no blockage of robot reachability
  smoke test video/log showing the original task still runs
```

这个项目的核心不再是 task program synthesis，而是：

- 语义理解：自然语言中的背景物体、风格、约束是什么。
- 资产 grounding：从丰富资产库里找到合适 asset。
- 桌面布局：把 asset 放到桌面上，语义合理且物理稳定。
- 任务兼容性：背景不能破坏已有 RoboTwin task 的执行。
- agentic loop：用 Designer / Critic / Orchestrator 迭代出可用 scene。

---

## 2. 新项目在大任务里的位置

Self-Improving Agents for Physical AI 需要一个能持续生成、评估、诊断、再生成的数据环境系统。新的 tabletop background generator 是这个闭环里的 setup / environment variation 模块。

它回答的问题是：

```text
给定一个机器人任务，怎样自动生成更多有语义、有难度梯度、但不破坏任务定义的仿真背景？
```

在闭环里的位置：

```text
Task / policy failure need
-> generate targeted tabletop background variants
-> collect data or evaluate policy
-> diagnose failures under clutter/background variation
-> generate next round of scenes
```

例如：

- policy 在 cluttered table 下失败，就生成更多不同 clutter density 的桌面背景。
- policy 对 breakfast objects 误识别，就生成餐盘、杯子、餐具、水果等语义相关背景。
- policy 被 distractor 干扰，就控制 distractor 距离、颜色、形状和数量。

---

## 3. SceneSmith 给我们的启发

SceneSmith 的关键不是某个具体 asset，而是 agentic scene generation workflow。

我们参考它的三类 agent：

### 3.1 Designer

Designer 负责提出初始场景设计。

输入：

- RoboTwin task name。
- task-critical objects / target region / robot setup。
- natural-language background request。
- asset catalog summary。
- tabletop bounds。

输出：

- 需要哪些 background assets。
- 每个 asset 的语义角色，例如 distractor、decor、support、container、occluder。
- 每个 asset 的候选位置、朝向、尺度。
- keep-out zones，避免碰撞 task object 和 robot motion path。
- 预期难度，例如 clean / light clutter / medium clutter。

### 3.2 Critic

Critic 负责判断场景是否合理。

检查范围：

- 语义匹配：资产是否符合自然语言。
- 资产可用性：asset id 是否存在于资产库。
- 桌面边界：物体是否在 tabletop bounds 内。
- 碰撞：background assets 是否互相碰撞，是否碰 task-critical objects。
- 稳定性：物体是否会掉落、穿桌、倾倒。
- 任务兼容性：是否挡住抓取、放置、目标区域、相机视野。
- 难度控制：clutter 是否过多或过少。

Critic 不负责重新写 task，不负责训练 policy。

### 3.3 Orchestrator

Orchestrator 负责沟通 Designer 和 Critic。

它决定：

- 接受当前 scene spec。
- 要求 Designer 修改位置、换 asset、减少 clutter。
- 触发 RoboTwin smoke test。
- 把失败日志反馈给下一轮。

最终输出：

```text
final tabletop scene spec
validation report
RoboTwin scene adapter command
```

---

## 4. RoboTwin 在新项目里的角色

RoboTwin 仍然是执行底座，但我们不再把重点放在创建新的 task program。

RoboTwin 负责：

- 提供已有 task。
- 提供机器人、桌面、相机、物理仿真。
- 加载资产。
- 执行原 task 的 scripted policy / data collection / eval。
- 输出 smoke logs、video、HDF5、success/failure。

我们要接入的位置：

```text
~/RoboTwin/envs/<task_name>.py
```

主要关注已有 task 的：

```python
load_actors()
play_once()
check_success()
```

新项目只改或扩展 background scene 部分：

- 在 `load_actors()` 之后或内部插入 background assets。
- 不改变 `play_once()` 的核心动作逻辑。
- 不改变 `check_success()` 的任务语义，除非只是增加 scene sanity check。

推荐未来做一个轻量 adapter：

```text
SceneSpec JSON
-> inject background assets into RoboTwin task reset/load_actors
-> run smoke
```

---

## 5. 资产问题的新边界

之前担心的是：如果自然语言里出现 RoboTwin 没有的 asset，例如 peach，流程会失效。

新的项目边界是：

> 资产生成或资产收集由其他人负责。我们假设后续会有一个更丰富的 asset library。我的重点是让 agent 理解自然语言并从资产库里选对、摆对、验证对。

因此我们需要关心的是资产库接口，而不是训练 3D 生成模型。

### 5.1 资产库需要提供什么

每个 asset 至少需要：

```text
asset_id
category
natural-language tags
dimensions
visual mesh path
collision mesh path
mass / static flag
stable pose hint
optional contact points
optional functional points
thumbnail / preview image
```

RoboTwin 安装路径仍然是：

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

### 5.2 我们需要做的 asset grounding

自然语言：

```text
a tidy breakfast tabletop with a plate, spoon, napkin, and fruit
```

需要转成：

```json
[
  {"semantic": "plate", "asset_id": "plate_...", "role": "background"},
  {"semantic": "spoon", "asset_id": "spoon_...", "role": "background"},
  {"semantic": "napkin", "asset_id": "napkin_...", "role": "background"},
  {"semantic": "fruit", "asset_id": "apple_..." , "role": "background"}
]
```

这一步可以用：

- 文本 embedding。
- CLIP / SigLIP 这类 image-text embedding。
- VLM 对 asset thumbnails 做语义描述。
- LLM 根据 asset catalog tags 选择。

资产生成模型不是本项目重点。

---

## 6. 新的中间表示：Tabletop SceneSpec

旧的 Text2Env JSON 是为了生成 task program。新项目需要的是 SceneSpec，也就是“桌面背景场景规格”。

建议 v0 schema：

```json
{
  "schema_version": "robotwin.tabletop_scene.v0",
  "task_name": "place_empty_cup",
  "scene_name": "breakfast_light_clutter_v0",
  "language_request": "a tidy breakfast tabletop with a plate, spoon, napkin, and fruit around the task area",
  "workspace": {
    "surface": "table",
    "bounds": {
      "x": [-0.45, 0.45],
      "y": [-0.35, 0.25],
      "z": [0.74, 1.10]
    }
  },
  "task_anchors": {
    "task_objects": ["cup", "coaster"],
    "target_regions": ["coaster_region"],
    "keep_out_zones": [
      {
        "id": "main_manipulation_zone",
        "center": [0.0, -0.1, 0.75],
        "size": [0.35, 0.25, 0.15]
      }
    ]
  },
  "background_assets": [
    {
      "id": "plate_1",
      "asset_id": "plate_white_01",
      "semantic": "plate",
      "role": "background_distractor",
      "pose": {
        "xyz": [0.25, 0.05, 0.75],
        "qpos": [1, 0, 0, 0]
      },
      "physical": {
        "is_static": true,
        "collision": true
      }
    }
  ],
  "constraints": [
    "do_not_overlap_task_objects",
    "do_not_block_robot_reach",
    "remain_on_table",
    "preserve_task_success_definition"
  ],
  "validation": {
    "semantic_match": "pending",
    "collision_check": "pending",
    "stability_check": "pending",
    "task_smoke": "pending"
  }
}
```

这个 SceneSpec 不生成新 task，它只描述 background assets 如何放进已有 task。

---

## 7. What To Do

### 7.1 必须完成

- [ ] 选 1-2 个已有 RoboTwin tabletop task 作为基准，例如 `place_empty_cup`、`beat_block_hammer`。
- [ ] 摸清这些 task 的 `load_actors()` 中哪些是 task-critical objects。
- [ ] 定义 Tabletop SceneSpec v0。
- [ ] 定义 asset catalog format。
- [ ] 写 Designer / Critic / Orchestrator prompt。
- [ ] 写一个人工 SceneSpec example。
- [ ] 写 SceneSpec -> RoboTwin background injection 的最小 adapter。
- [ ] 写 collision / bounds / keep-out validation。
- [ ] 跑 RoboTwin smoke，证明原 task 加 background 后还能执行。
- [ ] 保存视频、日志、validation report。

### 7.2 暂不做

- [ ] 不生成新的 RoboTwin task program。
- [ ] 不训练 3D asset generation model。
- [ ] 不做完整房间/住宅场景。
- [ ] 不做大规模 policy training result。
- [ ] 不解决复杂 articulated asset 生成。

### 7.3 最小交付物 MVP

MVP 应该包含：

```text
1. SceneSpec schema draft
2. 一个已有 RoboTwin task 的 task-context note
3. 一个 asset catalog 小样例
4. Designer / Critic / Orchestrator prompt
5. 一个 background scene example
6. 一个 RoboTwin adapter prototype
7. 一次 smoke test 视频或失败日志
```

---

## 8. How To Do

### Step 1: 选择已有 RoboTwin task

优先选择已有、稳定、scripted policy 能跑通的 task。

候选：

```text
place_empty_cup
beat_block_hammer
place_object_basket
move_pillbottle_pad
```

选择标准：

- task 逻辑简单。
- task-critical object 数量少。
- 桌面空间还有余量放 background。
- `collect_data.sh <task> demo_smoke 0` 能跑。
- 视频可解释。

产出：

```text
task_context/<task_name> summary
critical objects
target region
keep-out zone
baseline smoke command
```

### Step 2: 读 RoboTwin task 的场景接口

需要明确：

- task 在哪里创建 object。
- 哪些 object 是必须保留的。
- 物体 pose 的桌面坐标范围。
- `add_prohibit_area(...)` 如何保护区域。
- background assets 是否应该 static。
- 当前 task 的相机能否看到 background。

重点文件：

```text
~/RoboTwin/envs/<task_name>.py
~/RoboTwin/envs/utils/create_actor.py
~/RoboTwin/envs/utils/rand_create_actor.py
```

### Step 3: 定义 asset catalog

资产库不需要由本项目生成，但需要能被 agent 读懂。

建议 catalog entry：

```json
{
  "asset_id": "plate_white_01",
  "category": "plate",
  "tags": ["breakfast", "kitchen", "white plate", "flat"],
  "size_m": [0.18, 0.18, 0.02],
  "stable_on_table": true,
  "graspable": false,
  "is_static_default": true,
  "robotwin_path": "~/RoboTwin/assets/objects/plate_white_01",
  "thumbnail": "asset_thumbnails/plate_white_01.png"
}
```

### Step 4: 做 SceneSmith-lite agents

三个 agent 的输入输出：

```text
Designer:
  task context + scene request + asset catalog
  -> initial SceneSpec

Critic:
  SceneSpec + constraints + validation logs
  -> issues + repair suggestions

Orchestrator:
  Designer draft + Critic report
  -> final SceneSpec or retry request
```

Critic 必须明确限制在：

- tabletop semantic fit。
- asset availability。
- collision / stability。
- object poses。
- task compatibility。
- RoboTwin API usage。

### Step 5: SceneSpec -> RoboTwin adapter

adapter 不应该生成新 task，而是把 background assets 注入已有 task。

可能路线：

```text
Option A: 生成一个 task wrapper / subclass
Option B: 在现有 task 的 load_actors 后插入 background loader
Option C: 做一个通用 helper: load_background_scene(self, scene_spec)
```

推荐从 Option C 开始。

伪代码：

```python
def load_background_scene(task, scene_spec):
    for item in scene_spec["background_assets"]:
        actor = create_actor(
            scene=task,
            pose=sapien.Pose(item["pose"]["xyz"], item["pose"]["qpos"]),
            modelname=item["asset_id"],
            convex=True,
            is_static=item["physical"].get("is_static", True),
            model_id=item["asset"].get("model_id", 0),
        )
        task.background_actors.append(actor)
```

### Step 6: validation

先做 lightweight validation，再做 simulator smoke。

静态检查：

- asset id 是否存在。
- pose 是否在 tabletop bounds 内。
- bounding boxes 是否重叠。
- 是否进入 keep-out zone。
- 数量是否符合 clutter level。

仿真检查：

- reset 后物体是否稳定。
- 是否穿桌或飞走。
- task scripted policy 是否还能跑。
- success rate 是否明显下降。
- 视频中语义是否符合 scene request。

### Step 7: smoke / eval

最小 smoke：

```bash
cd ~/RoboTwin
source ~/miniconda3/etc/profile.d/conda.sh
conda activate RoboTwin
timeout 900 bash collect_data.sh <task_name> demo_smoke 0
```

未来 eval：

```text
baseline task
vs
task + generated background scene variants
```

对比：

- success / fail。
- collision fail。
- planning fail。
- camera visibility。
- policy robustness。

---

## 9. 新旧文件判断

旧路线中以下内容已经不再是主线：

- Text2Env task schema。
- env JSON -> RoboTwin task program generator。
- generated `move_object_between_zones` task。
- TaskB smoke preview。
- ACT policy hook for generated task。

这些可以删除或移出主仓库，避免 GitHub 首页和代码结构继续暗示“我们在做 task generation”。

仍然有参考价值但不作为主线：

- 旧 smoke 经验：说明 RoboTwin data collection 如何跑。
- 旧 `create_actor` 调试经验：说明 asset 的 `is_static`、collision、qpos 会影响稳定性。
- 旧 agent loop：Designer / Critic / Orchestrator 的组织方式仍可保留思想。

---

## 10. 当前 TODO

### High priority

- [ ] 选定第一个已有 RoboTwin task 作为 background generation demo。
- [ ] 写 task context note，列出 task-critical objects、target region、keep-out zone。
- [ ] 定义 Tabletop SceneSpec v0。
- [ ] 定义 asset catalog entry format。
- [ ] 写 Designer / Critic / Orchestrator prompt v0。
- [ ] 手写一个 background scene spec 作为 reference。

### Medium priority

- [ ] 写 SceneSpec validator。
- [ ] 写 RoboTwin background loader helper。
- [ ] 跑 baseline task smoke。
- [ ] 跑 task + background smoke。
- [ ] 保存视频、scene spec、validation report。

### Lower priority

- [ ] 接入 VLM/embedding 做 asset retrieval。
- [ ] 生成多种 clutter level。
- [ ] 做 scene diversity metrics。
- [ ] 对 policy eval success rate 做对比。

---

## 11. 风险和判断

### Risk 1: background 干扰原 task scripted policy

处理方式：

- 明确 keep-out zone。
- 默认 background assets 放到 task manipulation path 外。
- 先用 static assets。
- 每个 scene 必须跑 smoke。

### Risk 2: 资产语义匹配不准

处理方式：

- asset catalog 必须有 tags、category、thumbnail。
- 用 VLM 或 embedding 做 asset retrieval。
- Critic 检查 selected asset 是否符合 scene request。

### Risk 3: collision mesh 不可靠

处理方式：

- background asset 优先使用已验证 collision。
- 先做 simple bounding-box overlap check。
- 再用 RoboTwin reset stability check。

### Risk 4: 场景好看但对机器人无意义

处理方式：

- scene request 必须和 task/failure mode 相关。
- 设计 clutter level、semantic distractor、visual distractor。
- eval 时记录 task success/failure reason。

### Risk 5: 又滑回 task generation

处理方式：

- 规定本项目不生成新的 `play_once()` 和 `check_success()`。
- 只对已有 task 注入 background scene。
- README 和计划文档统一使用 scene/background generation 表述。

---

## 12. 远程环境状态

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

## 13. References

- RoboTwin project page: https://robotwin-platform.github.io/
- RoboTwin official repo: https://github.com/robotwin-Platform/robotwin
- RoboTwin documentation: https://robotwin-platform.github.io/doc/index.html
- SceneSmith project page: https://scenesmith.github.io/
- SceneSmith repo: https://github.com/nepfaff/scenesmith
