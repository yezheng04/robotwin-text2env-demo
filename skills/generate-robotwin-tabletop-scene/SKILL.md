---
name: generate-robotwin-tabletop-scene
description: Generate and validate RoboTwin tabletop placement scenes from new natural-language prompts. Use when Codex needs to turn a prompt such as "a laptop is on the right side of a knife" into a RoboTwin scene preview by creating or updating an asset catalog, running the harness, performing smoke validation, requiring visual/VLM review, repairing placement failures, and recording new lessons back into skills.
---

# Generate RoboTwin Tabletop Scene

Use this skill as the top-level workflow for a new tabletop placement prompt. It coordinates the repo's existing components:

- `harness/` for prompt-to-placement pipeline.
- `mcp_lite/` for validation, smoke, artifact, and visual-review tools.
- `scripts/run_robotwin_placement_smoke.py` for RoboTwin loading and preview rendering.
- `asset_catalogs/` for prompt-specific asset metadata and placement defaults.
- The focused skills under `skills/` for Designer, Critic, Orchestrator, asset grounding, and smoke review behavior.

This skill assumes the agent is working in the `robotwin-text2env-demo` repo and the user has a RoboTwin install such as `~/RoboTwin`. If the repo components are missing, ask for the repo or clone it before running.

## Required Workflow

1. Read the user's prompt and identify all objects plus spatial relations.
2. Find or create an asset catalog for those objects.
3. Run static pipeline first.
4. Run RoboTwin smoke with `--run-smoke`.
5. Inspect preview image/video with human, Codex visual reference, or external VLM.
6. If visual review fails, repair catalog defaults or placement logic and rerun.
7. Only mark full pass when static validation, smoke, and explicit visual review all pass.
8. Record any newly discovered pitfall in the relevant skill and catalog.

## References

Read these only as needed:

- `references/new-prompt-workflow.md`: exact end-to-end commands and artifact expectations.
- `references/asset-catalog-rules.md`: how to build prompt-specific catalogs and handle rigid/articulated assets.
- `references/visual-review-gate.md`: how to decide pass/pending/fail and write visual review JSON.
- `references/known-pitfalls.md`: lessons learned from apple/plate, vegetable/basket, laptop/knife runs.

## Status Rules

- `PASS_STATIC_ONLY`: static JSON/catalog validation passed; no RoboTwin render yet.
- `REVIEW_REQUIRED` / `pending_visual_review`: smoke rendered artifacts, but no valid visual report has passed.
- `PASS`: static validation, smoke, and explicit visual review report all passed.
- `FAIL`: static validation, smoke, or visual review failed.

Never treat smoke success as visual success.

## Standard Commands

Static-only:

```bash
python harness/run_placement_pipeline.py \
  --prompt "<placement prompt>" \
  --asset-catalog asset_catalogs/<catalog>.json \
  --robotwin-root ~/RoboTwin \
  --model-provider codex_reference \
  --out-dir runs/<run_name>
```

Smoke render:

```bash
python harness/run_placement_pipeline.py \
  --prompt "<placement prompt>" \
  --asset-catalog asset_catalogs/<catalog>.json \
  --robotwin-root ~/RoboTwin \
  --model-provider codex_reference \
  --out-dir runs/<run_name> \
  --run-smoke
```

Full pass after visual review:

```bash
python harness/run_placement_pipeline.py \
  --prompt "<placement prompt>" \
  --asset-catalog asset_catalogs/<catalog>.json \
  --robotwin-root ~/RoboTwin \
  --model-provider codex_reference \
  --out-dir runs/<run_name>_visual_pass \
  --run-smoke \
  --visual-review-report previews/<run_name>/visual_review_codex_reference.json
```

## Non-Negotiables

- Do not invent RoboTwin asset ids or model ids.
- Do not rely on object mention order for spatial relations.
- Interpret natural-language directions from the robot / dual-arm first-person viewpoint. Left, right, front, and back mean the robot's left/right/front/back unless the prompt explicitly names another frame of reference.
- Do not mark a scene pass without visual review.
- Do not commit large generated data such as HDF5, full `runs/`, checkpoints, or RoboTwin assets.
- Do keep small preview evidence and prompt-specific asset catalogs when useful.
- Do update focused skills with new lessons after each new prompt.
