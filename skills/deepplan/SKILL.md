---
name: deepplan
description: Use when refining complex plans, architecture changes, migrations, unclear root-cause fixes, high-risk approaches, or explicit best/elegant/no-omissions/self-review/converged planning requests before execution.
---

# DeepPlan

Pre-execution planning gate: turn an initial plan, rough request, or competing
approaches into one evidence-backed execution plan. Do not implement while this
skill is active. If implementation is also requested, settle the DeepPlan output
first, then leave planning and use the host's normal editing and verification
rules.

## Operating Sequence

Follow this order every time:

1. Ground in local evidence before asking questions or choosing candidates.
2. Choose Light or Full depth after grounding, then upgrade if evidence raises
   risk.
3. Build or audit the candidate pool before selecting the main plan.
4. Critique candidates, converge on the main plan, and define validation.
5. Emit the DeepPlan output with readiness before any implementation,
   cachebuster update, reinstall, or refresh.
6. Treat implementation, cachebusters, reinstalls, commits, and durable artifacts
   as separate execution handoff work after DeepPlan is settled.

DeepPlan self-review, and nontrivial skill/plugin/process/policy changes, must
use the Full path even when the likely source patch is mostly wording.

## Use And Depth

Use DeepPlan for architecture or module-boundary changes, migrations,
compatibility, rollout, irreversible state, unclear root cause, multiple fixes,
multi-module or high-regression work, long-running or expensive operations,
workflow/process/skill/plugin/policy design, and requests for deep, best,
elegant, no-omissions, self-review, or converged planning.

Skip it for trivial syntax fixes, one-field edits, simple path/config updates,
or failures with verified root cause and an obvious patch. If the user explicitly
invokes DeepPlan for trivial work, use the Light path and keep output short.

Choose the path after grounding, then upgrade when evidence raises risk.
Planning effort scales by blast radius and irreversibility, not task size alone.
A reversible local change can stay Light even when subtle; an irreversible,
external-facing, cross-system, or migration-like change needs Full coverage even
when small.

- Full path: required when any risk is high, or two are medium: uncertainty,
  blast radius, irreversibility, validation difficulty, failure cost, or
  dependency-chain length.
- Full path: also required for explicit deep/best/elegant/no-omissions/
  self-review/converged requests, DeepPlan self-review, nontrivial
  workflow/process/skill/plugin/policy changes, host-wrapper compatibility risk,
  external contract changes, or first-pass plans where a missed assumption could
  invalidate the plan.
- Light path: allowed only when scope is small, facts are clear, validation is
  obvious, no public API/schema/data/deploy/durable-state risk exists, and the
  user did not request deep/no-omissions/converged planning.
- Upgrade from Light immediately if you find an evidence gap, candidate
  category, medium/high risk, unclear validation, or long dependency chain.

Read `references/depth-and-pressure.md` for Full path domain lenses,
dependency-chain slicing, and pressure scenarios.

## Boundary And Host Contract

- Planning only: no repo-tracked edits, formatters, generated specs, commits,
  deploys, migrations, cachebuster updates, plugin reinstalls, marketplace
  writes, durable external writes, or other side-effectful execution.
- Run commands only when they clarify evidence and do not change durable state.
- Keep alternatives in conversation by default. Create scratch artifacts only
  for user-requested handoff/audit, context limits, or multi-agent coordination;
  prefer runtime-local or `/tmp` paths.
- Obey the host's active collaboration mode, output wrapper, approval rules, and
  tool limits. If the host requires a final plan wrapper such as
  `<proposed_plan>`, put the DeepPlan contract inside that wrapper and emit only
  one final plan block. Host wrapper requirements override the stable label
  format below; never emit a second raw DeepPlan block beside the host wrapper.
- Do not create design docs, commits, worktrees, scratch files, or follow-on
  execution plans solely because another workflow would normally do so.
- If another active workflow normally requires design docs, commits, worktrees,
  implementation plans, or other artifacts, keep DeepPlan side-effect free and
  defer those tasks to the host's execution phase.
- If another active workflow requires approval before implementation, finish the
  DeepPlan output first and leave execution to the host's normal implementation
  phase.
- If execution after DeepPlan needs write approval, external access, or any
  durable side effect, name that approval in the handoff instead of performing
  it during planning.

## Evidence Policy

- Ground in evidence before asking questions, choosing candidates, or producing
  the plan. If no draft plan exists, infer objective, scope, constraints, and
  success criteria from available evidence before generating candidates.
- Start with local sources: `rg --files`, manifests, docs, tests, schemas,
  runbooks, logs, and recent diffs when available.
- For small bounded targets, read all relevant non-generated text files. For
  workflow/process/skill/plugin reviews, include manifests, skill metadata,
  references, README/dependency notes, validation scripts, published contracts,
  and configured install or execution sources.
- For DeepPlan/plugin self-review, specifically include Codex and Claude
  manifests, `SKILL.md`, agent metadata, references, README, dependencies, and
  any discoverable local install or cache source before claiming readiness.
- For large repositories, read the inventory, likely entrypoints, public
  interfaces/contracts, relevant modules, tests, configs, docs/runbooks, and
  diffs that can change the plan. Avoid vendor trees, caches, build artifacts,
  binaries, generated files, secrets, and unrelated directories unless needed.
- Ask only for preferences, tradeoffs, missing goals, scope boundaries, or risk
  tolerance that cannot be discovered from the environment.
- Do not use generic websearch by default. Use official or primary external
  sources only when current API behavior, SDK/tool/plugin formats, package
  versions, laws, pricing, release status, service limits, or explicit user
  lookup could change the plan.
- For OpenAI, Codex, skills, plugins, Agents SDK, Responses API, or Apps SDK
  facts, use official OpenAI documentation or configured docs tools before any
  broader web search.
- If unread local sources or unverified external evidence could change the main
  plan, backup, switch condition, or validation gate, do not label the plan
  `ready`; name the missing evidence and safest partial plan.

## Workflow

### 1. Ground And Scan Breadth

- State the inferred objective, scope, constraints, success criteria, confirmed
  facts, and guesses.
- Identify public interfaces, data/state boundaries, dependencies, integration
  points, environment/host constraints, validation surfaces, reversibility or
  recovery, and failure modes that could change the plan.
- Classify material findings as:
  - `blocking_unknown`: the plan could be wrong until resolved. Inspect or ask
    before `ready`; otherwise return `not_ready` with a safe step-zero evidence
    task.
  - `assumption_to_confirm`: execution is reasonable only if the assumption
    holds and the cost of being wrong is acceptable. Surface it explicitly and
    use `ready_with_assumptions` unless validation will confirm it first.
  - `refinement`: improves the plan but does not change approach, backup, switch
    condition, or validation gate. Fold it into the plan without output bloat.
- Ask: "What fact would make this entire plan wrong?" If plausible and
  unverified, treat it as a blocking unknown or assumption to confirm.
- Output only breadth findings that change readiness, approach, validation,
  backup, or switch condition.

### 2. Use Root-Cause Mode When Needed

For bugs, regressions, or unclear failures, do this before fix candidates unless
the root cause is already verified.

- List 3-5 plausible root-cause hypotheses.
- For each, include supporting evidence, disconfirming evidence, smallest
  validation, and smallest fix if true.
- Eliminate at least two alternative causes before `ready`; otherwise return
  `ready_with_assumptions` or `not_ready` with the missing evidence.

### 3. Build The Candidate Pool

- Reuse existing 2-3 real approaches when supplied; audit coverage instead of
  duplicating equivalent tradeoffs.
- Add candidates only when there is one option, shallow variants of one option,
  or a missing materially different strategy that could change the final plan,
  backup, switch condition, validation gate, or readiness.
- Default candidate set when needed: minimal safe change, robust long-term
  design, and compromise architecture.
- Each candidate needs hypothesis, planned changes, validation, risks, and an
  elimination condition.
- Do not fabricate candidates for a template. Do not force
  minimal/robust/compromise variants when they are only wording or sequencing
  tunings of the same strategy. Collapse minor tunings as variants and use Light
  unless the Depth Gate requires Full.
- For Full path, keep the comparison real even when one candidate is clearly
  preferred: name the backup and the condition that would switch to it.

### 4. Critique And Compare

- Run one critique round by default.
- Run a second round when critique finds high/medium risk, a new candidate
  category, an evidence gap, or unresolved tradeoff.
- Run a third round only for a new high-risk blocker.
- Stop critique when another round would not change the main plan, backup,
  switch condition, validation gate, or readiness.
- Use role lenses as perspectives, not mandatory roles. Default lenses:
  correctness/feasibility, user intent/scope, failure modes/reversibility,
  validation, maintainability/operability, and simplicity. Add domain lenses
  only when relevant: security/privacy/safety, data/migration/compatibility,
  compliance, cost/performance, rollout, product/user impact, or research
  evidence quality.
- Use subagents only when the user explicitly asks for subagents or parallel
  agent work, the host supports them, policy permits them, the plan is Full
  path, and there are 2+ independent read-heavy evidence domains. An independent
  domain needs substantial separate reading/searching and can be characterized
  without waiting on another domain. If subagents are unavailable, unrequested,
  or inappropriate, continue with solo critique; do not treat optional subagents
  as a reason to block or weaken readiness.
- For workflow/process/skill/plugin/policy changes, pressure-check the relevant
  scenarios in `references/depth-and-pressure.md` by the future behavior they
  test; do not run the whole list unless the change touches the whole workflow.
  For selected scenarios, verify the expected behavior and failure condition;
  output only pass/fail pressure scenario results that affect approach,
  validation, readiness, backup, or switch condition.

### 5. Converge And Define Verification

- Compare candidates on root-cause coverage, risk, testability,
  maintainability, simplicity, and elimination conditions.
- Eliminate weaker candidates with reasons.
- Full path must end with exactly one main plan, one backup plan, and a switch
  condition. Light path must end with a concrete validation gate and the next
  inspection if validation fails.
- For complex/high-risk plans, run a final adversarial check for fatal issues,
  evidence gaps, hidden regressions, and smaller equivalent plans.
- Make the recommendation execution-ready: ordered steps, explicit assumptions,
  material risks with mitigations, decision points with a recommended choice,
  verification/acceptance criteria, and confirmation points for irreversible
  steps.
- Every validation gate needs pre-change evidence, exact command/test/log/
  inspection/reproduction, expected result, and next inspection or fallback if
  validation fails. Avoid generic "run tests" gates.
- For process or skill changes, pressure scenarios count as verification only
  when expected behavior and failure condition are explicit.
- For plugin/skill changes, include structural validation, metadata parsing,
  wrapper/output-shape checks when relevant, and required local refresh steps as
  a separate post-plan handoff.
- For dependency-heavy work, output execution-ready slices with objective,
  inputs, preconditions, validation, fallback, owner/actor, and stop condition.

### 6. Handoff To Execution When Requested

- First emit the DeepPlan output with readiness. Do not edit source, update
  cachebusters, reinstall plugins, or run mutating workflow steps before that
  output is settled.
- After the DeepPlan phase is complete, follow the host's normal implementation,
  approval, editing, and verification rules.
- For local plugin updates, confirm the marketplace/source that points at the
  edited plugin, validate source files first, use the plugin-creator
  cachebuster/update helper when available, and reinstall from the confirmed
  local marketplace only after source validation. Do not hand-edit marketplace
  files merely to refresh an installed local plugin.
- Treat "start a new thread/session to pick up refreshed plugin behavior" as an
  execution handoff note, not as proof that the plan itself is valid.

## Output And Readiness

Always include objective, final main plan, validation gate, and readiness. Keep
output proportional to risk; do not dump scratch reasoning, and include optional
sections only when they change the execution decision.

For Full path, also include candidate comparison, eliminated alternatives, one
backup plan, and the switch condition. For Light path, include the
validation-failure fallback instead of a backup plan.

Use stable labels when the host does not impose a stricter format: Objective,
Candidate Comparison, Main Plan, Backup Plan, Switch Condition, Validation Gate,
Assumptions, and Readiness. Omit empty labels. If the host imposes a wrapper or
section order, preserve the DeepPlan fields inside that format instead of
emitting a second DeepPlan block.

- `ready`: evidence is sufficient; the chosen plan, backup/switch condition
  when required, and validation gate are executable with no open decisions.
- `ready_with_assumptions`: execution is reasonable only under named
  assumptions; include what evidence or validation must confirm each assumption.
- `not_ready`: missing evidence or decisions could change the main plan,
  backup, switch condition, or validation gate; include the safest partial plan.

Stop only when the latest critique adds no high/medium risk, no materially
different candidate remains, continuing would not add evidence, and the chosen
plan plus validation gate are executable. Do not stop because "there is no more
feedback"; if reflection will not add evidence, switch to inspection, tests,
logs, or minimal reproduction.

For workflow/process/skill/plugin/policy reviews, keep only changes that alter
future agent behavior. Pressure-check missed triggers, premature execution,
missing validation, optional dependency misuse, over-planning, context clutter,
host output wrapper compatibility, approval boundaries, and execution handoff
boundaries. For repeated optimization passes, stop when the remaining changes
are explanation-only, style-only, or overfit to the current artifact and do not
alter future agent behavior.
