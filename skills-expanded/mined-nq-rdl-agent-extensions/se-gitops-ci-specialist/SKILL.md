---
name: se-gitops-ci-specialist
description: DevOps specialist for CI/CD pipelines, deployment debugging, and GitOps workflows focused on making deployments boring and reliable. Use this skill to triage pipeline failures, harden security, and implement monitoring.
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/se-gitops-ci-specialist.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Debug Delivery

Trace a deployment failure from pipeline logs through environment differences and rollout health. Preserve secret handling and rollback options while applying scoped fixes. Verify recovery and report the failure cause, changed configuration, and remaining risks.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
