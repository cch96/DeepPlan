---
name: deepplan
description: Use when refining complex plans, architecture changes, migrations, unclear root-cause fixes, high-risk approaches, or explicit best/elegant/no-omissions/self-review/converged planning requests before execution.
---

# DeepPlan

Planning gate: turn a first plan into an evidence-backed plan. Do not implement
while active.

## Boundaries

- Planning only: no repo-tracked edits, formatters, commits, deploys,
  migrations, durable external writes, or side-effectful execution.
- Read code, docs, configs, logs, schemas, tests, and prior plans; run checks
  only to clarify evidence without changing durable state. Cache
  or build artifacts are acceptable only when the host permits them.
- Ask only for preferences or tradeoffs that cannot be discovered.
- Respect host and user constraints for permissions, cost, privacy, tools, and
  side effects; do not restate platform policy inside the plan.
- Oversized work becomes execution-ready slices with objective, scope,
  acceptance criteria, validation, dependencies, and stop condition.

## When To Use

Use for architecture/module-boundary changes; migrations, compatibility, or
rollout decisions; unclear root cause or multiple fixes; multi-module or
high-regression work; long-running/expensive operations; and best,
elegant, no-omissions, self-review, or converged-plan requests.

Skip for trivial syntax fixes, one-field edits, simple path/config updates, or
a failure with verified root cause and obvious patch.

## Depth Gate

Full path when any risk is high, or two are medium: uncertainty, blast radius,
irreversibility, validation difficulty, failure cost, or dependency-chain
length. Full path also applies when the user asks for deep, best, elegant,
no-omissions, converged, or self-review planning; or for skill/process/policy
design beyond typo or manifest fixes.

Light path is allowed only when scope is small, facts are clear, validation is
obvious, no public API/schema/data/deploy/durable-state risk exists, and the
user did not request deep/no-omissions/converged planning. If light path finds a
new evidence gap, candidate category, medium/high risk, unclear validation, or
long dependency chain, upgrade to full path.

For domain lenses, dependency-chain handling, and pressure scenarios, read
`references/depth-and-pressure.md` for full-path, skill/process/policy, or
dependency-heavy plans.

## Path Requirements

- Light path: ground facts, run one focused critique pass, produce a concrete
  validation gate, and name the next inspection if validation fails.
- Full path: compare candidates, critique, eliminate weaker options, choose one
  main plan and one backup plan, define the switch condition, run a final fatal
  risk check, and produce readiness.

## Workflow

### 1. Ground The Plan

- Identify objective, constraints, success criteria, and scope.
- Inspect relevant code, docs, tests, logs, configs, or provided plans.
- Separate confirmed facts from guesses.

### 2. Root-Cause Mode For Bugs Or Regressions

Run this before fix candidates when the task is a bug, regression, or unclear
failure. Skip it only when the root cause is already verified.

- List 3-5 plausible root-cause hypotheses.
- For each, include supporting and disconfirming evidence, smallest validation,
  and smallest fix if true.
- Mark unsupported claims as guesses.
- Eliminate at least two alternative root causes before `ready`, or return
  `ready_with_assumptions` / `not_ready` with the missing evidence.

### 3. Build The Candidate Pool

- Reuse existing 2-3 real approaches; do not duplicate covered tradeoffs.
- Add candidates only for one option or shallow variants of one.
- Defaults when needed: minimal fix, long-term design, compromise architecture.
- Each candidate needs hypothesis, changes, validation, risks, and elimination
  condition.

Keep candidates and eliminated alternatives in conversation by default. Do not
create temporary or tracked files for alternatives unless the user asks for a
durable handoff/audit artifact, host context is too small, or multiple agents
need a shared scratch artifact. If needed, use a runtime-local or `/tmp` path
and summarize it in the final output.

### 4. Critique In Rounds

Run one critique round by default. Run a second when the first finds high or
medium risk, a new candidate category, an evidence gap, or an unresolved
tradeoff. Run a third only for a new high-risk blocker.

Always cover architecture, implementation, tests, risk, and simplicity. Add
security/privacy, performance/cost, rollout, compatibility, product, or domain
evidence only when relevant.

### 5. Optional Subagents

Use subagents at your discretion on the full path when the host supports them
and the task has 2+ independent, read-heavy critique domains whose results can
be merged without shared edits.

Do not use subagents for light path, trivial work, obvious patches, or when the
main blocker requires one coherent system-level judgment. If subagents are
unavailable or disallowed by host/user constraints, continue with solo
critique. Summarize must-change, optional improvement, evidence, and readiness
verdict.

### 6. Tournament And Elimination

- Compare candidates on root-cause coverage, risk, testability,
  maintainability, simplicity, and elimination conditions.
- Eliminate weaker candidates and state why they are not chosen now.
- Full path ends with exactly one main plan and one backup plan, plus the switch
  condition. Final output must preserve candidate comparison.
- Light path may use validation failure-next-step as the fallback.
- For complex/high-risk plans, run one final adversarial review for fatal
  issues, evidence gaps, hidden regressions, and smaller equivalent plans. If a
  new high or medium issue appears, run one more critique round, then finalize
  unless the user asks to continue.

### 7. Verification Gate

- Evidence for the current issue or risk before the change.
- Command, test, log, inspection, or reproduction that should pass after.
- Expected result for each validation step.
- Next inspection if validation fails.

### 8. Stop Rules

Stop only when a critique round is complete, the latest round adds no high or
medium risk, no materially different candidate remains, continuing would not add
evidence, the main plan and validation gate are ready, and the full path has a
backup plus switch condition. Light path needs a validation-failure fallback.

Do not stop because "the agent has no more feedback." If reflection would not
create evidence, switch to tests, logs, minimal reproduction, or inspection.

## Pressure Checks

For skill, process, or policy reviews, keep only changes that alter future agent
behavior; remove explanation-only wording unless it prevents misuse. Check:

- missed trigger: would the agent load this skill for the right request?
- premature execution: could the agent start editing while planning?
- missing validation: are evidence, expected results, and failure inspection
  defined?
- optional dependency misuse: could integrations be treated as required?
- over-planning: would trivial work be slowed down without reducing risk?
- context clutter: is this rule correct but unnecessary for DeepPlan's planning
  responsibility?

## Final Output

Always include objective, final main plan, validation gate, and readiness
(`ready`, `ready_with_assumptions`, or `not_ready`).

Add only when relevant: facts/guesses, root-cause hypotheses, eliminated
alternatives, candidate comparison, backup/switch condition, risks, regression
points, execution-ready slices, and convergence log.

For full path, include candidate comparison, eliminated alternatives, one backup
plan, and the switch condition. For light path, include the validation-failure
fallback instead of a separate backup plan.

If the host requires a final-plan wrapper or format, follow it and place
DeepPlan sections inside.

If not ready, list unresolved decisions and the safest partial plan.
