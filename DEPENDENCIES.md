# Dependencies

DeepPlan has no hard runtime or workflow dependencies.

## Optional Integrations

- Superpowers: Reuse upstream 2-3 approach brainstorming as the candidate pool
  and audit coverage instead of duplicating alternatives.
- Codex or Claude subagents: optional, read-only critique help on explicit user
  request or a managed `AGENTS.md` opt-in with independent read-heavy domains.
  Full modes, precedence, and limits in
  `skills/deepplan/references/subagent-opt-in.md`.
- Official docs or web tools: Use only when current external contracts,
  API/tool behavior, package versions, or explicit lookup requests can change
  the plan.
- OpenAI Docs MCP: Declared in `skills/deepplan/agents/openai.yaml` as optional
  UI metadata for OpenAI, Codex, skill, plugin, API, and SDK contract checks.

## Policy

- Do not require Superpowers, subagents, external docs lookup, or OpenAI Docs
  MCP for local planning work.
- Do not ask for approval solely because optional subagents are available.
- Do not vendor external workflow skills.
- Continue with solo critique when optional integrations are unavailable,
  unrequested, or inappropriate; do not pad lens-roles or create fake debate
  roles.
- If an OpenAI/Codex contract matters and cannot be verified through configured
  docs or official OpenAI-domain fallback, lower readiness instead of guessing.

## Maintenance Dependencies

Runtime DeepPlan usage has no hard dependency on plugin-creator, PyYAML, or
subagent tooling. Local maintenance validation uses:

- Python 3 with the standard library for `scripts/configure_subagents.py`.
- PyYAML for validating `skills/deepplan/agents/openai.yaml`.
- The plugin-creator validator, discovered from
  `$DEEPPLAN_PLUGIN_VALIDATOR` or
  `$CODEX_HOME/skills/.system/plugin-creator/scripts/validate_plugin.py`.
