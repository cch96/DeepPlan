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
CLAUDE_MANIFEST_FIELDS = frozenset(
    {
        "name",
        "displayName",
        "version",
        "description",
        "author",
        "skills",
    }
)
CLAUDE_REQUIRED_STRINGS = {
    "name": "deepplan",
    "displayName": "DeepPlan",
    "skills": "./skills/",
}
AnchorSpec = tuple[str, tuple[tuple[str, ...], ...]]
SectionAnchorSpec = tuple[str, str, tuple[tuple[str, ...], ...]]
SectionSpec = tuple[str, str]
README_ANCHORS: tuple[AnchorSpec, ...] = (
    (
        "README optimization_axis",
        (
            ("optimization axis",),
            ("broad", "improve"),
            ("source changes", "implementation starts"),
        ),
    ),
    (
        "README no_source_edit",
        (
            ("no-source-edit", "no source edit", "no-edit"),
            ("behavior",),
            ("validation",),
            ("metadata",),
        ),
    ),
    (
        "README validation_gates",
        (
            ("validation gates",),
            ("hidden decisions", "actionability gate"),
            ("fallbacks", "fallback"),
        ),
    ),
    (
        "README host_wrapper",
        (
            ("host wrappers", "wrapper"),
            ("<proposed_plan>", "plan mode"),
        ),
    ),
    (
        "README execution_handoff",
        (
            ("cachebuster",),
            ("reinstalls", "reinstall"),
            ("execution handoff", "handoff"),
        ),
    ),
    (
        "README subagent_lens_roles",
        (
            ("subagents",),
            ("explicitly requests", "explicit user request"),
            ("lenses", "lens-roles", "lens roles"),
            ("independent read-heavy", "independent critique"),
        ),
    ),
    (
        "README host_specific_goal_handoff",
        (
            ("goal mode", "/goal"),
            ("codex",),
            ("claude", "non-codex", "non codex"),
            ("optional", "host-specific", "host specific"),
            ("handoff",),
        ),
    ),
)
DEPENDENCIES_ANCHORS: tuple[AnchorSpec, ...] = (
    (
        "Dependencies subagent_optional_lens_roles",
        (
            ("subagents",),
            ("explicitly asks", "explicit user request"),
            ("lenses", "lens-roles", "lens roles"),
            ("solo critique",),
        ),
    ),
)
SKILL_SECTIONS: dict[str, SectionSpec] = {
    "boundaries": ("## Boundaries And Evidence", "## Workflow"),
    "grounding": ("Grounding rules:", "Optimization requests:"),
    "optimization": ("Optimization requests:", "## Workflow"),
    "critique": ("### 4. Critique And Compare", "### 5. Converge And Verify"),
    "converge": ("### 5. Converge And Verify", "### 6. Handoff To Execution"),
    "handoff": ("### 6. Handoff To Execution", "## Output And Readiness"),
}
SKILL_ANCHORS: tuple[SectionAnchorSpec, ...] = (
    (
        "SKILL optimization_axis",
        "optimization",
        (
            ("axis",),
            ("broad", "improve", "optimize", "optimization"),
            ("objective", "assumptions"),
            ("ready",),
        ),
    ),
    (
        "SKILL repeated_no_edit",
        "optimization",
        (
            ("new_behavior_gap",),
            ("validation_gap",),
            ("metadata_drift",),
            ("no_material_delta",),
            ("no-source-edit", "no source edit", "no-edit"),
            ("behavior delta",),
        ),
    ),
    (
        "SKILL actionability_gate",
        "converge",
        (
            ("actionability gate",),
            ("implementer",),
            ("expected result",),
            ("fallback",),
            ("switch condition",),
            ("approval boundary",),
        ),
    ),
    (
        "SKILL host_wrapper_boundary",
        "boundaries",
        (
            ("wrapper",),
            ("<proposed_plan>",),
            ("single",),
            ("second raw block", "second block"),
        ),
    ),
    (
        "SKILL plugin_refresh_handoff",
        "handoff",
        (
            ("cachebuster",),
            ("reinstall",),
            ("marketplace",),
            ("hand-edit",),
            ("thread/session", "new thread", "new session"),
        ),
    ),
    (
        "SKILL host_specific_goal_handoff",
        "handoff",
        (
            ("goal mode", "/goal"),
            ("codex",),
            ("claude", "non-codex", "non codex"),
            ("optional", "host-specific", "host specific"),
            ("completion criteria", "acceptance criteria"),
            ("validation",),
            ("do not require", "must not require", "not require"),
        ),
    ),
    (
        "SKILL metadata_discovery",
        "grounding",
        (
            ("codex",),
            ("claude",),
            ("manifests", "manifest"),
            ("agent/default prompts", "default prompts"),
            ("install/cache sources", "cache sources"),
        ),
    ),
    (
        "SKILL websearch_primary_source_boundary",
        "grounding",
        (
            ("websearch",),
            ("official",),
            ("primary sources", "primary source"),
            ("openai",),
            ("readiness", "ready"),
        ),
    ),
    (
        "SKILL subagent_lens_role_selection",
        "critique",
        (
            ("explicitly asks", "explicit user request"),
            ("subagents", "parallel agent"),
            ("select", "selected"),
            ("lenses", "lens-roles", "lens roles"),
            ("2-4", "two to four"),
            ("independent read-heavy", "independent critique"),
            ("main plan",),
            ("backup",),
            ("switch condition",),
            ("validation",),
            ("readiness",),
        ),
    ),
    (
        "SKILL subagent_negative_guardrails",
        "critique",
        (
            ("not request", "not requested", "unrequested"),
            ("solo critique",),
            ("optional subagents",),
            ("block", "weaken"),
            ("fake debate",),
            ("padding", "pad"),
            ("duplicate",),
        ),
    ),
)
REFERENCE_SCENARIOS = (
    "Repeated Optimization Loops Need A Behavior Delta",
    "No-Edit Optimization Can Be Ready",
    "Discovery Metadata Must Match Skill Behavior",
    "Actionability Gate Must Reject Hidden Decisions",
    "Subagent Lens-Roles Need Explicit Request And Independent Scope",
    "Host-Specific Goal Handoff Stays Optional",
)
CODEX_PROMPT_ANCHORS: tuple[AnchorSpec, ...] = (
    (
        "Codex defaultPrompt planning",
        (
            ("deepplan",),
            ("converge", "compare alternatives"),
            ("plan",),
            ("validation", "validation gates"),
        ),
    ),
    (
        "Codex defaultPrompt backup",
        (
            ("main plan",),
            ("backup",),
        ),
    ),
    (
        "Codex defaultPrompt optimization",
        (
            ("optimize",),
            ("workflow",),
            ("skill",),
            ("plugin",),
            ("grounding", "ground"),
            ("no-edit", "no source edit", "no-source-edit"),
        ),
    ),
)
OPENAI_PROMPT_ANCHORS: tuple[AnchorSpec, ...] = (
    (
        "OpenAI default_prompt",
        (
            ("deepplan",),
            ("ground",),
            ("evidence",),
            ("alternatives",),
            ("optimization axes", "optimization axis"),
            ("no-edit", "no source edit", "no-source-edit"),
        ),
    ),
)


def main() -> int:
    checks = (
        check_json_manifests,
        check_claude_manifest_contract,
        check_agent_yaml,
        check_plugin_structure,
        check_behavior_anchors,
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


def check_claude_manifest_contract() -> None:
    data = read_required_json(".claude-plugin/plugin.json")
    errors = []

    extra_fields = sorted(set(data) - CLAUDE_MANIFEST_FIELDS)
    if extra_fields:
        errors.append(
            "unexpected fields for intentionally minimal Claude manifest: "
            + ", ".join(extra_fields)
        )

    for field, expected in CLAUDE_REQUIRED_STRINGS.items():
        if data.get(field) != expected:
            errors.append(f"{field} must be {expected!r}")

    for field in ("version", "description"):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} must be a non-empty string")

    author = data.get("author")
    if not isinstance(author, dict):
        errors.append("author must be an object")
    else:
        author_name = author.get("name")
        if not isinstance(author_name, str) or not author_name.strip():
            errors.append("author.name must be a non-empty string")

    if errors:
        raise ValidationError("; ".join(errors))
    print("OK claude manifest contract")


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


def check_behavior_anchors() -> None:
    missing: list[str] = []
    check_readme_anchors(missing)
    check_dependencies_anchors(missing)
    check_skill_anchors(missing)
    check_reference_anchors(missing)
    check_prompt_intent_anchors(missing)

    if missing:
        raise ValidationError("missing behavior anchors: " + "; ".join(missing))
    print("OK behavior anchors")


def check_readme_anchors(missing: list[str]) -> None:
    content = read_required_text("README.md")
    require_anchors(missing, content, README_ANCHORS)


def check_dependencies_anchors(missing: list[str]) -> None:
    content = read_required_text("DEPENDENCIES.md")
    require_anchors(missing, content, DEPENDENCIES_ANCHORS)


def check_skill_anchors(missing: list[str]) -> None:
    content = read_required_text("skills/deepplan/SKILL.md")
    sections = {
        name: extract_required_section(missing, f"SKILL {name}", content, *bounds)
        for name, bounds in SKILL_SECTIONS.items()
    }
    for anchor, section_name, term_groups in SKILL_ANCHORS:
        require_anchor(missing, anchor, sections[section_name], *term_groups)


def check_reference_anchors(missing: list[str]) -> None:
    content = read_required_text("skills/deepplan/references/depth-and-pressure.md")
    for scenario in REFERENCE_SCENARIOS:
        require_anchor(
            missing,
            f"reference scenario {scenario}",
            content,
            (scenario,),
        )


def check_prompt_intent_anchors(missing: list[str]) -> None:
    require_anchors(missing, read_codex_default_prompt_text(), CODEX_PROMPT_ANCHORS)
    require_anchors(missing, read_openai_default_prompt_text(), OPENAI_PROMPT_ANCHORS)


def extract_required_section(
    missing: list[str],
    anchor: str,
    content: str,
    start: str,
    end: str,
) -> str:
    lower_content = content.lower()
    lower_start = start.lower()
    start_index = lower_content.find(lower_start)
    if start_index == -1:
        missing.append(f"{anchor}: section start {start!r}")
        return ""

    end_index = lower_content.find(end.lower(), start_index + len(lower_start))
    if end_index == -1:
        missing.append(f"{anchor}: section end {end!r}")
        return content[start_index:]
    return content[start_index:end_index]


def require_anchor(
    missing: list[str],
    anchor: str,
    content: str,
    *term_groups: tuple[str, ...],
) -> None:
    normalized = content.lower()
    missing_groups = [
        " or ".join(group)
        for group in term_groups
        if not any(term.lower() in normalized for term in group)
    ]
    if missing_groups:
        missing.append(f"{anchor}: {', '.join(missing_groups)}")


def require_anchors(
    missing: list[str],
    content: str,
    anchors: tuple[AnchorSpec, ...],
) -> None:
    for anchor, term_groups in anchors:
        require_anchor(missing, anchor, content, *term_groups)


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
