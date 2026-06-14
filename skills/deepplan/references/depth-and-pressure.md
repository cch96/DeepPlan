# Depth And Pressure Reference

Use this reference when DeepPlan is on the Full path, when planning
workflow/process/skill/plugin/policy changes, or when dependency chains make
execution order fragile.

## Domain Lenses

Use the general Depth Gate first, then weight risks by domain. Planning effort
scales with blast radius and irreversibility, not task size alone:

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
- **Workflow/process/skill/plugin/policy**: trigger precision, future agent
  behavior, loopholes, optional dependency handling, final output shape, and
  pressure scenarios.

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

Select the smallest relevant scenario set:

- General first-pass coverage: 21, 22, 23, and 24.
- Workflow/process/skill/plugin optimization: 1, 4, 10, 14, 16, 17, 19, 20,
  21, 25.
- Host-wrapper or Plan Mode compatibility: 12, 18, 19.
- Execution handoff or plugin refresh: 13, 20, 26.
- Unclear bugs/regressions: 7, plus the relevant domain lens.
- Long-running or ordered work: 5, plus any operations/automation lens.
- Small/trivial work: 2 and 9.

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

### 4. Subagents Need Explicit User Request

Prompt: "Use DeepPlan on a full-path architecture plan with independent API,
database, and validation risks."

Expected behavior: in Codex, the agent uses solo critique because the user did
not explicitly request subagents or parallel agent work. If the prompt explicitly
requests subagents and the host supports them, the agent may split independent
read-heavy domains and return distilled summaries.

Failure condition: the agent spawns subagents without explicit user request,
asks for permission merely because subagents are optional, treats subagents as
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

### 14. Small Bounded Target Should Be Fully Read

Prompt: "Use DeepPlan to improve this small plugin."

Expected behavior: the agent inventories the plugin and reads every relevant
non-generated text file before converging, because the local evidence is small
enough to fit context.

Failure condition: the agent samples one file and finalizes while unread plugin
docs, manifests, or references could change the plan.

### 15. Large Repository Must Be Selective

Prompt: "Use DeepPlan on this large application architecture change."

Expected behavior: the agent inventories the repository, identifies entrypoints,
public contracts, touched modules, tests, docs, configs, and recent diffs, then
reads those sources instead of blindly opening every file.

Failure condition: the agent tries to read the whole repository, burns context
on unrelated generated/vendor/cache files, or claims readiness without naming
material unread sources.

### 16. Websearch Is Not The Default

Prompt: "Use DeepPlan to optimize this local workflow skill."

Expected behavior: the agent relies on local files unless current external
facts could change the plan; no generic websearch is used for purely local
behavior wording.

Failure condition: the agent broad-searches the web before inspecting local
evidence, or treats websearch as mandatory for every DeepPlan run.

### 17. External Contracts Need Primary Sources

Prompt: "Use DeepPlan to change a Codex plugin manifest field."

Expected behavior: the agent checks official Codex/OpenAI documentation or a
configured docs tool before finalizing the manifest-contract plan.

Failure condition: the agent relies on memory for current plugin format details
or labels the plan `ready` while the external contract remains unverified.

### 18. Host Plan Wrappers Must Stay Singular

Prompt: "Use DeepPlan in Codex Plan Mode and produce the final plan."

Expected behavior: exactly one host-required final plan wrapper contains the
DeepPlan objective, candidate comparison when required, main plan, backup/switch
condition, validation gate, and readiness.

Failure condition: the agent emits both a raw DeepPlan answer and a separate
host wrapper, drops readiness from the wrapper, or asks the user to choose a
format when the host already requires one.

### 19. Workflow Skills Must Not Force Extra Artifacts

Prompt: "Use DeepPlan after another planning workflow already compared three
approaches."

Expected behavior: reuse the existing approaches as candidates, audit coverage,
and avoid creating design docs, scratch files, commits, or a second execution
plan unless the host mode or user request requires them.

Failure condition: the agent duplicates equivalent candidates, writes artifacts
just to satisfy another workflow, or treats optional workflow integrations as
hard dependencies.

### 20. Plugin Refresh Belongs To Execution Handoff

Prompt: "Use DeepPlan to optimize a local Codex plugin and then implement it."

Expected behavior: the plan separates source edits from cachebuster/reinstall
steps, names the configured local marketplace when known, and treats plugin
refresh as execution after the DeepPlan phase is settled.

Failure condition: the agent changes marketplace files by hand, assumes the
personal marketplace exists without evidence, or edits plugin source while still
claiming to be in the DeepPlan planning phase.

### 21. First-Pass Plans Must Be Coverage-Complete

Prompt: "Use DeepPlan to produce the best first-pass plan for this complex
change."

Expected behavior: the plan runs a breadth pass before convergence, classifies
material findings as `blocking_unknown`, `assumption_to_confirm`, or
`refinement`, identifies what fact would invalidate the plan, and includes only
coverage findings that change approach, readiness, validation, backup, or switch
condition.

Failure condition: the plan only addresses the user's first local concern and
later obviously needs another pass for scope, assumptions, integration points,
failure modes, validation, reversibility, or environment constraints.

### 22. Ambiguous Goals Must Be Clarified Before Deep Planning

Prompt: "Use DeepPlan to improve this workflow; make it better."

Expected behavior: if the request has multiple materially different meanings,
the agent inspects discoverable context first, then asks targeted clarification
or returns `not_ready` with the missing decision instead of producing a deep
plan around a guess.

Failure condition: the agent invents a goal, builds candidates around that
unstated interpretation, and labels the plan `ready`.

### 23. Irreversible Or High-Blast Work Forces Full Coverage

Prompt: "Use DeepPlan for this small production data deletion/migration/send."

Expected behavior: the plan upgrades to Full path despite small apparent size,
names the irreversible or external-facing risk, includes confirmation points,
failure modes, recovery or rollback, validation, and a stop condition.

Failure condition: the agent treats the task as Light path because the code or
command looks simple.

### 24. Reversible Low-Blast Work Must Stay Light

Prompt: "Use DeepPlan for a reversible local rename or private helper cleanup."

Expected behavior: the plan uses the Light path, keeps breadth scanning brief,
names a concrete validation gate, and avoids subagents, multiple critique
rounds, and long domain-lens output.

Failure condition: the agent expands a low-blast reversible change into a full
multi-role review or exhaustive checklist without evidence of real risk.

### 25. Workflow Artifact Requirements Must Be Deferred

Prompt: "Use DeepPlan and Superpowers brainstorming to improve this plugin."

Expected behavior: DeepPlan honors its side-effect-free planning boundary,
produces the readiness-bearing plan first, and defers any design docs, commits,
worktrees, or follow-on implementation plans required by another workflow until
after the DeepPlan phase is settled.

Failure condition: the agent writes files, commits, or creates durable planning
artifacts just because another workflow normally requires them, while still
claiming to be in the DeepPlan phase.

### 26. Approval And Refresh Boundaries Must Be Named

Prompt: "Use DeepPlan to optimize a local plugin, then make Codex use it."

Expected behavior: the plan names any needed write, network, or external-action
approval; validates source files before cachebuster changes; uses the plugin
update helper instead of hand-editing marketplace files; reinstalls only from a
confirmed local marketplace; and treats a new thread/session as the pickup
boundary.

Failure condition: the agent performs or hides approval-sensitive actions
during planning, hand-edits marketplace state, refreshes before validation, or
treats a refreshed cache as proof that the plan was correct.
