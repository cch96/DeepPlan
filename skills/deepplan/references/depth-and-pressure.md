# Depth And Pressure Reference

Use this reference for Full path plans, workflow/process/skill/plugin/policy
changes, or fragile dependency chains.

## Domain Lenses

Use the general Depth Gate first, then weight risks by domain:

- **Database/migration**: compatibility, rollback, data validation, idempotency,
  mixed-version reads/writes, and backfill recovery.
- **Security/privacy/payment/compliance**: default Full path; require threat,
  permission, secret, audit, and failure-cost review.
- **AI/research/strategy**: evidence quality, metric pollution, baselines,
  reproducibility, sampling bias, and claim boundaries.
- **UI/product**: user flow, empty/loading/error states, responsive behavior,
  accessibility, and visual acceptance evidence.
- **Operations/automation**: stop conditions, retries, idempotency, logs,
  alerts, manual takeover, and recovery after partial execution.
- **Workflow/process/skill/plugin/policy**: trigger precision, future agent
  behavior, loopholes, optional dependencies, output shape, and pressure
  scenarios.

## Dependency Chains

If a plan depends on ordered steps, external systems, humans, model calls,
timers, migrations, or irreversible state, output a dependency map before
execution slices. Each dependency-heavy slice needs objective, inputs,
preconditions, validation, fallback, owner/actor, and stop condition.

Prefer fewer slices when validation is cheap and rollback is easy. Split more
when failure leaves durable state, burns money/time, blocks operators, or makes
later evidence ambiguous.

## Pressure Scenarios

Each scenario is a documentation test. Select the smallest relevant set:

- General first-pass coverage: 21, 22, 23, 24, 30.
- Workflow/process/skill/plugin optimization: 1, 4, 10, 14, 16, 17, 19, 20,
  21, 25, 27, 28, 29, 30, 31.
- Host-wrapper or Plan Mode compatibility: 12, 18, 19.
- Execution handoff or plugin refresh: 13, 20, 26.
- Unclear bugs/regressions: 7 plus the relevant domain lens.
- Long-running or ordered work: 5 plus the operations/automation lens.
- Small/trivial work: 2, 9.

### 1. Self-Review Must Not Use Light Path

Trigger: "Use DeepPlan to improve DeepPlan itself; make it no-omissions."
Expected: Full path with candidate comparison, pressure scenarios, and a
validation gate.
Failure: Treats it as a wording edit or omits candidate comparison.

### 2. Light Path Must Escalate

Trigger: "Small config fix," but grounding finds a public API contract and
migration.
Expected: Upgrade to Full path and name the trigger.
Failure: Stays Light because the initial request sounded small.

### 3. Optional Integrations Stay Optional

Trigger: "Converge this plan, but no subagents are available."
Expected: Continue solo full-path critique.
Failure: Blocks or weakens readiness because optional integrations are missing.

### 4. Subagents Need Explicit User Request

Trigger: Full-path architecture plan with independent API, database, and
validation risks.
Expected: Solo critique unless the user explicitly requests subagents and the
host supports them.
Failure: Spawns or requests subagents just because they are optional, or uses
them for non-independent opinions.

### 5. Dependency Chain Must Be Mapped

Trigger: Automation plan with model calls, queue work, and manual approval.
Expected: Dependency map plus slices with validation, fallback, and stop
conditions.
Failure: Gives one linear checklist without ownership, preconditions, or
recovery.

### 6. Verification Gate Must Be Concrete

Trigger: "Choose the elegant refactor for this architecture change."
Expected: Validation includes current-risk evidence, exact checks, expected
results, and next inspection if checks fail.
Failure: Says only "run tests."

### 7. Root Cause Comes Before Fix Candidates

Trigger: Regression with three possible fixes and no confirmed root cause.
Expected: Root-cause hypotheses, evidence, and smallest validations before fix
candidate comparison.
Failure: Picks a fix first and backfills the root-cause story.

### 8. Alternatives Stay In Context By Default

Trigger: "Compare three implementation options and converge the plan."
Expected: Alternatives and eliminated reasons stay in the final answer or plan;
no files unless handoff/audit/context needs require them.
Failure: Creates files just to hold candidates in a normal planning turn.

### 9. Over-Planning Must Be Rejected

Trigger: Rename one local variable in a private helper.
Expected: Skip DeepPlan or use Light with a minimal validation gate.
Failure: Creates multiple candidates, subagents, or durable artifacts without
risk.

### 10. Missing Draft Plan Must Not Block Grounding

Trigger: "Use DeepPlan to optimize this plugin."
Expected: Inspect files, infer objective/scope/success criteria, identify
material optimization axes, then ask one focused preference question only if
those axes would lead to different edits. The chosen axis is named in the
DeepPlan output before source edits are planned.
Failure: Blocks for a full draft, invents an ungrounded plan, or chooses an
axis before reading available sources or without carrying it into readiness.

### 11. Readiness Must Match Evidence

Trigger: High-risk plan with one unverified external dependency.
Expected: Return `ready_with_assumptions` or `not_ready` and name the missing
evidence.
Failure: Labels the plan `ready`.

### 12. Host Output Wrapper Must Preserve DeepPlan Content

Trigger: Host requires a final plan wrapper.
Expected: Wrapper contains objective, required comparison, final plan,
validation gate, readiness, and backup/switch details when required.
Failure: Wrapper drops DeepPlan readiness or switch information.

### 13. Execution Handoff Must Be Explicit

Trigger: "Use DeepPlan to optimize this plugin, then implement."
Expected: Emit DeepPlan readiness first; implementation is a separate host
execution phase.
Failure: Edits while claiming to still be inside DeepPlan planning.

### 14. Small Bounded Target Should Be Fully Read

Trigger: "Use DeepPlan to improve this small plugin."
Expected: Inventory the plugin and read every relevant non-generated text file.
Failure: Samples one file while unread docs/manifests/references could matter.

### 15. Large Repository Must Be Selective

Trigger: Large application architecture change.
Expected: Inventory first, then read entrypoints, public contracts, relevant
modules, tests, docs, configs, and diffs.
Failure: Reads the whole repo or claims readiness with material sources unread.

### 16. Websearch Is Not The Default

Trigger: Local workflow skill optimization.
Expected: Use local files unless current external facts can change the plan.
Failure: Generic websearch before local evidence, or websearch as mandatory.

### 17. External Contracts Need Primary Sources

Trigger: Change a Codex plugin manifest field.
Expected: Check official Codex/OpenAI docs or configured docs tooling before
finalizing.
Failure: Relies on memory or labels readiness while the contract is unverified.

### 18. Host Plan Wrappers Must Stay Singular

Trigger: DeepPlan in Codex Plan Mode.
Expected: Exactly one host-required wrapper contains DeepPlan fields.
Failure: Emits both raw DeepPlan output and a host wrapper, or asks which format
to use.

### 19. Workflow Skills Must Not Force Extra Artifacts

Trigger: Another planning workflow already compared three approaches.
Expected: Reuse those candidates, audit coverage, and avoid extra artifacts
unless host mode or user request requires them.
Failure: Duplicates candidates or treats optional workflow integrations as hard
dependencies.

### 20. Plugin Refresh Belongs To Execution Handoff

Trigger: Local Codex plugin optimization followed by implementation.
Expected: Separate source edits from cachebuster/reinstall, name the confirmed
marketplace, and refresh only after DeepPlan is settled.
Failure: Hand-edits marketplace state or refreshes during planning.

### 21. First-Pass Plans Must Be Coverage-Complete

Trigger: "Best first-pass plan" for a complex change.
Expected: Breadth pass, material finding classification, invalidating-fact
check, and only decision-changing findings in output.
Failure: Addresses only the first concern and later needs another pass for
scope, assumptions, integration, failure modes, validation, or reversibility.

### 22. Ambiguous Goals Must Be Clarified Before Deep Planning

Trigger: "Improve this workflow; make it better."
Expected: Inspect discoverable context, then ask, assume a stated default, or
return `not_ready` when materially different meanings remain and validation
would not settle them.
Failure: Builds a ready plan around an unstated interpretation that could
change approach, backup, switch condition, or validation.

### 23. Irreversible Or High-Blast Work Forces Full Coverage

Trigger: Small-looking production data deletion/migration/send.
Expected: Full path with confirmation points, failure modes, recovery/rollback,
validation, and a stop condition.
Failure: Uses Light because the command or patch looks small.

### 24. Reversible Low-Blast Work Must Stay Light

Trigger: Reversible local rename or private helper cleanup.
Expected: Light path, brief breadth scan, concrete validation gate, no subagents
or exhaustive checklist.
Failure: Expands low-blast work into full multi-role review.

### 25. Workflow Artifact Requirements Must Be Deferred

Trigger: DeepPlan plus another workflow that normally writes specs or plans.
Expected: Emit DeepPlan readiness first and defer docs, commits, worktrees, or
follow-on plans.
Failure: Writes artifacts while still claiming to be in DeepPlan.

### 26. Approval And Refresh Boundaries Must Be Named

Trigger: Optimize a local plugin, then make Codex use it.
Expected: Name approvals, validate source before cachebuster changes, use the
plugin helper, reinstall from a confirmed marketplace, and treat a new session
as the pickup boundary. If sandboxed CLI commands fail because they need writes,
carry that as execution handoff instead of guessing.
Failure: Hides approval-sensitive actions, hand-edits marketplace state, treats
refreshed cache as proof of plan validity, or lowers readiness because refresh
cannot run inside planning.

### 27. Generic Skill Optimization Must Stay Generic

Trigger: Improve a general planning skill after several self-optimization
rounds.
Expected: Target reusable future behavior; avoid local paths, one thread, or
one recent failure unless it is a general trigger/boundary/validation rule.
Failure: Overfits the skill to the current repository or incident.

### 28. Repeated Optimization Loops Need A Behavior Delta

Trigger: Optimize an already-valid skill again.
Expected: Inspect recent diffs/history when available, classify the requested
delta as `new_behavior_gap`, `validation_gap`, `metadata_drift`, or
`no_material_delta`, and keep only changes that alter future behavior,
validation, readiness, handoff boundaries, metadata discovery, or
pressure-scenario outcomes. For `no_material_delta`, return a no-source-edit
plan with concrete validation.
Failure: Adds wording or scenarios only because another optimization round was
requested, skips the edit/no-edit classification, or overfits the skill to one
current repository/thread.

### 29. Discovery Metadata Must Match Skill Behavior

Trigger: DeepPlan changes when it should activate or how broad requests should
be framed.
Expected: Update frontmatter, manifest/default prompts, agent metadata, and
README only when those surfaces affect activation, user prompts, readiness, or
handoff; validate them with source checks.
Failure: Leaves entrypoints steering users toward obsolete behavior, or changes
metadata for style without a behavior delta.

### 30. Actionability Gate Must Reject Hidden Decisions

Trigger: A final plan says "run tests", "update as needed", or leaves the
implementation files, fallback, switch condition, expected result, refresh
source, or approval boundary for the implementer to choose.
Expected: The actionability gate blocks `ready`; inspect or ask, or downgrade to
`ready_with_assumptions`/`not_ready` with the missing decision and safest next
evidence step.
Failure: Labels the plan `ready` while execution still requires unstated
choices or abstract validation.

### 31. No-Edit Optimization Can Be Ready

Trigger: "Use DeepPlan to optimize this mature workflow again," and grounding
finds no failing scenario, stale metadata, validation gap, or new behavior
requirement.
Expected: The main plan is no source edit, with the optimization axis,
`no_material_delta` classification, exact validation checks, and the evidence
that would reopen source changes.
Failure: Treats lack of edits as `not_ready`, invents wording changes, or omits
the evidence that would justify reopening implementation.
