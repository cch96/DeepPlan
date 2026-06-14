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

### 4. Subagent Discretion Is Agent-Owned

Prompt: "Use DeepPlan on a full-path architecture plan with independent API,
database, and validation risks."

Expected behavior: the agent decides whether subagents would improve independent
read-heavy critique, then either uses them or records why solo critique is
enough.

Failure condition: the agent asks for permission by default, treats subagents as
required, or uses them for non-independent opinions.

### 5. Dependency Chain Must Be Mapped

Prompt: "Plan a long-running automation with model calls, queue work, and manual
approval."

Expected behavior: dependency map plus slices with validation, fallback, and
stop conditions.

Failure condition: the agent gives one linear checklist without ownership,
preconditions, or recovery points.

### 6. Verification Gate Must Be Concrete

Prompt: "Choose the elegant refactor for this architecture change."

Expected behavior: validation includes current-risk evidence, exact
post-change checks, expected results, and next inspection if validation fails.

Failure condition: the agent says "run tests" without naming what proves the
plan or what to inspect on failure.

### 7. Root Cause Comes Before Fix Candidates

Prompt: "DeepPlan this regression; I have three possible fixes but no confirmed
root cause."

Expected behavior: root-cause hypotheses, evidence, and smallest validations are
listed before fix candidates are compared.

Failure condition: the agent picks a fix candidate first and backfills a root
cause story afterward.

### 8. Alternatives Stay In Context By Default

Prompt: "Compare three implementation options and converge the plan."

Expected behavior: alternatives and eliminated reasons appear in the final
answer or plan; no temporary or tracked alternative file is created unless the
user asks for a handoff/audit artifact or context constraints require scratch.

Failure condition: the agent creates files just to hold candidates for a normal
single-agent planning turn.

### 9. Over-Planning Must Be Rejected

Prompt: "Rename one local variable in a private helper."

Expected behavior: skip DeepPlan or use light path with a minimal validation
gate.

Failure condition: the agent creates multiple candidates, subagents, or a
durable design artifact without risk.

### 10. Missing Draft Plan Must Not Block Grounding

Prompt: "Use DeepPlan to optimize this plugin."

Expected behavior: inspect available files, infer objective, scope, and success
criteria, then build candidates from evidence before asking for preferences.

Failure condition: the agent blocks until the user supplies a full draft plan or
invents an ungrounded plan without inspection.

### 11. Readiness Must Match Evidence

Prompt: "Finalize this high-risk plan; one external dependency is still
unverified."

Expected behavior: return `ready_with_assumptions` or `not_ready`, name the
missing evidence, and include the safest validation or partial plan.

Failure condition: the agent labels the plan `ready` while an unverified
dependency could change the chosen approach.

### 12. Host Output Wrapper Must Preserve DeepPlan Content

Prompt: "Use DeepPlan in a host that requires a final plan wrapper."

Expected behavior: follow the host wrapper while preserving objective,
candidate comparison when required, final plan, validation gate, and readiness.

Failure condition: the wrapper output drops DeepPlan's readiness, backup/switch
condition, or candidate elimination details.

### 13. Execution Handoff Must Be Explicit

Prompt: "Use DeepPlan to optimize this plugin, then implement the changes."

Expected behavior: the agent completes or settles the DeepPlan planning output
first, then treats implementation as a separate phase using the host's normal
editing and verification rules.

Failure condition: the agent edits files while still claiming to be inside the
DeepPlan planning phase, or skips the planning output because implementation was
also requested.
