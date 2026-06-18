#!/usr/bin/env python3
"""Validate the local DeepPlan plugin maintenance contract."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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
SectionSpec = str
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
        "README subagent_pointer",
        (
            ("subagents",),
            ("subagent-opt-in",),
        ),
    ),
    (
        "README subagent_opt_in_config",
        (
            ("configure_subagents.py",),
            ("suggest-only",),
            ("allow-readonly-subagents",),
            ("dry-run",),
            ("AGENTS.override.md",),
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
        "Dependencies subagent_pointer",
        (
            ("subagents",),
            ("subagent-opt-in",),
        ),
    ),
    (
        "Dependencies maintenance_dependencies",
        (
            ("Maintenance Dependencies",),
            ("PyYAML",),
            ("DEEPPLAN_PLUGIN_VALIDATOR",),
            ("CODEX_HOME",),
        ),
    ),
)
SKILL_SECTIONS: dict[str, SectionSpec] = {
    "boundaries": "## Boundaries And Evidence",
    "grounding": "### Grounding Rules",
    "optimization": "### Optimization Requests",
    "critique": "### 4. Critique And Compare",
    "converge": "### 5. Converge And Verify",
    "handoff": "### 6. Handoff To Execution",
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
        "SKILL host_wrapper_principle",
        "boundaries",
        (
            ("wrapper",),
            ("single",),
            ("second raw block", "second block"),
        ),
    ),
    (
        "SKILL handoff_principle",
        "handoff",
        (
            ("readiness",),
            ("approval", "external", "durable"),
            ("thread/session", "new thread", "new session"),
            ("host-integration",),
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
            ("readiness", "ready"),
        ),
    ),
    (
        "SKILL subagent_decision_rule",
        "critique",
        (
            ("subagents", "parallel agent"),
            ("explicit", "request", "opt-in"),
            ("independent",),
            ("solo",),
            ("subagent-opt-in",),
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
DEPTH_AND_PRESSURE_ANCHORS: tuple[AnchorSpec, ...] = (
    (
        "Depth self_optimization_classification",
        (
            ("self-optimization classification",),
            ("new_behavior_gap",),
            ("validation_gap",),
            ("metadata_drift",),
            ("no_material_delta",),
            ("behavior delta",),
        ),
    ),
)
SUBAGENT_OPT_IN_ANCHORS: tuple[AnchorSpec, ...] = (
    (
        "Subagent opt-in default conservative",
        (
            ("conservative by default",),
            ("explicit",),
            ("additional tokens",),
        ),
    ),
    (
        "Subagent opt-in modes",
        (
            ("suggest-only",),
            ("allow-readonly-subagents",),
            ("remove",),
        ),
    ),
    (
        "Subagent opt-in markers and failure",
        (
            ("deepplan-subagents:start",),
            ("deepplan-subagents:end",),
            ("fail closed",),
            ("byte-stable",),
        ),
    ),
    (
        "Subagent opt-in host limits",
        (
            ("sandbox",),
            ("approval",),
            ("filesystem",),
            ("network",),
            ("host policy",),
        ),
    ),
    (
        "Subagent opt-in precedence",
        (
            ("closer",),
            ("AGENTS.override.md",),
            ("no subagents",),
        ),
    ),
    (
        "Subagent opt-in subagent limits",
        (
            ("recursive",),
            ("CSV fan-out",),
            ("role padding",),
            ("parent agent",),
        ),
    ),
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
HOST_INTEGRATION_ANCHORS: tuple[AnchorSpec, ...] = (
    (
        "Host wrapper",
        (
            ("wrapper",),
            ("<proposed_plan>",),
            ("single",),
            ("second raw block", "second block"),
        ),
    ),
    (
        "Host goal handoff",
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
        "Host external contracts",
        (
            ("openai",),
            ("docs", "primary source", "official"),
            ("ready_with_assumptions", "not_ready", "lower readiness"),
        ),
    ),
    (
        "Host plugin refresh",
        (
            ("cachebuster",),
            ("reinstall",),
            ("marketplace",),
            ("hand-edit",),
            ("thread/session", "new thread", "new session"),
        ),
    ),
)


def main() -> int:
    checks = (
        check_json_manifests,
        check_claude_manifest_contract,
        check_manifest_consistency,
        check_agent_yaml,
        check_plugin_structure,
        check_subagent_opt_in_artifacts,
        check_configure_subagents_smoke,
        check_behavior_anchors,
        check_skill_portability,
        check_no_stale_local_paths,
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


def read_openai_yaml() -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise ValidationError("PyYAML is required for maintenance validation") from exc
    data = yaml.safe_load(read_required_text("skills/deepplan/agents/openai.yaml"))
    if not isinstance(data, dict):
        raise ValidationError("skills/deepplan/agents/openai.yaml must be a mapping")
    return data


def check_manifest_consistency() -> None:
    """Cross-manifest facts must agree. The Codex and Claude manifests share
    name + description; the human-facing display name is identical across the
    Codex, Claude, and OpenAI surfaces. Catches updating one surface and
    forgetting the others -- drift that the keyword anchors cannot see."""
    claude = read_required_json(".claude-plugin/plugin.json")
    codex = read_required_json(".codex-plugin/plugin.json")
    openai = read_openai_yaml()

    errors = []
    if claude.get("name") != codex.get("name"):
        errors.append(
            f"name differs: .claude-plugin {claude.get('name')!r} vs "
            f".codex-plugin {codex.get('name')!r}"
        )
    if claude.get("description") != codex.get("description"):
        errors.append(
            "description differs between .claude-plugin and .codex-plugin manifests"
        )

    claude_display = claude.get("displayName")
    codex_display = (codex.get("interface") or {}).get("displayName")
    openai_display = (openai.get("interface") or {}).get("display_name")
    displays = {claude_display, codex_display, openai_display}
    if None in displays or len(displays) != 1:
        errors.append(
            "display name differs across manifests: "
            f".claude-plugin {claude_display!r}, .codex-plugin {codex_display!r}, "
            f"openai.yaml {openai_display!r}"
        )

    if errors:
        raise ValidationError("; ".join(errors))
    print("OK manifest consistency")


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
    plugin_validator = find_plugin_validator()
    if plugin_validator is None:
        if os.environ.get("DEEPPLAN_REQUIRE_PLUGIN_STRUCTURE"):
            raise ValidationError(
                "plugin-creator validator not found; set DEEPPLAN_PLUGIN_VALIDATOR "
                "or install plugin-creator under "
                "$CODEX_HOME/skills/.system/plugin-creator "
                "(required because DEEPPLAN_REQUIRE_PLUGIN_STRUCTURE is set)"
            )
        print(
            "SKIP plugin structure (plugin-creator validator not found; set "
            "DEEPPLAN_PLUGIN_VALIDATOR, or DEEPPLAN_REQUIRE_PLUGIN_STRUCTURE=1 to enforce)"
        )
        return
    run((sys.executable, str(plugin_validator), str(ROOT)))
    print("OK plugin structure")


def find_plugin_validator() -> Path | None:
    override = os.environ.get("DEEPPLAN_PLUGIN_VALIDATOR")
    if override:
        path = Path(override).expanduser()
        if path.is_file():
            return path
        raise ValidationError(f"missing plugin validator from DEEPPLAN_PLUGIN_VALIDATOR: {path}")

    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    path = codex_home / "skills/.system/plugin-creator/scripts/validate_plugin.py"
    if path.is_file():
        return path
    return None


def check_subagent_opt_in_artifacts() -> None:
    for relative_path in (
        "scripts/configure_subagents.py",
        "skills/deepplan/references/subagent-opt-in.md",
    ):
        path = ROOT / relative_path
        if not path.is_file():
            raise ValidationError(f"missing {relative_path}")
    print("OK subagent opt-in artifacts")


def check_configure_subagents_smoke() -> None:
    script = ROOT / "scripts/configure_subagents.py"
    help_result = run_capture((sys.executable, str(script), "--help"))
    require_output_terms(
        "configure_subagents --help",
        help_result.stdout,
        "--mode",
        "suggest-only",
        "allow-readonly-subagents",
        "remove",
        "--write",
        "--check",
        "--print-snippet",
    )

    snippet_result = run_capture(
        (sys.executable, str(script), "--print-snippet", "--mode", "suggest-only")
    )
    require_output_terms(
        "configure_subagents --print-snippet",
        snippet_result.stdout,
        "deepplan-subagents:start",
        "deepplan-subagents:end",
        "suggest-only",
        "sandbox",
        "approval",
    )

    with tempfile.TemporaryDirectory(prefix="deepplan subagents ") as tmp:
        tmp_root = Path(tmp)
        repo = tmp_root / "repo with spaces"
        nested = repo / "nested" / "cwd"
        nested.mkdir(parents=True)

        run_capture((sys.executable, str(script), "--repo", str(repo), "--mode", "suggest-only"))
        agents_path = repo / "AGENTS.md"
        if agents_path.exists():
            raise ValidationError("dry-run unexpectedly created AGENTS.md")

        run_capture(
            (
                sys.executable,
                str(script),
                "--repo",
                str(repo),
                "--mode",
                "suggest-only",
                "--write",
            ),
            cwd=nested,
        )
        first = agents_path.read_text(encoding="utf-8")
        require_output_terms(
            "suggest-only managed block",
            first,
            "deepplan-subagents:start",
            "deepplan-subagents:end",
            "Mode: suggest-only",
            "may recommend",
            "must not spawn",
        )

        run_capture(
            (
                sys.executable,
                str(script),
                "--repo",
                str(repo),
                "--mode",
                "suggest-only",
                "--write",
            )
        )
        second = agents_path.read_text(encoding="utf-8")
        if second != first:
            raise ValidationError("same-mode write is not byte-stable")

        run_capture(
            (
                sys.executable,
                str(script),
                "--repo",
                str(repo),
                "--mode",
                "allow-readonly-subagents",
                "--write",
            )
        )
        third = agents_path.read_text(encoding="utf-8")
        require_output_terms(
            "allow-readonly-subagents managed block",
            third,
            "Mode: allow-readonly-subagents",
            "standing explicit request",
            "read-heavy",
            "sandbox",
            "approval",
        )
        if third == second:
            raise ValidationError("mode replacement did not change AGENTS.md")

        run_capture((sys.executable, str(script), "--repo", str(repo), "--check"))

        before_remove_dry_run = agents_path.read_text(encoding="utf-8")
        run_capture((sys.executable, str(script), "--repo", str(repo), "--mode", "remove"))
        if agents_path.read_text(encoding="utf-8") != before_remove_dry_run:
            raise ValidationError("dry-run remove changed AGENTS.md")

        agents_path.write_text(
            "prefix\n\n" + before_remove_dry_run + "\n\nsuffix\n",
            encoding="utf-8",
        )
        run_capture(
            (
                sys.executable,
                str(script),
                "--repo",
                str(repo),
                "--mode",
                "remove",
                "--write",
            )
        )
        removed = agents_path.read_text(encoding="utf-8")
        if "deepplan-subagents:" in removed or "prefix" not in removed or "suffix" not in removed:
            raise ValidationError("remove did not preserve surrounding AGENTS.md content")

        malformed = "before\n<!-- deepplan-subagents:start -->\nmissing end\n"
        agents_path.write_text(malformed, encoding="utf-8")
        bad_result = run_capture(
            (
                sys.executable,
                str(script),
                "--repo",
                str(repo),
                "--mode",
                "suggest-only",
                "--write",
            ),
            check=False,
        )
        if bad_result.returncode == 0:
            raise ValidationError("malformed marker write unexpectedly succeeded")
        if agents_path.read_text(encoding="utf-8") != malformed:
            raise ValidationError("malformed marker failure changed AGENTS.md")

        override_repo = tmp_root / "override repo"
        override_repo.mkdir()
        (override_repo / "AGENTS.override.md").write_text("override\n", encoding="utf-8")
        override_result = run_capture(
            (
                sys.executable,
                str(script),
                "--repo",
                str(override_repo),
                "--mode",
                "suggest-only",
                "--write",
            ),
            check=False,
        )
        if override_result.returncode == 0:
            raise ValidationError("non-empty AGENTS.override.md did not fail closed")
        if (override_repo / "AGENTS.md").exists():
            raise ValidationError("override failure unexpectedly created AGENTS.md")

    print("OK configure_subagents smoke")


def check_behavior_anchors() -> None:
    missing: list[str] = []
    check_readme_anchors(missing)
    check_dependencies_anchors(missing)
    check_skill_anchors(missing)
    check_reference_anchors(missing)
    check_host_integration_anchors(missing)
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
        name: extract_required_section(missing, f"SKILL {name}", content, heading)
        for name, heading in SKILL_SECTIONS.items()
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
    require_anchors(missing, content, DEPTH_AND_PRESSURE_ANCHORS)
    require_anchors(
        missing,
        read_required_text("skills/deepplan/references/subagent-opt-in.md"),
        SUBAGENT_OPT_IN_ANCHORS,
    )


def check_host_integration_anchors(missing: list[str]) -> None:
    require_anchors(
        missing,
        read_required_text("skills/deepplan/references/host-integration.md"),
        HOST_INTEGRATION_ANCHORS,
    )


def check_prompt_intent_anchors(missing: list[str]) -> None:
    require_anchors(missing, read_codex_default_prompt_text(), CODEX_PROMPT_ANCHORS)
    require_anchors(missing, read_openai_default_prompt_text(), OPENAI_PROMPT_ANCHORS)


def check_no_stale_local_paths() -> None:
    stale_home = "/" + "home/ubuntu"
    stale_marketplace = "deepplan" + "-local"
    for relative_path in (
        "README.md",
        "DEPENDENCIES.md",
        "scripts/validate_deepplan_plugin.py",
    ):
        content = read_required_text(relative_path)
        if stale_home in content:
            raise ValidationError(f"{relative_path} contains stale {stale_home} path")
        if stale_marketplace in content:
            raise ValidationError(
                f"{relative_path} contains stale {stale_marketplace} marketplace"
            )
    print("OK no stale local paths")


SKILL_HOST_ONLY_TOKENS = (
    "$deepplan",
    "/goal",
    "<proposed_plan>",
    "cachebuster",
    "marketplace",
    "reinstall",
)


def check_skill_portability() -> None:
    """The SKILL.md spine must stay host-agnostic: a host-specific token may appear
    only on a line that also points to references/host-integration.md."""
    content = read_required_text("skills/deepplan/SKILL.md")
    offenders: list[str] = []
    for lineno, line in enumerate(content.splitlines(), start=1):
        lowered = line.lower()
        if "host-integration" in lowered:
            continue
        for token in SKILL_HOST_ONLY_TOKENS:
            if token in lowered:
                offenders.append(f"line {lineno}: {token!r}")
    if offenders:
        raise ValidationError(
            "SKILL.md spine must be host-agnostic; move host-specific mechanics to "
            "references/host-integration.md (offending tokens: "
            + "; ".join(offenders)
            + ")"
        )
    print("OK skill portability")


def heading_level(line: str) -> int:
    stripped = line.lstrip()
    hashes = len(stripped) - len(stripped.lstrip("#"))
    if hashes < 1 or hashes > 6 or not stripped[hashes:].startswith(" "):
        return 0
    return hashes


def extract_required_section(
    missing: list[str],
    anchor: str,
    content: str,
    heading: str,
) -> str:
    """Return a markdown section: its heading down to the next heading of
    equal-or-higher level. Heading-aware (not first-occurrence substring), so
    rewording or moving prose inside a section does not break validation."""
    target = heading.strip().lower()
    target_level = heading_level(heading)
    lines = content.splitlines(keepends=True)

    start_line = -1
    in_fence = False
    for index, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and heading_level(line) and line.strip().lower() == target:
            start_line = index
            break
    if start_line == -1:
        missing.append(f"{anchor}: section heading {heading!r}")
        return ""

    collected = [lines[start_line]]
    in_fence = False
    for line in lines[start_line + 1:]:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            collected.append(line)
            continue
        level = 0 if in_fence else heading_level(line)
        if level and level <= target_level:
            break
        collected.append(line)
    return "".join(collected)


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


def require_output_terms(anchor: str, content: str, *terms: str) -> None:
    normalized = content.lower()
    missing = [term for term in terms if term.lower() not in normalized]
    if missing:
        raise ValidationError(f"{anchor} missing terms: {', '.join(missing)}")


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


def run_capture(
    command: tuple[str, ...],
    *,
    cwd: Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        cwd=cwd or ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if check and completed.returncode != 0:
        details = "\n".join(
            part.strip()
            for part in (completed.stdout, completed.stderr)
            if part.strip()
        )
        raise ValidationError(details or f"{command!r} exited {completed.returncode}")
    return completed


class ValidationError(Exception):
    """Raised when a validation check fails."""


if __name__ == "__main__":
    raise SystemExit(main())
