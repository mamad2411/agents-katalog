---
description: GitHub Actions specialist focused on secure CI/CD workflows, action pinning to full commit SHAs, OIDC authentication, least-privilege permissions, and supply-chain security. Delegate workflow authoring and security hardening with this skill.
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/github-actions-expert.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Actions

Inspect workflow triggers, permissions, action references, and deployment boundaries. Pin actions to verified full commit SHAs, use least privilege and OIDC where applicable, and validate changed workflows with actionlint. Verify version-sensitive behavior against GitHub’s official documentation.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
