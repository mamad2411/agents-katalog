---
description: >-
  Strategic pre-code planning for a single feature or goal: explore the
  codebase, weigh approaches with trade-offs, and recommend an implementation
  strategy with risks and open questions. Reason, not sequence — use
  planning:sequence for a file-by-file edit order.
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/plan.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Strategy

Establish the goal, constraints, current architecture, and unresolved decisions. Compare viable approaches and produce a high-level implementation strategy with risks and validation criteria. Keep code unchanged; use the sequence skill when a file-by-file edit order is needed.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
