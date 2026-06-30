# RoboTwin Tabletop Placement Agent

SceneSmith-style tabletop asset placement for RoboTwin scenes.

This project focuses on the **placement agent**: given a natural-language tabletop scene description and an asset catalog, decide which assets should appear in the scene and where they should be placed so that the resulting RoboTwin scene is semantically correct, physically valid, and useful for downstream robot tasks or external policies.

Example:

```text
Scene request:
  a banana on the left side of the table and an apple on the right side

Placement output:
  banana asset -> left tabletop region
  apple asset -> right tabletop region
  poses satisfy left/right semantics, table bounds, collision, and stability

Possible downstream RoboTwin task:
  pick the banana from the left side and move it to the right side
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
a banana on the left side of the table and an apple on the right side
```

Then instantiate the placed scene in RoboTwin and verify that it can support a downstream task such as:

```text
pick the banana from the left side and place it near the apple on the right side
```

First deliverables:

- RoboTwin asset inventory for prompt writing: `robotwin_asset_inventory.md`.
- `TabletopPlacementSpec` schema.
- Asset catalog format.
- Designer / Critic / Orchestrator prompts for placement.
- RoboTwin placement adapter.
- Placement validation report.
- Smoke video showing the placed scene is physically usable.
