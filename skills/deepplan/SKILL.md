---
name: deepplan
description: Use when refining complex plans, architecture changes, migrations, unclear root-cause fixes, high-risk approaches, or explicit best/elegant/no-omissions/self-review/converged planning requests before execution.
---

# DeepPlan

Pre-execution planning gate: turn an initial plan, rough request, or competing
approaches into one evidence-backed execution plan. Do not implement while this
skill is active. If the user also requested implementation, finish or settle the
DeepPlan output first, then treat execution as a separate phase under the host's
normal editing and verification rules.

## Boundaries

- Planning only: no repo-tracked edits, formatters, commits, deploys,
  migrations, durable external writes, or side-effectful execution.
- If execution is also requested, explicitly end the DeepPlan phase before
  editing files, running formatters, or making durable changes.
- Ground in evidence first: read code, docs, configs, schemas, tests, logs,
  runbooks, and provided plans before asking questions or choosing candidates.
- Run commands only when they clarify evidence and do not change durable state.
- Ask only for preferences, tradeoffs, or missing goals that cannot be
  discovered from the environment.
- If no draft plan exists, infer objective, scope, constraints, and success
  criteria from available evidence before generating candidates.
- Keep alternatives in conversation by default. Create scratch artifacts only
  for user-requested handoff/audit, context limits, or multi-agent coordination;
  prefer runtime-local or `/tmp` paths.

## Evidence Scope

- Start by inventorying available local sources with `rg --files`, manifests,
  docs, tests, schemas, runbooks, logs, and recent diffs when available.
- Read all relevant non-generated text files when the target is small and
  bounded enough to fit context, especially for skill/plugin/process reviews.
- For large repositories, do not blanket-read every file. Read the inventory,
  likely entrypoints, public interfaces/contracts, relevant modules, tests,
  configs, docs/runbooks, and diffs that can change the plan.
- Do not spend context on vendor trees, caches, build artifacts, binaries,
  generated files, secrets, or unrelated directories unless the plan depends on
  them.
- If an unread local source could materially change the main plan, backup plan,
  or validation gate, return `ready_with_assumptions` or `not_ready` and name
  the missing evidence.

## External Evidence

- Do not use generic websearch by default. Prefer local code and primary
  project documentation unless an external fact can change the plan.
- Use official or primary external sources when the plan depends on current API
  behavior, SDK/tool/plugin formats, package versions, laws, pricing, release
  status, service limits, or the user explicitly asks for lookup.
- For OpenAI, Codex, skills, plugins, Agents SDK, Responses API, or Apps SDK
  facts, use official OpenAI documentation or configured docs tools before any
  broader web search.
- If required external evidence is unavailable or unverified, do not label the
  plan `ready`; state the dependency and the safest partial plan or validation.

## Use Or Skip

Use DeepPlan for architecture/module-boundary changes; migrations,
compatibility, rollout, or irreversible state; unclear root cause or multiple
fixes; multi-module or high-regression work; long-running/expensive operations;
skill/process/policy design; and requests for deep, best, elegant,
no-omissions, self-review, or converged planning.

Skip it for trivial syntax fixes, one-field edits, simple path/config updates,
or failures with verified root cause and an obvious patch. If the user
explicitly invokes DeepPlan for trivial work, use the Light path and keep the
output short instead of running a full review.

## Depth Gate

Choose the path after grounding, then upgrade when new evidence raises risk.

- Full path: required when any risk is high, or two are medium: uncertainty,
  blast radius, irreversibility, validation difficulty, failure cost, or
  dependency-chain length.
- Full path: also required for explicit deep/best/elegant/no-omissions/
  self-review/converged requests, DeepPlan self-review or optimization, and
  nontrivial skill/process/policy changes.
- Light path: allowed only when scope is small, facts are clear, validation is
  obvious, no public API/schema/data/deploy/durable-state risk exists, and the
  user did not request deep/no-omissions/converged planning.
- Upgrade from Light path immediately if you find a new evidence gap, candidate
  category, medium/high risk, unclear validation, or long dependency chain.

Read `references/depth-and-pressure.md` for Full path domain lenses,
dependency-chain slicing, and pressure scenarios.

## Workflow

### 1. Ground The Work

- State the inferred objective, scope, constraints, and success criteria.
- Separate confirmed facts from guesses.
- Identify public interfaces, data/state boundaries, dependencies, and
  validation surfaces that could change the plan.
- If grounding reveals an unresolved user preference that could change the main
  plan, ask before finalizing.

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
  or a missing materially different strategy.
- Default candidate set when needed: minimal safe change, robust long-term
  design, and compromise architecture.
- Each candidate needs hypothesis, planned changes, validation, risks, and an
  elimination condition.

### 4. Critique And Compare

- Run one critique round by default.
- Run a second round when critique finds high/medium risk, a new candidate
  category, an evidence gap, or unresolved tradeoff.
- Run a third round only for a new high-risk blocker.
- Always cover architecture, implementation, tests, risk, and simplicity. Add
  security/privacy, performance/cost, rollout, compatibility, product, or domain
  evidence only when relevant.

Optional integrations stay optional. Use subagents only when the host supports
them, policy permits them, and the Full path has 2+ independent read-heavy
critique domains. Do not ask for permission solely because subagents are
optional. If unavailable or inappropriate, continue with solo critique.

For skill/process/policy changes, pressure-check the relevant scenarios in
`references/depth-and-pressure.md` or define an equivalent scenario before
converging.

### 5. Converge

- Compare candidates on root-cause coverage, risk, testability,
  maintainability, simplicity, and elimination conditions.
- Eliminate weaker candidates with reasons.
- Full path must end with exactly one main plan, one backup plan, and a switch
  condition.
- Light path must end with a concrete validation gate and the next inspection if
  validation fails.
- For complex/high-risk plans, run a final adversarial check for fatal issues,
  evidence gaps, hidden regressions, and smaller equivalent plans.

### 6. Define The Verification Gate

Every final plan needs:

- Pre-change evidence for the current issue, risk, or requirement.
- Exact command, test, log, inspection, or reproduction to run after execution.
- Expected result for each validation step.
- Next inspection or fallback when validation fails.
- Avoid generic gates such as "run tests" unless they name the expected signal
  and what failure would inspect next.

For dependency-heavy work, output execution-ready slices with objective, inputs,
preconditions, validation, fallback, owner/actor, and stop condition.

## Stop Rules

Stop only when the latest critique adds no high/medium risk, no materially
different candidate remains, continuing would not add evidence, and the chosen
plan plus validation gate are executable.

Full path also requires candidate comparison, eliminated alternatives, one
backup plan, and the switch condition. Light path requires the
validation-failure fallback.

Do not stop because "there is no more feedback." If reflection will not add
evidence, switch to inspection, tests, logs, or minimal reproduction.

## Readiness Labels

- `ready`: evidence is sufficient; the chosen plan, backup/switch condition when
  required, and validation gate are executable with no open decisions.
- `ready_with_assumptions`: execution is reasonable only under named
  assumptions; include what evidence or validation must confirm each assumption.
- `not_ready`: missing evidence or decisions could change the main plan,
  backup, or validation gate; include the safest partial plan.

Never label a plan `ready` when unverified external dependencies, evidence
gaps, or unresolved user preferences could change the plan.

## Final Output

Always include objective, final main plan, validation gate, and readiness. Keep
the output proportional to the risk; do not dump scratch reasoning, and include
optional sections only when they change the execution decision.

For Full path, also include candidate comparison, eliminated alternatives, one
backup plan, and the switch condition. For Light path, include the
validation-failure fallback instead of a backup plan.

Add only when relevant: facts/guesses, root-cause hypotheses, risks, regression
points, dependency slices, and convergence log.

For skill/process/policy reviews, keep only changes that alter future agent
behavior. Pressure-check missed triggers, premature execution, missing
validation, optional dependency misuse, over-planning, context clutter, and
host output wrapper compatibility.

If the host requires a final-plan wrapper or format, follow it and place the
DeepPlan output contract inside that wrapper.
