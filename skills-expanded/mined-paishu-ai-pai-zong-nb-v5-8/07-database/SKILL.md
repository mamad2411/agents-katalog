---
name: database
description: Design and modify database schemas, migrations, SQL queries, indexes, transactions, constraints, and query performance. Use for PostgreSQL, MySQL, SQLite, SQL Server, Prisma, ORM changes, migration planning, and data consistency issues.
---

# Database

## Workflow

1. Inspect existing schema, migration style, ORM conventions, and naming.
2. Model invariants in the database where practical: primary keys, foreign keys, unique constraints, check constraints, and nullability.
3. Choose indexes based on real query predicates, joins, sorting, and cardinality.
4. Define transaction boundaries and isolation expectations.
5. Plan migration rollout, backfill, lock risk, and rollback.
6. Verify with tests, migration dry run, or query plan when possible.

## Required Checks

- Do not rely only on application code for critical uniqueness or referential integrity.
- Avoid adding indexes without a query reason.
- Treat large-table migrations as risky until lock and backfill behavior is understood.
- Be explicit about destructive migrations and data loss.

## Output

Summarize schema/query change, invariant protected, index rationale, migration risk, and verification.
