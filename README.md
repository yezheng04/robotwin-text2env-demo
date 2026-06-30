# RoboTwin Tabletop Scene Generator

SceneSmith-style tabletop scene generation for RoboTwin.

This project is being refocused around **simulation-ready tabletop scenes**. The goal is not to generate a new RoboTwin task program directly. The goal is to generate a tabletop scene that a downstream robot task or external policy can use.

Example:

```text
Scene request:
  a banana on the left side of the table and an apple on the right side

Generated scene:
  table + banana placed on the left + apple placed on the right

Possible downstream RoboTwin task:
  pick the banana from the left side and move it to the right side
```

## What We Are Building

A lightweight SceneSmith-inspired agent loop:

```text
Natural-language scene request
-> Designer agent proposes objects and tabletop layout
-> Critic agent checks semantic fit and physical/robot usability
-> Orchestrator agent revises and finalizes the scene
-> RoboTwin scene adapter instantiates the scene
-> Downstream robot task or external policy runs in the scene
```

The asset problem is treated as a library/retrieval problem. Assets are expected to come from a richer asset library; this repo focuses on understanding the scene request, selecting assets, placing them correctly, and validating the scene in RoboTwin.

## Scope

In scope:

- Generate tabletop scenes from natural language.
- Retrieve semantically appropriate assets from an asset catalog.
- Place assets on the table with meaningful spatial relations.
- Produce a structured `TabletopSceneSpec`.
- Instantiate the scene in RoboTwin.
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

Start with simple tabletop scene prompts:

```text
a banana on the left side of the table and an apple on the right side
```

Then instantiate the scene in RoboTwin and verify that it can support a downstream task such as:

```text
pick the banana from the left side and place it near the apple on the right side
```

First deliverables:

- `TabletopSceneSpec` schema.
- Asset catalog format.
- Designer / Critic / Orchestrator prompts.
- RoboTwin scene adapter.
- Scene validation report.
- Smoke video showing the generated scene is physically usable.
