---
name: deepplan
description: Use when refining complex plans, architecture changes, migrations, unclear root-cause fixes, high-risk approaches, workflow/process/skill/plugin optimization, or explicit best/elegant/no-omissions/self-review/converged planning requests before execution.
---

# DeepPlan

Pre-execution planning gate: turn a rough request, draft plan, or competing
approaches into one evidence-backed execution plan. Do not implement while this
skill is active. If implementation is also requested, settle the DeepPlan output
first, then leave DeepPlan and use the host's normal editing and verification
rules.

## Operating Sequence

1. Ground in local evidence before asking questions or choosing candidates.
2. Choose Light or Full depth after grounding; upgrade when evidence raises
   risk.
3. For broad "improve/optimize" requests, lock the material optimization axis
   after grounding before planning source changes.
4. Build or audit the candidate pool before selecting the main plan.
5. Critique candidates, converge, and define validation.
6. Run the actionability gate: no hidden implementer decisions, abstract
   validation, or vague fallback remains.
7. Emit readiness before implementation, cachebuster updates, reinstalls,
   commits, durable artifacts, or other execution work.

DeepPlan self-review, and nontrivial workflow/process/skill/plugin/policy
changes, must use Full path even when the likely patch is mostly wording.

## Use And Depth

Use DeepPlan for architecture or module-boundary changes, migrations,
compatibility, rollout, irreversible state, unclear root cause, multiple fixes,
multi-module or high-regression work, long-running or expensive operations,
workflow/process/skill/plugin/policy design, and explicit deep/best/elegant/
no-omissions/self-review/converged planning requests.

Skip it for trivial syntax fixes, one-field edits, simple path/config updates,
or failures with verified root cause and an obvious patch. If the user
explicitly invokes DeepPlan for trivial work, use Light and keep output short.

Depth scales by blast radius and irreversibility, not apparent task size:

- Full path: required for any high risk, or two medium risks, across
  uncertainty, blast radius, irreversibility, validation difficulty, failure
  cost, or dependency-chain length.
- Full path: also required for explicit deep/no-omissions/converged requests,
  DeepPlan self-review, nontrivial workflow/process/skill/plugin/policy changes,
  host-wrapper compatibility risk, external contract changes, or first-pass
  plans where a missed assumption could invalidate the plan.
- Light path: allowed only when scope is small, facts are clear, validation is
  obvious, no public API/schema/data/deploy/durable-state risk exists, and the
  user did not request deep/no-omissions/converged planning.
- Upgrade from Light when evidence exposes a gap, a candidate category,
  medium/high risk, unclear validation, or a long dependency chain.

Read `references/depth-and-pressure.md` for Full path lenses, dependency-chain
slicing, and pressure scenarios.

## Boundaries And Evidence

- Planning only: no repo-tracked edits, formatters, generated specs, commits,
  deploys, migrations, cachebuster updates, plugin reinstalls, marketplace
  writes, durable external writes, or other side-effectful execution.
- Run commands only when they clarify evidence and do not change durable state.
- Keep alternatives in conversation by default. Create scratch artifacts only
  for user-requested handoff/audit, context limits, or multi-agent coordination;
  prefer runtime-local or `/tmp` paths.
- Obey the host's collaboration mode, output wrapper, approval rules, and tool
  limits. If the host requires a wrapper such as `<proposed_plan>`, put the
  DeepPlan contract inside that single wrapper; do not emit a second raw
  DeepPlan block.
- If another workflow normally requires design docs, commits, worktrees,
  implementation plans, or other artifacts, defer them until after DeepPlan
  readiness is emitted.
- If execution after DeepPlan needs write approval, external access, or durable
  side effects, name that approval in the handoff instead of performing it.

Grounding rules:

- Infer objective, scope, constraints, and success criteria from local evidence
  before asking questions or generating candidates.
- Start with `rg --files`, manifests, docs, tests, schemas, runbooks, logs, and
  recent diffs. For small bounded targets, read all relevant non-generated text.
- For workflow/process/skill/plugin reviews, include manifests, skill metadata,
  references, README/dependency notes, validation scripts, published contracts,
  and configured install or execution sources.
- For DeepPlan/plugin self-review, include Codex and Claude manifests,
  `SKILL.md`, frontmatter trigger metadata, agent/default prompts, references,
  README, dependencies, and discoverable local install/cache sources before
  claiming readiness.
- For large repositories, inventory first, then read likely entrypoints, public
  contracts, relevant modules, tests, configs, docs/runbooks, and diffs. Avoid
  vendor, cache, build, binary, generated, secret, and unrelated trees unless
  they can change the plan.
- Ask only for preferences, tradeoffs, missing goals, scope boundaries, or risk
  tolerance that local evidence cannot answer.
- Do not use generic websearch by default. Use official or primary sources only
  when current external contracts, APIs, SDK/tool behavior, package versions,
  laws, pricing, releases, or explicit lookup requests can change the plan.
- For OpenAI, Codex, skills, plugins, Agents SDK, Responses API, or Apps SDK
  facts, use official OpenAI documentation or configured docs tools before
  broader web search.
- If unread local sources or unverified external evidence could change the main
  plan, backup, switch condition, or validation gate, do not label the plan
  `ready`.

Optimization requests:

- For broad requests such as "optimize this", "improve this plugin", or "make
  this better", infer likely axes from evidence first: behavior reliability,
  token length, user experience, metadata/installability, validation coverage,
  and maintainability.
- If two or more axes would produce materially different edits, ask one focused
  preference question or state the recommended default as an assumption before
  emitting a `ready` plan.
- Name the chosen optimization axis in the Objective or Assumptions so execution
  cannot silently optimize for a different quality than the plan reviewed.
- Repeated optimization must have a behavior delta. Do not propose source edits
  for explanation-only, style-only, local-path-specific, or current-thread-only
  changes unless they alter future behavior, readiness, validation, handoff
  boundaries, or pressure-scenario outcomes.

## Workflow

### 1. Ground And Scan Breadth

State the inferred objective, scope, constraints, success criteria, confirmed
facts, and guesses. Identify public interfaces, data/state boundaries,
dependencies, integration points, host constraints, validation surfaces,
reversibility/recovery, and failure modes that could change the plan.

Classify material findings:

- `blocking_unknown`: inspect or ask before `ready`; otherwise return
  `not_ready` with the safest step-zero evidence task.
- `assumption_to_confirm`: execution is reasonable only if named assumptions
  hold; use `ready_with_assumptions` unless validation will confirm them first.
- `refinement`: improves execution but does not change approach, backup, switch
  condition, readiness, or validation gate; fold it in without output bloat.

Ask: "What fact would make this entire plan wrong?" Treat plausible unverified
answers as blocking unknowns or assumptions.

### 2. Use Root-Cause Mode When Needed

For bugs, regressions, or unclear failures, verify root cause before fix
candidates unless already known:

- List 3-5 plausible causes with supporting evidence, disconfirming evidence,
  smallest validation, and smallest fix if true.
- Eliminate at least two alternatives before `ready`; otherwise return
  `ready_with_assumptions` or `not_ready`.

### 3. Build Candidates

- Reuse supplied 2-3 real approaches and audit coverage instead of duplicating
  equivalent tradeoffs.
- Add candidates only when there is one option, shallow variants of one option,
  or a missing materially different strategy that could change the final plan,
  backup, switch condition, readiness, or validation gate.
- Default candidate set when needed: minimal safe change, robust long-term
  design, and compromise architecture.
- Each candidate needs hypothesis, planned changes, validation, risks, and an
  elimination condition.
- Do not fabricate template candidates. Collapse wording or sequencing tunings
  as variants and use Light unless the Depth Gate requires Full.
- Full path must still name a real backup and the condition that would switch to
  it.

### 4. Critique And Compare

- Run one critique round by default; run a second when critique finds
  high/medium risk, a new candidate category, an evidence gap, or unresolved
  tradeoff; run a third only for a new high-risk blocker.
- Stop when another round would not change the main plan, backup, switch
  condition, readiness, or validation gate.
- Use lenses as perspectives, not mandatory roles: correctness/feasibility,
  user intent/scope, failure modes/reversibility, validation,
  maintainability/operability, and simplicity. Add domain lenses only when
  relevant.
- Use subagents only when the user explicitly asks for subagents or parallel
  agent work, the host supports them, policy permits them, the plan is Full, and
  there are 2+ independent read-heavy evidence domains. Otherwise continue with
  solo critique; optional subagents must not block or weaken readiness.
- For workflow/process/skill/plugin/policy changes, pressure-check only relevant
  scenarios from `references/depth-and-pressure.md`; output only results that
  affect approach, validation, readiness, backup, or switch condition.

### 5. Converge And Verify

- Compare candidates on root-cause coverage, risk, testability,
  maintainability, simplicity, and elimination conditions.
- Full path must end with exactly one main plan, one backup plan, and a switch
  condition. Light path must end with one validation gate and the next
  inspection if validation fails.
- For complex/high-risk plans, run a final adversarial check for fatal issues,
  evidence gaps, hidden regressions, and smaller equivalent plans.
- Make the recommendation execution-ready: ordered steps, assumptions, material
  risks/mitigations, decision points, verification/acceptance criteria, and
  confirmation points for irreversible steps.
- Every validation gate needs pre-change evidence, exact command/test/log/
  inspection/reproduction, expected result, and next inspection or fallback if
  validation fails.
- Before marking `ready`, run an actionability gate: the implementer should not
  need to choose the optimization axis, files/modules, main vs backup approach,
  test command, expected result, fallback, switch condition, refresh source, or
  approval boundary. Inspect, ask, lower readiness, or state a validation-backed
  assumption instead.
- Reject `TBD`, `as needed`, "run tests", "verify works", and similar vague
  phrasing unless paired with the exact command/inspection, expected result, and
  failure fallback.
- For process or skill changes, pressure scenarios count as verification only
  when expected behavior and failure condition are explicit.
- For plugin/skill changes, include structural validation, metadata parsing,
  trigger/default-prompt discovery checks, wrapper/output-shape checks when
  relevant, and required local refresh steps as a separate post-plan handoff.
- For dependency-heavy work, output execution slices with objective, inputs,
  preconditions, validation, fallback, owner/actor, and stop condition.

### 6. Handoff To Execution

First emit the DeepPlan output with readiness. After that, follow the host's
normal implementation, approval, editing, and verification rules.

For local plugin updates, confirm the marketplace/source that points at the
edited plugin, validate source files first, use the plugin-creator
cachebuster/update helper when available, and reinstall from the confirmed local
marketplace only after source validation. Do not hand-edit marketplace files to
refresh an installed local plugin. If confirmation or reinstall commands need
approval, external access, or writes outside the current sandbox, name that as
execution handoff work instead of lowering planning rigor. Treat a new
thread/session as the pickup boundary, not as proof that the plan was valid.

## Output And Readiness

Always include objective, final main plan, validation gate, and readiness. Keep
output proportional to risk; do not dump scratch reasoning.

For Full path, also include candidate comparison, eliminated alternatives, one
backup plan, and the switch condition. For Light path, include the
validation-failure fallback instead of a backup plan.

Use stable labels when the host does not impose a stricter format: Objective,
Candidate Comparison, Main Plan, Backup Plan, Switch Condition, Validation Gate,
Assumptions, and Readiness. If the host imposes a wrapper or section order,
preserve these fields inside that format instead of emitting a second block.

- `ready`: evidence is sufficient; the chosen plan, required backup/switch
  condition, and validation gate are executable with no open or hidden decisions.
- `ready_with_assumptions`: execution is reasonable only under named
  assumptions; include how evidence or validation must confirm them.
- `not_ready`: missing evidence or decisions could change the main plan,
  backup, switch condition, or validation gate; include the safest partial plan.

Stop only when critique adds no high/medium risk, no materially different
candidate remains, more reflection would not add evidence, and the chosen plan
plus validation gate are executable. For workflow/process/skill/plugin/policy
reviews, keep only changes that alter future agent behavior; stop when remaining
ideas are explanation-only, style-only, or overfit to the current artifact.
