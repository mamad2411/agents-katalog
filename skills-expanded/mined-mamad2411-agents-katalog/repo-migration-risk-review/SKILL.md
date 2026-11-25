---
name: repo-migration-risk-review
description: Reviews database migrations, ORM schema changes, seed scripts, and migration commands for destructive operations, reversibility, locking risk, data loss, production impact, and rollout sequencing. Use before editing, applying, or approving migrations.
---

# Repository Migration Risk Review

Use this skill to review migration-related repository changes before implementation, merge, or execution.

## When to Use This Skill

Use this skill for:

- migration files
- ORM schema files
- seed scripts
- generated migration SQL
- migration commands
- rollback scripts
- schema diff output
- database cleanup or repair scripts
- imports, exports, and backfills that change persistent state

## Review Focus

1. **Destructiveness**
   - Drops, truncates, deletes, renames, overwrites, resets, and destructive constraint changes.
2. **Reversibility**
   - Whether rollback is possible and realistic.
3. **Compatibility**
   - Whether old and new application versions can coexist.
4. **Data integrity**
   - Constraints, foreign keys, nullability, uniqueness, indexes, and referential safety.
5. **Operational risk**
   - Locks, long-running statements, batching, retries, resumability, and deployment sequencing.
6. **Environment risk**
   - Production or shared environment targeting.
7. **Privacy**
   - Production data, dumps, exports, and sensitive records.

## Workflow

Use `workflows/migration-risk-review-workflow.md` before applying or approving migrations.

## Resources

Use `resources/migration-risk-checklist.md` for a review checklist.

## Scripts

This skill owns:

```text
scripts/migration-risk-scan.py
scripts/guard-data-migration-command.py
```

The root-level `hooks.json` calls `scripts/guard-data-migration-command.py`. Run scripts with `--help` before manual use.
