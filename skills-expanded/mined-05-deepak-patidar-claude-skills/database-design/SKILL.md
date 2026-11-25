---
name: database-design
description: Schema design, data modeling, migrations, and query correctness for relational databases (and when to use non-relational). Use when creating or altering tables, designing schemas, writing migrations, modeling money/inventory/ledgers, adding indexes, or when the user says "schema", "data model", "migration", "database design", or "normalize".
---

# Database Design

The schema outlives every framework, every rewrite, and every AI model that touches the codebase. Code bugs ship and get fixed; schema mistakes and corrupted data are forever. Design the schema as if the application code were hostile — because one day, some version of it will be.

## Principle: the database defends its own invariants

Any rule the business cannot tolerate being violated goes **in the schema**, not only in application code:

- `NOT NULL` by default; nullable is an explicit decision meaning "absence is a valid state" (and every reader must handle it).
- `FOREIGN KEY` for every reference. `UNIQUE` for every natural key (mobile number, invoice number per tenant, SKU per account). `CHECK` for domains (quantity >= 0, status in allowed set, rate between 0 and 100).
- Application-level checks are UX; database constraints are truth. You need both, but only one of them holds under race conditions, bad deploys, and manual fixes.

## Modeling rules that prevent the classic disasters

- **Money and quantity are exact decimals** (`NUMERIC`), never float — no exceptions, including "it's just a percentage". Store currency explicitly if there could ever be more than one.
- **Timestamps**: store UTC (`timestamptz`), render in local zone. Name columns `*_at`. Every mutable table gets `created_at`/`updated_at`.
- **IDs**: surrogate primary key (UUID or bigint — pick per project and stay consistent); enforce natural keys with UNIQUE constraints, don't make them the PK. Never expose sequential IDs where enumeration leaks business volume (invoice counts, user counts) unless numbering is a product requirement.
- **State machines as data**: a `status` column needs its legal transitions written down (in code comments/docs) and enforced in exactly one service function. If history matters, an append-only events/audit table beats overwriting.
- **Financial and inventory data is append-only at heart**: model corrections as new compensating rows (credit notes, stock adjustments with reasons), not UPDATEs that destroy what happened. If a regulator, accountant, or angry customer could ask "what was it before?", keep the before.
- **Soft delete vs hard delete** is a product decision — but referencing rows must never dangle either way; decide `ON DELETE` behavior per FK deliberately (RESTRICT is the safe default).
- **Multi-tenant**: `account_id NOT NULL` on every tenant table, composite indexes leading with it, and row-level security or a mandatory scoping mechanism so a missing WHERE clause fails closed, not open.

## Normalization: the practical rule

Normalize until it hurts (one fact, one place — eliminate update anomalies), then denormalize only with a named owner for the copy and its update path. Storing `line_total = qty × rate` is fine for immutable invoice lines (they're history, frozen at sale time — that's not denormalization, that's a snapshot). Storing a customer's "current balance" is a cache — it needs either a recomputation job or transactional dual-writes, and a way to audit drift.

## Concurrency: assume two requests arrive at once

- Any read-modify-write (stock decrement, balance update, counter, "next invoice number") needs an explicit strategy: atomic single UPDATE (`SET stock = stock - :n WHERE stock >= :n`), `SELECT ... FOR UPDATE`, or a serializable/retry pattern. "We'll be small" doesn't prevent double-submits from one user's double-click.
- Uniqueness under concurrency is a constraint + handled violation, not check-then-insert.
- Multi-row financial writes (invoice + lines + stock + ledger) are **one transaction, all or nothing** — and keep transactions short; never call external APIs inside one.

## Indexes and queries

- Index every FK, every column in frequent WHERE/ORDER BY, and tenant-scoped composites `(account_id, x)`. But each index taxes every write — add them for observed query shapes, not superstition.
- Before shipping a list endpoint: it must paginate (keyset for large/growing sets), and its query must not be N+1 (verify by looking at emitted SQL once, not by assuming the ORM is smart).
- `EXPLAIN` any query you're about to optimize; never index-guess.

## Migration discipline

- Migrations are code-reviewed, hand-verified artifacts — whether hand-written or generated, read every line and know its lock behavior before it touches production data.
- Additive first; destructive only after code no longer reads the old shape (see deployment-safety: expand → migrate → contract).
- Every migration answers: is it idempotent/re-runnable? does it run safely while old code is live? what's the down-path or restore plan? does the backfill batch (not one giant UPDATE locking the table)?

## When someone says "let's use NoSQL / JSONB for this"

JSONB/document columns are right for genuinely schemaless payloads you don't query relationally (provider webhook dumps, user-defined custom fields). They are wrong for anything with relationships, constraints, or reporting needs — that's just a schema you've decided not to enforce. Default to relational; earn your way out.
