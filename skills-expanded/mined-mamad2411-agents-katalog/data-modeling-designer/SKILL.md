---
name: data-modeling-designer
description: "Designs schemas from access patterns and invariants: normalization, constraints, indexing, relational vs document tradeoffs. Use when creating or evolving a data model for any persistent store."
---

# Data Modeling Designer

## Overview

Transform a domain description into a data model that is correct by construction. A good data model enforces invariants at the schema layer — not in application logic — and is shaped by the access patterns the system actually needs, not by entity diagrams drawn in isolation. Every constraint that can be expressed in the schema must be. Every index must justify its existence with a real query.

**Core principle:** Model from access patterns and invariants first; let the schema enforce what must always be true, and defer normalization decisions until query reality is known.

## The Iron Law

```
NEVER DESIGN A SCHEMA WITHOUT FIRST LISTING YOUR ACCESS PATTERNS AND INVARIANTS.
A SCHEMA THAT CANNOT ENFORCE ITS OWN RULES IS BROKEN BY DESIGN.
```

## When to Use

**Use this when:**
- Starting a new service or feature that requires persistent storage
- Choosing between relational, document, key-value, or hybrid storage
- Designing or reviewing table/collection schemas and indexes
- Planning a schema migration or introducing a breaking structural change
- A system is slow and index or normalization decisions are suspected

**Use this ESPECIALLY when:**
- Someone says "we'll normalize it later" or "just use a JSON blob for now"
- The domain has complex many-to-many relationships or polymorphic entities
- You are reaching for a NoSQL database without having written the query list first
- A new invariant is being enforced only in application code (not the schema)
- Read performance is being sacrificed because the write model is convenient

**Never skip when:**
- Under time pressure — a wrong schema costs weeks of migrations
- The feature seems simple — simple domains often have subtle cardinality traps
- A team member asks to "just add a column" to an existing table

## Phase 1: Enumerate Access Patterns and Invariants

Before touching any schema syntax:

1. **List every read query** the system must answer — exact fields returned, filter predicates, sort order, cardinality (one row vs. many rows), and acceptable latency.
2. **List every write operation** — inserts, updates, deletes, upserts, batch writes.
3. **List every invariant** — facts that must be true in the data at all times (e.g., "an order total equals the sum of its line items", "a user must have exactly one primary email", "a slot cannot be double-booked").
4. **Identify cardinality** for every relationship: one-to-one, one-to-many, many-to-many.
5. **Identify mutability** — which fields change frequently, which are append-only, which are immutable after creation.

```
Access pattern table (fill in before writing DDL):

| ID  | Operation | Entity        | Filter / Key           | Sort       | Cardinality | Latency SLA |
|-----|-----------|---------------|------------------------|------------|-------------|-------------|
| R1  | Read      | orders        | user_id                | created_at | many        | < 50 ms     |
| R2  | Read      | order_items   | order_id               | —          | many        | < 50 ms     |
| W1  | Write     | orders        | insert on checkout     | —          | one         | < 200 ms    |
| W2  | Update    | orders.status | order_id               | —          | one         | < 100 ms    |
```

## Phase 2: Choose Storage Paradigm

Use the access pattern list — not preference — to pick storage:

| Signal | Lean Relational | Lean Document/Key-Value |
|--------|----------------|------------------------|
| Queries join 3+ normalized tables regularly | yes | no |
| Writes are transactional across multiple entities | yes | no |
| Data shape is uniform and known at design time | yes | maybe |
| Queries are always by a single primary key or partition key | maybe | yes |
| Data shape varies per record (polymorphic) | no | yes |
| Reads vastly outnumber writes; read shape equals write shape | maybe | yes |
| Strong consistency required across entities | yes | hard |

A hybrid is legitimate: relational for transactional core, document/key-value for derived read models or config blobs. Name the boundary explicitly.

## Phase 3: Relational Schema Design

### Normalization — apply in order, justify each deviation

| Normal Form | Rule | Violation Example | Fix |
|-------------|------|--------------------|-----|
| 1NF | No repeating groups; every column is atomic | `tags VARCHAR` storing `"a,b,c"` | `tags` table with FK |
| 2NF | Every non-key column depends on the whole PK | `order_items(order_id, product_id, product_name)` — `product_name` depends only on `product_id` | Move to `products` table |
| 3NF | No transitive dependencies | `orders(order_id, customer_id, customer_city)` — city depends on customer, not order | Move city to `customers` |

**When to intentionally denormalize** (document the reason inline as a comment):
- A computed aggregate is read on every page load and recomputing it joins > 3 tables — cache it as a materialized column with a trigger or background job.
- A reporting query is read-only and latency-sensitive — a separate read model is acceptable.
- An entity has a stable, bounded set of attributes that vary by type — a JSONB column with a CHECK constraint is preferable to a 20-column sparse table.

Denormalization without a documented access-pattern justification is forbidden.

### Example: relational schema

```sql
-- INVARIANT: an order must have at least one line item (enforced at app layer + CHECK via trigger)
-- INVARIANT: order.total_cents = SUM(order_items.unit_price_cents * quantity) — enforce via trigger or app layer with test coverage
-- ACCESS PATTERN R1: SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC

CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       TEXT NOT NULL UNIQUE,          -- INVARIANT: one primary email per user
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE orders (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id),
    status          TEXT NOT NULL CHECK (status IN ('pending','confirmed','shipped','cancelled')),
    total_cents     INTEGER NOT NULL CHECK (total_cents >= 0),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for R1
CREATE INDEX idx_orders_user_created ON orders (user_id, created_at DESC);

CREATE TABLE order_items (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id        UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id      UUID NOT NULL REFERENCES products(id),
    quantity        INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0)
);

-- Index for R2
CREATE INDEX idx_order_items_order ON order_items (order_id);
```

Every index maps back to a named access pattern. No index without a query that needs it.

## Phase 4: NoSQL / Document Schema Design

**Rule:** design the collection structure from the query list, not from an entity diagram.

### Access-pattern-driven document design example

Scenario: a chat application. Access patterns:
- R1: "Fetch the last 50 messages in a room, newest first" — hottest path
- R2: "Fetch a single message by id"
- W1: "Append a message to a room"

Wrong approach (entity-first): separate `rooms`, `users`, `messages` collections mirroring the relational model — R1 requires joining across collections, which NoSQL does not do cheaply.

Right approach (query-first):

```json
// Collection: messages
// Partition key: room_id   Sort key: created_at (descending in query)
// R1 is a single partition scan — O(1) partition lookup, range scan on sort key
{
  "room_id": "room_abc",
  "message_id": "msg_001",
  "created_at": "2025-05-25T10:00:00Z",
  "sender_id": "user_xyz",
  "sender_display_name": "Alice",   // DENORMALIZED: avoids a join on R1; acceptable because display_name changes rarely
  "body": "Hello, world",
  "type": "text"
}
```

Document the denormalization decision and the stale-read risk. If `sender_display_name` changes, describe the update propagation strategy (event-driven fan-out, eventual consistency window, or acceptable staleness).

### Partition key selection rules

1. Cardinality must be high enough to spread load — never partition by a low-cardinality field (e.g., `status`).
2. The hottest query must resolve to a single partition (no scatter reads).
3. Items within a partition must not exceed storage limits (DynamoDB: 10 GB; Firestore: no hard partition limit but avoid hot partitions).

## Phase 5: Constraints and Schema Evolution

### Enforce invariants in the schema

| Invariant type | Enforcement mechanism |
|----------------|----------------------|
| Non-null field | `NOT NULL` constraint |
| Allowed values | `CHECK` constraint or foreign key to a lookup table |
| Uniqueness | `UNIQUE` constraint or unique index |
| Referential integrity | `FOREIGN KEY` with explicit `ON DELETE` / `ON UPDATE` behaviour |
| Computed aggregate | Trigger or deferrable constraint; document if app-enforced only |
| Temporal ordering | `CHECK (ended_at > started_at)` |

### Schema evolution rules

- **Additive changes only** for backward compatibility: add nullable columns, add indexes, add tables.
- **Non-additive changes** (rename, type change, drop) require a multi-step migration: (1) add new column/table, (2) dual-write, (3) backfill, (4) flip reads, (5) drop old.
- **Never rename a column in a single migration** on a live database.
- **Every migration must be reversible** or have an explicit rollback plan documented before it runs.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I'll add a JSON column and we can figure out the structure later"
- "We don't need indexes yet, the table is small"
- "NoSQL is simpler, let's just use a document store" (without a query list)
- "That invariant is enforced in the service layer, the schema doesn't need to care"
- "We can normalize it when performance becomes a problem"
- "One more nullable column won't hurt"
- No access pattern table written before DDL
- Indexes added after tables with no query mapped to them

**ALL of these mean: STOP. Return to Phase 1.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We'll add constraints later once the schema stabilizes" | A schema without constraints is wrong now. Retrofitting constraints on populated tables requires migrations and downtime. |
| "JSON blob is flexible" | Flexible schemas shift validation errors from schema-time to runtime, where they are harder to catch and fix. |
| "NoSQL is faster" | NoSQL with the wrong partition key is slower than a well-indexed relational table. Speed comes from access pattern alignment, not storage paradigm. |
| "We only have a few rows, indexes don't matter" | Schemas outlive their initial row counts by years. Indexes added under production load are dangerous. |
| "Denormalization is fine for performance" | Denormalization without a documented access pattern that justifies it is technical debt, not optimization. |
| "The ORM handles the schema" | ORMs generate schemas from models, not from access patterns. Review and own the DDL the ORM emits. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Why is this query so slow?" — An index was missing because access patterns were not enumerated first.
- "We need to migrate this column, it's the wrong type" — Type was chosen without knowing how the field would be used in queries.
- "This data is inconsistent" — An invariant was left to application code instead of being encoded in the schema.
- "NoSQL was a mistake for this" — The storage paradigm was chosen before the query list was written.
- "We have a hot partition" — The partition key was chosen by entity convenience, not by query distribution.

**When you see these:** STOP. Return to Phase 1 and rebuild the access pattern table from the queries that are actually running.

## Related Skills

- **architecture-planner** — use to decide service boundaries before committing to a schema per service
- **backend-senior-engineer** — use alongside for API contract design that matches the data model
- **spec-first-development** — run before this skill; the spec's data section feeds Phase 1's invariant list
- **validation-designer** — use after schema is locked to design application-layer validation that complements schema constraints
- **tech-stack-advisor** — use when the relational vs. document decision is not yet made

## Verification

Before handing off the schema:

- [ ] Access pattern table completed with every read and write operation, filter keys, sort order, and latency SLA
- [ ] Every invariant listed and mapped to a schema enforcement mechanism (constraint, FK, trigger) or documented as app-enforced with test coverage
- [ ] Normal form evaluated for every table; any deviation from 3NF has a named access pattern as justification
- [ ] Every index maps to a named access pattern; no orphan indexes
- [ ] For NoSQL: partition key chosen based on query distribution, not entity convenience; hot partition risk assessed
- [ ] Denormalized fields have documented stale-read risk and an update propagation strategy
- [ ] Schema evolution strategy defined: additive changes identified, non-additive changes broken into multi-step migration plan
- [ ] `CHECK` constraints cover all known value-domain invariants
- [ ] `ON DELETE` / `ON UPDATE` behaviour explicit on every foreign key
- [ ] Human partner has reviewed the access pattern table and the schema before any migration is written
