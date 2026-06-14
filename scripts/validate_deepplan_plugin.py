#!/usr/bin/env python3
"""Validate the local DeepPlan plugin maintenance contract."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_VALIDATOR = Path(
    "/home/ubuntu/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py"
)
MARKERS = (
    "optimization axis",
    "workflow/process/skill/plugin optimization",
    "broad optimization",
    "actionability",
    "no_material_delta",
    "no-source-edit",
)
MARKER_FILES = (
    "README.md",
    ".codex-plugin/plugin.json",
    "skills/deepplan/SKILL.md",
    "skills/deepplan/agents/openai.yaml",
    "skills/deepplan/references/depth-and-pressure.md",
)


def main() -> int:
    checks = (
        check_json_manifests,
        check_agent_yaml,
        check_plugin_structure,
        check_markers,
        check_git_diff,
    )
    for check in checks:
        try:
            check()
        except ValidationError as exc:
            print(f"FAIL {check.__name__}: {exc}", file=sys.stderr)
            return 1
    print("DeepPlan plugin validation passed.")
    return 0


def check_json_manifests() -> None:
    for relative_path in (
        ".codex-plugin/plugin.json",
        ".claude-plugin/plugin.json",
    ):
        path = ROOT / relative_path
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ValidationError(f"missing {relative_path}") from exc
        except json.JSONDecodeError as exc:
            raise ValidationError(f"{relative_path} is invalid JSON: {exc}") from exc
    print("OK json manifests")


def check_agent_yaml() -> None:
    try:
        import yaml
    except ImportError as exc:
        raise ValidationError("PyYAML is required for maintenance validation") from exc

    path = ROOT / "skills/deepplan/agents/openai.yaml"
    try:
        yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError("missing skills/deepplan/agents/openai.yaml") from exc
    except yaml.YAMLError as exc:
        raise ValidationError(f"agent metadata is invalid YAML: {exc}") from exc
    print("OK agent yaml")


def check_plugin_structure() -> None:
    if not PLUGIN_VALIDATOR.is_file():
        raise ValidationError(f"missing plugin validator: {PLUGIN_VALIDATOR}")
    run((sys.executable, str(PLUGIN_VALIDATOR), str(ROOT)))
    print("OK plugin structure")


def check_markers() -> None:
    haystack = {}
    for relative_path in MARKER_FILES:
        path = ROOT / relative_path
        try:
            haystack[relative_path] = path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise ValidationError(f"missing marker file {relative_path}") from exc

    missing = [
        marker
        for marker in MARKERS
        if not any(marker in content for content in haystack.values())
    ]
    if missing:
        raise ValidationError(f"missing markers: {', '.join(missing)}")
    print("OK behavior markers")


def check_git_diff() -> None:
    run(("git", "diff", "--check"))
    print("OK git diff --check")


def run(command: tuple[str, ...]) -> None:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        details = "\n".join(
            part.strip()
            for part in (completed.stdout, completed.stderr)
            if part.strip()
        )
        raise ValidationError(details or f"{command!r} exited {completed.returncode}")


class ValidationError(Exception):
    """Raised when a validation check fails."""


if __name__ == "__main__":
    raise SystemExit(main())
