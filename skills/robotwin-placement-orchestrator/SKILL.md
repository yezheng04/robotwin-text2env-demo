# RoboTwin Placement Orchestrator

Use this skill when combining Designer output, Critic review, and validation results into the next pipeline artifact.

## Rules

- If the Critic rejects the placement, stop with a blocked decision.
- If repair is required, produce concrete repair instructions.
- If accepted, write a final `robotwin.tabletop_placement.v0` artifact with stage `final_static_for_smoke`.
- Preserve valid object ids, asset ids, model ids, and poses.
- Carry simulator and render checks into the validation plan.
- Do not claim visual verification until RoboTwin preview evidence has been reviewed.

## Output

Return final placement JSON and a validation plan.
