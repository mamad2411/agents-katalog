---
name: database-migrations-management
description: Manage schema migrations safely. Use when changing database
  structure in a deployed system.
metadata:
  tags: database, migrations, management
---

# Database Migrations

## Use this skill when
- Writing and reviewing schema migrations
- Applying migrations to production safely
- Rolling back and repairing migrations

## Do not use this skill when
- Ad-hoc DDL in production
- Schema design from scratch (use its own skill)

## Instructions
1. Every schema change is a reviewable, numbered migration.
2. Prefer additive changes; avoid destructive or long-locking DDL.
3. Use expand-and-contract for large tables (backfill, then swap).
4. Run migrations in CI against a migrated-staged test DB.
5. Set timeouts and avoid full-table rewrites during peak.
6. Provide a tested rollback or forward-fix path.
7. Mirror production shape before release.

## Checklist
- Migrations are additive first
- No destructive change without a data plan
- Rollback path exists

## Output Format
- Migration | change | lock risk | backfill/rollback plan

## Common Mistakes
- ALTER TABLE dropping columns in prod blindly
- Data-only changes mixed with schema
- Migrations that block traffic for hours
