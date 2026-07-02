# RoboTwin Asset Inventory

Source path: `~/RoboTwin/assets/objects` (`/data/sdb/zhengye/RoboTwin/assets/objects`)

Purpose: a prompt-writing reference for the RoboTwin tabletop placement agent. Use these asset names when drafting the first placement prompts.

## Summary

- Top-level asset directories scanned: `125`
- Rigid assets with `model_data*.json`, `visual/base*.glb`, and `collision/base*.glb`: `111`
- Articulated/URDF-style assets: `9`
- Collection/helper directories: `5`
- Assets with `points_info.json`: `119`

Important prompt note: the current RoboTwin library has `035_apple` but no direct top-level `banana` asset. There is a generic `103_fruit` asset, but a banana-specific prompt may need the future richer asset library.

Current first MVP placement prompt: `an apple and a plate on the table`, using `035_apple` and `003_plate`.

## Good First Placement Prompt Ingredients

- Fruit/food prompts: `035_apple`, `103_fruit`, `075_bread`, `054_baguette`, `006_hamburg`, `005_french-fries`, `071_can`, `068_boxdrink`, `101_milk-tea`.
- Breakfast/table setting prompts: `003_plate`, `002_bowl`, `021_cup`, `039_mug`, `033_fork`, `034_knife`, `019_coaster`, `008_tray`, `076_breadbasket`.
- Office desk prompts: `015_laptop`, `092_notebook`, `010_pen`, `058_markpen`, `017_calculator`, `047_mouse`, `116_keyboard`, `077_phone`.
- Toolbench prompts: `020_hammer`, `030_drill`, `032_screwdriver`, `082_smallshovel`, `083_brush`, `084_woodenmallet`.
- Clutter/distractor prompts: `043_book`, `081_playingcards`, `073_rubikscube`, `057_toycar`, `046_alarm-clock`, `089_globe`, `090_trophy`.

## Prompt-Friendly Groups

### Fruit / food / drink
- `005_french-fries` (rigid, models=4, points=yes)
- `006_hamburg` (rigid, models=6, points=yes)
- `025_chips-tub` (rigid, models=4, points=yes)
- `029_olive-oil` (rigid, models=5, points=yes)
- `031_jam-jar` (rigid, models=5, points=yes)
- `035_apple` (rigid, models=2, points=yes)
- `038_milk-box` (rigid, models=4, points=yes)
- `054_baguette` (rigid, models=2, points=yes)
- `064_msg` (rigid, models=6, points=yes)
- `065_soy-sauce` (rigid, models=5, points=yes)
- `066_vinegar` (rigid, models=3, points=yes)
- `068_boxdrink` (rigid, models=4, points=yes)
- `069_vagetable` (rigid, models=7, points=yes)
- `071_can` (rigid, models=6, points=yes)
- `075_bread` (rigid, models=7, points=yes)
- `101_milk-tea` (rigid, models=6, points=yes)
- `103_fruit` (rigid, models=7, points=yes)
- `105_sauce-can` (rigid, models=5, points=yes)
- `112_tea-box` (rigid, models=6, points=yes)
- `113_coffee-box` (rigid, models=7, points=yes)

### Tableware / kitchen
- `002_bowl` (rigid, models=7, points=yes)
- `003_plate` (rigid, models=1, points=yes)
- `008_tray` (rigid, models=4, points=yes)
- `009_kettle` (articulated/urdf, models=0, points=yes)
- `019_coaster` (rigid, models=1, points=yes)
- `021_cup` (rigid, models=13, points=yes)
- `022_cup-with-liquid` (rigid, models=1, points=yes)
- `033_fork` (rigid, models=1, points=yes)
- `034_knife` (rigid, models=1, points=yes)
- `039_mug` (rigid, models=13, points=yes)
- `053_teanet` (rigid, models=5, points=yes)
- `060_kitchenpot` (articulated/urdf, models=0, points=yes)
- `062_plasticbox` (rigid, models=11, points=yes)
- `067_steamer` (rigid, models=3, points=yes)
- `076_breadbasket` (rigid, models=5, points=yes)
- `087_waterer` (rigid, models=8, points=yes)
- `088_wineglass` (rigid, models=5, points=yes)
- `091_kettle` (rigid, models=6, points=yes)
- `106_skillet` (rigid, models=4, points=yes)
- `110_basket` (rigid, models=4, points=yes)

### Containers / furniture / support objects
- `007_shoe-box` (rigid, models=1, points=yes)
- `011_dustbin` (rigid, models=1, points=yes)
- `012_plant-pot` (rigid, models=5, points=yes)
- `013_dumbbell-rack` (rigid, models=4, points=yes)
- `014_bookcase` (rigid, models=4, points=yes)
- `016_oven` (articulated/urdf, models=0, points=yes)
- `023_tissue-box` (rigid, models=7, points=yes)
- `036_cabinet` (articulated/urdf, models=0, points=yes)
- `037_box` (articulated/urdf, models=0, points=no)
- `040_rack` (rigid, models=1, points=yes)
- `042_wooden_box` (rigid, models=1, points=yes)
- `044_microwave` (articulated/urdf, models=0, points=yes)
- `063_tabletrashbin` (rigid, models=11, points=yes)
- `074_displaystand` (rigid, models=5, points=yes)
- `078_phonestand` (rigid, models=7, points=yes)
- `094_rest` (rigid, models=4, points=yes)
- `119_mini-chalkboard` (rigid, models=1, points=yes)

### Office / electronics / stationery
- `010_pen` (articulated/urdf, models=0, points=no)
- `015_laptop` (articulated/urdf, models=0, points=yes)
- `017_calculator` (rigid, models=6, points=yes)
- `018_microphone` (rigid, models=4, points=yes)
- `024_scanner` (rigid, models=5, points=yes)
- `043_book` (rigid, models=2, points=yes)
- `047_mouse` (rigid, models=3, points=yes)
- `048_stapler` (rigid, models=7, points=yes)
- `055_small-speaker` (rigid, models=3, points=yes)
- `056_switch` (articulated/urdf, models=0, points=yes)
- `058_markpen` (rigid, models=6, points=yes)
- `059_pencup` (rigid, models=7, points=yes)
- `061_battery` (rigid, models=6, points=yes)
- `070_paymentsign` (rigid, models=4, points=yes)
- `072_electronicscale` (rigid, models=5, points=yes)
- `077_phone` (rigid, models=5, points=yes)
- `079_remotecontrol` (rigid, models=7, points=yes)
- `081_playingcards` (rigid, models=3, points=yes)
- `092_notebook` (rigid, models=3, points=yes)
- `093_brush-pen` (rigid, models=6, points=yes)
- `095_glue` (rigid, models=6, points=yes)
- `097_screen` (rigid, models=4, points=yes)
- `098_speaker` (rigid, models=6, points=yes)
- `116_keyboard` (rigid, models=4, points=yes)
- `117_whiteboard-eraser` (rigid, models=1, points=yes)

### Tools / hardware / cleaning
- `020_hammer` (rigid, models=1, points=yes)
- `030_drill` (rigid, models=7, points=yes)
- `032_screwdriver` (rigid, models=1, points=yes)
- `052_dumbbell` (rigid, models=7, points=yes)
- `082_smallshovel` (rigid, models=4, points=yes)
- `083_brush` (rigid, models=4, points=yes)
- `084_woodenmallet` (rigid, models=5, points=yes)
- `096_cleaner` (rigid, models=4, points=yes)
- `100_seal` (rigid, models=6, points=yes)
- `102_roller` (rigid, models=3, points=yes)
- `104_board` (rigid, models=5, points=yes)

### Decor / toys / miscellaneous
- `004_fluted-block` (rigid, models=2, points=no)
- `026_pet-collar` (rigid, models=4, points=yes)
- `027_table-tennis` (rigid, models=2, points=yes)
- `028_roll-paper` (rigid, models=4, points=yes)
- `041_shoe` (rigid, models=10, points=yes)
- `045_sand-clock` (rigid, models=3, points=yes)
- `046_alarm-clock` (rigid, models=6, points=yes)
- `050_bell` (rigid, models=2, points=yes)
- `051_candlestick` (rigid, models=5, points=yes)
- `057_toycar` (rigid, models=6, points=yes)
- `073_rubikscube` (rigid, models=3, points=yes)
- `085_gong` (rigid, models=6, points=yes)
- `086_woodenblock` (rigid, models=5, points=yes)
- `089_globe` (rigid, models=2, points=yes)
- `090_trophy` (rigid, models=5, points=yes)
- `099_fan` (rigid, models=7, points=yes)
- `107_soap` (rigid, models=4, points=yes)
- `108_block` (rigid, models=7, points=yes)
- `109_hydrating-oil` (rigid, models=4, points=yes)
- `111_callbell` (rigid, models=6, points=yes)
- `114_bottle` (rigid, models=4, points=yes)
- `115_perfume` (rigid, models=4, points=yes)
- `118_tooth-paste` (rigid, models=1, points=yes)
- `120_plant` (rigid, models=1, points=yes)

### Special / collections / helper geometry
- `001_bottle` (rigid, models=23, points=yes)
- `049_shampoo` (rigid, models=7, points=yes)
- `080_pillbottle` (rigid, models=5, points=yes)
- `cube` (collection/helper, models=0, points=no)
- `objaverse` (collection/helper, models=0, points=no)
- `sapien-block1` (collection/helper, models=0, points=yes)
- `sapien-block2` (collection/helper, models=0, points=yes)
- `vis_box` (collection/helper, models=0, points=no)

## Complete Top-Level Asset Table

| Asset name | Type | Models | Visual GLBs | Collision GLBs | URDFs | points_info |
|---|---:|---:|---:|---:|---:|---:|
| `001_bottle` | rigid | 23 | 23 | 23 | 0 | yes |
| `002_bowl` | rigid | 7 | 7 | 7 | 0 | yes |
| `003_plate` | rigid | 1 | 1 | 1 | 0 | yes |
| `004_fluted-block` | rigid | 2 | 2 | 2 | 0 | no |
| `005_french-fries` | rigid | 4 | 4 | 4 | 0 | yes |
| `006_hamburg` | rigid | 6 | 6 | 6 | 0 | yes |
| `007_shoe-box` | rigid | 1 | 1 | 1 | 0 | yes |
| `008_tray` | rigid | 4 | 4 | 4 | 0 | yes |
| `009_kettle` | articulated/urdf | 0 | 3 | 0 | 3 | yes |
| `010_pen` | articulated/urdf | 0 | 0 | 0 | 7 | no |
| `011_dustbin` | rigid | 1 | 1 | 1 | 0 | yes |
| `012_plant-pot` | rigid | 5 | 5 | 5 | 0 | yes |
| `013_dumbbell-rack` | rigid | 4 | 4 | 4 | 0 | yes |
| `014_bookcase` | rigid | 4 | 4 | 4 | 0 | yes |
| `015_laptop` | articulated/urdf | 0 | 11 | 0 | 11 | yes |
| `016_oven` | articulated/urdf | 0 | 0 | 0 | 4 | yes |
| `017_calculator` | rigid | 6 | 6 | 6 | 0 | yes |
| `018_microphone` | rigid | 4 | 4 | 4 | 0 | yes |
| `019_coaster` | rigid | 1 | 1 | 1 | 0 | yes |
| `020_hammer` | rigid | 1 | 1 | 1 | 0 | yes |
| `021_cup` | rigid | 13 | 13 | 13 | 0 | yes |
| `022_cup-with-liquid` | rigid | 1 | 1 | 1 | 0 | yes |
| `023_tissue-box` | rigid | 7 | 7 | 7 | 0 | yes |
| `024_scanner` | rigid | 5 | 5 | 5 | 0 | yes |
| `025_chips-tub` | rigid | 4 | 4 | 4 | 0 | yes |
| `026_pet-collar` | rigid | 4 | 4 | 4 | 0 | yes |
| `027_table-tennis` | rigid | 2 | 2 | 2 | 0 | yes |
| `028_roll-paper` | rigid | 4 | 4 | 4 | 0 | yes |
| `029_olive-oil` | rigid | 5 | 5 | 5 | 0 | yes |
| `030_drill` | rigid | 7 | 7 | 7 | 0 | yes |
| `031_jam-jar` | rigid | 5 | 5 | 5 | 0 | yes |
| `032_screwdriver` | rigid | 1 | 1 | 1 | 0 | yes |
| `033_fork` | rigid | 1 | 1 | 1 | 0 | yes |
| `034_knife` | rigid | 1 | 1 | 1 | 0 | yes |
| `035_apple` | rigid | 2 | 2 | 2 | 0 | yes |
| `036_cabinet` | articulated/urdf | 0 | 1 | 0 | 1 | yes |
| `037_box` | articulated/urdf | 0 | 1 | 0 | 1 | no |
| `038_milk-box` | rigid | 4 | 4 | 4 | 0 | yes |
| `039_mug` | rigid | 13 | 13 | 13 | 0 | yes |
| `040_rack` | rigid | 1 | 1 | 1 | 0 | yes |
| `041_shoe` | rigid | 10 | 10 | 10 | 0 | yes |
| `042_wooden_box` | rigid | 1 | 1 | 1 | 0 | yes |
| `043_book` | rigid | 2 | 2 | 2 | 0 | yes |
| `044_microwave` | articulated/urdf | 0 | 2 | 0 | 2 | yes |
| `045_sand-clock` | rigid | 3 | 3 | 3 | 0 | yes |
| `046_alarm-clock` | rigid | 6 | 6 | 6 | 0 | yes |
| `047_mouse` | rigid | 3 | 3 | 3 | 0 | yes |
| `048_stapler` | rigid | 7 | 7 | 7 | 0 | yes |
| `049_shampoo` | rigid | 7 | 7 | 7 | 0 | yes |
| `050_bell` | rigid | 2 | 2 | 2 | 0 | yes |
| `051_candlestick` | rigid | 5 | 5 | 5 | 0 | yes |
| `052_dumbbell` | rigid | 7 | 7 | 7 | 0 | yes |
| `053_teanet` | rigid | 5 | 5 | 5 | 0 | yes |
| `054_baguette` | rigid | 2 | 2 | 2 | 0 | yes |
| `055_small-speaker` | rigid | 3 | 3 | 3 | 0 | yes |
| `056_switch` | articulated/urdf | 0 | 8 | 0 | 8 | yes |
| `057_toycar` | rigid | 6 | 6 | 6 | 0 | yes |
| `058_markpen` | rigid | 6 | 6 | 6 | 0 | yes |
| `059_pencup` | rigid | 7 | 7 | 7 | 0 | yes |
| `060_kitchenpot` | articulated/urdf | 0 | 8 | 0 | 7 | yes |
| `061_battery` | rigid | 6 | 6 | 6 | 0 | yes |
| `062_plasticbox` | rigid | 11 | 11 | 11 | 0 | yes |
| `063_tabletrashbin` | rigid | 11 | 11 | 11 | 0 | yes |
| `064_msg` | rigid | 6 | 6 | 6 | 0 | yes |
| `065_soy-sauce` | rigid | 5 | 5 | 5 | 0 | yes |
| `066_vinegar` | rigid | 3 | 3 | 3 | 0 | yes |
| `067_steamer` | rigid | 3 | 3 | 3 | 0 | yes |
| `068_boxdrink` | rigid | 4 | 4 | 4 | 0 | yes |
| `069_vagetable` | rigid | 7 | 7 | 7 | 0 | yes |
| `070_paymentsign` | rigid | 4 | 4 | 4 | 0 | yes |
| `071_can` | rigid | 6 | 6 | 6 | 0 | yes |
| `072_electronicscale` | rigid | 5 | 5 | 5 | 0 | yes |
| `073_rubikscube` | rigid | 3 | 3 | 3 | 0 | yes |
| `074_displaystand` | rigid | 5 | 5 | 5 | 0 | yes |
| `075_bread` | rigid | 7 | 7 | 7 | 0 | yes |
| `076_breadbasket` | rigid | 5 | 5 | 5 | 0 | yes |
| `077_phone` | rigid | 5 | 5 | 5 | 0 | yes |
| `078_phonestand` | rigid | 7 | 7 | 7 | 0 | yes |
| `079_remotecontrol` | rigid | 7 | 7 | 7 | 0 | yes |
| `080_pillbottle` | rigid | 5 | 5 | 5 | 0 | yes |
| `081_playingcards` | rigid | 3 | 3 | 3 | 0 | yes |
| `082_smallshovel` | rigid | 4 | 4 | 4 | 0 | yes |
| `083_brush` | rigid | 4 | 4 | 4 | 0 | yes |
| `084_woodenmallet` | rigid | 5 | 5 | 5 | 0 | yes |
| `085_gong` | rigid | 6 | 6 | 6 | 0 | yes |
| `086_woodenblock` | rigid | 5 | 5 | 5 | 0 | yes |
| `087_waterer` | rigid | 8 | 8 | 8 | 0 | yes |
| `088_wineglass` | rigid | 5 | 5 | 5 | 0 | yes |
| `089_globe` | rigid | 2 | 2 | 2 | 0 | yes |
| `090_trophy` | rigid | 5 | 5 | 5 | 0 | yes |
| `091_kettle` | rigid | 6 | 6 | 6 | 0 | yes |
| `092_notebook` | rigid | 3 | 3 | 3 | 0 | yes |
| `093_brush-pen` | rigid | 6 | 6 | 6 | 0 | yes |
| `094_rest` | rigid | 4 | 4 | 4 | 0 | yes |
| `095_glue` | rigid | 6 | 6 | 6 | 0 | yes |
| `096_cleaner` | rigid | 4 | 4 | 4 | 0 | yes |
| `097_screen` | rigid | 4 | 4 | 4 | 0 | yes |
| `098_speaker` | rigid | 6 | 6 | 6 | 0 | yes |
| `099_fan` | rigid | 7 | 7 | 7 | 0 | yes |
| `100_seal` | rigid | 6 | 6 | 6 | 0 | yes |
| `101_milk-tea` | rigid | 6 | 6 | 6 | 0 | yes |
| `102_roller` | rigid | 3 | 3 | 3 | 0 | yes |
| `103_fruit` | rigid | 7 | 7 | 7 | 0 | yes |
| `104_board` | rigid | 5 | 5 | 5 | 0 | yes |
| `105_sauce-can` | rigid | 5 | 5 | 5 | 0 | yes |
| `106_skillet` | rigid | 4 | 4 | 4 | 0 | yes |
| `107_soap` | rigid | 4 | 4 | 4 | 0 | yes |
| `108_block` | rigid | 7 | 7 | 7 | 0 | yes |
| `109_hydrating-oil` | rigid | 4 | 4 | 4 | 0 | yes |
| `110_basket` | rigid | 4 | 4 | 4 | 0 | yes |
| `111_callbell` | rigid | 6 | 6 | 6 | 0 | yes |
| `112_tea-box` | rigid | 6 | 6 | 6 | 0 | yes |
| `113_coffee-box` | rigid | 7 | 7 | 7 | 0 | yes |
| `114_bottle` | rigid | 4 | 4 | 4 | 0 | yes |
| `115_perfume` | rigid | 4 | 4 | 4 | 0 | yes |
| `116_keyboard` | rigid | 4 | 4 | 4 | 0 | yes |
| `117_whiteboard-eraser` | rigid | 1 | 1 | 1 | 0 | yes |
| `118_tooth-paste` | rigid | 1 | 1 | 1 | 0 | yes |
| `119_mini-chalkboard` | rigid | 1 | 1 | 1 | 0 | yes |
| `120_plant` | rigid | 1 | 1 | 1 | 0 | yes |
| `cube` | collection/helper | 0 | 0 | 0 | 0 | no |
| `objaverse` | collection/helper | 0 | 0 | 0 | 0 | no |
| `sapien-block1` | collection/helper | 0 | 0 | 0 | 0 | yes |
| `sapien-block2` | collection/helper | 0 | 0 | 0 | 0 | yes |
| `vis_box` | collection/helper | 0 | 0 | 0 | 0 | no |

## Objaverse Subcollection Names
- `bottle`: 006, 007, 013, 017, 019, 020, 025
- `bowl`: 001, 002, 003, 004, 005, 007, 010, 011, 012, 016, 018, 020, 021, 022, 024
- `brush`: 005, 006, 007
- `can`: 001, 005, 008, 009, 011, 013, 015, 017, 018
- `chip_can`: 003, 007, 008
- `clock`: 005, 006
- `drinkbox`: 003
- `hammer`: 001, 002, 003, 004, 005
- `marker`: 002, 004
- `notebook`: 001, 002, 003, 004, 008
- `plate`: 003, 004, 007, 008, 009
- `pot`: 002, 004, 005, 006, 007, 008, 009, 010
- `ramen_box`: 001, 002, 005, 012, 013, 015, 017, 018, 019, 022, 023, 024
- `remote`: 002, 004, 005, 006
- `slipper`: 001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 012, 015, 020, 021, 022, 023, 024, 026, 027, 028, 029, 031, 033, 035
- `snack_box`: 018, 020, 022, 025, 031, 034, 047
- `snack_package`: 003, 004
- `sneaker`: 001, 002, 003, 005, 006, 007
- `spoon`: 011, 020
- `steel_tape`: 003
- `tape`: 001, 002, 003, 004
- `thermos`: 002, 003, 005
- `tissue`: 004, 005
- `toothbrush`: 009, 010, 019, 030
- `toy_car`: 001, 002, 003, 005, 006, 007, 009, 011, 013
- `wallet`: 003, 007, 010, 011, 012, 017
