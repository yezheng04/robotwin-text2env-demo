# RoboTwin Tabletop Scene Generation Workflow

更新时间：2026-07-02

本文档是当前仓库的主流程说明。目标是让你、博士生、或另一个 Codex/agent 能看清楚：

- 每一步输入是什么
- 调用什么代码或工具
- 输出什么文件
- 如何判断这一步是否通过

当前项目不是生成 RoboTwin task 的 `play_once()`，而是生成一个可被 RoboTwin 下游任务复用的 tabletop scene/background。

---

## 0. 一句话流程

```text
Natural language scene prompt
-> asset grounding
-> prompt case catalog
-> Designer placement
-> Critic/static validation
-> Orchestrator final placement
-> scene Python codegen
-> RoboTwin smoke render
-> visual/VLM review
-> repair loop if needed
```

例子：

```text
Input prompt:
  an apple and a plate on the table

Main output:
  generated_scenes/apple_plate_scene.py
```

这个 scene module 以后可以被下游 RoboTwin task import，例如再写一个 task 去执行 “pick the apple and place it on the plate”。

---

## 1. 一条命令跑完整流程

### 普通复现机器

假设 RoboTwin 仓库在 `~/RoboTwin`：

```bash
python generate_scene/run_scene_generation_pipeline.py \
  --prompt "an apple and a plate on the table" \
  --master-catalog asset_catalogs/robotwin_tabletop_assets_master.json \
  --case-name apple_plate \
  --robotwin-root ~/RoboTwin \
  --generated-scene-dir generated_scenes \
  --out-dir runs/apple_plate_scene \
  --run-smoke
```

### 5090 机器

如果没有提前激活 RoboTwin conda 环境，显式指定 RoboTwin Python：

```bash
cd /data/sdb/zhengye/robotwin-text2env-demo

python3 generate_scene/run_scene_generation_pipeline.py \
  --prompt "an apple and a plate on the table" \
  --master-catalog asset_catalogs/robotwin_tabletop_assets_master.json \
  --case-name apple_plate \
  --robotwin-root /data/sdb/zhengye/RoboTwin \
  --generated-scene-dir generated_scenes \
  --out-dir runs/apple_plate_scene \
  --run-smoke \
  --python-executable /data/sdb/zhengye/miniconda3/envs/RoboTwin/bin/python
```

---

## 2. Step-by-step Pipeline

| Step | Purpose | Input | Code / tool | Output | Pass signal |
| --- | --- | --- | --- | --- | --- |
| 1 | 接收自然语言场景描述 | prompt string | `generate_scene/run_scene_generation_pipeline.py` | run config in `scene_generation_summary.json` | prompt 被记录 |
| 2 | 抽取并匹配资产 | prompt + master catalog | `generate_scene/asset_grounding.py` | `runs/<case>/asset_grounding.json` | `unmatched_mentions` 为空 |
| 3 | 生成 prompt case catalog | `asset_grounding.json` + master catalog | `prompt_case_from_grounding()` | `asset_catalogs/prompt_cases/<case>.json` and `runs/<case>/prompt_case.json` | selected assets 都在 master catalog 中 |
| 4 | Designer 初始摆放 | prompt case + spatial relations | `generate_scene/model_providers.py` | `runs/<case>/designer_initial_placement.json` | pose 在桌面 bounds 内 |
| 5 | Static Critic 检查 | initial placement | `generate_scene/schemas.py`, `validate_placement_spec()` | `runs/<case>/static_validation_initial.json` | no schema/asset/bounds/collision failure |
| 6 | Orchestrator 输出 final placement | designer + critic results | `generate_scene/model_providers.py` | `runs/<case>/final_placement.json` | final placement validation pass |
| 7 | 生成 RoboTwin scene module | final placement | `generate_scene/scene_codegen.py` | `generated_scenes/<case>_scene.py` | module imports and exposes `load_scene()` |
| 8 | RoboTwin smoke render | generated scene module + RoboTwin | `generate_scene/run_robotwin_placement_smoke.py`, `generate_scene/tools.py` | `runs/<case>/smoke/`, preview images, `smoke_report.json` | simulator starts, objects load, render saved |
| 9 | Visual/VLM review | smoke preview images | current human/Codex review, future VLM backend | `runs/<case>/visual_review.json` | object identity, pose, contact, direction all pass |
| 10 | Repair loop | failed review or smoke report | Orchestrator + affected file | updated placement/catalog/scene module | rerun passes |

---

## 3. Artifact Map

For a case named `apple_plate`, the important artifacts are:

```text
runs/apple_plate_scene/
  asset_grounding.json              # prompt mentions -> asset ids
  prompt_case.json                  # copied prompt-specific catalog
  designer_initial_placement.json   # first placement proposal
  static_validation_initial.json    # schema/static checks before repair
  final_placement.json              # final placement spec
  static_validation_final.json      # schema/static checks after finalization
  scene_codegen_report.json         # generated module path and codegen status
  smoke/
    smoke_report.json               # RoboTwin smoke result
    observer_camera.png             # external preview
    head_camera.png                 # robot/head preview
  visual_review.json                # required before final pass
  scene_generation_summary.json     # one-file run summary

generated_scenes/
  apple_plate_scene.py              # reusable RoboTwin scene/background loader

asset_catalogs/prompt_cases/
  apple_plate.json                  # prompt-specific selected assets
```

Small review evidence can be copied to:

```text
previews/apple_plate_scene_module_smoke/
```

Do not commit the full `runs/` directory.

---

## 4. Main Files and Responsibilities

Current Python implementation lives in one Code_gen-style package:

```text
generate_scene/
```

The older `harness/`, `scripts/`, and `mcp_lite/` paths now contain compatibility wrappers only, so old commands can still run while new work should edit `generate_scene/`.

### `asset_catalogs/robotwin_tabletop_assets_master.json`

Master asset catalog. It records available RoboTwin tabletop objects, aliases, model ids, default poses, size hints, and placement defaults.

Used by:

```text
generate_scene/asset_grounding.py
generate_scene/asset_catalog.py
generate_scene/run_scene_generation_pipeline.py
```

### `asset_catalogs/prompt_cases/*.json`

Prompt-specific small catalogs. They select only the assets needed for one scene prompt.

Example:

```text
asset_catalogs/prompt_cases/apple_plate.json
```

### `generate_scene/run_scene_generation_pipeline.py`

Main orchestrator. This is the preferred entry point.

It calls:

```text
asset grounding
prompt case generation
Designer/Critic/Orchestrator reference provider
scene code generator
optional RoboTwin smoke
```

### `generate_scene/asset_grounding.py`

Maps natural-language mentions to asset ids in the master catalog.

Current behavior:

```text
deterministic exact match over semantic_name / aliases / tags
```

Future behavior:

```text
LLM/VLM/embedding retrieval over larger asset library
```

Important rule:

```text
Do not invent asset ids. If unsure, write unmatched_mentions.
```

### `generate_scene/model_providers.py`

Reference agent backend for Designer, Critic, and Orchestrator.

Current backend:

```text
codex_reference / deterministic reference logic
```

Future backend:

```text
OpenAI API, Qwen, Claude, local vLLM, or VLM services
```

### `generate_scene/scene_codegen.py`

Converts `final_placement.json` into a reusable Python module:

```text
generated_scenes/<case>_scene.py
```

The generated file should expose:

```python
def load_scene(task, placement_spec=None):
    ...
```

It must not generate a task `play_once()` as the main output.

### `generate_scene/run_robotwin_placement_smoke.py`

Runs RoboTwin preview/smoke against either a placement spec or generated scene module.

For this project, the important mode is:

```text
--scene-module generated_scenes/<case>_scene.py
```

### `generate_scene/tools.py`

Thin callable wrapper around the local harness. It is useful for MCP-style or agent-tool usage.

Notably, `run_robotwin_smoke()` can call the RoboTwin smoke runner and pass the correct Python executable.

### `skills/generate-robotwin-tabletop-scene/`

Handoff skill for another Codex/agent. If another agent needs to generate a new scene from a fresh prompt, give it this skill plus the repo.

---

## 5. Coordinate and Direction Convention

Natural-language directions use the robot or dual-arm first-person frame by default.

```text
right = robot's right side
left = robot's left side
front = away from robot on the table
back = closer to robot
up = positive z
```

Example:

```text
a laptop is on the right side of a knife
```

Expected placement:

```text
laptop x > knife x
```

Do not judge left/right only from `observer_camera.png`, because the observer camera can rotate or mirror the view.

---

## 6. What Counts as Pass

Static pass means:

```text
schema is valid
assets exist in catalog
poses are inside tabletop bounds
approx collision checks pass
spatial relations are consistent with robot-centric coordinates
```

Smoke pass means:

```text
RoboTwin imports the generated scene module
objects are loaded
simulation starts
preview images or video are written
smoke_report.json status is pass
```

Final visual pass means:

```text
requested objects are visible
object identities are correct
objects are on the table
no obvious penetration or floating
orientation is reasonable
robot-centric spatial relation matches the prompt
scene can support a downstream robot task
```

Important:

```text
smoke pass != final pass
```

A scene can render successfully but still fail visual review, for example if a basket penetrates the table or an object is oriented incorrectly.

---

## 7. How To Add a New Prompt

Example new prompt:

```text
a laptop is on the right side of a knife
```

Run:

```bash
python generate_scene/run_scene_generation_pipeline.py \
  --prompt "a laptop is on the right side of a knife" \
  --master-catalog asset_catalogs/robotwin_tabletop_assets_master.json \
  --case-name laptop_knife \
  --robotwin-root ~/RoboTwin \
  --generated-scene-dir generated_scenes \
  --out-dir runs/laptop_knife_scene \
  --run-smoke
```

Then inspect:

```text
runs/laptop_knife_scene/asset_grounding.json
runs/laptop_knife_scene/final_placement.json
generated_scenes/laptop_knife_scene.py
runs/laptop_knife_scene/smoke/observer_camera.png
runs/laptop_knife_scene/smoke/head_camera.png
```

If visual review fails, repair one of:

```text
asset_catalogs/robotwin_tabletop_assets_master.json
runs/<case>/final_placement.json
generate_scene/model_providers.py
generate_scene/scene_codegen.py
```

Then rerun the same command.

---

## 8. Repository Cleanliness Rules

Keep:

```text
source code
schemas
asset catalog samples
prompt case samples
generated scene modules that are useful examples
small preview images and summary JSON for review evidence
docs
skills
```

Do not keep in git:

```text
full runs/
HDF5 data
large videos
RoboTwin assets/
checkpoints/
logs/
wandb/
venv/
__pycache__/
```

Local old review packets such as `robotwin_text2env_demo/` are historical review material, not part of the current runnable pipeline.

---

## 9. Current MVP Status

Completed:

```text
prompt -> asset grounding
asset grounding -> prompt case
prompt case -> PlacementSpec
PlacementSpec -> generated scene module
generated scene module -> RoboTwin smoke
small smoke evidence saved for apple_plate
```

Still important:

```text
formal visual/VLM review schema
automatic visual repair loop
larger asset catalog
downstream task consuming generated scene module
```
