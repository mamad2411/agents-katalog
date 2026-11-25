---
name: safe-change-planning
description: Plans repository changes safely before implementation. Use for broad edits, refactors, generated rewrites, dependency updates, migrations, infrastructure changes, production-adjacent work, or any change where rollback and verification matter.
---

# Safe Change Planning

Use this skill to plan changes before editing files or running mutating commands.

## When to Use This Skill

Use this skill for:

- broad changes across many files
- refactors
- dependency upgrades
- generated code updates
- database migrations
- infrastructure or deployment changes
- permission or security configuration changes
- production-adjacent tasks
- tasks involving secrets or private data
- tasks where rollback matters

## Safe Planning Process

1. Restate the requested outcome.
2. Identify the affected areas.
3. Classify risk using `resources/risk-matrix.md`.
4. Inspect relevant files before editing.
5. Prefer minimal, reversible changes.
6. Preserve user work.
7. Define validation before implementation.
8. Identify rollback or recovery steps.
9. Ask for approval before high-risk operations.

## Implementation Constraints

- Do not make broad rewrites when a targeted change is sufficient.
- Do not edit generated files unless the generator is unavailable or the user explicitly requests it.
- Do not regenerate lockfiles casually.
- Do not create migrations without explaining schema/data impact.
- Do not modify deployment or infrastructure files without identifying environment impact.
- Do not touch secrets except to remove, redact, or replace with placeholders.

## Workflow

Use `workflows/safe-change-plan-workflow.md` for complex or high-risk changes.

## Scripts

This skill owns:

```text
scripts/final_safety_reminder.py
```

The root-level `hooks.json` Stop hook calls this script. Run it with `--help` before manual use.
