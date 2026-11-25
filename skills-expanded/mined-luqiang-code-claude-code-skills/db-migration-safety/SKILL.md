---
name: db-migration-safety
description: |
  Review database migrations for safety: locking, rollback, data loss, and
  performance risks. Triggers on "review migration", "check migration", "migration safety".
metadata:
  type: tool
  version: "1.0.0"
  author: community
  tags: [database, migration, postgresql, mysql, safety]
triggers:
  - "review migration"
  - "check migration"
  - "migration safety"
  - "is this migration safe"
allowed-tools:
  - Read
  - Bash
---

# Database Migration Safety Review

Review migrations for safety risks before they hit production.

## When to Use
- About to run a migration on a large table
- Reviewing a PR with migration files
- User mentions "migration", "schema change", "alter table"

## When NOT to Use
- Writing new migrations (use normal review for that)
- NoSQL databases (different safety profile)
- Small dev databases with no data

## Workflow
1. Read the migration file(s)
2. For each operation, check:

### Adding a column
- Does it have a DEFAULT? (instant in PG11+, slow without)
- Is it NOT NULL without DEFAULT? (DANGER: will fail on existing rows)
- Is there a backfill plan for existing rows?

### Removing a column
- Are there any code references still using it? (grep the codebase)
- Is it part of any indexes or constraints?

### Adding an index
- Is it CREATE INDEX CONCURRENTLY? (non-blocking, preferred)
- Estimated index size and creation time on table with N rows?

### Changing a column type
- Will it lock the table? (most type changes require ACCESS EXCLUSIVE lock)
- Is there data that won't convert cleanly?

### Adding a foreign key
- Are both tables on the same database?
- Is the referenced column indexed?

3. Check for rollback safety: does the `down` migration actually revert the `up`?
4. Flag any operations that will cause downtime
5. Output a risk assessment

## Output Format
```
## Migration Safety Review: 0042_add_user_preferences.sql

### Risk: HIGH
- Line 12: ALTER TABLE users ADD COLUMN preferences JSONB NOT NULL
  → Will fail if users table has rows. Add DEFAULT '{}' first.

### Risk: MEDIUM
- Line 8: CREATE INDEX idx_users_email ON users(email)
  → Consider CREATE INDEX CONCURRENTLY to avoid table lock
  → Table has ~500K rows, estimated time: ~3s

### Safe
- Line 3: CREATE TABLE user_preferences — new table, no risk
- Line 15: ALTER TABLE users ADD COLUMN timezone VARCHAR DEFAULT 'UTC' — has DEFAULT, PG11+, instant

### Rollback: PARTIAL
- Down migration removes user_preferences table (destructive, data loss)
  → Consider RENAME instead of DROP for rollback safety
```

## Notes
- PostgreSQL: ACCESS EXCLUSIVE locks block ALL reads and writes
- For large tables (>1M rows), almost any ALTER needs a maintenance window
- Always check the framework's migration tool limitations (Prisma, Alembic, etc.)
- Recommend testing migrations on a staging clone before production
