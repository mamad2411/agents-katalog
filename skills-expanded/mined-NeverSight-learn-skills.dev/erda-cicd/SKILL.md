---
name: erda-cicd
description: Operate, troubleshoot, and explain ERDA CI/CD workflows through erda-cli. Use when users need help running pipelines, checking status, reading logs, reviewing build history, or diagnosing delivery failures across the build and deploy path.
---

# ERDA CI/CD

This skill focuses on the real `erda-cli` command surface for pipeline and delivery workflows, not just static YAML editing.

Do not assume repository-level shared files are present when this skill is installed. Start from the skill-local references and scripts first.

This skill is backed by command knowledge and working assets:

- prerequisites and fallback rules: [`references/prerequisites.md`](references/prerequisites.md)
- command guidance: [`references/cli-capabilities.md`](references/cli-capabilities.md)
- diagnostic playbook: [`references/diagnostics.md`](references/diagnostics.md)
- reusable templates: [`assets/templates/basic-pipeline.yml`](assets/templates/basic-pipeline.yml), [`assets/templates/build-release-deploy.yml`](assets/templates/build-release-deploy.yml)
- deterministic prerequisite check: [`scripts/doctor.sh`](scripts/doctor.sh)
- validation prompts: see [`references/cli-capabilities.md`](references/cli-capabilities.md)

## Use This Skill For

- running ERDA pipelines through `erda-cli`
- checking pipeline status, history, and logs
- diagnosing failed or stuck CI/CD flows
- explaining how pipeline and delivery commands fit together
- reviewing pipeline-oriented workflow assumptions when they affect execution
- diagnosing failed or stuck pipelines
- identifying missing branch, workspace, application, or task context

## Workflow

1. Verify CLI availability with the skill-local doctor script or direct probing from [`references/prerequisites.md`](references/prerequisites.md).
2. Identify the repository context, branch, workspace, org, project, and application.
3. Before `pipeline run`, check `git status --short`.
4. If the workspace is dirty, stop. Treat this as a hard prerequisite failure and require the user to commit the intended changes first.
5. Only use a temporary clean clone as a secondary troubleshooting or reproduction technique, not as the default path for running new pipeline content.
6. In a temporary clean clone, verify `git remote -v` and `.erda.d/config` or equivalent project context before running the pipeline.
7. Use the minimal diagnostic sequence from [`references/diagnostics.md`](references/diagnostics.md): `whoami`, `pipeline history`, then `erda-cli -V pipeline run ...`.
8. Separate context discovery failure, permission failure, and pipeline execution failure.
9. When giving commands, prefer exact subcommands and flags over abstract descriptions.

## Review Priorities

- wrong branch or workspace assumptions
- missing pipeline context such as pipeline ID, task name, or application binding
- missing repository context such as `.erda.d/config` or correct `origin`
- confusion between run creation, status inspection, history inspection, and log inspection
- attempts to run pipelines from uncommitted workspace content
- read permission versus run permission mismatches
- delivery failures that are actually earlier build failures
- commands that skip authentication or repository cleanliness requirements

## References

- Prerequisites and fallback: [`references/prerequisites.md`](references/prerequisites.md)
- Command guidance: [`references/cli-capabilities.md`](references/cli-capabilities.md)
- Diagnostics: [`references/diagnostics.md`](references/diagnostics.md)
- Templates: [`assets/templates/basic-pipeline.yml`](assets/templates/basic-pipeline.yml), [`assets/templates/build-release-deploy.yml`](assets/templates/build-release-deploy.yml)
