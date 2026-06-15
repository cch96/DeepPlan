# Subagent Opt-In

DeepPlan is conservative by default. It does not spawn subagents only because a
task is complex. Codex subagents consume additional tokens, inherit the parent
sandbox and approval policy, and should be used only when the user has made
that delegation intent explicit.

`scripts/configure_subagents.py` can add a managed block to a repository
`AGENTS.md`. The block is durable project guidance. It is not a Codex
permission primitive and does not change filesystem, network, sandbox,
approval, model, custom-agent, thread-depth, or host policy.

## First-Use Prompt

When no explicit user request and no `allow-readonly-subagents` block applies,
DeepPlan may ask on the first suitable subagent use in the current session. The
prompt is session-scoped for the active repository and only appears after
grounding confirms a Full-path task, host support, policy permission, no closer
"no subagents" rule, and two to four independent read-heavy domains that could
change the main plan, backup, switch condition, validation gate, or readiness.

The prompt is an ephemeral current-task authorization path, not durable repo
policy:

- `Use for this task`: authorize bounded read-only/explorer subagents for the
  current task only.
- `Use now and enable repo`: authorize the current task and add a post-DeepPlan
  execution handoff to run `python3 scripts/configure_subagents.py --repo
  <repo> --mode allow-readonly-subagents --write`. Future sessions may rely on
  the durable block only after it is written and a new session starts.
- `Do not use`: continue with solo critique for this task/session opportunity
  and do not lower readiness.

The first-use prompt must not spawn subagents before the user chooses, must not
write `AGENTS.md` while DeepPlan is active, and must not treat install, update,
cachebuster, or reinstall work as subagent authorization.

## Modes

### suggest-only

DeepPlan may notice that a Full-path planning task has two to four independent
read-heavy evidence domains and recommend a bounded subagent lineup. It must
stop and wait for the current user to approve subagents or parallel agent work
before spawning any agent.

Use this mode when a repository wants a reminder to delegate without committing
token spend automatically.

### allow-readonly-subagents

The managed block is a standing explicit request for DeepPlan to use direct
read-only/explorer subagents when all of these are true:

- The active task is a Full-path DeepPlan task.
- Two to four independent read-heavy evidence domains exist.
- Each subagent output could change the main plan, backup, switch condition,
  validation gate, or readiness.
- The host exposes subagent tools and policy permits them.
- No current user instruction or closer project instruction forbids subagents.

This mode authorizes DeepPlan's decision to spawn bounded read-heavy subagents.
It does not authorize write-heavy worker subagents while DeepPlan is active.

### remove

`remove` is a script action, not a persistent mode. It deletes only the managed
DeepPlan block and preserves surrounding `AGENTS.md` content.

## Managed Markers

The script owns only this region:

```md
<!-- deepplan-subagents:start -->
...
<!-- deepplan-subagents:end -->
```

The script must fail closed when markers are malformed, mismatched, duplicated,
or appear in an unexpected order. Re-running the same mode must be byte-stable.
Mode replacement must replace the existing managed block rather than appending a
second block.

## Precedence

Codex loads `AGENTS.md` files from broader to narrower scopes. A current user
message, a closer `AGENTS.md`, or any `AGENTS.override.md` can override this
block. If the current user says not to use subagents, DeepPlan must not use
subagents for that task.

If root `AGENTS.override.md` is non-empty, the configuration script refuses to
write the root `AGENTS.md` block because that block may be ignored. A
"no subagents" instruction always wins for the current task.

## Subagent Limits

When subagents are allowed:

- Use direct child agents only; no recursive delegation.
- Use two to four subagents, and fewer when fewer independent domains exist.
- Do not use CSV fan-out.
- Do not use role padding, duplicate reviewers, or fake debate roles.
- Prefer read-heavy exploration, critique, testing, and summarization.
- The parent agent owns integration, final judgment, and readiness.
- Close completed agents after harvesting results.

Subagents gather evidence. They do not become alternate owners of user intent,
project policy, or DeepPlan's final plan.
