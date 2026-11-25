---
description: >-
  Sequence a multi-file change: map every affected file, trace dependencies, and
  emit an ordered edit plan before any code is touched. File-level ordering, not
  strategy — use planning:strategy to choose what to build.
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/context-architect.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Sequence

Map affected files, dependencies, existing patterns, and test coverage before implementation. Return an ordered edit plan with ripple effects and potential breaking changes. This task produces a plan; it does not authorize implementation.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
