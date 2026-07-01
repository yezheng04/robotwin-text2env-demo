# RoboTwin Placement Critic

Use this skill when reviewing a Designer-generated `TabletopPlacementSpec`.

## Scope

Check scene-construction quality only:

- Prompt/object semantic match.
- Asset and model availability.
- Workspace bounds.
- Approximate collision risk.
- Stability metadata.
- Reachability and camera visibility risk.
- Whether the scene can support a later downstream robot task.

Do not judge policy training, data collection quality, or task success predicates.

## Output

Return strict JSON using `robotwin.tabletop_placement_critic.v0` with verdict `accept_for_next_stage`, `repair_required`, or `reject`.
