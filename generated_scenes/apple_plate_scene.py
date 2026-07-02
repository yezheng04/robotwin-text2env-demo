#!/usr/bin/env python3
"""Generated RoboTwin tabletop scene: apple_plate_table.

Source placement: runs/apple_plate_scene_smoke/final_placement.json
Generated at: 2026-07-02
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


SCENE_NAME = "apple_plate_table"
SOURCE_PLACEMENT = "runs/apple_plate_scene_smoke/final_placement.json"
PLACEMENT_SPEC: dict[str, Any] = { 'schema_version': 'robotwin.tabletop_placement.v0',
  'placement_name': 'apple_plate_table_final_static_v0',
  'stage': 'final_static_for_smoke',
  'language_prompt': 'an apple and a plate on the table',
  'asset_catalog_path': 'asset_catalogs/prompt_cases/apple_plate.json',
  'generated_by': { 'agent': 'orchestrator',
                    'model_backend': 'codex_reference',
                    'prompt_template': 'skills/orchestrate-placement-pipeline/SKILL.md',
                    'generated_at': '2026-07-02'},
  'workspace': { 'surface': 'table',
                 'coordinate_convention': 'robot_first_person_tabletop; x is robot-left/right across the table, y is '
                                          'robot-front/back on the table, z is height; the RoboTwin adapter maps this '
                                          'frame into the simulator task frame',
                 'bounds': {'x': [-0.45, 0.45], 'y': [-0.35, 0.25], 'z': [0.74, 1.1]},
                 'spatial_regions': { 'left_reachable_area': { 'x': [-0.24, -0.06],
                                                               'y': [-0.16, 0.08],
                                                               'purpose': 'reachable free tabletop area for the first '
                                                                          'mentioned object'},
                                      'right_reachable_area': { 'x': [0.08, 0.3],
                                                                'y': [-0.16, 0.08],
                                                                'purpose': 'reachable tabletop area for the second '
                                                                           'mentioned object'},
                                      'center_clearance_area': { 'x': [-0.05, 0.07],
                                                                 'y': [-0.2, 0.12],
                                                                 'purpose': 'free corridor for downstream '
                                                                            'manipulation'}}},
  'objects': [ { 'id': 'apple_1',
                 'semantic': 'apple',
                 'asset_id': '035_apple',
                 'model_id': 0,
                 'role': 'manipuland_candidate',
                 'pose': { 'region': 'left_reachable_area',
                           'xyz': [-0.15, -0.04, 0.76],
                           'qpos': [1, 0, 0, 0],
                           'z_policy': 'snap_to_tabletop_on_load'},
                 'physical': {'is_static': False, 'collision': True, 'stable_on_table': True},
                 'asset_metadata': { 'approx_scaled_extents_m': [ 0.06611724393084956,
                                                                  0.06433970880288944,
                                                                  0.05572773730724063],
                                     'scale': [0.7, 0.7, 0.7],
                                     'asset_type': 'rigid',
                                     'graspable': True,
                                     'support_surface_candidate': False,
                                     'placement_defaults': {}},
                 'affordance_notes': []},
               { 'id': 'plate_1',
                 'semantic': 'plate',
                 'asset_id': '003_plate',
                 'model_id': 0,
                 'role': 'support_or_target_candidate',
                 'pose': { 'region': 'right_reachable_area',
                           'xyz': [0.18, -0.04, 0.755],
                           'qpos': [0.5, 0.5, 0.5, 0.5],
                           'z_policy': 'snap_to_tabletop_on_load'},
                 'physical': {'is_static': True, 'collision': True, 'stable_on_table': True},
                 'asset_metadata': { 'approx_scaled_extents_m': [ 0.22973311309440356,
                                                                  0.02797171981547376,
                                                                  0.23002034072493324],
                                     'scale': [0.025, 0.025, 0.025],
                                     'asset_type': 'rigid',
                                     'graspable': False,
                                     'support_surface_candidate': True,
                                     'placement_defaults': {}},
                 'affordance_notes': []}],
  'relations': [ {'type': 'on_surface', 'subject': 'apple_1', 'object': 'table', 'status': 'designed'},
                 {'type': 'on_surface', 'subject': 'plate_1', 'object': 'table', 'status': 'designed'},
                 { 'type': 'separated_initially',
                   'subject': 'apple_1',
                   'object': 'plate_1',
                   'minimum_center_distance_m': 0.28,
                   'status': 'designed'}],
  'constraints': [ 'use_only_catalog_assets',
                   'objects_on_table',
                   'no_initial_collision',
                   'keep_robot_reachable',
                   'keep_camera_visible',
                   'do_not_generate_task_program'],
  'downstream_task_hints': ['the placed scene can be consumed by a downstream manipulation task'],
  'validation': { 'semantic_check': 'pass_static',
                  'asset_check': 'pass_static',
                  'bounds_check': 'pass_static',
                  'approx_collision_check': 'pass_static',
                  'stability_metadata_check': 'pass_static',
                  'robotwin_load_check': 'pending_simulator_smoke',
                  'render_visibility': 'pending_render_review',
                  'simulator_stability': 'pending_simulator_smoke'},
  'designer_notes': [ 'codex_reference is a deterministic reference provider, not a live LLM call.',
                      'Future providers should keep the same output schema and validation gate.',
                      'For lateral language relations, left/right/front/back are interpreted from the robot or '
                      'dual-arm first-person viewpoint unless the prompt explicitly names another frame.'],
  'source_designer_placement': 'designer_initial_placement.json',
  'source_critic_review': 'critic_review.json',
  'orchestrator_decision': { 'decision': 'accept_for_smoke',
                             'reason': 'Critic accepted the static placement.',
                             'remaining_uncertainties': [ 'Exact simulator contact must be confirmed by RoboTwin '
                                                          'smoke.',
                                                          'Camera visibility must be confirmed by render evidence.']}}


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
