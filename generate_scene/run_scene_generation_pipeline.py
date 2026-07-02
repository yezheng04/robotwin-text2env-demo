#!/usr/bin/env python3
"""Run natural-language prompt to generated RoboTwin tabletop scene module."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from generate_scene.asset_catalog import load_asset_catalog
from generate_scene.asset_grounding import (
    ground_assets,
    prompt_case_from_grounding,
    slugify_prompt,
    validate_asset_grounding_result,
)
from generate_scene.model_providers import (
    critic_review_from_validation,
    design_initial_spec,
    orchestrate_final_spec,
    validation_plan_for,
)
from generate_scene.scene_codegen import generate_scene_module
from generate_scene.schemas import read_json, validate_placement_spec, write_json
from generate_scene.tools import get_smoke_artifacts, run_robotwin_smoke, visual_review


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def _case_base_catalog(case_path: Path, master_catalog_path: Path) -> str:
    try:
        return str(master_catalog_path.resolve().relative_to(case_path.parent.resolve())).replace("\\", "/")
    except ValueError:
        return str(master_catalog_path.resolve())


def main() -> int:
    parser = argparse.ArgumentParser(description="Run prompt to generated RoboTwin scene module.")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--master-catalog", default="asset_catalogs/robotwin_tabletop_assets_master.json")
    parser.add_argument("--prompt-case")
    parser.add_argument("--case-name")
    parser.add_argument("--overwrite-prompt-case", action="store_true")
    parser.add_argument("--robotwin-root", default=str(Path.home() / "RoboTwin"))
    parser.add_argument("--model-provider", default="codex_reference")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--generated-scene-dir", default="generated_scenes")
    parser.add_argument("--run-smoke", action="store_true")
    parser.add_argument("--task-config", default="demo_smoke")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--settle-steps", type=int, default=240)
    parser.add_argument("--video-frames", type=int, default=60)
    parser.add_argument("--fps", type=int, default=15)
    parser.add_argument("--python-executable", help="Python executable for RoboTwin smoke. Also configurable through ROBOTWIN_PYTHON.")
    parser.add_argument("--visual-review-mode", choices=["required", "artifact_only"], default="required")
    parser.add_argument("--visual-review-report")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    master_catalog_path = Path(args.master_catalog)
    master_catalog = load_asset_catalog(master_catalog_path)
    case_name = args.case_name or slugify_prompt(args.prompt)
    prompt_case_path = Path(args.prompt_case) if args.prompt_case else Path("asset_catalogs") / "prompt_cases" / f"{case_name}.json"

    summary: dict[str, Any] = {
        "schema_version": "robotwin.tabletop_scene_generation_summary.v0",
        "prompt": args.prompt,
        "case_name": case_name,
        "master_catalog": _rel(master_catalog_path),
        "prompt_case": _rel(prompt_case_path),
        "model_provider": args.model_provider,
        "out_dir": _rel(out_dir),
        "status": "started",
        "artifacts": {},
    }

    try:
        grounding = ground_assets(
            prompt=args.prompt,
            master_catalog=master_catalog,
            master_catalog_path=_rel(master_catalog_path),
        )
        grounding_validation = validate_asset_grounding_result(grounding, master_catalog)
        grounding["validation"] = grounding_validation
        grounding_path = out_dir / "asset_grounding.json"
        write_json(grounding_path, grounding)
        summary["artifacts"]["asset_grounding"] = _rel(grounding_path)

        if grounding_validation["status"] != "pass":
            summary["status"] = "fail_asset_grounding"
            write_json(out_dir / "scene_generation_summary.json", summary)
            print(f"FAIL {out_dir / 'scene_generation_summary.json'}")
            return 1

        if prompt_case_path.exists() and not args.overwrite_prompt_case:
            prompt_case_status = "exists_not_overwritten"
        else:
            prompt_case = prompt_case_from_grounding(
                grounding=grounding,
                case_name=case_name,
                base_catalog=_case_base_catalog(prompt_case_path, master_catalog_path),
            )
            write_json(prompt_case_path, prompt_case)
            prompt_case_status = "written"
        case_copy_path = out_dir / "prompt_case.json"
        shutil.copyfile(prompt_case_path, case_copy_path)
        summary["prompt_case_status"] = prompt_case_status
        summary["artifacts"]["prompt_case_copy"] = _rel(case_copy_path)

        catalog = load_asset_catalog(prompt_case_path)
        designer_spec = design_initial_spec(
            prompt=args.prompt,
            catalog=catalog,
            asset_catalog_path=_rel(prompt_case_path),
            model_provider=args.model_provider,
        )
        designer_path = out_dir / "designer_initial_placement.json"
        write_json(designer_path, designer_spec)

        initial_validation = validate_placement_spec(designer_spec, catalog, robotwin_root=args.robotwin_root)
        initial_validation_path = out_dir / "static_validation_initial.json"
        write_json(initial_validation_path, initial_validation)

        critic_review = critic_review_from_validation(
            placement=designer_spec,
            validation_report=initial_validation,
            model_provider=args.model_provider,
        )
        critic_path = out_dir / "critic_review.json"
        write_json(critic_path, critic_review)

        final_spec = orchestrate_final_spec(
            designer_spec=designer_spec,
            critic_review=critic_review,
            model_provider=args.model_provider,
        )
        final_path = out_dir / "final_placement.json"
        write_json(final_path, final_spec)

        final_validation = validate_placement_spec(final_spec, catalog, robotwin_root=args.robotwin_root)
        final_validation_path = out_dir / "static_validation_final.json"
        write_json(final_validation_path, final_validation)

        validation_plan_path = out_dir / "validation_plan.json"
        write_json(validation_plan_path, validation_plan_for(final_spec))
        summary["artifacts"].update(
            {
                "designer_initial_placement": _rel(designer_path),
                "static_validation_initial": _rel(initial_validation_path),
                "critic_review": _rel(critic_path),
                "final_placement": _rel(final_path),
                "static_validation_final": _rel(final_validation_path),
                "validation_plan": _rel(validation_plan_path),
            }
        )

        if final_validation["status"] != "pass":
            summary["status"] = "fail_static_validation"
            write_json(out_dir / "scene_generation_summary.json", summary)
            print(f"FAIL {out_dir / 'scene_generation_summary.json'}")
            return 1

        scene_module_path = Path(args.generated_scene_dir) / f"{case_name}_scene.py"
        scene_report = generate_scene_module(placement_path=final_path, out_path=scene_module_path)
        scene_report_path = out_dir / "scene_codegen_report.json"
        write_json(scene_report_path, scene_report)
        summary["artifacts"].update(
            {
                "generated_scene_module": _rel(scene_module_path),
                "scene_codegen_report": _rel(scene_report_path),
            }
        )

        if args.run_smoke:
            smoke_dir = out_dir / "smoke"
            smoke_report = run_robotwin_smoke(
                robotwin_root=Path(args.robotwin_root).expanduser(),
                placement=final_path,
                out_dir=smoke_dir,
                task_config=args.task_config,
                seed=args.seed,
                settle_steps=args.settle_steps,
                video_frames=args.video_frames,
                fps=args.fps,
                scene_module=scene_module_path,
                python_executable=args.python_executable,
            )
            smoke_report_path = out_dir / "smoke_report_with_command.json"
            write_json(smoke_report_path, smoke_report)
            visual_review_report = visual_review(smoke_dir, args.prompt, mode=args.visual_review_mode)
            if args.visual_review_report:
                visual_review_report = read_json(Path(args.visual_review_report))
            visual_review_path = out_dir / "visual_review.json"
            write_json(visual_review_path, visual_review_report)
            summary["artifacts"].update(
                {
                    "smoke_report": _rel(smoke_dir / "smoke_report.json"),
                    "smoke_report_with_command": _rel(smoke_report_path),
                    "visual_review": _rel(visual_review_path),
                    "preview": get_smoke_artifacts(smoke_dir),
                }
            )
            smoke_passed = smoke_report.get("status") == "pass" and smoke_report.get("returncode") == 0
            visual_status = str(visual_review_report.get("status", ""))
            if not smoke_passed:
                summary["status"] = "fail_smoke"
            elif visual_status == "pass":
                summary["status"] = "pass"
            elif visual_status.startswith("fail"):
                summary["status"] = "fail_visual_review"
            else:
                summary["status"] = "pending_visual_review"
        else:
            summary["status"] = "pass_static_scene_module"

        write_json(out_dir / "scene_generation_summary.json", summary)
        if summary["status"] == "pass":
            label = "PASS"
        elif summary["status"] == "pending_visual_review":
            label = "REVIEW_REQUIRED"
        elif summary["status"] == "pass_static_scene_module":
            label = "PASS_STATIC"
        else:
            label = "FAIL"
        print(f"{label} {out_dir / 'scene_generation_summary.json'}")
        return 0 if summary["status"] in {"pass", "pending_visual_review", "pass_static_scene_module"} else 1
    except Exception as exc:
        summary["status"] = "fail_exception"
        summary["error"] = repr(exc)
        write_json(out_dir / "scene_generation_summary.json", summary)
        print(f"FAIL {out_dir / 'scene_generation_summary.json'}")
        raise


if __name__ == "__main__":
    raise SystemExit(main())
