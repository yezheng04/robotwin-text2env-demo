# RoboTwin Tabletop Scene Generation

This repo is a SceneSmith-inspired tabletop scene/background generation harness for RoboTwin.

Given a natural-language scene prompt, the pipeline grounds objects to RoboTwin assets, designs tabletop poses, validates the placement, generates a reusable RoboTwin scene module, and optionally runs a RoboTwin smoke render.

Current example:

```text
an apple and a plate on the table
```

Output:

```text
generated_scenes/apple_plate_scene.py
runs/<case>/scene_generation_summary.json
runs/<case>/smoke/observer_camera.png
runs/<case>/smoke/head_camera.png
```

## Start Here

Read the full step-by-step workflow:

```text
docs/scene_generation_workflow.md
```

That document explains, for every stage:

- input
- code or tool used
- output
- validation signal
- where the artifact is saved

## One-Command Run

From this repo:

```bash
python harness/run_scene_generation_pipeline.py \
  --prompt "an apple and a plate on the table" \
  --master-catalog asset_catalogs/robotwin_tabletop_assets_master.json \
  --case-name apple_plate \
  --robotwin-root ~/RoboTwin \
  --generated-scene-dir generated_scenes \
  --out-dir runs/apple_plate_scene \
  --run-smoke
```

On the 5090 machine, if RoboTwin's conda Python is not already active, use:

```bash
python3 harness/run_scene_generation_pipeline.py \
  --prompt "an apple and a plate on the table" \
  --master-catalog asset_catalogs/robotwin_tabletop_assets_master.json \
  --case-name apple_plate \
  --robotwin-root /data/sdb/zhengye/RoboTwin \
  --generated-scene-dir generated_scenes \
  --out-dir runs/apple_plate_scene \
  --run-smoke \
  --python-executable /data/sdb/zhengye/miniconda3/envs/RoboTwin/bin/python
```

## Active Structure

```text
asset_catalogs/                         # RoboTwin asset metadata and prompt cases
generated_scenes/                       # generated reusable scene modules
harness/                                # main pipeline, schemas, grounding, placement, codegen
mcp_lite/                               # lightweight callable tools for agent/MCP-style usage
scripts/                                # RoboTwin smoke runner
skills/generate-robotwin-tabletop-scene/ # handoff skill for another Codex/agent
previews/                               # small committed visual evidence only
docs/                                  # workflow and repository documentation
```

## Main Entry Points

```text
harness/run_scene_generation_pipeline.py   # prompt -> generated scene -> optional smoke
harness/asset_grounding.py                 # prompt assets -> RoboTwin asset ids
harness/scene_codegen.py                   # final placement -> generated scene module
scripts/run_robotwin_placement_smoke.py    # RoboTwin render/smoke validation
```

## Current Project Plan

The living project plan is:

```text
robotwin2_text2env_scenesmith_lite_plan.md
```

The old Text2Env task-generation direction is no longer the main objective. The current objective is scene/background generation for downstream RoboTwin tasks or external policies.

## Commit Policy

Do commit:

- source code
- schemas
- asset catalog samples
- generated scene modules
- small preview images and summary JSON needed for review

Do not commit:

- HDF5 datasets
- full `runs/`
- large videos
- RoboTwin assets
- checkpoints, logs, wandb, or install caches
