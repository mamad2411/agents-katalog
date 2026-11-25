---
name: repo-runbook-writing
description: Creates and reviews operational runbooks, incident procedures, rollback instructions, and support playbooks. Use when documenting operational tasks that require safe commands, validation, escalation, or recovery steps.
---

# Runbook Writing

Use this skill to create or review operational documentation.

## Process

1. State purpose and scope.
2. Identify environment and permissions.
3. Mark destructive or irreversible steps.
4. Use placeholders for environment-specific values and secrets.
5. Include expected output or success criteria.
6. Include validation after each risky operation.
7. Include rollback or recovery steps.
8. Include escalation conditions.

## Workflows

- `workflows/runbook-authoring-workflow.md`
- `workflows/runbook-review-workflow.md`

## Resources

- `resources/runbook-template.md`
- `resources/runbook-quality-checklist.md`

## Examples

- `examples/runbook-example.md`

## Scripts

This skill owns `scripts/runbook-safety-scan.py`. Run it with `--help` before manual use.
