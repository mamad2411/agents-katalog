---
name: db-migration
description: >
  Reusable method for applying schema migrations in a staging environment.
  Use when the task is a bounded schema change with a known script.
---

# DB Migration Skill

Use this when the task is a schema migration with a known script and a
defined target environment.

## Method

1. Confirm the target environment, script path, and paired rollback script.
2. Check for active long-running writers on the target table before proceeding.
   If any are found, report back and wait for approval before continuing.
3. Verify the rollback script with a dry-run or diff check before applying the
   forward migration.
4. Run the migration script.
5. Verify the schema matches the expected state.
6. Report what changed and confirm the rollback path is still valid.

## Avoid

- Running against production without explicit approval.
- Applying more than one migration per task.
- Treating exit 0 from the migration script as full verification.

## Output

```text
Environment:
Script applied:
Active writers at apply time:
Rollback verified:
Schema diff:
Verification:
Residual risk:
Lesson candidate:
```