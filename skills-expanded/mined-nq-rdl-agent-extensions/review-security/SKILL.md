---
description: Use when the user wants a security review of code, configurations, or architectural patterns. Identifies vulnerabilities with severity ratings and provides specific, implementable fixes.
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/wg-code-sentinel.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Review Security

Trace concrete security risks in the requested code, configuration, or architecture. Rank findings by severity with locations, attack conditions, implementable fixes, and verification steps. Keep a review read-only unless fixes are requested.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
