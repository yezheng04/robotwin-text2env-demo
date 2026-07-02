# Scene Generation Workflow

更新时间：2026-07-02

本项目当前目标：从自然语言生成 RoboTwin tabletop scene/background，而不是生成 RoboTwin task `play_once()`。

## Main Command

```bash
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

## Step Table

| Step | Input | Code | Output |
| --- | --- | --- | --- |
| 1. Asset discovery | `--robotwin-root` | `generate_scene/asset_discovery.py` | `runs/<case>/robotwin_discovered_asset_catalog.json` |
| 2. Asset grounding | prompt + discovered catalog | `generate_scene/gpt_agent.py`, `prompts/asset_grounding_agent.md` | `asset_grounding.json`, `prompt_case_catalog.json` |
| 3. Designer placement | prompt case catalog | `generate_scene/gpt_agent.py`, `prompts/designer_agent.md` | `designer_initial_placement.json` |
| 4. Static validation | placement + catalog | `generate_scene/schemas.py` | `static_validation_initial.json` |
| 5. Static critic/orchestrator | validation report | `generate_scene/gpt_agent.py`, critic/orchestrator prompts | `critic_review.json`, `final_placement.json` |
| 6. Scene codegen | `final_placement.json` | `generate_scene/scene_codegen.py` | `generated_scenes/<case>_scene.py` |
| 7. RoboTwin smoke | generated scene module | `generate_scene/run_robotwin_placement_smoke.py` | `smoke/head_camera.png`, `smoke/observer_camera.png`, `smoke_report.json` |
| 8. VLM review | smoke images | `generate_scene/observation_agent.py`, `prompts/observation_vlm_agent.md` | `visual_review.json` |
| 9. Optional repair | visual failure | `generate_scene/gpt_agent.py`, `prompts/visual_repair_agent.md` | repaired placement, rerun smoke/review |

## Core Files

```text
generate_scene/run_scene_generation_pipeline.py   # pipeline entry
generate_scene/asset_discovery.py                 # scan RoboTwin assets/objects
generate_scene/gpt_agent.py                       # text agents
generate_scene/observation_agent.py               # VLM review agent
generate_scene/moonshot_client.py                 # OpenAI-compatible Moonshot/Kimi client
generate_scene/scene_codegen.py                   # PlacementSpec -> scene module
generate_scene/schemas.py                         # static validation
generate_scene/run_robotwin_placement_smoke.py    # RoboTwin render evidence
```

## Prompt Specs

```text
generate_scene/prompts/asset_grounding_agent.md
generate_scene/prompts/designer_agent.md
generate_scene/prompts/static_critic_agent.md
generate_scene/prompts/orchestrator_agent.md
generate_scene/prompts/observation_vlm_agent.md
generate_scene/prompts/visual_repair_agent.md
```

These markdown files define how external LLM/VLM models should behave.

## Orientation Lesson

Thin everyday objects such as:

```text
notebook, book, phone, remote control, cards
```

should normally be placed flat on the tabletop with the broad face down. A scene where such objects stand upright on a narrow edge should fail visual review unless the prompt explicitly requests upright/standing/leaning placement.

Once an object is physically flat, different in-plane yaw angles are acceptable scene diversity unless the prompt specifies a facing direction or alignment.

## Outputs To Review

For each run:

```text
runs/<case>/scene_generation_summary.json
runs/<case>/asset_grounding.json
runs/<case>/final_placement.json
runs/<case>/visual_review.json
runs/<case>/smoke/head_camera.png
runs/<case>/smoke/observer_camera.png
generated_scenes/<case>_scene.py
```

For GitHub, keep only small curated examples under `previews/` and generated scene examples under `generated_scenes/`. Do not commit full `runs/`, HDF5 data, checkpoints, logs, or real API keys.
