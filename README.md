# RoboTwin Tabletop Placement Agent

SceneSmith-style tabletop asset placement for RoboTwin scenes.

This project focuses on the **placement agent**: given a natural-language tabletop scene description and an asset catalog, decide which assets should appear in the scene and where they should be placed so that the resulting RoboTwin scene is semantically correct, physically valid, and useful for downstream robot tasks or external policies.

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

A lightweight SceneSmith-inspired placement loop:

```text
Natural-language scene request
-> Designer agent proposes assets and tabletop placements
-> Critic agent checks semantic fit and physical/robot usability
-> Orchestrator agent revises and finalizes the placement spec
-> RoboTwin adapter instantiates the placed scene
-> Downstream robot task or external policy runs in the scene
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
- Asset catalog sample: `asset_catalogs/robotwin_tabletop_assets_sample.json`.
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

## One-Command Prompt To Preview

After RoboTwin is installed at `~/RoboTwin`, run:

```bash
python harness/run_placement_pipeline.py \
  --prompt "an apple and a plate on the table" \
  --asset-catalog asset_catalogs/robotwin_tabletop_assets_sample.json \
  --robotwin-root ~/RoboTwin \
  --model-provider codex_reference \
  --out-dir runs/apple_plate_table_harness \
  --run-smoke
```

The harness writes Designer, Critic, Orchestrator, validation, smoke, and preview artifacts under the selected `--out-dir`.
