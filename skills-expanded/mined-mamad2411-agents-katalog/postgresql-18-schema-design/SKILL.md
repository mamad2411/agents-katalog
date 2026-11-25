---
name: postgresql-18-schema-design
description: Designs and reviews PostgreSQL 18 schemas, tables, constraints, indexes, generated columns, views, functions, and database boundaries. Use when a task mentions schema design, DDL, tables, indexes, constraints, data types, views, functions, triggers, or database modeling for PostgreSQL.
license: MIT
compatibility: PostgreSQL 18 release line; scripts require bash.
---

# PostgreSQL 18 Schema Design

Use this skill for new schemas, table design, constraints, indexes, generated columns, views, extensions, SQL functions, triggers, and database-facing API boundaries.

## Start Here

1. Confirm the target database is PostgreSQL 18.
2. Identify whether the change is local, test, staging, or production.
3. Read existing migrations, schema definitions, naming conventions, and deployment process.
4. Prefer additive schema evolution unless the user requests a breaking change.
5. Use supporting files as needed:
   - `resources/schema-design-checklist.md`
   - `resources/type-and-constraint-guide.md`
   - `examples/safe-ddl-patterns.md`
6. Run scripts with `--help` before using them:
   - `scripts/postgresql-18-schema-lint.sh`

## Design Principles

- Put durable integrity in the database with primary keys, foreign keys, unique constraints, check constraints, `NOT NULL`, and exclusion constraints where appropriate.
- Choose PostgreSQL native types deliberately.
- Prefer `timestamptz` for real-world instants.
- Use `jsonb` for flexible documents, not to avoid modeling stable relational concepts.
- Index for observed query patterns and constraints, not for every column.
- Name constraints and indexes consistently.
- Treat `SECURITY DEFINER` functions, broad grants, and RLS changes as security-sensitive.
- For large tables, discuss locks, rewrites, backfills, and validation separately from DDL syntax.

## Workflows

Use `workflows/schema-change-workflow.md` when designing or reviewing a schema change from requirements through rollout.

## Expected Output

When answering schema design tasks, provide:

- Proposed DDL or migration snippets.
- PostgreSQL 18 compatibility notes.
- Lock/rewrite and rollout risks.
- Required tests.
- Rollback or forward-fix plan.
