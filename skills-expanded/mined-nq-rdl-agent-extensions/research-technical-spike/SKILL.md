---
name: research-technical-spike
description: Use when asked to validate a technical spike document through exhaustive, recursive research; it mines documentation, analyzes code patterns, runs experiments with permission, and continuously updates the spike with structured findings.
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/research-technical-spike.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Research

Identify the spike’s hypotheses, evidence gaps, and decision criteria. Research authoritative documentation and source code, run only authorized experiments, and update the requested spike document. Separate observations, assumptions, and unresolved questions.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
