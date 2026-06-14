# Depth And Pressure Reference

Use this reference when DeepPlan is on the full path, when planning
skill/process/policy changes, or when dependency chains make execution order
fragile.

## Domain Lenses

Use the general Depth Gate first, then weight risks by domain:

- **Database/migration**: compatibility, rollback, data validation, idempotency,
  mixed-version reads/writes, and backfill recovery.
- **Security/privacy/payment/compliance**: default full path; require threat,
  permission, secret, audit, and failure-cost review.
- **AI/research/strategy**: evidence quality, metric pollution, baselines,
  reproducibility, sampling bias, and claim boundaries.
- **UI/product**: user flow, empty/loading/error states, responsive behavior,
  accessibility, and visual acceptance evidence.
- **Operations/automation**: stop conditions, retries, idempotency, logs,
  alerts, manual takeover, and recovery after partial execution.
- **Skill/process/policy**: trigger precision, future agent behavior,
  loopholes, optional dependency handling, final output shape, and pressure
  scenarios.

## Dependency Chains

If the plan depends on ordered steps, external systems, humans, model calls,
timers, migrations, or irreversible state, output a dependency map before
execution slices. Each dependency-heavy slice needs objective, inputs,
preconditions, validation, fallback, owner/actor, and stop condition.

Prefer fewer slices when validation is cheap and rollback is easy. Split more
aggressively when failure leaves durable state, burns money/time, blocks
operators, or makes later evidence ambiguous.

## Pressure Scenarios

Each scenario is a documentation test. A DeepPlan run passes only if the
expected behavior appears in the plan or final answer.

### 1. Self-Review Must Not Use Light Path

Prompt: "Use DeepPlan to improve DeepPlan itself; make it no-omissions."

Expected behavior: full path, candidate comparison, pressure scenarios, and a
validation gate.

Failure condition: the agent treats it as a simple wording edit or omits
candidate comparison.

### 2. Light Path Must Escalate

Prompt: "Small config fix." During grounding, evidence shows a public API
contract and migration are involved.

Expected behavior: upgrade to full path and explain the new trigger.

Failure condition: the agent continues with one critique pass because the
initial request sounded small.

### 3. Optional Integrations Stay Optional

Prompt: "Converge this plan, but no subagents are available."

Expected behavior: solo full-path critique continues; subagents are not treated
as required.

Failure condition: the agent blocks or weakens the plan because optional
integrations are unavailable.

### 4. Dependency Chain Must Be Mapped

Prompt: "Plan a long-running automation with model calls, queue work, and manual
approval."

Expected behavior: dependency map plus slices with validation, fallback, and
stop conditions.

Failure condition: the agent gives one linear checklist without ownership,
preconditions, or recovery points.

### 5. Verification Gate Must Be Concrete

Prompt: "Choose the elegant refactor for this architecture change."

Expected behavior: validation includes current-risk evidence, exact
post-change checks, expected results, and next inspection if validation fails.

Failure condition: the agent says "run tests" without naming what proves the
plan or what to inspect on failure.

### 6. Over-Planning Must Be Rejected

Prompt: "Rename one local variable in a private helper."

Expected behavior: skip DeepPlan or use light path with a minimal validation
gate.

Failure condition: the agent creates multiple candidates, subagents, or a
durable design artifact without risk.
