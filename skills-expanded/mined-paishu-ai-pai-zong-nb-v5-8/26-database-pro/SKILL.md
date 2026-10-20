---
name: database-pro
description: Professional database design, migration, transaction, indexing, query optimization, and data integrity skill for SQL databases and ORMs. Use for schema design, migrations, indexes, constraints, query performance, data modeling, consistency, backfills, and database review across PostgreSQL, MySQL, SQLite, Prisma, Drizzle, TypeORM, SQLAlchemy, and similar tools.
---

# Database Pro

## Workflow

1. Identify DB engine, ORM/migration tool, schema ownership, and production data size risk.
2. Model invariants with constraints: primary key, foreign key, unique, check, not null, default, and enum/domain choices.
3. Design indexes from actual access patterns: predicates, joins, sort order, cardinality, and write cost.
4. Define transaction boundaries, isolation assumptions, locking risks, and idempotency needs.
5. Plan migrations with expand/contract when compatibility or large data is involved.
6. Verify using tests, migration dry run, query plan, or representative SQL.

## Design Checklist

- Data ownership and lifecycle are explicit.
- Deletes are intentional: restrict, cascade, soft delete, archival, or tombstone.
- Timestamps, audit fields, and actor attribution exist when needed.
- Money, counts, and precision-sensitive values avoid unsafe floating point.
- Status fields have valid transitions, not just arbitrary strings.
- Multitenant data includes tenant boundary constraints and indexes.

## Migration Checklist

- Separate schema change, backfill, application switch, and cleanup for risky changes.
- Avoid long locks on large tables.
- Make rollback strategy explicit.
- Keep old and new app versions compatible during deployment when needed.

## Avoid

- Only enforcing critical integrity in application code.
- Adding indexes without query evidence.
- Dangerous destructive migrations without warning.
- Hiding N+1 queries behind caching.

## Output

State invariant, schema/migration change, index rationale, transaction/lock risk, and verification.

## Bundled Resources

- `references/database-production-checklist.md`: schema, migration, index, transaction, and data-access production checks.
- `scripts/find-migrations.ps1`: locates likely migration/schema files before database work.
