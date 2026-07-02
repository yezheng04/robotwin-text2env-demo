# RoboTwin Tabletop Scene Generation Agent

SceneSmith-style tabletop scene/background generation for RoboTwin.

This project focuses on generating reusable RoboTwin tabletop scenes: given a natural-language tabletop scene description, ground mentioned objects to RoboTwin assets, decide where they should be placed, generate a scene/background Python module, and validate the result with RoboTwin smoke plus visual review.

Example:

```text
Scene request:
  an apple and a plate on the table

Placement output:
  apple asset -> reachable tabletop region
  plate asset -> reachable tabletop region
  poses satisfy object presence, table bounds, collision, and stability

Possible downstream RoboTwin task:
  pick the apple and place it on the plate
```

## What We Are Building

A lightweight SceneSmith-inspired scene generation loop:

```text
Natural-language scene request
-> Asset Grounding agent maps mentions to RoboTwin assets
-> Designer proposes tabletop placements
-> Critic checks semantic fit and physical/robot usability
-> Scene codegen writes generated_scenes/<scene>_scene.py
-> RoboTwin smoke + visual/VLM review validate the scene
-> Downstream robot task or external policy imports the scene
```

The asset problem is treated as a library/retrieval problem. Assets are expected to come from a richer asset library; this repo focuses on semantic grounding, tabletop placement, and validation in RoboTwin.

## Planned System Direction

The next system-level goal is to turn the current prompt-and-script demo into an MCP + skill + harness workflow:

```text
Skills define how Designer / Critic / Orchestrator should reason
-> MCP tools expose RoboTwin asset, validation, smoke, and render functions
-> Harness runner executes the full reproducible pipeline from prompt to preview
```

This keeps agent roles independent from the model backend. The same workflow should later work with Codex reference outputs, OpenAI API models, Qwen, Claude, or local vLLM/VLM backends.

## Agent Handoff Skill

For another Codex or agent to reproduce a new prompt-to-scene run, start from the top-level skill:

```text
skills/generate-robotwin-tabletop-scene/
```

That skill is the handoff entry point. It tells the agent how to parse a new placement prompt, ground objects to assets, run the harness, require RoboTwin smoke evidence, require visual/VLM review before calling a scene passed, repair failures, and write newly discovered pitfalls back into the focused skills.

The focused skills remain available for individual capabilities:

```text
skills/design-tabletop-placement/
skills/critique-tabletop-placement/
skills/orchestrate-placement-pipeline/
skills/ground-objects-to-robotwin-assets/
skills/review-robotwin-smoke-preview/
```

## Scope

In scope:

- Parse tabletop placement intent from natural language.
- Retrieve semantically appropriate assets from an asset catalog.
- Place assets on the table with meaningful spatial relations.
- Produce a structured `TabletopPlacementSpec`.
- Instantiate the placed scene in RoboTwin.
- Validate collision, stability, reachability, camera visibility, and downstream task usability.

Out of scope for this repo:

- Training a 3D asset generation model.
- Directly generating a new RoboTwin task program as the main objective.
- Full room/house-scale SceneSmith reproduction.
- Solving every downstream manipulation policy.

## Active Design

The current project plan is:

```text
robotwin2_text2env_scenesmith_lite_plan.md
```

The old Text2Env task-generation prototype has been removed from the main repo to avoid confusion.

## RoboTwin Path Assumption

Examples assume RoboTwin is installed at:

```text
~/RoboTwin
```

On the 5090 machine this points to:

```text
/data/sdb/zhengye/RoboTwin
```

## Next MVP

Start with a simple placement prompt:

```text
an apple and a plate on the table
```

Then instantiate the placed scene in RoboTwin and verify that it can support a downstream task such as:

```text
pick the apple and place it on the plate
```

First deliverables:

- RoboTwin asset inventory for prompt writing: `robotwin_asset_inventory.md`.
- Master asset catalog: `asset_catalogs/robotwin_tabletop_assets_master.json`.
- Prompt case catalog sample: `asset_catalogs/prompt_cases/apple_plate.json`.
- Designer prompt: `prompts/designer_prompt.md`.
- Designer initial placement: `placements/apple_plate_table/designer_initial_placement.json`.
- Critic prompt: `prompts/critic_prompt.md`.
- Critic static review: `placements/apple_plate_table/critic_review.json`.
- Orchestrator prompt: `prompts/orchestrator_prompt.md`.
- Final static placement for smoke: `placements/apple_plate_table/final_placement.json`.
- Validation plan: `placements/apple_plate_table/validation_plan.json`.
- RoboTwin smoke runner: `scripts/run_robotwin_placement_smoke.py`.
- Smoke result: `placements/apple_plate_table/smoke_result.json`.
- Visual review: `placements/apple_plate_table/visual_review.json`.
- Preview image/video: `previews/apple_plate_table/`.
- `TabletopPlacementSpec` schema.
- RoboTwin placement adapter.
- Placement validation report.
- Smoke video showing the placed scene is physically usable.

## One-Command Prompt To Generated Scene

After RoboTwin is installed at `~/RoboTwin`, run:

```bash
python harness/run_scene_generation_pipeline.py \
  --prompt "an apple and a plate on the table" \
  --master-catalog asset_catalogs/robotwin_tabletop_assets_master.json \
  --case-name apple_plate \
  --robotwin-root ~/RoboTwin \
  --model-provider codex_reference \
  --out-dir runs/apple_plate_scene \
  --run-smoke
```

The harness writes asset grounding, prompt case, Designer, Critic, Orchestrator, generated scene module, validation, smoke, and preview artifacts under the selected `--out-dir`. The reusable generated scene module is written to `generated_scenes/apple_plate_scene.py`.

The older `harness/run_placement_pipeline.py` remains available when you already have a prompt case catalog and only need PlacementSpec-to-preview behavior.
