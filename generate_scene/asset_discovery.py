#!/usr/bin/env python3
"""Discover RoboTwin object assets and build lightweight tabletop catalogs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from generate_scene.schemas import write_json


SKIP_ASSET_DIRS = {"objaverse", "vis_box"}


def _semantic_from_asset_id(asset_id: str) -> str:
    name = re.sub(r"^\d+_", "", asset_id)
    name = name.replace("-", " ").replace("_", " ")
    return re.sub(r"\s+", " ", name).strip()


def _aliases_for(asset_id: str, semantic_name: str) -> list[str]:
    aliases = [semantic_name]
    compact = semantic_name.replace(" ", "")
    dashed = semantic_name.replace(" ", "-")
    underscored = semantic_name.replace(" ", "_")
    for item in [compact, dashed, underscored, asset_id]:
        if item and item not in aliases:
            aliases.append(item)
    # Small lexical normalizations that help natural prompts match RoboTwin names.
    if semantic_name == "phone":
        aliases.extend(["mobile phone", "cell phone", "smartphone"])
    if semantic_name == "phonestand":
        aliases.extend(["phone stand", "mobile phone stand"])
    if semantic_name == "remotecontrol":
        aliases.append("remote control")
    if semantic_name == "pillbottle":
        aliases.append("pill bottle")
    if semantic_name == "plasticbox":
        aliases.append("plastic box")
    if semantic_name == "shoe box":
        aliases.append("shoebox")
    result = []
    for alias in aliases:
        alias = alias.strip()
        if alias and alias not in result:
            result.append(alias)
    return result


def _model_ids(asset_dir: Path) -> list[int]:
    ids: set[int] = set()
    for path in asset_dir.glob("model_data*.json"):
        suffix = path.stem.replace("model_data", "")
        if suffix == "":
            ids.add(0)
        elif suffix.isdigit():
            ids.add(int(suffix))
    for path in (asset_dir / "visual").glob("base*.glb") if (asset_dir / "visual").exists() else []:
        suffix = path.stem.replace("base", "")
        if suffix.isdigit():
            ids.add(int(suffix))
    return sorted(ids) or [0]


def _read_model_metadata(asset_dir: Path, model_id: int) -> dict[str, Any]:
    path = asset_dir / f"model_data{model_id}.json"
    if not path.exists() and model_id == 0:
        path = asset_dir / "model_data.json"
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def _raw_extents(metadata: dict[str, Any]) -> Any:
    return (
        metadata.get("extents")
        or metadata.get("extent")
        or metadata.get("bbox")
        or metadata.get("bounding_box")
    )


def _scaled_extents(metadata: dict[str, Any]) -> list[float] | None:
    extents = _raw_extents(metadata)
    if not (isinstance(extents, list) and len(extents) == 3 and all(isinstance(item, (int, float)) for item in extents)):
        return None

    scale = metadata.get("scale")
    if isinstance(scale, (int, float)):
        return [float(item) * float(scale) for item in extents]
    if isinstance(scale, list) and len(scale) == 3 and all(isinstance(item, (int, float)) for item in scale):
        return [float(extents[idx]) * float(scale[idx]) for idx in range(3)]

    # Many RoboTwin model_data files store normalized mesh extents around 1-2
    # without an explicit scale. Treat those as unknown for static collision
    # radius instead of causing false collision failures.
    if max(float(item) for item in extents) > 0.5:
        return None
    return [float(item) for item in extents]


def _entry_for_asset(asset_dir: Path) -> dict[str, Any]:
    asset_id = asset_dir.name
    semantic_name = _semantic_from_asset_id(asset_id)
    model_ids = _model_ids(asset_dir)
    model_metadata = []
    for model_id in model_ids:
        metadata = _read_model_metadata(asset_dir, model_id)
        model_metadata.append(
            {
                "model_id": model_id,
                "source_model_data": f"model_data{model_id}.json",
                "scale": metadata.get("scale"),
                "approx_scaled_extents_m": _scaled_extents(metadata),
            }
        )
    return {
        "asset_id": asset_id,
        "semantic_name": semantic_name,
        "aliases": _aliases_for(asset_id, semantic_name),
        "tags": [semantic_name, *semantic_name.split()],
        "asset_type": "rigid",
        "available_model_ids": model_ids,
        "default_model_id": model_ids[0],
        "model_metadata": model_metadata,
        "placement_defaults": {
            "loader": "create_actor",
            "qpos": [1, 0, 0, 0],
            "z_policy": "snap_to_tabletop_on_load",
        },
        "placement_affordances": {
            "graspable": True,
            "stable_on_table": True,
            "support_surface_candidate": False,
            "role_candidates": ["scene_object"],
        },
        "discovery": {
            "source": "robotwin.assets.objects",
            "asset_dir": str(asset_dir),
            "has_collision_dir": (asset_dir / "collision").exists(),
            "has_visual_dir": (asset_dir / "visual").exists(),
        },
    }


def discover_robotwin_assets(robotwin_root: Path) -> dict[str, Any]:
    objects_dir = robotwin_root.expanduser() / "assets" / "objects"
    if not objects_dir.exists():
        raise FileNotFoundError(f"RoboTwin objects directory not found: {objects_dir}")

    entries = []
    for asset_dir in sorted(path for path in objects_dir.iterdir() if path.is_dir()):
        if asset_dir.name in SKIP_ASSET_DIRS:
            continue
        entries.append(_entry_for_asset(asset_dir))

    return {
        "catalog_version": "robotwin.tabletop_asset_catalog_discovered.v0",
        "catalog_name": "robotwin_discovered_tabletop_assets",
        "updated_at": date.today().isoformat(),
        "robotwin_root": str(robotwin_root.expanduser()),
        "objects_dir": str(objects_dir),
        "entries": entries,
    }


def select_prompt_assets(prompt: str, catalog: dict[str, Any]) -> dict[str, Any]:
    prompt_lower = prompt.lower()
    selected = []
    for entry in catalog.get("entries", []):
        terms = [entry.get("semantic_name", ""), *entry.get("aliases", []), *entry.get("tags", [])]
        for term in terms:
            term = str(term).lower().strip()
            if not term:
                continue
            pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
            if re.search(pattern, prompt_lower):
                selected.append(entry["asset_id"])
                break
    return {
        "catalog_version": "robotwin.tabletop_asset_catalog_case.v0",
        "catalog_name": "auto_discovered_prompt_case",
        "updated_at": date.today().isoformat(),
        "purpose": f"Auto-selected assets for prompt: {prompt}",
        "base_catalog": None,
        "mvp_prompt": prompt,
        "selected_asset_ids": selected,
        "entry_overrides": {},
        "direction_frame": "robot_or_dual_arm_first_person",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a lightweight asset catalog from RoboTwin assets/objects.")
    parser.add_argument("--robotwin-root", default=str(Path.home() / "RoboTwin"))
    parser.add_argument("--out", required=True)
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-case-out")
    args = parser.parse_args()

    catalog = discover_robotwin_assets(Path(args.robotwin_root))
    write_json(Path(args.out), catalog)
    if args.prompt and args.prompt_case_out:
        prompt_case = select_prompt_assets(args.prompt, catalog)
        prompt_case["base_catalog"] = str(Path(args.out))
        write_json(Path(args.prompt_case_out), prompt_case)
    print(f"PASS discovered_assets={len(catalog.get('entries', []))} {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
