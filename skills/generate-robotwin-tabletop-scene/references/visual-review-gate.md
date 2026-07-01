# Visual Review Gate

The visual gate prevents bad scenes from being marked as successful just because RoboTwin rendered an image.

## Rule

```text
static pass + smoke pass != full pass
static pass + smoke pass + visual review pass = full pass
```

## What To Check

- requested objects are present
- no extra obvious wrong object dominates the scene
- spatial relations match the prompt in the preview image
- object orientation is plausible
- no obvious table penetration
- no severe floating
- no severe occlusion
- object identity is recognizable enough for the prompt

## Left/Right Prompts

Judge left/right in the preview image frame, not only in tabletop-local coordinates. The default RoboTwin observer camera can mirror local x.

## Failure Examples

- Basket appears sideways or penetrates the table.
- Laptop appears on the visual left when prompt says right of knife.
- A support/container object is loaded dynamically and falls or rotates.
- An articulated object is loaded through the rigid loader.

## Status Values

- `pending_human_or_vlm_visual_review`: artifacts exist but no semantic visual review has passed.
- `pass`: a human, Codex visual reference, or external VLM explicitly checked and accepted.
- `fail`: visual issue found; repair and rerun.

## Repair Hints

When failing, specify:

- object id
- visible problem
- likely fix: qpos, xyz, loader, static flag, scale, model id, or catalog default
- whether the fix belongs in code or `asset_catalogs/<catalog>.json`
