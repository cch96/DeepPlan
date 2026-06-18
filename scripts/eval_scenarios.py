#!/usr/bin/env python3
"""Behavioral eval for the DeepPlan skill.

Runs each pressure scenario in
``skills/deepplan/references/depth-and-pressure.md`` against a fresh model that
is given ONLY the skill text (SKILL.md + references), then uses an LLM judge to
score the response against the scenario's Expected / Failure. Reports a
per-scenario pass-rate and an overall result.

This complements ``scripts/validate_deepplan_plugin.py``, which only checks
structure/metadata. This script checks whether the skill TEXT actually drives
behavior -- the writing-skills RED/GREEN method, automated.

It is an OPTIONAL maintenance/test tool and is NOT a runtime dependency of the
plugin. It needs the ``anthropic`` package and ``ANTHROPIC_API_KEY``.

Note: this is an LLM behavioral eval, not a deterministic unit test. Use
``--runs N`` to sample each scenario several times and read the pass-rate.

Usage:
  python3 scripts/eval_scenarios.py --dry-run                 # parse only, no API/key
  python3 scripts/eval_scenarios.py                           # all scenarios, 1 run each
  python3 scripts/eval_scenarios.py --scenarios 1,2,4,30,31,33
  python3 scripts/eval_scenarios.py --runs 3 --threshold 0.8
  python3 scripts/eval_scenarios.py --model claude-sonnet-4-6 --judge-model claude-opus-4-8
  python3 scripts/eval_scenarios.py --show                    # also print each agent response
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "deepplan"
SCENARIO_FILE = SKILL_DIR / "references" / "depth-and-pressure.md"
SKILL_FILES = (
    SKILL_DIR / "SKILL.md",
    SKILL_DIR / "references" / "depth-and-pressure.md",
    SKILL_DIR / "references" / "subagent-opt-in.md",
    SKILL_DIR / "references" / "host-integration.md",
)

DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_JUDGE_MODEL = "claude-opus-4-8"
GATE_MANIFEST = ROOT / "scripts" / "deepplan_gate_cases.json"

HEADING_RE = re.compile(r"^### (\d+)\.\s+(.*)$")
FIELD_RE = re.compile(r"^(Trigger|Expected|Failure):\s*(.*)$")

PLANNER_SYSTEM = """You operate strictly under the DeepPlan skill provided below; follow it exactly.
You will be given ONE hypothetical situation. Treat it as self-contained: do not
perform real work, do not claim to have run tools, and reason only from the skill
plus the situation (including any grounding result the situation states).

Respond exactly as the DeepPlan skill directs for this situation — in the shape
and at the length the skill prescribes. Do not add structure the skill does not
ask for.

===== DEEPPLAN SKILL =====
{skill}
"""

JUDGE_SYSTEM = """You are a strict evaluator of an AI planning skill's behavior.
Given a scenario's Expected behavior and its Failure mode, and the agent's
response, decide whether the response satisfies the Expected behavior AND avoids
the Failure mode. Be skeptical: if it only partially complies, that is a fail.
Record your decision by calling the record_verdict tool."""

# Forcing this single tool (tool_choice below) makes the judge return a
# schema-shaped {pass, reason} object instead of free-text JSON we have to
# hand-parse, removing the fragile first-`{` / last-`}` extraction.
VERDICT_TOOL = {
    "name": "record_verdict",
    "description": (
        "Record whether the agent response satisfies the Expected behavior "
        "and avoids the Failure mode."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "pass": {
                "type": "boolean",
                "description": "true only if Expected is satisfied AND Failure is avoided",
            },
            "reason": {"type": "string", "description": "<= 240 char justification"},
        },
        "required": ["pass", "reason"],
        "additionalProperties": False,
    },
}


def parse_scenarios(text: str) -> list[dict]:
    """Parse `### N. Title` blocks with Trigger/Expected/Failure fields."""
    scenarios: list[dict] = []
    cur: dict | None = None
    field: str | None = None
    for line in text.splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            if cur:
                scenarios.append(cur)
            cur = {
                "num": int(heading.group(1)),
                "title": heading.group(2).strip(),
                "trigger": "",
                "expected": "",
                "failure": "",
            }
            field = None
            continue
        if cur is None:
            continue
        if line.startswith("## ") or line.startswith("### "):
            scenarios.append(cur)
            cur, field = None, None
            continue
        match = FIELD_RE.match(line)
        if match:
            field = match.group(1).lower()
            cur[field] = match.group(2).strip()
        elif not line.strip():
            field = None
        elif field:
            cur[field] = (cur[field] + " " + line.strip()).strip()
    if cur:
        scenarios.append(cur)
    complete = []
    for s in scenarios:
        if s["trigger"] and s["expected"] and s["failure"]:
            complete.append(s)
        else:
            missing = ", ".join(
                field for field in ("trigger", "expected", "failure") if not s[field]
            )
            print(
                f"WARNING: scenario #{s['num']} {s['title']!r} is missing "
                f"{missing}; skipped. Fix its heading/fields in "
                f"depth-and-pressure.md so the eval covers it.",
                file=sys.stderr,
            )
    return complete


def build_skill_context() -> str:
    parts = []
    for path in SKILL_FILES:
        text = path.read_text(encoding="utf-8")
        if path.name == "depth-and-pressure.md":
            # Strip the numbered pressure-scenario answer-keys (their
            # Trigger/Expected/Failure) so the planner under test never receives
            # the answers it is being judged against -- otherwise the eval mostly
            # measures whether the model can match a trigger to its documented
            # scenario. Keep the guidance above them (domain lenses, dependency
            # chains, self-optimization classification, number-only index).
            text = re.split(r"\n### \d+\.\s", text, maxsplit=1)[0]
        parts.append(f"----- {path.relative_to(ROOT)} -----\n{text}")
    return "\n\n".join(parts)


def extract_verdict(message) -> dict:
    """Read the forced record_verdict tool call. Defaults to a *fail* (never a
    silent pass) if the judge somehow returns no verdict."""
    for block in message.content:
        if getattr(block, "type", None) == "tool_use" and block.name == "record_verdict":
            data = block.input or {}
            return {
                "pass": bool(data.get("pass", False)),
                "reason": str(data.get("reason", ""))[:240],
            }
    return {"pass": False, "reason": "judge returned no record_verdict tool call"}


def load_scenario_floors() -> dict:
    """Per-scenario pass-rate floors from the committed gate manifest (e.g. S34
    ceremony). Returns {scenario_num_str: float}. Empty if the manifest is absent."""
    try:
        data = json.loads(GATE_MANIFEST.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    floors = data.get("abstract_eval", {}).get("per_scenario_floor", {})
    return {str(k): float(v) for k, v in floors.items()}


def main() -> int:
    ap = argparse.ArgumentParser(description="Behavioral eval for the DeepPlan skill.")
    ap.add_argument("--scenarios", help="comma-separated scenario numbers (default: all)")
    ap.add_argument("--runs", type=int, default=1, help="samples per scenario (default 1)")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"planner model (default {DEFAULT_MODEL})")
    ap.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL, help=f"judge model (default {DEFAULT_JUDGE_MODEL})")
    ap.add_argument("--threshold", type=float, default=1.0, help="min overall pass-rate for exit 0 (default 1.0)")
    ap.add_argument("--show", action="store_true", help="print each agent response")
    ap.add_argument("--dry-run", action="store_true", help="parse scenarios and exit (no API calls)")
    args = ap.parse_args()

    all_scenarios = parse_scenarios(SCENARIO_FILE.read_text(encoding="utf-8"))
    if args.scenarios:
        wanted = {int(x) for x in args.scenarios.split(",") if x.strip()}
        scenarios = [s for s in all_scenarios if s["num"] in wanted]
    else:
        scenarios = all_scenarios

    if not scenarios:
        print("No scenarios matched.", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"Parsed {len(all_scenarios)} scenarios; selected {len(scenarios)}:")
        for s in scenarios:
            print(f"  #{s['num']:>2} {s['title']}")
        return 0

    try:
        from anthropic import Anthropic
    except ImportError:
        print("The 'anthropic' package is required: pip install anthropic", file=sys.stderr)
        return 2
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        return 2

    client = Anthropic()
    planner_system = PLANNER_SYSTEM.format(skill=build_skill_context())

    results = []
    for s in scenarios:
        passes = 0
        last_reason = ""
        for _ in range(args.runs):
            plan = client.messages.create(
                model=args.model,
                max_tokens=2000,
                system=planner_system,
                messages=[{"role": "user", "content": f"SITUATION: {s['trigger']}"}],
            ).content[0].text
            if args.show:
                print(f"\n----- #{s['num']} {s['title']} -----\n{plan}\n")
            verdict_message = client.messages.create(
                model=args.judge_model,
                max_tokens=400,
                system=JUDGE_SYSTEM,
                tools=[VERDICT_TOOL],
                tool_choice={"type": "tool", "name": "record_verdict"},
                messages=[{
                    "role": "user",
                    "content": (
                        f"Expected: {s['expected']}\nFailure: {s['failure']}\n\n"
                        f"Agent response:\n{plan}"
                    ),
                }],
            )
            verdict = extract_verdict(verdict_message)
            if verdict.get("pass"):
                passes += 1
            else:
                last_reason = verdict.get("reason", "")
        rate = passes / args.runs
        results.append((s, rate, last_reason))
        mark = "PASS" if rate >= 0.5 else "FAIL"
        suffix = f"  (rate {passes}/{args.runs})" if args.runs > 1 else ""
        note = "" if rate >= 0.5 else f"  -- {last_reason}"
        print(f"[{mark}] #{s['num']:>2} {s['title']}{suffix}{note}")

    overall = sum(r for _, r, _ in results) / len(results)
    passed = sum(1 for _, r, _ in results if r >= 0.5)
    print(f"\n{passed}/{len(results)} scenarios passed; mean pass-rate {overall:.2f}")

    # Per-scenario floors from the committed gate manifest (e.g. S34 ceremony):
    # a single target scenario must not be able to fail while the mean stays green.
    floors = load_scenario_floors()
    floor_failures = [
        (s["num"], rate, floors[str(s["num"])])
        for s, rate, _ in results
        if str(s["num"]) in floors and rate < floors[str(s["num"])]
    ]
    for num, rate, floor in floor_failures:
        print(f"FLOOR FAIL #{num}: rate {rate:.2f} < floor {floor:.2f}", file=sys.stderr)

    return 0 if overall >= args.threshold and not floor_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
