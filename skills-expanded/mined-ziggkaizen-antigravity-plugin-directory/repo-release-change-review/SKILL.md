---
name: repo-release-change-review
description: Reviews release-impacting repository changes such as publishing behavior, approval gates, pipeline secrets, environment promotion, artifact retention, and release automation. Use when a code or configuration change can affect how software is built, released, deployed, or rolled back.
---

# Repo Release Change Review

Use this skill when repository changes could affect delivery, even if they are not inside obvious CI/CD files.

## When to Use This Skill

Use this skill for changes to:

- release scripts
- package metadata
- container build files
- version files
- changelog/release note conventions
- deployment manifests
- environment configs
- pipeline secrets or variables
- approval logic
- artifact retention
- rollback scripts

## Review Principles

1. Identify how the change affects build, test, release, deployment, or rollback.
2. Preserve approval gates and least privilege.
3. Avoid changing multiple release mechanisms at once.
4. Document validation and rollback.
5. Escalate provider-specific details to provider plugins.

## Workflows

Use:

- `workflows/release-impact-review-workflow.md`
- `workflows/pipeline-secret-review-workflow.md`

## Resources

Use:

- `resources/release-change-review-checklist.md`
