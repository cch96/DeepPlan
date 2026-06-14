# Dependencies

DeepPlan has no hard runtime or workflow dependencies.

## Optional Integrations

- Superpowers: Reuse upstream 2-3 approach brainstorming as the candidate pool
  and audit coverage instead of duplicating alternatives.
- Codex or Claude subagents: Use only when the user explicitly asks for
  subagents or parallel agent work, host policy permits it, and the plan has
  independent read-heavy critique domains.
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
  unrequested, or inappropriate.
- If an OpenAI/Codex contract matters and cannot be verified through configured
  docs or official OpenAI-domain fallback, lower readiness instead of guessing.
