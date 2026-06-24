# RoboTwin2 Text2Env Demo (SceneSmith-lite Tabletop)

This repository contains a minimal Text2Env pipeline for generating a RoboTwin2 tabletop task from natural language.

The smoke-tested task is:

```text
Move the green block from the left zone to the right zone without moving the blue bowl.
```

## What Is Included

- Text2Env schema and examples.
- SceneSmith-lite Designer / Critic / Orchestrator prompts.
- A JSON validator and natural-language-to-Text2Env helper.
- A Text2Env-to-RoboTwin2 task scaffold generator.
- Generated RoboTwin2 task code for `move_object_between_zones`.
- Smoke-test report and small preview artifacts.

RoboTwin itself and RoboTwin assets are not vendored in this repository. Clone and install RoboTwin separately.

## Repository Layout

```text
schemas/
  text2env.schema.json
  text2env_schema_v0.md

examples/tabletop_tasks/
  move_object_between_zones.json
  move_red_block_to_blue_zone.json
  put_cup_in_drawer.json

prompts/
  text2env_designer.md
  text2env_critic.md
  text2env_orchestrator.md

scripts/
  generate_text2env.py
  generate_robotwin_task.py
  deploy_to_robotwin.sh

generated/robotwin_tasks/move_object_between_zones/
  envs/move_object_between_zones.py
  description/task_instruction/move_object_between_zones.json
  manifest.json

reports/smoke_tests/move_object_between_zones/
  notes.md

robotwin_text2env_smoke/move_object_between_zones/
  episode0.mp4
  episode0.json
  scene_info.json
  seed.txt
  frame_start.jpg
  frame_mid.jpg
  frame_end.jpg
```

## Reproduce On Your Machine

First, make sure RoboTwin exists on your machine. The examples below assume the RoboTwin repository lives at:

```text
~/RoboTwin
```

If you already have RoboTwin installed somewhere else, replace `~/RoboTwin` in the commands with your own RoboTwin path.

If you do not have RoboTwin yet, clone and install RoboTwin following the official RoboTwin documentation:

```bash
git clone https://github.com/robotwin-Platform/robotwin ~/RoboTwin
```

Then install RoboTwin dependencies and assets according to:

```text
https://robotwin-platform.github.io/doc/usage/index.html
```

The tested conda environment name was:

```text
RoboTwin
```

Confirm the repository layout before deploying:

```bash
test -d ~/RoboTwin/envs
test -d ~/RoboTwin/description/task_instruction
```

Deploy the generated task into RoboTwin:

```bash
cd /path/to/this/repo
bash scripts/deploy_to_robotwin.sh ~/RoboTwin move_object_between_zones
```

This copies the generated files into:

```text
~/RoboTwin/envs/move_object_between_zones.py
~/RoboTwin/description/task_instruction/move_object_between_zones.json
```

Run the smoke/data dry run:

```bash
cd ~/RoboTwin
source ~/miniconda3/etc/profile.d/conda.sh
conda activate RoboTwin
timeout 900 bash collect_data.sh move_object_between_zones demo_smoke 0 2>&1 | tee install_logs/smoke_collect_move_object_between_zones_step5_pass.log
```

If your conda installation is not under `~/miniconda3`, replace the `source` path with your own conda profile path.

Expected outputs:

```text
data/move_object_between_zones/demo_smoke/data/episode0.hdf5
data/move_object_between_zones/demo_smoke/video/episode0.mp4
data/move_object_between_zones/demo_smoke/instructions/episode0.json
data/move_object_between_zones/demo_smoke/scene_info.json
data/move_object_between_zones/demo_smoke/seed.txt
```

The HDF5 file is intentionally not tracked here because it is about 348 MB. Regenerate it with the command above.

## Regenerate The RoboTwin Task Scaffold

From this repository:

```bash
python scripts/generate_text2env.py check examples/tabletop_tasks/move_object_between_zones.json
python scripts/generate_robotwin_task.py generate examples/tabletop_tasks/move_object_between_zones.json
```

Then deploy again:

```bash
bash scripts/deploy_to_robotwin.sh ~/RoboTwin move_object_between_zones
```

## Smoke-Test Summary

The passing smoke run generated:

- One episode with seed `0`.
- Video: `2293` frames, `320x240`, `30 FPS`.
- HDF5 groups: `endpose`, `joint_action`, `observation`, `pointcloud`.
- Checked HDF5 fields:
  - `joint_action/vector`: `(2293, 14)`, `float64`
  - `observation/head_camera/rgb`: `(2293,)`
  - `endpose/left_endpose`: `(2293, 7)`, `float64`

See `reports/smoke_tests/move_object_between_zones/notes.md` for details.

## Known Limitations

- Current v0 uses RoboTwin existing assets or simple geometry. It does not generate missing mesh assets such as a novel `peach`.
- Region grounding still needs improvement: natural-language phrases such as `from the left zone` should be enforced as an initial-state constraint.
- The passing task uses visible zone markers as tabletop mats, but they are not added as planner keep-out obstacles.
- RoboTwin may print many `svulkan2 OIDN Error: invalid handle` messages during video export. In the tested run, these warnings did not prevent MP4, HDF5, or instruction generation.
