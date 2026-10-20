---
name: prisma-7-migration-review
description: Reviews Prisma ORM 7 migrations for destructive SQL, data loss, lock risk, production safety, and merge readiness. Use when schema changes generate migration SQL, when reviewing prisma/migrations files, or when planning migrate deploy.
license: MIT
compatibility: Requires Prisma ORM 7 migration files or a Prisma 7 migration plan.
---

# Prisma ORM 7 Migration Review

Use this skill for migration SQL review, merge readiness, destructive change analysis, and production deployment planning.

## When to Use This Skill

Use this skill when:

- A Prisma migration is created or edited.
- `prisma/schema.prisma` changes.
- Migration SQL contains `DROP`, `TRUNCATE`, `ALTER COLUMN`, enum changes, or raw SQL.
- The user asks whether a migration is safe.
- Preparing production `prisma migrate deploy`.

## Workflows

- `workflows/migration-review-workflow.md`: Use for pre-merge migration review.
- `workflows/production-migration-deploy-workflow.md`: Use for production deploy readiness.

## Resources

- `resources/migration-review-checklist.md`: Main migration review checklist.
- `resources/destructive-sql-patterns.md`: Patterns that require extra review.

## Examples

- `examples/migration-review-report.md`: Review report template.

## Scripts

- `scripts/prisma-migration-safety-check.sh`: Hook helper for destructive Prisma commands and risky migration SQL.

Run scripts with `--help` before using them.

## Operating Guidance

1. Review generated SQL, not only Prisma schema diffs.
2. Treat applied migrations as immutable.
3. Prefer expand-and-contract for risky production changes.
4. Require explicit confirmation for destructive commands.
5. Confirm `prisma generate`, typecheck, and tests after schema/migration changes.
6. Document rollback or forward-fix plan for risky migrations.
