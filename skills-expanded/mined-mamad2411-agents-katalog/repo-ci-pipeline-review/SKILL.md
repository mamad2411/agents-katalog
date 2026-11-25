---
name: repo-ci-pipeline-review
description: Reviews repository CI/CD pipeline configuration and triages CI failures without assuming a specific provider. Use when editing workflow files, build jobs, test jobs, release automation, caches, artifacts, triggers, permissions, or investigating failing CI.
---

# Repo CI Pipeline Review

Use this skill when reviewing CI/CD configuration or triaging CI failures.

## When to Use This Skill

Use this skill for:

- CI workflow edits
- build/test job changes
- release job changes
- deployment job changes
- pipeline permissions
- cache or artifact changes
- matrix, trigger, or schedule changes
- flaky CI triage
- local reproduction of CI failures
- review of pipeline-generated outputs

## Review Approach

1. Identify the CI provider or automation mechanism from repository files.
2. Separate build/test validation from deploy/release/publish behavior.
3. Inspect existing patterns before changing the pipeline.
4. Preserve required checks, approvals, secrets boundaries, and environment gates.
5. Avoid broad formatting or rewriting workflow files.
6. Prefer focused changes with clear validation.
7. Call out validation that cannot be performed locally.

## Workflows

Use:

- `workflows/pipeline-change-review-workflow.md` for pipeline configuration changes.
- `workflows/ci-failure-triage-workflow.md` for CI failure diagnosis.

## Resources

Use:

- `resources/ci-pipeline-risk-checklist.md`

## Scripts

This skill owns:

```text
scripts/ci-config-scan.py
scripts/ci-cd-stop-reminder.py
```

Run scripts with `--help` before manual use.
