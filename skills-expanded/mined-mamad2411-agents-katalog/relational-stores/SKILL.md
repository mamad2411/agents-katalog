---
name: relational-stores
description: >
  The application database — the OLTP side of Postgres/MySQL that analytics SQL doesn't cover.
  Carries: schema design and where to stop normalising, **migrations that don't take an outage**
  (expand-migrate-contract, backward-compatible for one release, never a destructive change in the
  same deploy as the code needing it), connection pooling and why pool exhaustion presents as a
  latency incident, indexes and reading a query plan, transactions and isolation levels, the N+1
  problem, and Postgres extensions (pgvector, AGE, TimescaleDB, PostGIS) as an alternative to
  operating a second database. Load when designing a schema, writing a migration, debugging slow or
  timing-out queries, or deciding whether a workload needs its own store. Triggers: postgres,
  mysql, sqlite, schema design, migration, alembic, foreign key, index, EXPLAIN, query plan, slow
  query, connection pool, pgbouncer, transaction, isolation level, deadlock, N+1, ORM, sequential
  scan, autovacuum, bloat, primary key. Analytics/warehouse queries are `sql`; provisioning the
  instance is the cloud skills; vector search is `vector-stores`.
---

# relational-stores — the database the application actually runs on

**Pinned:** postgresql, alembic, sqlalchemy, pgbouncer — unpinned · authored 2026-07 · run
`/skill-update relational-stores` once the stack is chosen. Examples are Postgres-first; the concepts
carry to MySQL, the syntax often doesn't.

> On-demand: load this for the transactional database behind a service. **Analytics and warehouse
> query discipline stays in `sql`** — that skill is about answering questions from data at rest; this
> one is about a store that serves live traffic. Provisioning the managed instance is the cloud
> skills (`infra-aws`/`infra-gcp`/`infra-azure`); its network and credential posture is canon
> (`platform-security.md` `P11`, `data-governance.md` `D8`–`D10`).

## When this applies

Designing a schema. Writing a migration. Debugging a slow query or a timeout. Deciding whether a new
workload needs its own database.

## Schema

Normalise until it hurts, denormalise until it works — and know which one you're doing and why.

- **Every table gets a primary key.** Prefer a natural key where a real one exists; otherwise
  `bigint` identity or UUIDv7 (time-ordered, so it doesn't destroy index locality the way UUIDv4
  does).
- **Foreign keys on, with deliberate `ON DELETE` behaviour.** Referential integrity enforced by the
  database is enforced; enforced by application code is enforced until the one path that forgets.
- **Constraints in the schema** — `NOT NULL`, `CHECK`, `UNIQUE`. They are documentation the database
  guarantees.
- **`timestamptz`, never `timestamp`.** Store UTC. This is the cheapest bug to prevent and among the
  most expensive to unpick.
- **Tenancy is a column with an index and a policy, not a convention** (`D8`). Consider Postgres
  row-level security as defence in depth — it makes the missing `WHERE` clause fail closed — but
  server-side authorization in the application is still required (`I4`); RLS is a second layer, not
  the only one.
- **JSONB for genuinely variable structure only.** It is not a way to avoid schema design, and
  querying it is slower and less checkable than columns.

## Migrations — the part that causes outages

The rule (`reliability.md` `R3`): **every migration is backward-compatible with the currently running
code for at least one release.** A deploy is not atomic — old and new code run simultaneously.

**Expand → migrate → contract**, across three deploys:

| Phase | Do | Old code still works? |
|---|---|---|
| **Expand** | Add the new column/table, nullable, with a default. Dual-write | Yes |
| **Migrate** | Backfill in batches. Switch reads to the new column | Yes |
| **Contract** | Only once nothing reads the old one: drop it | N/A — it's gone |

Renaming a column in one migration is the canonical way to take an outage.

Backfills run **in batches with a sleep**, never as one statement over millions of rows — a long
transaction holds locks, bloats the table, and blocks autovacuum.

```python
# Alembic: additive, safe, reversible
def upgrade() -> None:
    op.add_column("documents", sa.Column("tenant_id", sa.BigInteger(), nullable=True))
    # CONCURRENTLY needs autocommit — a plain CREATE INDEX takes an exclusive lock on a live table
    with op.get_context().autocommit_block():
        op.create_index("ix_documents_tenant", "documents", ["tenant_id"], postgresql_concurrently=True)

def downgrade() -> None:
    op.drop_index("ix_documents_tenant", table_name="documents")
    op.drop_column("documents", "tenant_id")
```

- **`CREATE INDEX CONCURRENTLY`** on any table serving traffic. The plain form locks writes for the
  duration.
- **Set a `lock_timeout`** before DDL. A migration that queues behind a long query and then blocks
  every subsequent query is how a one-second `ALTER` becomes a ten-minute outage.
- **Write `downgrade()`, and test it.** An untested rollback is a plan, not a capability (`R3`).
- Adding a `NOT NULL` column *with a default* is cheap on modern Postgres and a full table rewrite on
  older versions and on MySQL — check before assuming.

## Connection pooling

**Pool exhaustion presents as a latency incident, and gets misdiagnosed as a slow database.** The
database is fine; requests are queued waiting for a connection that never frees.

- Postgres connections are processes and are expensive. A pool per replica, sized deliberately — and
  remember the total is `pool_size × replicas`, which is what actually hits `max_connections`.
- **Always set a pool checkout timeout.** Without one, a request waits forever and the symptom is an
  unbounded latency tail with a healthy-looking database.
- Use **PgBouncer** (transaction mode) when replica count makes direct pooling untenable —
  serverless and autoscaled workloads especially. Note transaction mode breaks session-level
  features: prepared statements, `SET`, advisory locks, `LISTEN/NOTIFY`.
- **Never hold a connection across an LLM call.** A multi-second generation holding a pooled
  connection will exhaust the pool under trivial load — fetch, release, generate, reacquire.

## Indexes and query plans

`EXPLAIN (ANALYZE, BUFFERS)` — and read the actual plan rather than guessing:

- **Seq Scan on a large table** in a selective query → the index is missing or unusable.
- **Estimated vs actual rows wildly apart** → stale statistics (`ANALYZE`), or a correlation the
  planner can't see.
- **Nested Loop over many rows** → usually a bad estimate upstream.
- **Sort spilling to disk** → raise `work_mem` for that query, or add an index that provides the
  order.

What to know: a composite index serves queries on a **prefix** of its columns, so column order
matters and `(a, b)` does not help a query on `b` alone. A function in a predicate disables a plain
index — index the expression instead. Partial indexes (`WHERE deleted_at IS NULL`) are small and
fast. And **every index costs write throughput** — an unused index is pure overhead, so check
`pg_stat_user_indexes` before adding another.

## Transactions

Postgres defaults to **Read Committed**, which permits non-repeatable reads and phantoms. Know what
you need:

| Level | Prevents | Costs |
|---|---|---|
| Read Committed | Dirty reads | Default; two reads in one transaction can differ |
| Repeatable Read | Non-repeatable reads | Serialization failures you must retry |
| Serializable | Everything | More retries; genuine correctness for financial/counting logic |

- **Keep transactions short.** A transaction open across a network call — especially an LLM call —
  holds locks and bloats the table.
- `SELECT ... FOR UPDATE` for read-modify-write; otherwise you have a lost-update race.
- **Retry serialization failures** (`40001`) — with Repeatable Read or Serializable they're expected,
  not exceptional.
- Deadlocks: acquire locks in a consistent order everywhere.

## Postgres extensions — often the right answer to "do we need another database?"

Before adding a system to operate, back up, secure, and pay for:

| Need | Extension |
|---|---|
| Vector search | **pgvector** (see `vector-stores`) |
| Graph traversal | **Apache AGE** (see `graph-stores`) |
| Time-series | **TimescaleDB** — hypertables, compression, continuous aggregates |
| Geospatial | **PostGIS** |
| Query stats | **pg_stat_statements** — turn it on now; you'll want the history later |

One system means one backup, one restore drill (`D10`), one network posture (`P11`), one set of
credentials. That is worth a lot of benchmark headroom.

## Gotchas

- **The ORM's N+1.** One query for the list, one per row for its relations. Eager-load explicitly;
  log query counts per request in dev, because N+1 is invisible until production data volume.
- **`SELECT *` through an ORM** pulls large columns you didn't want across the wire on every row.
- **No statement timeout.** Set one at the role or connection level — one runaway query should not
  become an incident.
- **Autovacuum ignored until bloat is a crisis.** Monitor dead tuples; a high-churn table often needs
  per-table tuning.
- **String-interpolated SQL.** Parameterise. Model-generated SQL especially (`ai-security.md` `AI5`).
- **Read replicas assumed consistent.** They lag. Read-after-write against a replica returns stale
  data; route those reads to the primary.
- **Backups never restored.** Canon `D10` — an untested backup fails at the only moment it matters.
