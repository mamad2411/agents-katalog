---
name: zero-downtime-migrations
description: Expand-contract pattern, backward-compatible schema changes, feature flags for migrations, rollback plans, and production-like testing for database migrations.
invoke_when: Use when writing database migrations, altering schemas, renaming or removing columns, changing data types, or planning data model changes in production systems.
---

# Zero-Downtime Migrations

## Core Principle

During deployment, old code and new code run simultaneously. Every migration must be compatible with both the current and previous version of the application code.

## The Expand-Contract Pattern

### Phase 1: Expand (add new, keep old)

```sql
ALTER TABLE users ADD COLUMN display_name VARCHAR(255);
```

App code writes to BOTH columns during transition.

### Phase 2: Migrate (backfill in batches)

```sql
-- Backfill in batches, not one giant UPDATE
UPDATE users SET display_name = name WHERE display_name IS NULL LIMIT 1000;
```

### Phase 3: Contract (remove old, after full rollout + rollback window)

```sql
-- Only after ALL app instances use display_name exclusively
ALTER TABLE users DROP COLUMN name;
```

## What Never to Do in a Single Migration

```sql
ALTER TABLE users RENAME COLUMN name TO display_name;  -- breaks old code instantly
ALTER TABLE users DROP COLUMN legacy_field;              -- no deprecation
ALTER TABLE users ALTER COLUMN age TYPE text;            -- type change breaks queries
```

## Backward-Compatible Migration Rules

| Operation | Safe? | How to Do It Safely |
|-----------|-------|---------------------|
| Add nullable column | Yes | Direct `ADD COLUMN` |
| Add column with default | Yes (Postgres 11+) | Fast in modern Postgres |
| Rename column | No | Expand-contract |
| Drop column | No | Remove from app code first, drop later |
| Change column type | No | Add new column, migrate data, drop old |
| Add index | Caution | `CREATE INDEX CONCURRENTLY` |
| Drop table | No | Remove all references first, drop later |

## Feature Flags for Schema Changes

Gate new schema usage behind feature flags to decouple deploy from release:

```typescript
if (featureFlags.isEnabled('use-display-name')) {
  return user.display_name;
} else {
  return user.name;  // old column still works
}
```

## Rollback Plan Required

Every migration PR must answer:

1. **What does rollback look like?** Can you deploy the previous app version without a reverse migration?
2. **Is the migration reversible?** Adding a column is. Dropping one is not.
3. **What is the rollback window?** How long before the contract phase makes rollback impossible?

## Testing Against Production-Like Data

- Never test on an empty database. Use a production-sized dataset.
- Measure lock duration on a copy of production data.
- Test with concurrent reads/writes during the migration.
- Backfill scripts must handle millions of rows in batches.

## Migration Review Checklist

- [ ] Migration is backward-compatible with currently deployed code
- [ ] No `DROP COLUMN`, `RENAME COLUMN`, or type changes in a single step
- [ ] Large tables use `CONCURRENTLY` for index creation
- [ ] Backfill runs in batches, not a single `UPDATE`
- [ ] Rollback plan is documented in the migration PR
- [ ] Tested against production-sized data with measured lock time
- [ ] Feature flag gates the new schema usage (if applicable)
