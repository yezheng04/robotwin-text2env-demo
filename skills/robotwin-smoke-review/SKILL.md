# RoboTwin Smoke Review

Use this skill when checking RoboTwin smoke outputs from a placement run.

## Checks

- `smoke_report.json` exists and reports pass.
- `head_camera.png` and `observer_camera.png` exist.
- Optional `observer_camera.mp4` exists.
- The preview should be inspected by a human or VLM for object identity, prompt match, floating, penetration, severe occlusion, and wrong object count.

This skill does not replace a visual model. It defines the review criteria and artifact contract.
