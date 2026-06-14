# Dependencies

DeepPlan has no hard runtime or workflow dependencies.

## Optional Integrations

- Superpowers: If an upstream brainstorming pass already produced 2-3
  approaches, reuse those approaches as DeepPlan candidates and audit coverage
  instead of generating duplicate alternatives.
- Codex subagents: Use only when the user explicitly asks for subagents or
  parallel agent work, host tooling supports them, and the plan has independent
  read-heavy critique domains.
- Claude subagents: Use the same role split only when the user explicitly asks
  for subagents or parallel agent work and host policy allows it.
- Official docs or web tools: Use only as evidence sources when current
  external contracts, API/tool behavior, package versions, or explicit user
  lookup requests can change the plan.
- OpenAI Docs MCP: Declared in `skills/deepplan/agents/openai.yaml` as optional
  UI metadata so Codex can surface the right docs tool for OpenAI, Codex, skill,
  plugin, API, or SDK contract checks.

## Dependency Policy

- Do not require users to install Superpowers.
- Do not require subagent support.
- Do not ask for user approval solely because subagents are optional; if the
  user did not explicitly request them, continue with solo critique.
- Do not vendor external workflow skills.
- Do not fail the DeepPlan workflow when optional integrations are unavailable;
  fall back to the solo critique workflow.
- Keep optional integrations as interoperability notes, not activation
  requirements.
- Do not make websearch or external docs lookup a default dependency for local
  planning work.
- Do not fail the DeepPlan workflow merely because the OpenAI Docs MCP is
  unavailable. Use official OpenAI-domain fallback when the contract matters; if
  that still cannot verify the fact, lower readiness instead of guessing.
