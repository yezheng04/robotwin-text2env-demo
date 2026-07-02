# RoboTwin Tabletop Scene Generation

Scene generation harness for RoboTwin tabletop environments.

Given a natural-language prompt, the pipeline can:

```text
discover assets from RoboTwin/assets/objects
-> ground prompt objects to asset ids
-> generate a TabletopPlacementSpec
-> generate a RoboTwin scene Python module
-> run RoboTwin smoke render
-> review preview images with a VLM
-> optionally repair and rerun
```

Current accepted example:

```text
a remote control next to the notebook
```

## Repository Layout

```text
generate_scene/                 # main Python package
generate_scene/prompts/         # LLM/VLM behavior specs
generated_scenes/               # checked-in generated scene examples
asset_catalogs/                 # small fallback/sample catalogs
docs/                           # workflow and Moonshot/Kimi backend docs
previews/                       # small review images and JSON evidence
```

## One Command

On the 5090 machine:

```bash
cd /data/sdb/zhengye/robotwin-text2env-demo

python3 generate_scene/run_scene_generation_pipeline.py \
  --prompt "a remote control next to the notebook" \
  --case-name remote_control_notebook_kimi \
  --robotwin-root /data/sdb/zhengye/RoboTwin \
  --generated-scene-dir generated_scenes \
  --out-dir runs/remote_control_notebook_kimi \
  --discover-assets-from-robotwin \
  --model-provider moonshot \
  --run-smoke \
  --visual-review-mode moonshot \
  --visual-repair-attempts 1 \
  --python-executable /data/sdb/zhengye/miniconda3/envs/RoboTwin/bin/python
```

For another machine, replace `--robotwin-root` and `--python-executable` with that machine's RoboTwin paths.

## API Key

Do not commit API keys.

Use one of:

```bash
export MOONSHOT_API_KEY="..."
```

or create an ignored local file:

```text
generate_scene/local_config.py
```

with:

```python
MOONSHOT_API_KEY = "..."
```

## Important Docs

```text
docs/scene_generation_workflow.md
docs/moonshot_agent_backend.md
```

## Review Examples

```text
previews/apple_plate_scene_module_smoke/
previews/remote_control_notebook_flat_candidate/
```

The remote-control/notebook example records an important learned rule: thin everyday objects such as notebooks, phones, cards, and remote controls should normally lie flat on the tabletop. In-plane yaw variation is acceptable scene diversity unless the prompt specifies orientation.
