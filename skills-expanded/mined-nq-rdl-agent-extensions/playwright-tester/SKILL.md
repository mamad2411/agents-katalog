---
name: playwright-tester
description: Use when the user wants to generate, improve, or debug Playwright end-to-end tests for a web application. Explores the live site before writing tests, then iterates until all tests pass reliably.
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/playwright-tester.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Test

Explore the running site and capture page evidence before writing or changing tests. Derive locators from the observed UI, implement tests in the project’s established language, and run the relevant flows. Report what passed, remaining failures, and any inaccessible environment.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
