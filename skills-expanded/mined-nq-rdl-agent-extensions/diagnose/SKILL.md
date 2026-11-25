---
description: 'Use when the user reports a bug, test failure, or unexpected behavior and wants it systematically diagnosed and fixed. Follows a four-phase methodology: assess, investigate, resolve, and quality-assure.'
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/debug.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Diagnose

Reproduce the reported failure, trace its cause, and test a specific hypothesis before editing. Make a scoped fix, rerun the reproduction, and check relevant regression tests. Report the cause, changed files, and verification results.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
