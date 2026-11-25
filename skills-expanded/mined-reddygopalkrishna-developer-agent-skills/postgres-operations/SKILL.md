---
name: postgres-operations
description: Operates PostgreSQL in production - connection pooling with PgBouncer, autovacuum and bloat, transaction ID wraparound, replication and replication slots, backups with point-in-time recovery, restore tests and major version upgrades. Use when Postgres runs out of connections, tables bloat, vacuum falls behind, replicas lag, disk fills with WAL, or when setting up backups, pooling or an upgrade. Not for query tuning or schema changes.
license: MIT
---

# PostgreSQL Operations

Most Postgres outages are operational, not query bugs: too many connections, vacuum blocked by one forgotten transaction, a replication slot filling the disk with WAL, or a backup nobody ever restored. Measure the current state with the monitoring queries before changing any setting, and treat every change on a production cluster as a change that needs the user's explicit confirmation.

## When to use

- "too many connections", "remaining connection slots are reserved", pool exhaustion.
- Table or index bloat, autovacuum not keeping up, warnings about transaction ID wraparound.
- Replica lag, WAL directory or disk growing without stopping, logical replication or CDC setup.
- Designing or checking backups, point-in-time recovery (PITR), restore drills.
- Planning a major version upgrade.

Not for: slow individual queries and indexes (use sql-optimization), schema changes on live tables (use database-migrations), table design (use database-schema-design).

## Workflow

1. **Identify the setup.** Run `SELECT version();`. Find out whether it is self-managed or a managed service (RDS, Aurora, Cloud SQL, Azure Database for PostgreSQL, ...); managed services restrict some settings and run backups for you. Find the pooler (PgBouncer, a built-in proxy, or the application pool only).
2. **Gather facts with read-only queries** from [references/monitoring-queries.md](references/monitoring-queries.md): connections by state, longest transactions, dead tuples, wraparound age, replication lag, slot retention.
3. **Find the cause, not the symptom.** For example, bloat is usually caused by something preventing vacuum (a long transaction, an inactive slot), not by autovacuum being "too slow".
4. **Propose the smallest change** (a per-table setting, a timeout, a pool size) with the expected effect and how to roll it back.
5. **Stop and get explicit confirmation** before anything that changes a shared or production cluster: `ALTER SYSTEM`, restarts, `pg_terminate_backend`, `VACUUM FULL`, dropping a replication slot, failover, restoring over an existing database.
6. **Verify afterwards** with the same queries from step 2.

## Connection pooling

Each Postgres connection is a separate server process with its own memory, so thousands of direct connections hurt performance long before `max_connections` is reached. Put a pooler in front and keep `max_connections` modest.

| PgBouncer mode | Server connection returned to pool | Use for |
|---|---|---|
| `session` | When the client disconnects | Apps that need session features; little gain over no pooler |
| `transaction` | At the end of each transaction | **The usual choice** for web apps and serverless |
| `statement` | After each statement (multi-statement transactions are not allowed) | Rare; autocommit-only workloads |

In **transaction mode**, the next transaction may run on a different server connection, so session state is lost or leaks between clients:

| Breaks in transaction mode | Use instead |
|---|---|
| `SET search_path` / `SET statement_timeout` at session level | `SET LOCAL` inside the transaction, or set defaults per role: `ALTER ROLE app SET statement_timeout = '5s'` |
| Session advisory locks `pg_advisory_lock()` | Transaction-scoped `pg_advisory_xact_lock()` |
| `LISTEN` / `NOTIFY` listeners | A direct (unpooled) connection for listeners |
| Temp tables and `WITH HOLD` cursors across transactions | Keep them inside one transaction |
| Prepared statements | Depends on versions: newer PgBouncer releases can track protocol-level prepared statements (`max_prepared_statements`); older ones cannot. Check your PgBouncer version and your driver's docs, or disable server-side prepared statements in the driver |

Sizing:

- Total server connections = sum over every pool (app instances x pool size + workers + migrations + admin). Keep that well below `max_connections`, and leave room for superuser and replication connections.
- More connections rarely means more throughput. Start the pool near a small multiple of the CPU cores on the database server, then measure latency and throughput under load.
- Application pools behind PgBouncer should be small; PgBouncer does the multiplexing.

## Timeouts that prevent incidents

Set these per role or per application rather than globally, so admin and batch sessions can differ:

```sql
ALTER ROLE app SET statement_timeout = '15s';
ALTER ROLE app SET idle_in_transaction_session_timeout = '60s';
ALTER ROLE app SET lock_timeout = '5s';
```

- `idle_in_transaction_session_timeout` ends sessions that opened a transaction and went quiet. These hold locks and stop vacuum from cleaning up.
- `work_mem` applies **per sort or hash operation per query**, not per connection. One complex query can use it many times, times the number of connections. Raise it for a specific session or role that needs it, not globally.

## Autovacuum and bloat

`UPDATE` and `DELETE` leave dead row versions. Vacuum makes that space reusable; it can only remove rows that no open transaction might still need to see.

Things that stop vacuum from removing dead rows (check these first):

| Blocker | How to find it |
|---|---|
| Long-running or idle-in-transaction sessions | `pg_stat_activity` ordered by `xact_start` |
| Replication slots that are inactive or far behind | `pg_replication_slots` (`active`, `xmin`, `catalog_xmin`) |
| Long queries on a replica with `hot_standby_feedback = on` | `pg_stat_replication.backend_xmin` on the primary |
| Forgotten prepared transactions | `SELECT * FROM pg_prepared_xacts;` |

Tuning hot tables: the default thresholds scale with table size, so huge tables wait too long. Tune per table:

```sql
ALTER TABLE events SET (
  autovacuum_vacuum_scale_factor = 0.01,
  autovacuum_vacuum_threshold = 1000,
  autovacuum_analyze_scale_factor = 0.02
);
```

Removing existing bloat:

- Plain `VACUUM` makes space reusable but rarely shrinks the file. Fine to run online.
- `VACUUM FULL` and `CLUSTER` rewrite the table under an **ACCESS EXCLUSIVE lock**: all reads and writes block for the whole rewrite. Never run them on a busy production table without a maintenance window and the user's approval.
- Online alternatives: the `pg_repack` extension for tables, `REINDEX INDEX CONCURRENTLY` (PostgreSQL 12+) for bloated indexes.

### Transaction ID wraparound

Transaction IDs are 32-bit. Vacuum must "freeze" old rows before the counter wraps. If it falls too far behind, PostgreSQL stops accepting new write transactions to protect data. Treat this as a high-priority alert:

- Monitor `age(datfrozenxid)` per database and `age(relfrozenxid)` per table (queries in the reference).
- Autovacuum starts aggressive anti-wraparound vacuums at `autovacuum_freeze_max_age` (default 200 million). Alert well before the hard limit (about 2 billion), for example at 1 billion, and find out why freezing is not completing; it is almost always one of the blockers above.
- Never cancel an anti-wraparound autovacuum repeatedly; remove what blocks it instead.

## Replication

| Need | Use |
|---|---|
| Read scaling, high availability, failover | Physical streaming replicas |
| Major version upgrade with minimal downtime, replicating a subset of tables, feeding CDC tools (e.g. Debezium) | Logical replication (publications and subscriptions) |

- Monitor lag on the primary with `pg_stat_replication` (`write_lag`, `flush_lag`, `replay_lag`) and in bytes with `pg_wal_lsn_diff`.
- Reads from replicas are eventually consistent. Route read-your-own-writes paths to the primary.
- **Replication slots keep WAL until the consumer confirms it.** An abandoned or stalled slot (a dead CDC connector, a removed replica) keeps WAL forever and fills the disk. Monitor retained WAL per slot. On PostgreSQL 13+ cap it with `max_slot_wal_keep_size`. Dropping a slot (`pg_drop_replication_slot`) breaks that consumer, so confirm with the user and the slot's owner first.
- Logical replication needs a primary key (or a `REPLICA IDENTITY`) on tables that receive `UPDATE`/`DELETE`, and does not copy DDL. Check the docs for your version for what else it does not replicate (for example sequence values).

## Backups and restore

| Method | What you get | Limits |
|---|---|---|
| `pg_dump -Fc` / `pg_restore -j N` | Logical copy of one database; portable across versions | Point-in-time of the dump only; slow for large databases; roles need `pg_dumpall --globals-only` |
| Base backup + continuous WAL archiving | Point-in-time recovery to any moment in the retention window | Same major version; needs WAL archiving set up |
| Tools: pgBackRest, Barman, WAL-G | Base backups + WAL archive with retention, compression, parallelism, verification | Pick one and learn its restore command before you need it |
| Managed service snapshots + PITR | Same, run by the provider | Know the retention window and how long a restore takes |

Rules:

- **A backup is only proven by a restore.** Schedule restore drills (for example monthly) to a separate instance, run checks on the result, and record the time taken. That time is your real recovery time.
- Keep backups in a different account/region from the database, and protect them against deletion.
- Agree on RPO (how much data you can lose) and RTO (how long you can be down) with the user; they decide between nightly dumps and continuous archiving.
- Follow [references/backup-restore-runbook.md](references/backup-restore-runbook.md) for drills and real restores. Never restore over an existing database without explicit confirmation.

## Major version upgrades

| Method | Downtime | Notes |
|---|---|---|
| `pg_upgrade` (copy or `--link`) | Minutes, plus `ANALYZE` | Run `pg_upgrade --check` first. With `--link`, the old cluster cannot be used safely once the new one has started, so take a backup first |
| Logical replication to a new-version cluster | Seconds at switchover | Set up subscriptions, wait for sync, stop writes, sync sequences, switch the app |
| `pg_dump` / `pg_restore` | Long for big databases | Simplest for small databases |

After any upgrade: refresh planner statistics (`vacuumdb --all --analyze-in-stages`). From PostgreSQL 18, `pg_upgrade` keeps most statistics but not extended (`CREATE STATISTICS`) ones; run the commands it prints at the end (`vacuumdb --all --analyze-in-stages --missing-stats-only`, then `vacuumdb --all --analyze-only`). Rebuild or update extensions, and compare query latency with the old cluster. Test the whole upgrade on a copy first.

## Anti-patterns

- **Raising `max_connections` to fix "too many connections".** Add or fix pooling and find the connection leak.
- **Global `work_mem` increases.** Raise it per role or session for the queries that need it.
- **`VACUUM FULL` as routine maintenance.** It locks the table; fix what blocks autovacuum instead.
- **Ignoring idle-in-transaction sessions.** One can block vacuum on the whole database.
- **Leaving replication slots without an owner or monitoring.** The disk fills and the primary stops.
- **Backups that were never restored.** Assume they don't work until a drill proves they do.
- **Killing sessions or changing settings on production without asking.** `pg_terminate_backend` can roll back a user's long job; get confirmation.

## Done when

- The root cause is identified with query output, not guessed.
- Connections are pooled, total pool sizes fit under `max_connections` with headroom, and role-level timeouts are set.
- Dead tuples, wraparound age, replica lag and slot WAL retention are monitored with alerts.
- Backups exist and the latest restore drill succeeded within the agreed RTO.
- Any production change was confirmed by the user and verified afterwards.

## References

- [references/monitoring-queries.md](references/monitoring-queries.md) — read when diagnosing: copy-ready queries for connections, blocking, long transactions, bloat, wraparound, replication and slots.
- [references/backup-restore-runbook.md](references/backup-restore-runbook.md) — read when setting up backups, running a restore drill, or doing a real point-in-time restore.
