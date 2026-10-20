# ClickHouse Migration Writing

## Purpose
Creates versioned SQL migration files for ClickHouse schema changes.

## Role
Data Engineer

## Phase
Development

## Triggered By
ClickHouse schema change needed.

## Inputs
- `clickhouse-schema-design` table definition

## Tool
`clickhouse-migrations` (Python, Docker image). Location: `contracts/clickhouse/migrations/{VERSION}_{name}.sql`. Runs as: Kubernetes pre-install Job (same pattern as Prisma).

## Process

### Migration File Naming
`{VERSION}_{name}.sql` — e.g. `001_create_user_events_table.sql`, `002_add_session_column.sql`.

### DDL Mutation Awareness
- SAFE (instant): ADD COLUMN, CREATE TABLE, CREATE INDEX
- RISKY (background mutation): DROP COLUMN, MODIFY COLUMN type
- For risky operations: plan during low-traffic windows, document in migration comment

### Migration File Format
```sql
-- Migration: {description}
-- Author: Data Engineer
-- Date: {date}
-- Mutation risk: NONE | LOW | HIGH (with note if HIGH)

-- UP migration
{SQL statements}

-- DOWN migration (reverse of UP)
{SQL statements to undo}
```

### Steps
1. Write migration SQL file.
2. Test UP migration locally against ClickHouse dev instance.
3. Test DOWN migration to verify it cleanly reverts.
4. Commit to `contracts/clickhouse/migrations/`.

## Outputs
Committed, tested ClickHouse migration file.

## Quality Gates
- [ ] Descriptive name (not just timestamp)
- [ ] Both UP and DOWN migrations present
- [ ] Mutation risk documented in comments
- [ ] Both UP and DOWN tested locally

## References
- `.claude/skills/data-engineer/clickhouse-schema-design/SKILL.md`
