---
name: lyra-database
description: "Database engineering rules for Postgres, MySQL, and SQLite. Reach for it when writing SQL, designing schemas, optimizing queries, managing transactions, writing migrations, or sizing connection pools."
compatibility: "None. Optional: database clients (psql, mysql, sqlite3), ORM tools (Prisma, Drizzle, Knex, Alembic, Flyway)."
---

# lyra-database

## What it does

Rules for writing database code that doesn't wake people up at 3am. Covers schema design, query construction, optimization, transactions, migrations, and connection pooling across Postgres, MySQL, and SQLite. A few rules block merge — unparameterized SQL, external calls inside a transaction, destructive migrations without a rollback plan — because they cause data loss or outages. 
The rest is judgment; cite the rule number, don't argue taste.

## The rules

### 1. Match the database to the workload

Postgres for complex queries and rich types (JSONB, full-text). MySQL for read-heavy web workloads. SQLite for embedded, single-process, zero-config. Don't use Mongo or Redis as a primary transactional store.

### 2. Normalize first, denormalize on purpose

3NF by default. Denormalize only with measured evidence that a join is too slow. The exception is snapshot data (unit_price on an order line) — that's a business decision, not laziness.

### 3. Enforce integrity at the database level

Every constraint the database can enforce, it must. Application validation is defense in depth, not the primary line. A constraint in app code is a constraint that one code path forgot.

```sql
-- good — the database enforces it; app validates for UX
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### 4. Index every foreign key

Postgres and SQLite don't auto-index FKs. MySQL/InnoDB does, but with system-generated names that make `DROP INDEX` painful. An unindexed FK means every JOIN and CASCADE DELETE is a full table scan.

### 5. Use the narrowest correct type

`TIMESTAMPTZ` for timestamps (never strings), `DECIMAL` for money (never `FLOAT`), `BOOLEAN` for flags (never `INT`). Wider types waste disk, RAM, and bloat every index.

### 6. Unique constraint on every natural key

If a column uniquely identifies a row in the real world, it gets `UNIQUE` even when a surrogate `id` is the primary key. App-level duplicate checks are race conditions.

### 7. Prefer CHECK over ENUM for mutable value sets

ENUMs require a migration to add or remove a value. CHECK constraints are a one-line `ALTER TABLE`. Use ENUM only for truly closed sets in a mature domain.

### 8. Never SELECT \* in production code

Name every column. `SELECT *` fetches columns you don't need, breaks when schema changes, and prevents covering index scans.

### 9. Always parameterize — no string concatenation

String concatenation in SQL is injection. No exceptions, no "trusted input."

```javascript
// bad — SQL injection
const sql = `SELECT id FROM users WHERE email = '${email}'`;

// good — parameterized
const sql = "SELECT id FROM users WHERE email = $1"; // Postgres; MySQL/SQLite use ?
await pool.query(sql, [email]);
```

### 10. Eliminate N+1 queries

One query inside a loop is an N+1. Use a JOIN, a batch query, or ORM eager loading.

```javascript
// bad — 101 queries for 100 posts
for (const post of posts) {
  post.author = await db.users.findById(post.authorId);
}

// good — one query
const posts = await db.query(`
  SELECT p.id, p.title, u.name AS author
  FROM posts p JOIN users u ON u.id = p.author_id LIMIT 100`);
```

### 11. Run EXPLAIN before optimizing

Never guess at query performance. Read the plan. `Seq Scan` on a large table means add an index. Stale row estimates mean run `ANALYZE`.

### 12. Design covering indexes for hot queries

A covering index includes every column the query needs, so the database answers from the index alone. Highest-leverage optimization for read-heavy workloads.

### 13. Never wrap indexed columns in functions

A function on an indexed column makes the index unusable. Rewrite as a sargable range query.

```sql
-- bad — index is dead, full table scan
SELECT id FROM orders WHERE EXTRACT(YEAR FROM created_at) = 2024;

-- good — index on created_at is usable
SELECT id FROM orders WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
```

### 14. Use keyset pagination for deep pages

`OFFSET 100000 LIMIT 20` scans 100,020 rows. Keyset pagination seeks directly to the last-seen value — O(1) regardless of depth.

### 15. Wrap every multi-step write in a transaction

If a logical operation requires multiple INSERTs or UPDATEs, they either all succeed or all fail. No partial writes.

```javascript
// bad — crash between these loses money
await db.query("UPDATE accounts SET balance = balance - 100 WHERE id = 1");
await db.query("UPDATE accounts SET balance = balance + 100 WHERE id = 2");

// good — atomic
const client = await pool.connect();
try {
  await client.query("BEGIN");
  await client.query(
    "UPDATE accounts SET balance = balance - 100 WHERE id = 1",
  );
  await client.query(
    "UPDATE accounts SET balance = balance + 100 WHERE id = 2",
  );
  await client.query("COMMIT");
} catch (err) {
  await client.query("ROLLBACK");
  throw err;
} finally {
  client.release();
}
```

### 16. Choose isolation level deliberately

The default is a decision someone else made. For money movement, use `SERIALIZABLE` and retry on conflict. Acquire locks in a consistent order to minimize deadlocks.

### 17. Keep external calls out of transactions

A transaction holds locks and a pool connection. An HTTP call that hangs for 30s exhausts the pool and takes the service down with it. Charge first, then open the transaction and write.

### 18. Use expand-contract for schema changes

Never combine a schema change and a code change in one deploy. Expand first (backward-compatible), deploy code that uses it, then contract in a later release.

### 19. Every migration ships with a rollback plan

If you can't describe the rollback in one sentence, you're not ready to deploy. Never drop a column in the same deploy that stops using it — wait one release cycle.

### 20. Never lock a large table during migration

Table rewrites block all writes. For tables over ~1M rows, use zero-downtime strategies: Postgres 11+ adds columns with defaults instantly; MySQL needs `pt-online-schema-change` or `gh-ost`; SQLite requires a 12-step table rebuild.

### 21. Always use a connection pool

Opening a connection per query is 10–100x slower than reusing pooled ones. Size the pool to the database, not the app. Postgres formula: `pool_size = (cores * 2) + spindles`. Use PgBouncer for many app instances.

### 22. Set query timeouts on every connection

A query that runs forever holds a connection, blocks locks, and cascades failures. Set a timeout at the connection level so even a forgotten app-level timeout is protected.

## Quick reference

| Operation        | Postgres                | MySQL                          | SQLite                  |
| ---------------- | ----------------------- | ------------------------------ | ----------------------- |
| Query plan       | `EXPLAIN ANALYZE`       | `EXPLAIN FORMAT=JSON`          | `EXPLAIN QUERY PLAN`    |
| Auto-increment   | `SERIAL`                | `AUTO_INCREMENT`               | `INTEGER PRIMARY KEY`   |
| UPSERT           | `ON CONFLICT DO UPDATE` | `ON DUPLICATE KEY UPDATE`      | `ON CONFLICT DO UPDATE` |
| Boolean          | `BOOLEAN`               | `BOOLEAN` (= `TINYINT(1)`)     | `INTEGER` (0/1)         |
| Case-insensitive | `CITEXT`                | collation `utf8mb4_unicode_ci` | `COLLATE NOCASE`        |
| Covering index   | `INCLUDE (col)`         | composite (PK auto-appended)   | composite               |

---

_Part of the [skill collection](../README.md)._