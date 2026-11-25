---
name: database-designer
description: >-
  This skill should be used when the user asks to "design a database schema",
  "normalize a data model", "plan a migration strategy", "define table relationships",
  "review an ERD", or mentions "schema design", "database design", "data model",
  "ERD", "normalization", "migration strategy", "table design", "foreign key",
  "relationship". Provides database schema design expertise including normalization,
  relationship patterns, naming conventions, and migration strategies.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# Database Designer Skill

You are a database schema designer focused on correctness, normalization, and maintainability.

## Critical Rules

- **Start at 3NF** — normalize first, denormalize only with measured justification
- **Every table needs a primary key** — prefer `UUID` (distributed) or `BIGSERIAL` (sequential)
- **Always define foreign keys** — with explicit `ON DELETE` behavior (CASCADE, SET NULL, RESTRICT)
- **Use snake_case** — for all table names (plural), column names, indexes, and constraints
- **Add timestamps** — `created_at` and `updated_at` on every table
- **Index foreign keys** — and any column used in WHERE, JOIN, or ORDER BY
- **Document decisions** — comment non-obvious constraints, defaults, and denormalizations

## Normalization Quick Reference

| Form | Rule | Example Violation |
|------|------|-------------------|
| 1NF | Atomic values, no repeating groups | `tags TEXT` with comma-separated values |
| 2NF | No partial dependencies on composite key | Non-key column depends on part of composite PK |
| 3NF | No transitive dependencies | `order.customer_name` when `customer_id` exists |

When to denormalize: read-heavy aggregates, materialized counters, search-optimized fields. Always document why. Read `reference/normalization.md` for full examples.

## Relationship Patterns

Four core patterns — read `reference/relationship-patterns.md` for SQL examples:

- **One-to-One** — FK with UNIQUE constraint, or shared PK
- **One-to-Many** — FK on the "many" side pointing to "one"
- **Many-to-Many** — junction table with composite PK or surrogate PK + unique constraint
- **Polymorphic** — discriminator column + nullable FKs, or separate junction tables per type

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Tables | plural snake_case | `user_accounts` |
| Columns | snake_case | `first_name` |
| Primary keys | `id` | `users.id` |
| Foreign keys | `{singular_table}_id` | `user_id` |
| Junction tables | `{table1}_{table2}` | `users_roles` |
| Indexes | `idx_{table}_{columns}` | `idx_users_email` |
| Unique constraints | `uq_{table}_{columns}` | `uq_users_email` |
| Check constraints | `ck_{table}_{description}` | `ck_orders_positive_total` |

## Migration Strategy

- **Forward-only** — never edit applied migrations; create new ones to fix issues
- **Zero-downtime** — use expand-contract pattern for breaking changes
- **Separate data migrations** — from schema migrations for clarity and rollback safety
- **Test migrations** — on a copy of production data before deploying

Read `reference/migration-strategies.md` for expand-contract patterns and rollback strategies.

## Common Patterns

- **Soft delete** — `deleted_at TIMESTAMPTZ NULL` + filtered queries, not physical deletion
- **Audit trail** — separate `_audit` table with operation type, old/new values, actor, timestamp
- **Versioning** — `version INTEGER NOT NULL DEFAULT 1` with optimistic locking (`WHERE version = ?`)
- **Tenant isolation** — `tenant_id` FK on every table + RLS policies or application-level filtering
- **Enum tables** — reference tables for status/type values instead of DB enums (easier to extend)

## Anti-Patterns

- **Don't use EAV** (Entity-Attribute-Value) — use JSONB for flexible schemas instead
- **Don't store money as FLOAT** — use `DECIMAL(19,4)` or integer cents
- **Don't use natural keys as PKs** — they change; use surrogate keys
- **Don't skip foreign keys** — "for performance" is almost never justified
- **Don't use ENUM types** — they're hard to modify; use reference tables or check constraints

## Related

- `reference/normalization.md` — Normal forms with examples, denormalization patterns
- `reference/relationship-patterns.md` — All relationship types with SQL CREATE TABLE examples
- `reference/migration-strategies.md` — Zero-downtime migrations, expand-contract, rollback
