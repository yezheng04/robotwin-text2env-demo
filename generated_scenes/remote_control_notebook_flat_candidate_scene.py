#!/usr/bin/env python3
"""Generated RoboTwin tabletop scene: remote_control_notebook_flat_candidate_v0.

Source placement: runs/remote_control_notebook_kimi_flat_candidate/final_placement_flat_candidate.json
Generated at: 2026-07-02
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


SCENE_NAME = "remote_control_notebook_flat_candidate_v0"
SOURCE_PLACEMENT = "runs/remote_control_notebook_kimi_flat_candidate/final_placement_flat_candidate.json"
PLACEMENT_SPEC: dict[str, Any] = { 'schema_version': 'robotwin.tabletop_placement.v0',
  'placement_name': 'remote_control_notebook_flat_candidate_v0',
  'stage': 'manual_flat_orientation_candidate_for_review',
  'language_prompt': 'a remote control next to the notebook',
  'asset_catalog_path': 'runs/remote_control_notebook_kimi/prompt_case_catalog.json',
  'generated_by': { 'agent': 'orchestrator',
                    'model_backend': 'moonshot',
                    'prompt_template': 'generate_scene/gpt_agent.py',
                    'generated_at': '2026-07-02'},
  'workspace': { 'surface': 'table',
                 'coordinate_convention': 'robot_first_person_tabletop',
                 'bounds': {'x': [-0.45, 0.45], 'y': [-0.35, 0.25], 'z': [0.74, 1.1]},
                 'spatial_regions': { 'left_reachable_area': {'x': [-0.24, -0.06], 'y': [-0.16, 0.08]},
                                      'right_reachable_area': {'x': [0.08, 0.3], 'y': [-0.16, 0.08]},
                                      'center_clearance_area': {'x': [-0.05, 0.07], 'y': [-0.2, 0.12]}}},
  'objects': [ { 'id': 'notebook_1',
                 'semantic': 'notebook',
                 'asset_id': '092_notebook',
                 'model_id': 0,
                 'role': 'scene_object',
                 'pose': { 'region': 'left_reachable_area',
                           'xyz': [-0.15, 0.0, 0.76],
                           'qpos': [0.707, 0.707, 0, 0],
                           'z_policy': 'snap_to_tabletop_on_load'},
                 'physical': {'is_static': False, 'collision': True, 'stable_on_table': True},
                 'affordance_notes': ['graspable', 'flat_placement', 'manual_flat_qpos_candidate'],
                 'asset_metadata': { 'approx_scaled_extents_m': [ 0.19111362029537682,
                                                                  0.02024345549322655,
                                                                  0.1253791679502285],
                                     'scale': [0.1, 0.1, 0.1],
                                     'asset_type': 'rigid',
                                     'graspable': True,
                                     'support_surface_candidate': False,
                                     'placement_defaults': { 'loader': 'create_actor',
                                                             'qpos': [1, 0, 0, 0],
                                                             'z_policy': 'snap_to_tabletop_on_load'}},
                 'designer_notes': []},
               { 'id': 'remotecontrol_1',
                 'semantic': 'remotecontrol',
                 'asset_id': '079_remotecontrol',
                 'model_id': 0,
                 'role': 'scene_object',
                 'pose': { 'region': 'right_reachable_area',
                           'xyz': [0.15, 0.0, 0.76],
                           'qpos': [0.707, 0.707, 0, 0],
                           'z_policy': 'snap_to_tabletop_on_load'},
                 'physical': {'is_static': False, 'collision': True, 'stable_on_table': True},
                 'affordance_notes': ['graspable', 'flat_placement', 'manual_flat_qpos_candidate'],
                 'asset_metadata': { 'approx_scaled_extents_m': [ 0.1935049500633662,
                                                                  0.020872455593916962,
                                                                  0.0480324208980887],
                                     'scale': [0.1, 0.1, 0.1],
                                     'asset_type': 'rigid',
                                     'graspable': True,
                                     'support_surface_candidate': False,
                                     'placement_defaults': { 'loader': 'create_actor',
                                                             'qpos': [1, 0, 0, 0],
                                                             'z_policy': 'snap_to_tabletop_on_load'}},
                 'designer_notes': []}],
  'relations': [ { 'relation_type': 'spatial',
                   'description': 'next_to',
                   'subject_id': 'remotecontrol_1',
                   'reference_id': 'notebook_1',
                   'details': 'remote control placed to the right of notebook with approximately 0.30m '
                              'center-to-center distance'}],
  'constraints': [ 'use_only_catalog_assets',
                   'objects_on_table',
                   'no_initial_collision',
                   'keep_robot_reachable',
                   'keep_camera_visible',
                   'do_not_generate_task_program'],
  'downstream_task_hints': ['spatial_relationship', 'pick_and_place', 'relative_positioning'],
  'validation': {},
  'designer_notes': [ 'Placed notebook in left reachable area and remote control in right reachable area to satisfy '
                      "'next to' relationship while maintaining minimum 0.28m separation between object centers.",
                      'Both objects use default model_id 0 and snap_to_tabletop_on_load z_policy for stable placement.',
                      "Objects aligned along x-axis with clear left-right spatial relationship from robot's "
                      'perspective.'],
  '_moonshot_raw_response': '{\n'
                            '  "schema_version": "robotwin.tabletop_placement.v0",\n'
                            '  "placement_name": "remote_next_to_notebook_designer_initial_v0",\n'
                            '  "stage": "designer_initial",\n'
                            '  "language_prompt": "a remote control next to the notebook",\n'
                            '  "asset_catalog_path": "runs/remote_control_notebook_kimi/prompt_case_catalog.json",\n'
                            '  "generated_by": {\n'
                            '    "agent": "designer",\n'
                            '    "model_backend": "moonshot",\n'
                            '    "prompt_template": "generate_scene/prompts/designer_agent.md",\n'
                            '    "generated_at": "2024-01-15"\n'
                            '  },\n'
                            '  "workspace": {\n'
                            '    "surface": "table",\n'
                            '    "coordinate_convention": "robot_first_person_tabletop",\n'
                            '    "bounds": {\n'
                            '      "x": [-0.45, 0.45],\n'
                            '      "y": [-0.35, 0.25],\n'
                            '      "z": [0.74, 1.1]\n'
                            '    },\n'
                            '    "spatial_regions": {\n'
                            '      "left_reachable_area": {\n'
                            '        "x": [-0.24, -0.06],\n'
                            '        "y": [-0.16, 0.08]\n'
                            '      },\n'
                            '      "right_reachable_area": {\n'
                            '        "x": [0.08, 0.3],\n'
                            '        "y": [-0.16, 0.08]\n'
                            '      },\n'
                            '      "center_clearance_area": {\n'
                            '        "x": [-0.05, 0.07],\n'
                            '        "y": [-0.2, 0.12]\n'
                            '      }\n'
                            '    }\n'
                            '  },\n'
                            '  "objects": [\n'
                            '    {\n'
                            '      "id": "notebook_1",\n'
                            '      "semantic": "notebook",\n'
                            '      "asset_id": "092_notebook",\n'
                            '      "model_id": 0,\n'
                            '      "role": "scene_object",\n'
                            '      "pose": {\n'
                            '        "region": "left_reachable_area",\n'
                            '        "xyz": [-0.15, 0.0, 0.76],\n'
                            '        "qpos": [1, 0, 0, 0],\n'
                            '        "z_policy": "snap_to_tabletop_on_load"\n'
                            '      },\n'
                            '      "physical": {\n'
                            '        "is_static": false,\n'
                            '        "collision": true,\n'
                            '        "stable_on_table": true\n'
                            '      },\n'
                            '      "affordance_notes": ["graspable", "flat_placement"]\n'
                            '    },\n'
                            '    {\n'
                            '      "id": "remotecontrol_1",\n'
                            '      "semantic": "remotecontrol",\n'
                            '      "asset_id": "079_remotecontrol",\n'
                            '      "model_id": 0,\n'
                            '      "role": "scene_object",\n'
                            '      "pose": {\n'
                            '        "region": "right_reachable_area",\n'
                            '        "xyz": [0.15, 0.0, 0.76],\n'
                            '        "qpos": [1, 0, 0, 0],\n'
                            '        "z_policy": "snap_to_tabletop_on_load"\n'
                            '      },\n'
                            '      "physical": {\n'
                            '        "is_static": false,\n'
                            '        "collision": true,\n'
                            '        "stable_on_table": true\n'
                            '      },\n'
                            '      "affordance_notes": ["graspable", "flat_placement"]\n'
                            '    }\n'
                            '  ],\n'
                            '  "relations": [\n'
                            '    {\n'
                            '      "relation_type": "spatial",\n'
                            '      "description": "next_to",\n'
                            '      "subject_id": "remotecontrol_1",\n'
                            '      "reference_id": "notebook_1",\n'
                            '      "details": "remote control placed to the right of notebook with approximately 0.30m '
                            'center-to-center distance"\n'
                            '    }\n'
                            '  ],\n'
                            '  "constraints": [\n'
                            '    "use_only_catalog_assets",\n'
                            '    "objects_on_table",\n'
                            '    "no_initial_collision",\n'
                            '    "keep_robot_reachable",\n'
                            '    "keep_camera_visible",\n'
                            '    "do_not_generate_task_program"\n'
                            '  ],\n'
                            '  "downstream_task_hints": [\n'
                            '    "spatial_relationship",\n'
                            '    "pick_and_place",\n'
                            '    "relative_positioning"\n'
                            '  ],\n'
                            '  "validation": {},\n'
                            '  "designer_notes": [\n'
                            '    "Placed notebook in left reachable area and remote control in right reachable area to '
                            "satisfy 'next to' relationship while maintaining minimum 0.28m separation between object "
                            'centers.",\n'
                            '    "Both objects use default model_id 0 and snap_to_tabletop_on_load z_policy for stable '
                            'placement.",\n'
                            '    "Objects aligned along x-axis with clear left-right spatial relationship from '
                            'robot\'s perspective."\n'
                            '  ]\n'
                            '}',
  'source_designer_placement': 'designer_initial_placement.json',
  'source_critic_review': 'critic_review.json',
  'orchestrator_decision': { 'decision': 'accept_for_smoke',
                             'reason': "Static validation passed. Placement satisfies 'next_to' spatial relationship "
                                       'with adequate separation (0.30m center-to-center, ~0.11m clearance). Both '
                                       'objects positioned in reachable areas with valid asset configurations and '
                                       'stable tabletop placement policies.',
                             'remaining_uncertainties': [ 'Exact simulator contact must be confirmed by RoboTwin '
                                                          'smoke.',
                                                          'Semantic visual match must be confirmed by '
                                                          'observation_agent.']}}


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
