# Review RoboTwin Smoke Preview

Use this skill when checking RoboTwin smoke outputs from a placement run. Smoke success only proves that RoboTwin loaded and rendered the scene; it is not enough to accept the scene.

## Checks

- `smoke_report.json` exists and reports pass.
- `head_camera.png` and `observer_camera.png` exist.
- Optional `observer_camera.mp4` exists.
- The preview should be inspected by a human or VLM for object identity, prompt match, floating, penetration, severe occlusion, and wrong object count.
- Mark the scene failed when an object is visibly sideways, upside down, penetrating the table, floating, severely occluded, or semantically wrong.
- Mark the scene pending when no human/VLM/Codex-visual review has inspected the image.

This skill does not replace a visual model. It defines the review criteria and artifact contract.
