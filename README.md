# RoboTwin Tabletop Background Scene Generator

SceneSmith-style tabletop scene generation for RoboTwin.

This project is being refocused. The goal is no longer to generate a new RoboTwin task program from natural language. The new goal is:

```text
given an existing RoboTwin task
-> generate a semantically meaningful tabletop background scene
-> place assets around the task without breaking manipulation
-> validate collision, stability, reachability, and task compatibility
```

## What We Are Building

A lightweight SceneSmith-inspired agent loop for RoboTwin tabletop scenes:

```text
Natural-language scene request
-> Designer agent proposes tabletop background layout
-> Critic agent checks semantic fit and physical/task feasibility
-> Orchestrator agent revises and finalizes a scene spec
-> Scene adapter places assets in RoboTwin
-> RoboTwin smoke/eval verifies the task still works
```

The assets are expected to come from a richer asset library. This repo focuses on selecting, grounding, placing, and validating those assets in RoboTwin.

## Scope

In scope:

- Generate tabletop background/distractor scenes for existing RoboTwin tasks.
- Retrieve assets from a provided asset library.
- Produce a structured scene spec with asset ids, poses, keep-out zones, and constraints.
- Insert background assets into RoboTwin without changing the core task logic.
- Validate collision, stability, robot reachability, camera visibility, and task success.

Out of scope for this repo:

- Training a 3D asset generation model.
- Generating a new RoboTwin task from scratch.
- Creating articulated assets such as drawers from natural language.
- Full room/house-scale SceneSmith reproduction.

## Current Planning Document

The active design is in:

```text
robotwin2_text2env_scenesmith_lite_plan.md
```

The previous Text2Env task-generation prototype has been removed from the main repo to avoid confusion.

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

Use one existing RoboTwin task, for example `place_empty_cup` or `beat_block_hammer`, and generate 3-5 tabletop background variants such as:

```text
a tidy breakfast tabletop with a plate, spoon, napkin, and fruit around the task area, without blocking the robot arms
```

The first useful deliverables are:

- `SceneSpec` schema for tabletop background placement.
- Asset catalog format for retrieval and grounding.
- Designer / Critic / Orchestrator prompts.
- RoboTwin scene adapter that injects background assets.
- Smoke logs and videos showing the original task still runs with generated background scenes.
