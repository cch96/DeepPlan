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
- Selects relevant lens-roles for subagents only after an explicit user request,
  a permitted repository opt-in, or a first-use prompt confirms current-task
  consent for independent read-heavy critique domains.
- Can add explicit repository `AGENTS.md` opt-in guidance for suggest-only or
  read-only subagent use; install and reinstall never add that guidance by
  themselves.
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
- Use subagents only when the user explicitly requests them, the active
  repository has a DeepPlan-managed `AGENTS.md` opt-in block, or a first-use
  prompt gets current-task consent after grounding confirms a Full-path task with
  independent read-heavy critique domains. The prompt choices include
  `Use for this task`, `Use now and enable repo`, and `Do not use`; unsupported,
  unanswered, or declined prompts fall back to solo critique.
- `Use now and enable repo` adds a post-DeepPlan handoff to run
  `configure_subagents.py --mode allow-readonly-subagents --write`; install,
  update, and reinstall actions never authorize subagents by themselves.
- Use official OpenAI/Codex docs only when current external contracts can change
  the plan. If a needed contract remains unverified, lower readiness to
  `ready_with_assumptions` or `not_ready`.
- Codex Goal Mode (`/goal`) is an optional host-specific execution handoff for
  long tasks with clear completion criteria and validation. Claude and
  non-Codex hosts receive the same handoff as plain instructions.

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

Configure repository subagent guidance:

```bash
python3 scripts/configure_subagents.py --repo /path/to/repo --mode suggest-only
python3 scripts/configure_subagents.py --repo /path/to/repo --mode suggest-only --write
python3 scripts/configure_subagents.py --repo /path/to/repo --mode allow-readonly-subagents --write
python3 scripts/configure_subagents.py --repo /path/to/repo --mode remove --write
```

The script defaults to dry-run. It writes only a marker-delimited
DeepPlan-managed block in the target repo's `AGENTS.md`, refuses ambiguous
marker state, and refuses to write root `AGENTS.md` when a non-empty root
`AGENTS.override.md` could shadow it. Start a new Codex session/thread before
expecting changed `AGENTS.md` guidance to take effect.

## Repository Layout

```text
.codex-plugin/plugin.json
.claude-plugin/plugin.json
DEPENDENCIES.md
scripts/
  configure_subagents.py
  validate_deepplan_plugin.py
skills/deepplan/
  SKILL.md
  agents/openai.yaml
  references/depth-and-pressure.md
  references/subagent-opt-in.md
```

## Maintenance

Validate metadata after edits:

```bash
python3 scripts/validate_deepplan_plugin.py
```

For local Codex iteration, validate source first, then refresh through the
plugin-creator helper and confirmed marketplace. Read the marketplace name from
the personal marketplace file instead of hard-coding it:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
MARKETPLACE="$(python3 "$CODEX_HOME/skills/.system/plugin-creator/scripts/read_marketplace_name.py")"
python3 "$CODEX_HOME/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py" .
codex plugin add "deepplan@$MARKETPLACE"
```

Do not hand-edit marketplace files to refresh the installed local plugin. Start
a new thread/session after reinstalling to test refreshed behavior.

Keep `SKILL.md` compact. Move large examples or prompt packs into
`skills/deepplan/references/` and link to them.
