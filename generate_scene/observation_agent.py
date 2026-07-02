#!/usr/bin/env python3
"""Moonshot/Kimi vision observation agent for RoboTwin scene previews."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from generate_scene.moonshot_client import image_to_data_url, json_chat, model_from_env
from generate_scene.schemas import read_json, write_json

PROMPT_DIR = Path(__file__).resolve().parent / "prompts"


def _load_prompt(name: str) -> str:
    return (PROMPT_DIR / name).read_text(encoding="utf-8")


def _image_blocks(smoke_dir: Path) -> tuple[list[dict[str, Any]], list[str]]:
    content: list[dict[str, Any]] = []
    missing: list[str] = []
    for name in ["observer_camera.png", "head_camera.png"]:
        path = smoke_dir / name
        if not path.exists():
            missing.append(name)
            continue
        content.append({"type": "text", "text": f"Image: {name}"})
        content.append({"type": "image_url", "image_url": {"url": image_to_data_url(path)}})
    return content, missing


def observe_scene_with_moonshot(
    *,
    smoke_dir: Path,
    prompt: str,
    placement: dict[str, Any] | None = None,
    asset_grounding: dict[str, Any] | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    """Use a Moonshot/Kimi vision model to review rendered RoboTwin scene evidence."""

    smoke_dir = smoke_dir.expanduser()
    content, missing = _image_blocks(smoke_dir)
    if missing:
        return {
            "schema_version": "robotwin.tabletop_visual_review.v0",
            "prompt": prompt,
            "status": "fail_missing_artifacts",
            "review_mode": "moonshot",
            "model_backend": "moonshot",
            "missing_required_artifacts": missing,
            "checks": [],
            "issues": [{"severity": "blocker", "message": f"Missing preview image(s): {missing}"}],
            "repair_suggestions": [],
            "generated_at": date.today().isoformat(),
        }

    system = _load_prompt("observation_vlm_agent.md")
    text_prompt = {
        "task": "Review RoboTwin tabletop scene preview images.",
        "language_prompt": prompt,
        "placement": placement or {},
        "asset_grounding": asset_grounding or {},
        "required_output_schema": {
            "schema_version": "robotwin.tabletop_visual_review.v0",
            "prompt": prompt,
            "status": "pass | fail_visual_review | repair_required",
            "review_mode": "moonshot",
            "model_backend": "moonshot",
            "summary": "short summary",
            "checks": [
                {
                    "name": "object_identity | object_presence | table_contact | penetration | floating | orientation | occlusion | spatial_relation",
                    "status": "pass | fail | warning",
                    "evidence": "what you saw in the image",
                }
            ],
            "issues": [
                {
                    "severity": "blocker | major | minor",
                    "target": "object id or scene",
                    "message": "specific visual problem",
                }
            ],
            "repair_suggestions": [
                {
                    "target": "placement pose, qpos, z_policy, asset defaults, or catalog metadata",
                    "suggestion": "concrete repair action",
                }
            ],
        },
        "direction_rule": "left/right/front/back are judged in robot or dual-arm first-person frame, not image screen coordinates.",
    }
    user_content: list[dict[str, Any]] = [{"type": "text", "text": json.dumps(text_prompt, ensure_ascii=False, indent=2)}, *content]
    review = json_chat(system=system, user=user_content, model=model or model_from_env("vision"))
    review["schema_version"] = "robotwin.tabletop_visual_review.v0"
    review["prompt"] = prompt
    review["review_mode"] = "moonshot"
    review["model_backend"] = "moonshot"
    review.setdefault("generated_at", date.today().isoformat())
    review.setdefault("missing_required_artifacts", [])
    review.setdefault("checks", [])
    review.setdefault("issues", [])
    review.setdefault("repair_suggestions", [])
    if review.get("status") not in {"pass", "fail_visual_review", "repair_required"}:
        has_fail = any(check.get("status") == "fail" for check in review.get("checks", []))
        review["status"] = "fail_visual_review" if has_fail or review.get("issues") else "pass"
    return review


def main() -> int:
    parser = argparse.ArgumentParser(description="Review RoboTwin scene preview images with Moonshot/Kimi vision.")
    parser.add_argument("--smoke-dir", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--placement")
    parser.add_argument("--asset-grounding")
    parser.add_argument("--out", required=True)
    parser.add_argument("--model")
    args = parser.parse_args()

    placement = read_json(Path(args.placement)) if args.placement else None
    asset_grounding = read_json(Path(args.asset_grounding)) if args.asset_grounding else None
    review = observe_scene_with_moonshot(
        smoke_dir=Path(args.smoke_dir),
        prompt=args.prompt,
        placement=placement,
        asset_grounding=asset_grounding,
        model=args.model,
    )
    write_json(Path(args.out), review)
    print(f"{review['status'].upper()} {args.out}")
    return 0 if review["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
