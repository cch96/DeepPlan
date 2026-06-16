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

Host-specific execution mechanics (output wrappers, long-running goal handoff,
external-contract docs lookups, local plugin refresh) live in
`references/host-integration.md`; the planning spine below is host-agnostic.

## Process At A Glance

1. Ground in local evidence before asking questions or choosing candidates.
2. Choose Light or Full depth by blast radius; for broad "improve/optimize"
   requests, lock the optimization axis after grounding.
3. Verify root cause before fix candidates when failures are unclear.
4. Build or audit the candidate pool before selecting the main plan.
5. Critique and converge to one plan (plus a backup and switch condition on
   Full), define validation, and run the actionability gate.
6. Emit readiness, then hand off. Do no execution work while DeepPlan is active.

DeepPlan self-review and nontrivial workflow/process/skill/plugin/policy changes
use the Full path even when the likely patch is mostly wording. Each step is
detailed in the sections below.

## Use And Depth

Use DeepPlan for complex, high-blast, or irreversible work: architecture/module-
boundary changes, migrations, rollout, unclear root cause, multi-module or high-
regression work, long-running or expensive operations, workflow/process/skill/
plugin/policy design, and explicit deep/no-omissions/self-review/converged
requests. Skip trivial syntax/one-field/path/config edits and failures with a
verified root cause and an obvious patch; if explicitly invoked for trivial work,
use Light and keep the output short.

Depth scales by blast radius and irreversibility, not apparent task size.

| | Light path | Full path |
|---|---|---|
| Use when | small scope, clear facts, obvious validation, and no public-API / schema / data / deploy / durable-state risk; no deep/no-omissions/converged request | any high risk, or two medium risks across uncertainty / blast radius / irreversibility / validation difficulty / failure cost / dependency-chain length; an explicit deep/no-omissions/converged request; DeepPlan self-review; a nontrivial workflow/skill/plugin/policy change; host-wrapper or external-contract risk; a first-pass plan where a missed assumption could invalidate it |
| Output ends with | one validation gate + the next inspection if it fails | exactly one main plan + one backup + a switch condition + a validation gate |

Upgrade from Light to Full when evidence exposes a gap, a candidate category,
medium/high risk, unclear validation, or a long dependency chain.

Read `references/depth-and-pressure.md` for Full path lenses, dependency-chain
slicing, and pressure scenarios. Read `references/subagent-opt-in.md` before
treating repository `AGENTS.md` guidance as standing subagent authorization.

## Boundaries And Evidence

- Planning only: no repo-tracked edits, formatters, generated specs, commits,
  deploys, migrations, package or plugin installs, durable external writes, or
  other side-effectful execution. Run only commands that clarify evidence without
  changing durable state.
- Keep alternatives in conversation by default. Create scratch artifacts only
  for user-requested handoff/audit, context limits, or multi-agent coordination;
  prefer runtime-local or `/tmp` paths.
- Obey host collaboration mode, output wrapper, approval rules, and tool limits.
  Put the entire DeepPlan contract inside any single host-required wrapper; do not
  emit a second raw block.
- If another workflow normally requires design docs, commits, worktrees,
  implementation plans, or other artifacts, defer them until after DeepPlan
  readiness is emitted. If later execution needs write approval, external
  access, or durable side effects, name that approval in the handoff instead of
  performing it.

### Grounding Rules

- Infer objective, scope, constraints, and success criteria from local evidence
  before questions or candidates.
- Start with `rg --files`, manifests, docs, tests, schemas, runbooks, logs, and
  recent diffs. For small bounded targets, read all relevant non-generated text.
- For workflow/process/skill/plugin reviews, include manifests, metadata,
  references, README/dependency notes, validation scripts, published contracts,
  and configured install/execution sources.
- For DeepPlan/plugin self-review, include Codex and Claude manifests,
  `SKILL.md`, frontmatter trigger metadata, agent/default prompts, references,
  README, dependencies, and discoverable local install/cache sources before
  claiming readiness.
- For large repositories, inventory first, then read likely entrypoints, public
  contracts, relevant modules, tests, configs, docs/runbooks, and diffs; avoid
  vendor/cache/build/binary/generated/secret/unrelated trees unless they can
  change the plan.
- Ask only for preferences, tradeoffs, missing goals, scope boundaries, or risk
  tolerance that local evidence cannot answer.
- Do not use generic websearch by default. Use official or primary sources only
  when current external contracts, APIs, SDK/tool behavior, package versions,
  laws, pricing, releases, or explicit lookup requests can change the plan; prefer
  the host's configured docs tool over broad web search (see
  `references/host-integration.md`).
- If unread local sources or unverified external evidence could change the main
  plan, backup, switch condition, or validation gate, do not label the plan
  `ready`.

### Optimization Requests

- For broad requests ("optimize this", "improve this plugin"), infer the likely
  axes from evidence first (reliability, token length, user experience, metadata/
  installability, validation coverage, maintainability). If two or more axes would
  produce materially different edits, ask one focused question or state the
  recommended default as an assumption, and name the chosen optimization axis in
  the Objective or Assumptions before emitting `ready`.
- Repeated optimization must have a behavior delta: classify it as
  `new_behavior_gap`, `validation_gap`, `metadata_drift`, or `no_material_delta`;
  only the first three justify source edits, and `no_material_delta` returns a
  no-source-edit plan with validation. See `references/depth-and-pressure.md`
  (`## Self-Optimization Classification`) for the taxonomy and what counts as a
  delta.

## Workflow

### 1. Ground And Scan Breadth

State inferred objective, scope, constraints, success criteria, confirmed facts,
and guesses. Identify public interfaces, data/state boundaries, dependencies,
integration points, host constraints, validation surfaces, reversibility/
recovery, and failure modes that could change the plan.

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
candidates unless already known. List 3-5 plausible causes with supporting and
disconfirming evidence, smallest validation, and smallest fix if true. Eliminate
at least two alternatives before `ready`; otherwise return
`ready_with_assumptions` or `not_ready`.

### 3. Build Candidates

- Reuse supplied 2-3 real approaches and audit coverage instead of duplicating
  equivalent tradeoffs.
- Add candidates only for one-option inputs, shallow variants, or a missing
  materially different strategy that could change the plan, backup, switch
  condition, readiness, or validation gate. Default set when needed: minimal
  safe change, robust long-term design, and compromise architecture.
- Each candidate needs hypothesis, planned changes, validation, risks, and an
  elimination condition. Do not fabricate template candidates. Collapse wording
  or sequencing tunings as variants and use Light unless the Depth Gate requires
  Full.
- Full path must still name a real backup and its switch condition.

### 4. Critique And Compare

- Run one critique round by default; run a second for high/medium risk, a new
  candidate category, an evidence gap, or unresolved tradeoff; run a third only
  for a new high-risk blocker. Stop when another round would not change the main
  plan, backup, switch condition, readiness, or validation gate.
- Use lenses as perspectives, not mandatory roles: correctness/feasibility, user
  intent/scope, failure modes/reversibility, validation,
  maintainability/operability, and simplicity. Add domain lenses only when
  relevant.
- Critique solo by default. Use subagents only on explicit user request (or a
  permitted DeepPlan-managed `AGENTS.md` opt-in block) AND when the plan is Full
  with 2+ independent read-heavy evidence domains; then select 2-4 lens-roles
  after grounding. Otherwise stay solo, and optional subagents never block or
  weaken readiness. See `references/subagent-opt-in.md` for modes, precedence,
  and limits.
- For workflow/process/skill/plugin/policy changes, pressure-check only relevant
  scenarios from `references/depth-and-pressure.md`; output only results that
  affect approach, validation, readiness, backup, or switch condition.

### 5. Converge And Verify

- Compare candidates on root-cause coverage, risk, testability,
  maintainability, simplicity, and elimination conditions.
- Full path must end with exactly one main plan, one backup, and a switch
  condition. Light path must end with one validation gate and the next inspection
  if validation fails.
- For complex/high-risk plans, run a final adversarial check for fatal issues,
  evidence gaps, hidden regressions, and smaller equivalent plans. Make the
  recommendation execution-ready: ordered steps, assumptions, material risks/
  mitigations, decision points, verification/acceptance criteria, and
  confirmation points for irreversible steps.
- Every validation gate needs pre-change evidence, an exact command/test/log/
  inspection/reproduction, an expected result, and the next inspection or
  fallback.
- Run an actionability gate before `ready`: if any of the following is still open,
  inspect, ask, lower readiness, or state a validation-backed assumption instead
  of leaving it to the implementer:
  - the optimization axis;
  - the files/modules to touch;
  - the main vs backup approach;
  - the edit / no-edit classification;
  - the test command and its expected result;
  - the fallback and the switch condition;
  - the refresh source or approval boundary.
- Reject `TBD`, `as needed`, "run tests", "verify works", and similar vague
  phrasing unless paired with exact command/inspection, expected result, and
  failure fallback.
- For process/skill changes, pressure scenarios count as verification only with
  explicit expected behavior and failure condition. For plugin/skill changes, add
  structural validation, metadata/trigger/default-prompt discovery checks, and any
  required local refresh as a separate post-plan handoff.
- For dependency-heavy work, output slices with objective, inputs, preconditions,
  validation, fallback, owner/actor, and stop condition.

### 6. Handoff To Execution

First emit the DeepPlan output with readiness. After that, follow the host's
normal implementation, approval, editing, and verification rules. If later
execution needs write approval, external access, or durable side effects, name
that approval in the handoff instead of performing it. Treat a new thread/session
as the pickup boundary, not as proof that the plan was valid.

On a host with an output wrapper, a long-running goal handoff, external-contract
lookups, or a local plugin refresh, read `references/host-integration.md` for the
host-specific procedure before handing off.

## Output And Readiness

Always include objective, final main plan, validation gate, and readiness. Keep
output proportional to risk; do not dump scratch reasoning. Full path also
includes candidate comparison, eliminated alternatives, one backup, and the
switch condition. Light path includes the validation-failure fallback instead of
a backup.

Use stable labels when the host does not impose a stricter format: Objective,
Candidate Comparison, Main Plan, Backup Plan, Switch Condition, Validation Gate,
Assumptions, and Readiness. If the host imposes a wrapper or section order,
preserve these fields inside that format instead of emitting a second block.

| Readiness | When | Must also include |
|---|---|---|
| `ready` | evidence is sufficient; the chosen plan, backup/switch condition, and validation gate are executable with no open or hidden decisions | — |
| `ready_with_assumptions` | execution is reasonable only under named assumptions | how evidence or validation will confirm each assumption |
| `not_ready` | missing evidence or decisions could change the main plan, backup, switch condition, or validation gate | the safest partial plan / step-zero evidence task |

Stop only when critique adds no high/medium risk, no materially different
candidate remains, more reflection would not add evidence, and the chosen plan
plus validation gate are executable. For workflow/process/skill/plugin/policy
reviews, keep only future-behavior changes; stop when remaining ideas are
explanation-only, style-only, or overfit to the current artifact.
