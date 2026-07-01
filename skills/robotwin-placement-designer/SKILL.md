# RoboTwin Placement Designer

Use this skill when turning a natural-language tabletop scene request into an initial `TabletopPlacementSpec`.

## Inputs

- Placement prompt.
- Asset catalog JSON.
- Table workspace bounds.
- Optional downstream robot task hint.

## Rules

- Select only assets that exist in the catalog.
- Do not invent asset ids, model ids, paths, affordances, or task code.
- Convert spatial language such as left, right, near, on, inside, and separated into explicit tabletop poses or regions.
- Keep every object inside workspace bounds.
- Prefer simple stable tabletop placements unless the prompt requests contact, stacking, or containment.
- Mark simulator, render, and visual checks as pending until smoke evidence exists.

## Output

Return strict JSON matching `robotwin.tabletop_placement.v0`.
