---
description: Use when the user wants to clean up a codebase by eliminating tech debt, removing unused code, simplifying patterns, and improving dependency hygiene. Applies the "subtract to add value" principle aggressively.
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/janitor.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Clean

Establish which code and dependencies are actually used before removing anything. Simplify one concern at a time and validate retained behavior after each change. Preserve meaningful tests and public contracts; report deletions and verification.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
