# Host Integration

DeepPlan's planning spine is host-agnostic. This reference holds the host-specific
execution mechanics. Read it when handing off on a host that has an output
wrapper, a long-running goal handoff, external-contract docs lookups, or a local
plugin refresh. Nothing here is required to *plan*; it applies only at execution
handoff.

## Output Wrappers

Obey the host's output wrapper. Put the entire DeepPlan contract (objective,
candidate comparison, main plan, backup, switch condition, validation gate,
assumptions, readiness) inside the single host-required wrapper; do not emit a
second raw block. On Codex Plan Mode, that wrapper is `<proposed_plan>` — keep all
DeepPlan fields inside it and do not ask which format to use.

## Long-Running Goal Handoff

For long-running execution on Codex, Goal Mode (`/goal`) is an optional
host-specific handoff, available only after objective, completion criteria, and
validation are explicit. Do not require `/goal` for Claude or other non-Codex
hosts; give them the same execution handoff as plain instructions. Lack of `/goal`
never lowers readiness.

## External-Contract Lookups

For OpenAI, Codex, skills, plugins, Agents SDK, Responses API, or Apps SDK facts,
use official OpenAI docs or the configured docs tool (the OpenAI Docs MCP declared
in `agents/openai.yaml`) before broader web search. If a needed contract stays
unverified, lower readiness to `ready_with_assumptions` or `not_ready` instead of
guessing.

## Local Plugin Refresh

For local plugin updates, confirm the marketplace/source, validate source first,
use the plugin-creator cachebuster helper when available, and reinstall from the
confirmed local marketplace only after validation. Do not hand-edit marketplace
files. If refresh work needs approval, external access, or writes outside the
sandbox, name that handoff without lowering planning rigor. Treat a new
thread/session as the pickup boundary, not as proof that the plan was valid.
