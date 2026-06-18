#!/usr/bin/env python3
"""Configure DeepPlan subagent opt-in guidance in a repository AGENTS.md."""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path


START_MARKER = "<!-- deepplan-subagents:start -->"
END_MARKER = "<!-- deepplan-subagents:end -->"
MODES = ("suggest-only", "allow-readonly-subagents", "remove")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Add, replace, check, or remove DeepPlan's managed subagent policy "
            "block in a repository AGENTS.md. Dry-run is the default; pass "
            "--write to change files."
        )
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Repository root containing AGENTS.md, default: current directory",
    )
    parser.add_argument(
        "--mode",
        choices=MODES,
        default="suggest-only",
        help=(
            "Policy to configure: suggest-only, allow-readonly-subagents, or "
            "remove the managed block"
        ),
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Actually update AGENTS.md. Without this flag, print a dry-run summary.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the current managed block and exit without changing files.",
    )
    parser.add_argument(
        "--print-snippet",
        action="store_true",
        help="Print the managed block for --mode and exit without reading AGENTS.md.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.print_snippet:
        if args.mode == "remove":
            print("--print-snippet cannot be used with --mode remove", file=sys.stderr)
            return 2
        print(render_block(args.mode))
        return 0

    repo = Path(args.repo).expanduser().resolve()
    if not repo.is_dir():
        print(f"Repository path does not exist or is not a directory: {repo}", file=sys.stderr)
        return 1

    agents_path = repo / "AGENTS.md"
    override_path = repo / "AGENTS.override.md"
    content = read_text_or_empty(agents_path)

    try:
        block_span = find_managed_block(content)
        if args.check:
            check_current_state(agents_path, override_path, content, block_span)
            return 0

        if args.write and override_is_nonempty(override_path):
            raise ConfigError(
                f"{override_path} is non-empty and can shadow {agents_path}; "
                "remove or update the override before writing DeepPlan guidance."
            )

        next_content = apply_mode(content, block_span, args.mode)
    except ConfigError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not args.write:
        print_dry_run(agents_path, args.mode, content, next_content)
        return 0

    write_atomic(agents_path, next_content)
    print(f"Updated {agents_path} with DeepPlan subagent mode: {args.mode}")
    print("Start a new Codex session/thread before relying on changed AGENTS.md guidance.")
    return 0


def read_text_or_empty(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def override_is_nonempty(path: Path) -> bool:
    return path.exists() and bool(path.read_text(encoding="utf-8").strip())


def find_managed_block(content: str) -> tuple[int, int] | None:
    start_count = content.count(START_MARKER)
    end_count = content.count(END_MARKER)
    if start_count != end_count:
        raise ConfigError("managed marker mismatch in AGENTS.md")
    if start_count > 1:
        raise ConfigError("multiple managed DeepPlan subagent blocks in AGENTS.md")
    if start_count == 0:
        return None

    start = content.index(START_MARKER)
    end_marker_start = content.index(END_MARKER)
    end = end_marker_start + len(END_MARKER)
    if end_marker_start < start:
        raise ConfigError("managed end marker appears before start marker")
    return start, end


def check_current_state(
    agents_path: Path,
    override_path: Path,
    content: str,
    block_span: tuple[int, int] | None,
) -> None:
    if override_is_nonempty(override_path) and block_span is not None:
        raise ConfigError(f"{override_path} is non-empty and can shadow {agents_path}")
    if block_span is None:
        print(f"OK: no DeepPlan managed block in {agents_path}")
        return

    block = content[block_span[0] : block_span[1]]
    if "Mode: suggest-only" not in block and "Mode: allow-readonly-subagents" not in block:
        raise ConfigError("managed block does not declare a supported mode")
    print(f"OK: DeepPlan managed block is valid in {agents_path}")


def apply_mode(
    content: str,
    block_span: tuple[int, int] | None,
    mode: str,
) -> str:
    if mode == "remove":
        if block_span is None:
            return content
        before = content[: block_span[0]].rstrip()
        after = content[block_span[1] :].lstrip()
        if before and after:
            return before + "\n\n" + after
        if before:
            return before + "\n"
        return after

    block = render_block(mode)
    if block_span is not None:
        return content[: block_span[0]] + block + content[block_span[1] :]
    if not content.strip():
        return block + "\n"
    return content.rstrip() + "\n\n" + block + "\n"


def render_block(mode: str) -> str:
    if mode == "suggest-only":
        body = """## DeepPlan Subagent Policy

Mode: suggest-only

This repository asks DeepPlan to check whether a Full-path planning task has
two to four independent read-heavy evidence domains. DeepPlan may recommend a
bounded subagent lineup, but it must not spawn subagents unless the current
user message explicitly approves subagents or parallel agent work.

Limits:
- This block is durable guidance, not a Codex permission change.
- It does not change sandbox, approval, filesystem, network, model, or host
  policy.
- Current user instructions, closer AGENTS.md or AGENTS.override.md files, and
  any "no subagents" instruction override this block.
- DeepPlan remains planning-only; subagents gather evidence and do not own
  final planning decisions.
- Do not use recursive delegation, CSV fan-out, role padding, or duplicate
  reviewers."""
    elif mode == "allow-readonly-subagents":
        body = """## DeepPlan Subagent Policy

Mode: allow-readonly-subagents

This repository gives DeepPlan a standing explicit request to use direct
read-only/explorer subagents during Full-path planning when there are two to
four independent read-heavy evidence domains that could change the main plan,
backup, switch condition, validation gate, or readiness.

Limits:
- This block authorizes only DeepPlan's decision to spawn bounded read-heavy
  subagents; it does not authorize write-heavy worker subagents during DeepPlan
  planning.
- This block is durable guidance, not a Codex permission change.
- It does not change sandbox, approval, filesystem, network, model, or host
  policy.
- Current user instructions, closer AGENTS.md or AGENTS.override.md files, and
  any "no subagents" instruction override this block.
- The parent agent must integrate subagent findings and close completed agents.
- Do not use recursive delegation, CSV fan-out, role padding, or duplicate
  reviewers."""
    else:
        raise ConfigError(f"cannot render managed block for mode {mode!r}")

    return f"{START_MARKER}\n{body}\n{END_MARKER}"


def print_dry_run(
    agents_path: Path,
    mode: str,
    current_content: str,
    next_content: str,
) -> None:
    if current_content == next_content:
        print(f"Dry run: no changes needed for {agents_path}")
        return
    print(f"Dry run: would update {agents_path} with DeepPlan subagent mode: {mode}")
    print("Pass --write to apply this change.")


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as handle:
        handle.write(content)
        temp_path = Path(handle.name)
    temp_path.replace(path)


class ConfigError(Exception):
    """Raised when AGENTS.md cannot be updated safely."""


if __name__ == "__main__":
    raise SystemExit(main())
