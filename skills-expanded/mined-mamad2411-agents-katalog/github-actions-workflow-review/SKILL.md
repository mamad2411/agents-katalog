---
name: github-actions-workflow-review
description: Reviews GitHub Actions workflow files for trigger safety, permissions, jobs, steps, shell commands, caches, artifacts, deployments, reusable workflows, and maintainability. Use when editing or reviewing .github/workflows YAML files.
---


# GitHub Actions Workflow Review

Use this skill when reviewing or editing `.github/workflows/*.yml` or `.github/workflows/*.yaml`.

## Review Focus

1. Events and triggers
2. Workflow and job permissions
3. Job dependencies and conditions
4. Runner labels and trust boundaries
5. Shell commands and untrusted inputs
6. Third-party actions and reusable workflows
7. Secrets, variables, and environments
8. Cache keys and artifact handling
9. CI reliability and deployment safety
10. Maintainability and naming

## Workflow

Use `workflows/workflow-review-workflow.md`.

## Resources

- `resources/workflow-risk-matrix.md`

## Scripts

This skill owns:

```text
scripts/scan-github-actions-workflows.py
scripts/guard-github-actions-tool-use.py
```

Run scripts with `--help` before manual use.

