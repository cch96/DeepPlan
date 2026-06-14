# DeepPlan

DeepPlan is a pre-execution planning gate for AI coding agents. It turns rough
requests, draft plans, or competing approaches into one evidence-backed plan
with validation before implementation starts.

DeepPlan is not an execution framework, project manager, or durable state
system.

## What It Does

- Grounds plans in local code, docs, tests, logs, manifests, and user
  constraints.
- Scales evidence gathering: small targets can be read fully; large repositories
  are inventoried first and read selectively.
- Reuses existing candidate approaches when another workflow already produced
  them.
- Adds distinct candidates only when coverage is missing.
- Critiques risk, validation, reversibility, maintainability, and simplicity.
- Names the material optimization axis for broad "improve this" requests before
  planning source changes.
- Returns a no-source-edit plan when repeated optimization has no material
  behavior, validation, metadata, or pressure-scenario delta.
- Converges Full path reviews to one main plan, one backup, a switch condition,
  and concrete validation gates.
- Applies an actionability gate so `ready` plans do not leave hidden decisions,
  vague test commands, or ambiguous fallbacks to the implementer.
- Preserves host wrappers such as Codex Plan Mode `<proposed_plan>`.
- Keeps planning side-effect free; edits, commits, cachebuster updates,
  reinstalls, and durable artifacts belong to execution handoff.

## When To Use

Use DeepPlan for complex plans, architecture changes, migrations, unclear root
cause work, multi-module changes, high-regression work, long-running automation,
workflow/process/skill/plugin/policy changes, broad optimization requests, or
explicit deep/no-omissions/converged planning requests.

Skip it for trivial syntax fixes, one-field edits, simple path/config changes,
or failures with verified root cause and an obvious patch.

## Optional Integrations

DeepPlan has no hard dependencies. Superpowers, subagents, OpenAI Docs MCP, and
web/docs lookup are optional evidence sources only:

- Reuse upstream brainstorming approaches instead of generating duplicate
  candidates.
- Use subagents only when the user explicitly requests them and the host supports
  independent read-heavy critique domains.
- Use official OpenAI/Codex docs only when current external contracts can change
  the plan. If a needed contract remains unverified, lower readiness to
  `ready_with_assumptions` or `not_ready`.

## Usage

Codex prompt:

```text
Use $deepplan to converge this plan before execution.
```

Generic prompt:

```text
Invoke the deepplan skill to compare alternatives, critique risks, and converge
this plan before execution.
```

Broad optimization prompt:

```text
Use $deepplan to optimize this workflow/skill/plugin. Ground first, name the
optimization axis, then converge the plan before source edits. Return no-edit
when there is no behavior delta.
```

## Repository Layout

```text
.codex-plugin/plugin.json
.claude-plugin/plugin.json
DEPENDENCIES.md
skills/deepplan/
  SKILL.md
  agents/openai.yaml
  references/depth-and-pressure.md
```

## Maintenance

Validate metadata after edits:

```bash
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 -m json.tool .claude-plugin/plugin.json >/dev/null
python3 -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('skills/deepplan/agents/openai.yaml').read_text())"
python3 /home/ubuntu/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
rg -n "optimization axis|workflow/process/skill/plugin optimization|broad optimization|actionability|no_material_delta|no-source-edit" \
  README.md .codex-plugin/plugin.json skills/deepplan/SKILL.md \
  skills/deepplan/agents/openai.yaml skills/deepplan/references/depth-and-pressure.md
git diff --check
```

For local Codex iteration, validate source first, then refresh through the
plugin-creator helper and confirmed marketplace. In this workspace the
marketplace is `deepplan-local`:

```bash
python3 /home/ubuntu/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py .
codex plugin add deepplan@deepplan-local
```

Do not hand-edit marketplace files to refresh the installed local plugin. Start
a new thread/session after reinstalling to test refreshed behavior.

Keep `SKILL.md` compact. Move large examples or prompt packs into
`skills/deepplan/references/` and link to them.
