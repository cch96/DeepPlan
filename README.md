# DeepPlan

DeepPlan is a lightweight planning workflow for AI coding agents. It helps an
agent improve a first-draft plan before implementation by grounding the plan in
evidence, comparing alternatives, eliminating weaker options, and producing a
validation-ready final plan.

DeepPlan is not an execution framework, project manager, or durable state
system. It is a pre-execution quality gate.

## What It Does

- Grounds a plan in available code, docs, logs, tests, and user constraints.
- Reuses existing candidate approaches when another planning workflow already
  produced them.
- Adds distinct candidates only when the current plan has one option or shallow
  variants of the same option.
- Runs structured critique for architecture, implementation, tests, risk, and
  simplicity.
- Converges full-path reviews to one main plan, one backup plan, validation
  steps, and known residual risks.
- Splits oversized work into execution-ready slices.

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

If the current surface supports subagents and policy permits them, DeepPlan can
use them for full-path plans with independent read-heavy critique domains. It
does not require subagents and should continue with solo critique when optional
integrations are unavailable.

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
validation gate, and residual-risk review.

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
git diff --check
```

If your agent environment provides plugin or skill validators, run them against
the plugin root and `skills/deepplan` before publishing.

The skill itself should stay compact. If examples or agent-specific prompt
packs grow large, move them into `skills/deepplan/references/` and link to them
from `SKILL.md`.
