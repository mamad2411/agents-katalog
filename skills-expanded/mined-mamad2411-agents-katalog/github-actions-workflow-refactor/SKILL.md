---
name: github-actions-workflow-refactor
description: Refactors GitHub Actions workflows into clearer jobs, reusable workflows, composite actions, and shared conventions while preserving behavior and security boundaries.
---


# GitHub Actions Workflow Refactor

Use this skill when reducing workflow duplication, extracting reusable workflows, restructuring matrices, or cleaning up CI/CD YAML.

## Refactor Rules

- Preserve current behavior unless the user asks for behavior changes.
- Do not broaden triggers.
- Do not broaden permissions.
- Do not weaken environment protections.
- Keep secrets scoped to the jobs that need them.
- Validate behavior with a diff and a dry-run plan where possible.

## Workflow

Use `workflows/workflow-refactor-workflow.md`.

## Resources

- `resources/reusable-workflow-checklist.md`

