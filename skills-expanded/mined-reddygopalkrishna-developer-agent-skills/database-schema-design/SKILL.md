---
name: database-schema-design
description: Designs relational and document database schemas, covering entities, keys, constraints, data types, multi-tenancy, soft deletes, audit columns and access-pattern modeling for NoSQL. Use when doing schema design or data modeling, creating new tables or collections, designing the tables behind a new feature or API, reviewing a schema or ERD, choosing primary keys or column types, designing for multiple tenants, or deciding between embedding and referencing. Not for changing a live schema safely (use database-migrations).
license: MIT
---

# Database Schema Design

Data outlives code. Model the business's facts and rules, and make the database enforce them with types and constraints, so that no bug, script or future service can write data that breaks them.

## When to use

- Designing tables or collections for a new feature or service.
- Reviewing a schema, ERD or ORM model before it is created.
- Choosing primary keys, column types, enum strategies or JSON columns.
- Deciding how to isolate tenants, delete data, or record history.
- Modeling for a document or key-value store (MongoDB, DynamoDB, Cassandra).

Not for: migrating a live schema without downtime (database-migrations) or tuning queries (sql-optimization).

## Workflow

1. **List the entities, relationships and cardinalities** (1:1, 1:N, M:N) in plain language with the user. Name each entity's owner and lifecycle (who creates, changes and deletes it).
2. **List the access patterns:** the top reads and writes, their frequency, expected row counts and growth. For NoSQL, this list *is* the design input.
3. **Write down the invariants** ("an order has at least one line", "emails are unique per tenant", "price is never negative"). Each one becomes a constraint, or a documented reason why it cannot be.
4. **Draft a normalized schema** (third normal form): every non-key column describes the key, the whole key, and nothing but the key.
5. **Choose keys and types** using the tables below.
6. **Add constraints and indexes:** NOT NULL, foreign keys (with indexes on the referencing columns), UNIQUE, CHECK, and indexes for the listed access patterns.
7. **Denormalize only deliberately:** for each duplicated or derived value, name the source of truth and how it stays in sync.
8. **Decide the cross-cutting policies:** tenancy, deletion, auditing, time zones, and personal data (retention and erasure).
9. **Write the DDL and sample queries** for the top access patterns, then review against the checklist.

## Primary keys

| Option | Strengths | Weaknesses | Use when |
|---|---|---|---|
| `bigint` identity (`GENERATED ALWAYS AS IDENTITY` in PostgreSQL, `BIGINT AUTO_INCREMENT` in MySQL) | Small, fast, ordered inserts | Guessable; assigned by one database; awkward when merging data across databases | Default for internal tables |
| UUIDv4 (random) | Generated anywhere; not guessable | Random inserts scatter across the B-tree (page splits, cache misses); 16 bytes | Ids created outside the database at low to moderate volume |
| UUIDv7 (time-ordered, RFC 9562) | Generated anywhere; inserts arrive roughly in order | Reveals the creation time | Ids created outside the database at high volume; distributed systems |
| Natural key (email, SKU) | Meaningful | Real-world values change, and every reference must change with them | Only when truly immutable; otherwise use a surrogate key plus a UNIQUE constraint |

- Use `bigint`, not `int`, for tables that can grow. A 32-bit key overflows at about 2.1 billion, and changing a primary key type later is a major project.
- Store UUIDs as the native `uuid` type in PostgreSQL, or `BINARY(16)` in MySQL, not as 36-character strings.
- PostgreSQL 18 added a built-in `uuidv7()` function. Confirm with `SELECT uuidv7();` on your server; on older versions, generate UUIDv7 in the application or with an extension.
- If sequential ids must not be exposed publicly (to prevent enumeration), keep the internal `bigint` key and add a separate public id column with a UNIQUE constraint.

## Column types

| Data | Use | Avoid |
|---|---|---|
| Points in time | PostgreSQL `timestamptz`; MySQL `DATETIME(6)` storing UTC (`TIMESTAMP` ends in 2038) | `timestamp without time zone` for real instants; strings |
| Calendar dates (birthdays, due dates) | `date` | Timestamps at midnight |
| Money | `numeric(19,4)` / `DECIMAL(19,4)`, or integer minor units (cents), always with a currency code column | `float`, `double`, PostgreSQL's `money` type |
| Text | PostgreSQL `text`, with a CHECK on length if there is a business limit; MySQL `VARCHAR(n)` sized to the real limit, with `utf8mb4` | `char(n)`; arbitrary `varchar(255)` everywhere |
| Yes/no | `boolean` | `'Y'`/`'N'` strings, nullable booleans with three meanings |
| Small fixed set of values | CHECK constraint, or a native enum | Free-text status columns |
| Evolving set with attributes (labels, ordering, active flag) | Lookup table + foreign key | Hard-coded values in the application only |
| Genuinely schemaless attributes | PostgreSQL `jsonb`; MySQL `JSON` | JSON for fields you routinely filter, join or constrain on |
| IP addresses, ranges | PostgreSQL `inet`, range types (`tstzrange`) | Strings, or pairs of columns that need overlap logic |

Enum notes: a PostgreSQL enum accepts new values easily (`ALTER TYPE ... ADD VALUE`), but removing or renaming a value is hard. A MySQL `ENUM` change is an `ALTER TABLE`. If the set changes often or needs metadata, use a lookup table.

## Constraints

- **NOT NULL by default.** Allow NULL only when "unknown" or "not applicable" is a real state, and document which.
- **Foreign keys** for every reference. Choose `ON DELETE` deliberately: `RESTRICT`/`NO ACTION` (the default) for independent entities, `CASCADE` only for children owned by the parent (order lines of an order), `SET NULL` for optional links.
- **Index foreign key columns.** PostgreSQL does not create these indexes automatically. MySQL InnoDB does.
- **UNIQUE** for business uniqueness, scoped correctly: `UNIQUE (tenant_id, slug)`, not `UNIQUE (slug)`. For case-insensitive uniqueness use a unique index on `lower(email)`, or `citext` in PostgreSQL.
- **CHECK** for value rules: `CHECK (quantity > 0)`, `CHECK (ends_at > starts_at)`, `CHECK (status IN ('draft', 'sent', 'paid'))`.
- **Exclusion constraints** (PostgreSQL) for "no overlapping bookings": `EXCLUDE USING gist (room_id WITH =, during WITH &&)`, which needs the `btree_gist` extension for the equality part.
- **Name constraints explicitly** (`orders_customer_id_fkey`) so later migrations and error messages are readable.

## Relationships

- **1:N:** a foreign key on the "many" side.
- **M:N:** a join table with a composite primary key `(a_id, b_id)`, plus an index on `(b_id, a_id)` if you query from the other side. Give it its own columns (`created_at`, `role`) when the relationship has attributes.
- **1:1:** the foreign key with a UNIQUE constraint on the dependent side, or merge the tables if they always appear together.
- **Polymorphic references** (`commentable_type`, `commentable_id`) cannot have foreign keys. Prefer separate nullable foreign key columns with `CHECK (num_nonnulls(post_id, photo_id) = 1)` (PostgreSQL), or one join table per parent type.
- **Hierarchies:** an adjacency list (`parent_id`) with recursive CTEs is the default. Use a materialized path or closure table only when reads of whole subtrees dominate.

## Denormalization

Duplicate or precompute data only for a measured read need, and write down:

1. The source of truth.
2. How the copy is updated: same transaction, trigger, or async job.
3. How drift is detected and repaired (a periodic reconciliation query).

Common legitimate cases: counters and totals on a parent, read models for search or reporting, snapshotting values that must not change later (the price on an order line must not follow later product price changes; that is not duplication, it is a different fact).

## Deleting data

| Approach | Pros | Cons |
|---|---|---|
| Hard delete + history/audit table | Simple queries; real erasure possible | Restore needs the audit copy |
| Soft delete (`deleted_at timestamptz NULL`) | Easy restore and audit | Every query must filter; unique constraints need partial indexes (PostgreSQL `WHERE deleted_at IS NULL`); foreign keys do not cascade; personal-data erasure requests still need a hard delete |
| Archive table (move rows) | Hot table stays small | Two places to query for history |

Default to hard delete plus an audit or history table, unless the product explicitly needs users to restore deleted items. Whatever you choose, check it against data-retention and erasure obligations (for example GDPR), and confirm with the user.

## Audit and time

- `created_at` and `updated_at` (`timestamptz NOT NULL DEFAULT now()`) on most tables. Keep `updated_at` current in one consistent place (the ORM or a trigger, not both).
- `created_by` / `updated_by` when actions must be attributed.
- For full change history, use a history table written by triggers or the application, or an event log. Built-in temporal tables exist in some engines (for example SQL Server and MariaDB system-versioned tables).
- Store instants in UTC. Store the user's time zone separately when you need local-time logic (recurring events, business hours).

## Multi-tenancy (summary)

| Pattern | Isolation | Operational cost | Fits |
|---|---|---|---|
| Shared tables + `tenant_id` (+ row-level security) | Logical | Lowest | Many small tenants (SaaS default) |
| Schema per tenant | Medium | Migrations run N times; catalog bloat at thousands of tenants | Tens to hundreds of tenants |
| Database per tenant | Strongest | Highest (connections, migrations, monitoring per tenant) | Few large or regulated tenants |

Read [references/multi-tenancy.md](references/multi-tenancy.md) when designing or reviewing tenant isolation.

## Document and key-value stores (summary)

- Start from the access-pattern list, not the entity diagram.
- **Embed** data that is read together, owned by the parent, and bounded in size. **Reference** data that is shared, unbounded or updated independently.
- Never let an array grow without bound inside one document or item.

Read [references/nosql-modeling.md](references/nosql-modeling.md) when the target is MongoDB, DynamoDB, Cassandra, or a similar store.

## Naming conventions

- Pick one style and keep it: `snake_case`, and either singular or plural table names (be consistent).
- Foreign keys: `<referenced_table_singular>_id` (`customer_id`).
- Booleans: `is_`, `has_` (`is_active`). Timestamps: `_at` (`paid_at`). Dates: `_on` or `_date`.
- No reserved words (`user`, `order`, `group`) as unquoted identifiers. Prefer `app_user` and `orders`, or a consistent plural.
- No abbreviations that only the author understands.

## Anti-patterns

- **Entity-attribute-value tables** (`entity_id, attribute, value`) instead of columns. Types and constraints are lost. Use real columns, or `jsonb` for genuinely open-ended attributes.
- **Comma-separated lists in a column.** Use a join table.
- **Floats for money.**
- **Timestamps without time zone** for real-world instants.
- **Everything nullable** "for flexibility".
- **Missing indexes on foreign keys** (PostgreSQL), which makes parent deletes and joins slow.
- **Reusing a column for different meanings** depending on another column's value.
- **Uniqueness enforced only in application code.** Concurrent requests will race past it. Use a UNIQUE constraint.
- **Premature sharding or microservice-per-table splits** before a single, well-indexed database is shown to be insufficient.

## Done when

- Every entity, relationship and invariant from the conversation maps to a table, key or constraint, or there is a written reason why not.
- Keys and types follow the tables above; there are no floats for money and no instants without time zones.
- Every foreign key exists in the database and is indexed where needed.
- Each top access pattern has a sample query and an index that serves it.
- Every denormalization names its source of truth and sync mechanism.
- Tenancy, deletion, audit and time-zone policies are decided and written down.

## References

- [references/multi-tenancy.md](references/multi-tenancy.md) — read when choosing or implementing a tenant isolation model, including PostgreSQL row-level security.
- [references/nosql-modeling.md](references/nosql-modeling.md) — read when modeling for MongoDB, DynamoDB, Cassandra or Redis.
