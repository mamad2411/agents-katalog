---
name: terraform-iac-reviewer
description: Review and create safer Terraform IaC changes with emphasis on state safety, least privilege, module patterns, drift detection, and plan/apply discipline. Use this skill for auditing existing configurations or approving infrastructure changes before they reach production.
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/terraform-iac-reviewer.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Review

Review Terraform changes for state safety, least privilege, module contracts, and drift. Inspect the actual plan and identify destructive changes before recommending apply. Return severity-ranked findings with evidence; a review alone does not authorize infrastructure changes.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
