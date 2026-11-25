---
name: repo-backup-rollback-planning
description: Plans backup, restore, rollback, and forward-fix strategies for high-risk data and migration operations. Use before destructive migrations, production data changes, imports, exports, cleanup scripts, and irreversible transformations.
---

# Repository Backup and Rollback Planning

Use this skill before high-risk migration or data operations where recovery matters.

## When to Use This Skill

Use this skill for:

- destructive migrations
- production data changes
- irreversible transformations
- imports and exports
- cleanup scripts
- rollback procedures
- restore procedures
- data repair scripts
- incident follow-up involving data correction

## Recovery Planning Requirements

A good plan should identify:

1. what can fail
2. whether rollback is safe
3. whether forward-fix is safer
4. backup or snapshot availability
5. restore scope and time expectations
6. validation queries or checks
7. who must approve the operation
8. what evidence must be captured
9. when to stop or abort

## Workflow

Use `workflows/backup-rollback-plan-workflow.md` before high-risk data operations.

## Resources

Use `resources/rollback-readiness-checklist.md`.

## Scripts

This skill owns:

```text
scripts/data-migration-stop-reminder.py
```

The root-level `hooks.json` Stop hook calls this script. Run it with `--help` before manual use.
