# Ground Objects To RoboTwin Assets

Use this skill when mapping natural-language object mentions to RoboTwin asset catalog entries.

## Rules

- Match prompt terms against `semantic_name`, `aliases`, and `tags`.
- Prefer exact semantic matches over broad category matches.
- Return uncertainty when multiple assets plausibly match.
- Never fabricate missing assets; mark them as unavailable or request a richer catalog.
- Preserve the selected `asset_id`, `model_id`, and metadata needed by the placement validator.
