# DeepPlan

DeepPlan is a lightweight planning workflow for AI coding agents. It helps an
agent improve a first-draft plan before implementation by grounding the plan in
evidence, comparing alternatives, eliminating weaker options, and producing a
validation-ready final plan.

DeepPlan is not an execution framework, project manager, or durable state
system. It is a pre-execution quality gate.

## What It Does

- Grounds a plan in available code, docs, logs, tests, and user constraints.
- Scopes evidence gathering: small bounded targets can be read fully, while
  large repositories should be inventoried first and read selectively.
- Reuses existing candidate approaches when another planning workflow already
  produced them.
- Adds distinct candidates only when the current plan has one option or shallow
  variants of the same option.
- Runs structured critique for architecture, implementation, tests, risk, and
  simplicity.
- Converges full-path reviews to one main plan, one backup plan, validation
  steps, and known residual risks.
- Splits oversized work into execution-ready slices.
- Preserves host-specific output wrappers, such as Codex Plan Mode
  `<proposed_plan>`, while keeping DeepPlan readiness and validation details
  inside that wrapper.
- Keeps planning side-effect free: implementation, commits, plugin cachebuster
  updates, reinstalls, and durable artifacts belong to the execution handoff
  after the DeepPlan output is settled.

## When To Use

Use DeepPlan for complex plans, architecture changes, migrations, unclear root
cause work, multi-module changes, high regression risk, long-running
automation, or when you want the agent to converge on an evidence-backed plan
before execution.

Skip DeepPlan for trivial syntax fixes, one-field edits, simple path/config
changes, or failures with an already verified root cause and obvious patch.

## Optional Integrations

DeepPlan has no hard dependencies.

If another workflow, such as Superpowers brainstorming, already produced 2-3
approaches, DeepPlan treats them as the candidate pool and audits their
coverage instead of generating duplicate alternatives.

If the user explicitly requests subagents or parallel agent work, and the current
surface supports them, DeepPlan can use them for full-path plans with independent
read-heavy critique domains. It does not require subagents and should continue
with solo critique when subagents are unavailable, unrequested, or inappropriate.

For OpenAI, Codex, skill, plugin, API, or SDK contract changes, DeepPlan should
use official OpenAI documentation or configured docs tools before broader web
lookup. If those sources cannot verify a contract that could change the plan,
the final readiness should be `ready_with_assumptions` or `not_ready`.

## Execution Handoff

DeepPlan is a planning phase, not an implementation phase. If a user asks the
agent to use DeepPlan and then implement, the agent should first settle the
DeepPlan output, then leave the DeepPlan phase and apply the host's normal
editing and verification rules.

## Usage

Install DeepPlan as a Codex or Claude plugin, then invoke the skill before
implementation using the command or UI for your agent surface.

Codex prompt:

```text
Use $deepplan to converge this plan before execution.
```

Generic prompt:

```text
Invoke the deepplan skill to converge this plan before execution.
```

Requests for deep, no-omissions, converged planning, or skill/process/policy
improvements should use the full path: candidate comparison, critique,
validation gate, and residual-risk review. DeepPlan self-review and nontrivial
plugin or workflow-process changes also use the full path even when the source
patch is likely to be small.

DeepPlan does not require websearch by default. Use official or primary
external sources only when current external contracts, APIs, SDK/tool behavior,
package versions, laws, pricing, releases, or explicit user instructions can
change the plan.

Useful prompts:

```text
Use $deepplan. I think this plan may be too shallow; compare alternatives and
keep only one main plan and one backup.
```

```text
Use $deepplan. First determine whether the existing approaches are distinct
enough. Reuse them if they are; only add candidates if coverage is missing.
```

## Repository Layout

```text
.codex-plugin/plugin.json
.claude-plugin/plugin.json
DEPENDENCIES.md
skills/deepplan/
  SKILL.md
  agents/openai.yaml  # Codex UI metadata
  references/depth-and-pressure.md
```

## Maintenance

Validate plugin metadata after edits:

```bash
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 -m json.tool .claude-plugin/plugin.json >/dev/null
python3 -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('skills/deepplan/agents/openai.yaml').read_text())"
python3 <plugin-creator>/scripts/validate_plugin.py .
git diff --check
```

If your agent environment provides plugin or skill validators, run them against
the plugin root and `skills/deepplan` before publishing.

For local Codex plugin iteration, validate source edits first, then update the
Codex cachebuster and reinstall from the confirmed local marketplace. In this
workspace the local marketplace is `deepplan-local`; other checkouts should read
the marketplace name from their marketplace file before reinstalling. From the
plugin root, using the plugin-creator helper:

```bash
python3 <plugin-creator>/scripts/update_plugin_cachebuster.py .
codex plugin add deepplan@deepplan-local
```

Do not hand-edit marketplace files merely to refresh an installed local plugin.
After reinstalling, start a new thread/session to test the refreshed skill.

The skill itself should stay compact. If examples or agent-specific prompt
packs grow large, move them into `skills/deepplan/references/` and link to them
from `SKILL.md`.
