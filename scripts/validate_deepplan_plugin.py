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
REQUIRED_TEXT_MARKERS_BY_FILE = {
    "README.md": (
        "Names the material optimization axis",
        "Returns a no-source-edit plan",
        "concrete validation gates",
        "Preserves host wrappers",
        "execution handoff",
    ),
    "skills/deepplan/SKILL.md": (
        "broad \"improve/optimize\" requests",
        "lock the material optimization axis",
        "classify the delta as `new_behavior_gap`, `validation_gap`,",
        "`no_material_delta`",
        "emit a no-source-edit plan",
        "actionability gate",
        "Emit readiness before implementation, cachebuster updates, reinstalls",
        "Do not use generic websearch by default",
        "confirmed local marketplace",
        "Do not hand-edit marketplace",
    ),
    "skills/deepplan/references/depth-and-pressure.md": (
        "Repeated Optimization Loops Need A Behavior Delta",
        "No-Edit Optimization Can Be Ready",
        "Discovery Metadata Must Match Skill Behavior",
        "Actionability Gate Must Reject Hidden Decisions",
    ),
}
CODEX_DEFAULT_PROMPT_MARKERS = (
    "converge this plan",
    "compare alternatives",
    "one main plan, one backup, and validation gates",
    "optimize a workflow, skill, or plugin",
    "grounding first",
    "returning no-edit",
)
OPENAI_DEFAULT_PROMPT_MARKERS = (
    "ground evidence",
    "compare alternatives",
    "optimization axes",
    "return no-edit",
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
    missing_by_file = {}
    for relative_path, required_markers in REQUIRED_TEXT_MARKERS_BY_FILE.items():
        content = read_required_text(relative_path)
        missing = [marker for marker in required_markers if marker not in content]
        if missing:
            missing_by_file[relative_path] = missing

    codex_prompt = read_codex_default_prompt_text()
    codex_missing = [
        marker for marker in CODEX_DEFAULT_PROMPT_MARKERS if marker not in codex_prompt
    ]
    if codex_missing:
        missing_by_file[".codex-plugin/plugin.json interface.defaultPrompt"] = (
            codex_missing
        )

    openai_prompt = read_openai_default_prompt_text()
    openai_missing = [
        marker
        for marker in OPENAI_DEFAULT_PROMPT_MARKERS
        if marker not in openai_prompt
    ]
    if openai_missing:
        missing_by_file[
            "skills/deepplan/agents/openai.yaml interface.default_prompt"
        ] = openai_missing

    if missing_by_file:
        details = "; ".join(
            f"{relative_path}: {', '.join(missing)}"
            for relative_path, missing in missing_by_file.items()
        )
        raise ValidationError(f"missing behavior markers: {details}")
    print("OK behavior markers")


def read_required_text(relative_path: str) -> str:
    path = ROOT / relative_path
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValidationError(f"missing marker file {relative_path}") from exc


def read_codex_default_prompt_text() -> str:
    data = read_required_json(".codex-plugin/plugin.json")
    interface = data.get("interface")
    if not isinstance(interface, dict):
        raise ValidationError(".codex-plugin/plugin.json missing interface object")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not all(
        isinstance(prompt, str) for prompt in prompts
    ):
        raise ValidationError(
            ".codex-plugin/plugin.json interface.defaultPrompt must be a string list"
        )
    return "\n".join(prompts)


def read_openai_default_prompt_text() -> str:
    try:
        import yaml
    except ImportError as exc:
        raise ValidationError("PyYAML is required for maintenance validation") from exc

    data = yaml.safe_load(
        read_required_text("skills/deepplan/agents/openai.yaml")
    )
    if not isinstance(data, dict):
        raise ValidationError("skills/deepplan/agents/openai.yaml must be a mapping")
    interface = data.get("interface")
    if not isinstance(interface, dict):
        raise ValidationError(
            "skills/deepplan/agents/openai.yaml missing interface mapping"
        )
    prompt = interface.get("default_prompt")
    if not isinstance(prompt, str):
        raise ValidationError(
            "skills/deepplan/agents/openai.yaml interface.default_prompt "
            "must be a string"
        )
    return prompt


def read_required_json(relative_path: str) -> dict:
    path = ROOT / relative_path
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"missing {relative_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{relative_path} is invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationError(f"{relative_path} must contain a JSON object")
    return data


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
