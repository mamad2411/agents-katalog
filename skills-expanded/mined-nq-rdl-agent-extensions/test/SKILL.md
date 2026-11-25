---
description: Generate and refactor Go Terratest suites for Terraform modules, including CI-safe patterns, staged tests, and negative-path validation. Use this skill when creating or improving test coverage for Terraform modules.
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/terratest-module-testing.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Test

Inspect module inputs, expected outputs, and existing Go test conventions. Build staged Terratest coverage with unique resource names, reliable cleanup, and negative cases. Separate local validation from cloud tests that create billable resources and report which ran.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
