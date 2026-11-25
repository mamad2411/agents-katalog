---
name: hlbpa
description: >-
  Use when asked for high-level architecture documentation or a big-picture
  review: interfaces, data flows, contracts, failure modes, and accessible
  Mermaid diagrams. Writes documentation only; never changes code or tests.
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/hlbpa.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Architecture

Document interfaces, data flows, contracts, and boundary failure modes from source evidence. Keep implementation code and tests unchanged; write only the requested documentation. Mark unknowns explicitly and use accessible Mermaid diagrams where they clarify the architecture.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
