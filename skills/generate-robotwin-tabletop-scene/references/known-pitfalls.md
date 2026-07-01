# Known Pitfalls

## Smoke Pass Is Not Visual Pass

RoboTwin can load and render a scene while objects are visually wrong. Always require visual review before full pass.

## Basket Orientation

`110_basket` with identity qpos appears side-facing. Use:

```json
[0.70710678, 0.70710678, 0, 0]
```

Store this in `placement_defaults.qpos`.

## Laptop Loader

`015_laptop` is articulated/URDF. It needs `create_sapien_urdf_obj` through `placement_defaults.loader = "sapien_urdf"`.

Use the RoboTwin `open_laptop` convention:

```json
"qpos": [0.7, 0, 0, 0.7],
"fix_root_link": true
```

## Knife Stability

`034_knife` is rigid but metadata says `stable=false`. For scene-background placement, set it static and require visual review.

## Local Coordinates vs Visual Coordinates

For left/right language, final acceptance is the preview image. The observer camera can make tabletop-local x appear reversed.

## Relation Parsing

Normalize determiners before relation matching:

```text
a laptop is on the right side of a knife
-> laptop right_of knife
```

Do not infer relation from mention order.
