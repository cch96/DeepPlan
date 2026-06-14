# Dependencies

DeepPlan has no hard runtime or workflow dependencies.

## Optional Integrations

- Superpowers: If an upstream brainstorming pass already produced 2-3
  approaches, reuse those approaches as DeepPlan candidates and audit coverage
  instead of generating duplicate alternatives.
- Codex subagents: When host tooling and policy allow, use subagents for
  complex, read-heavy critique and independent review.
- Claude subagents: When host tooling and policy allow, use the same role split
  as the Codex subagent flow.

## Dependency Policy

- Do not require users to install Superpowers.
- Do not require subagent support.
- Do not ask for user approval solely because subagents are optional; follow the
  current host's policy and available tools.
- Do not vendor external workflow skills.
- Do not fail the DeepPlan workflow when optional integrations are unavailable;
  fall back to the solo critique workflow.
- Keep optional integrations as interoperability notes, not activation
  requirements.
