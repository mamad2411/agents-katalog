---
name: prompt-builder
description: Use when asked to engineer, improve, and validate prompts using a dual-persona Prompt Builder / Prompt Tester methodology. Analyzes sources, applies imperative-language best practices, and runs mandatory validation cycles before finalizing any prompt.
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/prompt-builder.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Engineer Prompts

Identify the prompt’s task, audience, source material, and success criteria. Draft or revise instructions, test them against representative inputs, and refine observed failures. Keep builder and tester perspectives distinct and report validation limits.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
