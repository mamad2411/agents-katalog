---
name: postgresql-18-migration-review
description: Reviews PostgreSQL 18 migrations for security, lock behavior, rollback risk, destructive DDL, data backfills, privilege changes, and operational safety. Use when a task mentions migrations, DDL rollout, schema changes, backfills, rollback, backup, restore, or migration diffs.
license: MIT
compatibility: PostgreSQL 18 release line; scripts require bash and git for changed-file hook scans.
---

# PostgreSQL 18 Migration Review

Use this skill for migration design, migration diff review, destructive DDL checks, backfills, rollback planning, backup/restore readiness, and safe production rollout sequencing.

## Start Here

1. Confirm source and target PostgreSQL versions.
2. Identify the migration tool and whether it wraps migrations in transactions.
3. Identify whether the target is local, test, staging, or production.
4. Inspect table sizes, write rates, replication, backups, and maintenance windows when relevant.
5. Use supporting files:
   - `resources/migration-risk-matrix.md`
   - `examples/zero-downtime-migration-examples.md`
6. Run scripts with `--help` before using them:
   - `scripts/postgresql-18-migration-diff-review.sh`
   - `scripts/postgresql-18-dangerous-ddl-check.sh`

## Review Principles

- Treat migrations as security-sensitive and rollback-sensitive.
- Prefer additive expand/contract migrations.
- Split schema changes, data backfills, constraint validation, and cleanup.
- Identify locks, table rewrites, replication impact, and transaction behavior.
- Add validation and rollback/forward-fix steps.
- Require explicit approval for destructive DDL/DML.
- For trust-critical flows, review state transition integrity, uniqueness, replay defense, and privilege changes.

## Workflows

Use:

- `workflows/migration-review-workflow.md` for migration diff review.
- `workflows/backup-restore-drill-workflow.md` before irreversible or high-risk operations.

## Expected Output

For migration tasks, provide:

- Risk classification.
- Lock/rewrite analysis.
- Rollout sequence.
- Validation SQL.
- Rollback/forward-fix plan.
- Approval gates.
