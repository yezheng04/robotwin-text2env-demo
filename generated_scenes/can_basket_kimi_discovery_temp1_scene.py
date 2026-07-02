#!/usr/bin/env python3
"""Generated RoboTwin tabletop scene: can_in_basket_final_v0.

Source placement: runs/can_basket_kimi_discovery_temp1/final_placement.json
Generated at: 2026-07-02
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


SCENE_NAME = "can_in_basket_final_v0"
SOURCE_PLACEMENT = "runs/can_basket_kimi_discovery_temp1/final_placement.json"
PLACEMENT_SPEC: dict[str, Any] = { 'schema_version': 'robotwin.tabletop_placement.v0',
  'stage': 'final_static_for_smoke',
  'placement_name': 'can_in_basket_final_v0_final_static_v0',
  'language_prompt': 'a can in the basket',
  'asset_catalog_path': 'runs/can_basket_kimi_discovery_temp1/prompt_case_catalog.json',
  'source_designer_placement': 'designer_initial_placement.json',
  'source_critic_review': 'critic_review.json',
  'orchestrator_decision': { 'decision': 'repair_then_smoke',
                             'reason': 'Static validation passed. The reported XY collision between can and basket is '
                                       "semantically intentional for the containment relation 'can in the basket'. "
                                       'Object heights and reachability constraints are satisfied. Ready for physics '
                                       'smoke test.',
                             'remaining_uncertainties': [ 'Exact simulator contact must be confirmed by RoboTwin '
                                                          'smoke.',
                                                          'Semantic visual match must be confirmed by '
                                                          'observation_agent.']},
  'workspace': { 'surface': 'table',
                 'coordinate_convention': 'robot_first_person_tabletop; x negative=robot-left, x positive=robot-right, '
                                          'y positive=front/away, z up',
                 'bounds': {'x': [-0.45, 0.45], 'y': [-0.35, 0.25], 'z': [0.74, 1.1]},
                 'spatial_regions': { 'left_reachable_area': {'x': [-0.24, -0.06], 'y': [-0.16, 0.08]},
                                      'right_reachable_area': {'x': [0.08, 0.3], 'y': [-0.16, 0.08]},
                                      'center_clearance_area': {'x': [-0.05, 0.07], 'y': [-0.2, 0.12]}}},
  'objects': [ { 'id': 'basket_1',
                 'semantic': 'basket',
                 'asset_id': '110_basket',
                 'model_id': 0,
                 'role': 'scene_object',
                 'pose': { 'region': 'right_reachable_area',
                           'xyz': [0.15, 0.0, 0.76],
                           'qpos': [1, 0, 0, 0],
                           'z_policy': 'snap_to_tabletop_on_load'},
                 'physical': {'is_static': False, 'collision': True, 'stable_on_table': True},
                 'affordance_notes': ['container_for_can'],
                 'asset_metadata': { 'approx_scaled_extents_m': [ 0.2298853760508108,
                                                                  0.17514074821341716,
                                                                  0.14392557376933823],
                                     'scale': [0.12, 0.12, 0.12],
                                     'asset_type': 'rigid',
                                     'graspable': True,
                                     'support_surface_candidate': False,
                                     'placement_defaults': { 'loader': 'create_actor',
                                                             'qpos': [1, 0, 0, 0],
                                                             'z_policy': 'snap_to_tabletop_on_load'}}},
               { 'id': 'can_1',
                 'semantic': 'can',
                 'asset_id': '071_can',
                 'model_id': 0,
                 'role': 'scene_object',
                 'pose': { 'region': 'right_reachable_area',
                           'xyz': [0.15, 0.0, 0.82],
                           'qpos': [1, 0, 0, 0],
                           'z_policy': 'absolute'},
                 'physical': {'is_static': False, 'collision': True, 'stable_on_table': True},
                 'affordance_notes': ['graspable', 'contained_in_basket'],
                 'asset_metadata': { 'approx_scaled_extents_m': [ 0.07114912222011581,
                                                                  0.09646788818255601,
                                                                  0.07118775383879648],
                                     'scale': [0.05, 0.05, 0.05],
                                     'asset_type': 'rigid',
                                     'graspable': True,
                                     'support_surface_candidate': False,
                                     'placement_defaults': { 'loader': 'create_actor',
                                                             'qpos': [1, 0, 0, 0],
                                                             'z_policy': 'snap_to_tabletop_on_load'}}}],
  'relations': [ { 'type': 'contained_in',
                   'source': 'can_1',
                   'target': 'basket_1',
                   'description': 'can is placed inside the basket'}],
  'constraints': [ 'use_only_catalog_assets',
                   'objects_on_table',
                   'no_initial_collision',
                   'keep_robot_reachable',
                   'keep_camera_visible',
                   'do_not_generate_task_program',
                   'containment_allows_close_placement'],
  'downstream_task_hints': ['pick_object_from_container', 'place_object_into_container'],
  'validation_notes': [ 'Approximate XY collision between can and basket is intentional for containment semantics.',
                        'Static validation passed with acknowledged warning on geometric overlap.'],
  '_moonshot_raw_response': '{\n'
                            '  "schema_version": "robotwin.tabletop_placement.v0",\n'
                            '  "stage": "final_static_for_smoke",\n'
                            '  "placement_name": "can_in_basket_final_v0",\n'
                            '  "language_prompt": "a can in the basket",\n'
                            '  "asset_catalog_path": "runs/can_basket_kimi_discovery_temp1/prompt_case_catalog.json",\n'
                            '  "source_designer_placement": "can_in_basket_designer_initial_v0",\n'
                            '  "source_critic_review": "critic_review_can_in_basket",\n'
                            '  "orchestrator_decision": {\n'
                            '    "decision": "accept_for_smoke",\n'
                            '    "reason": "The approximate XY collision flagged between can_1 and basket_1 '
                            "(clearance=-0.163m) is semantically intentional for the 'contained_in' relation required "
                            "by the user prompt. The 'containment_allows_close_placement' constraint explicitly "
                            'permits this geometric overlap. All other static validations pass: assets exist, poses '
                            'are within workspace bounds and reachable regions, and stability flags are correctly set. '
                            'The critic review acknowledged this collision as expected behavior with no repair '
                            'suggestions provided.",\n'
                            '    "remaining_uncertainties": [\n'
                            '      "Exact simulator contact must be confirmed by RoboTwin smoke.",\n'
                            '      "Semantic visual match must be confirmed by observation_agent."\n'
                            '    ]\n'
                            '  },\n'
                            '  "workspace": {\n'
                            '    "surface": "table",\n'
                            '    "coordinate_convention": "robot_first_person_tabletop; x negative=robot-left, x '
                            'positive=robot-right, y positive=front/away, z up",\n'
                            '    "bounds": {\n'
                            '      "x": [\n'
                            '        -0.45,\n'
                            '        0.45\n'
                            '      ],\n'
                            '      "y": [\n'
                            '        -0.35,\n'
                            '        0.25\n'
                            '      ],\n'
                            '      "z": [\n'
                            '        0.74,\n'
                            '        1.1\n'
                            '      ]\n'
                            '    },\n'
                            '    "spatial_regions": {\n'
                            '      "left_reachable_area": {\n'
                            '        "x": [\n'
                            '          -0.24,\n'
                            '          -0.06\n'
                            '        ],\n'
                            '        "y": [\n'
                            '          -0.16,\n'
                            '          0.08\n'
                            '        ]\n'
                            '      },\n'
                            '      "right_reachable_area": {\n'
                            '        "x": [\n'
                            '          0.08,\n'
                            '          0.3\n'
                            '        ],\n'
                            '        "y": [\n'
                            '          -0.16,\n'
                            '          0.08\n'
                            '        ]\n'
                            '      },\n'
                            '      "center_clearance_area": {\n'
                            '        "x": [\n'
                            '          -0.05,\n'
                            '          0.07\n'
                            '        ],\n'
                            '        "y": [\n'
                            '          -0.2,\n'
                            '          0.12\n'
                            '        ]\n'
                            '      }\n'
                            '    }\n'
                            '  },\n'
                            '  "objects": [\n'
                            '    {\n'
                            '      "id": "basket_1",\n'
                            '      "semantic": "basket",\n'
                            '      "asset_id": "110_basket",\n'
                            '      "model_id": 0,\n'
                            '      "role": "scene_object",\n'
                            '      "pose": {\n'
                            '        "region": "right_reachable_area",\n'
                            '        "xyz": [\n'
                            '          0.15,\n'
                            '          0.0,\n'
                            '          0.76\n'
                            '        ],\n'
                            '        "qpos": [\n'
                            '          1,\n'
                            '          0,\n'
                            '          0,\n'
                            '          0\n'
                            '        ],\n'
                            '        "z_policy": "snap_to_tabletop_on_load"\n'
                            '      },\n'
                            '      "physical": {\n'
                            '        "is_static": false,\n'
                            '        "collision": true,\n'
                            '        "stable_on_table": true\n'
                            '      },\n'
                            '      "affordance_notes": [\n'
                            '        "container_for_can"\n'
                            '      ],\n'
                            '      "asset_metadata": {\n'
                            '        "approx_scaled_extents_m": [\n'
                            '          0.2298853760508108,\n'
                            '          0.17514074821341716,\n'
                            '          0.14392557376933823\n'
                            '        ],\n'
                            '        "scale": [\n'
                            '          0.12,\n'
                            '          0.12,\n'
                            '          0.12\n'
                            '        ],\n'
                            '        "asset_type": "rigid",\n'
                            '        "graspable": true,\n'
                            '        "support_surface_candidate": false,\n'
                            '        "placement_defaults": {\n'
                            '          "loader": "create_actor",\n'
                            '          "qpos": [\n'
                            '            1,\n'
                            '            0,\n'
                            '            0,\n'
                            '            0\n'
                            '          ],\n'
                            '          "z_policy": "snap_to_tabletop_on_load"\n'
                            '        }\n'
                            '      }\n'
                            '    },\n'
                            '    {\n'
                            '      "id": "can_1",\n'
                            '      "semantic": "can",\n'
                            '      "asset_id": "071_can",\n'
                            '      "model_id": 0,\n'
                            '      "role": "scene_object",\n'
                            '      "pose": {\n'
                            '        "region": "right_reachable_area",\n'
                            '        "xyz": [\n'
                            '          0.15,\n'
                            '          0.0,\n'
                            '          0.82\n'
                            '        ],\n'
                            '        "qpos": [\n'
                            '          1,\n'
                            '          0,\n'
                            '          0,\n'
                            '          0\n'
                            '        ],\n'
                            '        "z_policy": "absolute"\n'
                            '      },\n'
                            '      "physical": {\n'
                            '        "is_static": false,\n'
                            '        "collision": true,\n'
                            '        "stable_on_table": true\n'
                            '      },\n'
                            '      "affordance_notes": [\n'
                            '        "graspable",\n'
                            '        "contained_in_basket"\n'
                            '      ],\n'
                            '      "asset_metadata": {\n'
                            '        "approx_scaled_extents_m": [\n'
                            '          0.07114912222011581,\n'
                            '          0.09646788818255601,\n'
                            '          0.07118775383879648\n'
                            '        ],\n'
                            '        "scale": [\n'
                            '          0.05,\n'
                            '          0.05,\n'
                            '          0.05\n'
                            '        ],\n'
                            '        "asset_type": "rigid",\n'
                            '        "graspable": true,\n'
                            '        "support_surface_candidate": false,\n'
                            '        "placement_defaults": {\n'
                            '          "loader": "create_actor",\n'
                            '          "qpos": [\n'
                            '            1,\n'
                            '            0,\n'
                            '            0,\n'
                            '            0\n'
                            '          ],\n'
                            '          "z_policy": "snap_to_tabletop_on_load"\n'
                            '        }\n'
                            '      }\n'
                            '    }\n'
                            '  ],\n'
                            '  "relations": [\n'
                            '    {\n'
                            '      "type": "contained_in",\n'
                            '      "source": "can_1",\n'
                            '      "target": "basket_1",\n'
                            '      "description": "can is placed inside the basket"\n'
                            '    }\n'
                            '  ],\n'
                            '  "constraints": [\n'
                            '    "use_only_catalog_assets",\n'
                            '    "objects_on_table",\n'
                            '    "no_initial_collision",\n'
                            '    "keep_robot_reachable",\n'
                            '    "keep_camera_visible",\n'
                            '    "do_not_generate_task_program",\n'
                            '    "containment_allows_close_placement"\n'
                            '  ],\n'
                            '  "downstream_task_hints": [\n'
                            '    "pick_object_from_container",\n'
                            '    "place_object_into_container"\n'
                            '  ],\n'
                            '  "validation_notes": [\n'
                            '    "Approximate XY collision between can and basket is intentional for containment '
                            'semantics.",\n'
                            '    "Static validation passed with acknowledged warning on geometric overlap."\n'
                            '  ]\n'
                            '}',
  'generated_by': { 'agent': 'orchestrator',
                    'model_backend': 'moonshot',
                    'prompt_template': 'generate_scene/gpt_agent.py',
                    'generated_at': '2026-07-02'}}


def load_scene(task: Any, placement_spec: dict[str, Any] | None = None) -> dict[str, Any]:
    """Load this generated tabletop scene into a RoboTwin task instance."""

    import sapien.core as sapien
    from envs.utils import create_actor, create_sapien_urdf_obj

    spec = deepcopy(placement_spec or PLACEMENT_SPEC)
    loaded: dict[str, Any] = {}
    table_z = 0.741 + getattr(task, "table_z_bias", 0)

    for obj in spec["objects"]:
        pose_data = obj["pose"]
        xyz = list(pose_data["xyz"])
        if pose_data.get("z_policy") == "snap_to_tabletop_on_load":
            xyz[2] = table_z

        qpos = list(pose_data.get("qpos", [1, 0, 0, 0]))
        if obj["asset_id"] == "003_plate" and qpos == [1, 0, 0, 0]:
            qpos = [0.5, 0.5, 0.5, 0.5]

        metadata = obj.get("asset_metadata", {})
        defaults = metadata.get("placement_defaults", {})
        loader = defaults.get("loader")
        asset_type = metadata.get("asset_type", "rigid")
        if loader == "sapien_urdf" or asset_type == "articulated":
            actor = create_sapien_urdf_obj(
                task,
                pose=sapien.Pose(xyz, qpos),
                modelname=obj["asset_id"],
                modelid=obj.get("model_id", 0),
                fix_root_link=defaults.get("fix_root_link", obj.get("physical", {}).get("is_static", False)),
            )
            if "articulation_qpos" in defaults:
                actor.set_qpos(defaults["articulation_qpos"])
        else:
            actor = create_actor(
                task,
                pose=sapien.Pose(xyz, qpos),
                modelname=obj["asset_id"],
                scale=metadata.get("scale", (1, 1, 1)) or (1, 1, 1),
                model_id=obj.get("model_id", 0),
                convex=True,
                is_static=obj.get("physical", {}).get("is_static", False),
            )
        if actor is None:
            raise RuntimeError(f"Failed to load asset {obj['asset_id']}")
        actor.set_name(obj["id"])
        loaded[obj["id"]] = actor

    task.generated_scene_objects = loaded
    return loaded
