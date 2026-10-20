---
name: postgresql-operations-and-performance-tuning
description: >
  Covers day-2 PostgreSQL operations: streaming and logical replication,
  vacuum/autovacuum tuning and bloat remediation, connection pooling with
  PgBouncer, query performance tuning (EXPLAIN ANALYZE, indexing, planner
  statistics), and major-version upgrade strategy (pg_upgrade vs. logical
  replication cutover). Use when the user asks to "tune PostgreSQL
  performance," "set up PostgreSQL replication," "fix table bloat," "size a
  PgBouncer pool," "why is this query slow," or "upgrade PostgreSQL to a new
  major version."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# PostgreSQL Operations and Performance Tuning

## Purpose

PostgreSQL's default configuration is tuned for compatibility on modest
hardware, not for the throughput and durability a production workload
needs — left untouched, autovacuum falls behind, connections exhaust
`max_connections` under a web-scale request fan-out, and query plans
degrade silently as statistics go stale. This skill covers the recurring
operational work of keeping a PostgreSQL fleet healthy under load:
replication for read scaling and failover readiness, vacuum/bloat
management, connection pooling, query tuning, and major-version upgrades.
It assumes a working, already-provisioned PostgreSQL instance; for
designing an HA/failover topology specifically, see
[postgresql-high-availability-and-failover](../postgresql-high-availability-and-failover/SKILL.md),
and for validating configuration changes before they reach production, see
[postgresql-configuration-validation](../postgresql-configuration-validation/SKILL.md).

## When to use

- Setting up streaming replication for a read replica, or logical
  replication for selective table replication / cross-version migration /
  zero-downtime major-version upgrades.
- Diagnosing table or index bloat (`pg_stat_user_tables`, oversized
  relation files relative to live row estimates) and remediating it.
- A query that used to be fast is now slow, or `EXPLAIN ANALYZE` shows a
  sequential scan where an index scan is expected.
- Sizing or troubleshooting a PgBouncer pool (connection exhaustion,
  "too many clients already," transaction pooling breaking prepared
  statements or session-level features).
- Planning a major-version upgrade (e.g. PostgreSQL 14 → 16) and deciding
  between `pg_upgrade` (in-place, minimal-downtime with `--link`) and a
  logical-replication-based cutover (near-zero downtime, more moving
  parts).
- Autovacuum is falling behind (`n_dead_tup` climbing, transaction ID
  wraparound warnings in logs).

## Prerequisites & environment

- PostgreSQL 13+ assumed for the guidance below; logical replication is
  available from PostgreSQL 10 onward but this skill's examples assume
  13+ behavior (e.g. `pg_stat_progress_vacuum`, improved logical
  replication of large transactions in 13+). Note explicitly where a
  feature requires a specific newer version (e.g. logical replication of
  `TRUNCATE` requires 11+; replication of generated columns and row
  filters for logical replication require 15+).
- Superuser or a role with `REPLICATION` privilege for setting up
  streaming/logical replication; `pg_monitor` role membership is
  sufficient for most read-only diagnostic queries below.
- `wal_level` must be `replica` (streaming) or `logical` (logical
  replication) — this is a restart-required setting, not reloadable.
- PgBouncer (or an equivalent pooler, e.g. pgbouncer/pgcat/odyssey)
  installed on a host between the application and PostgreSQL for
  connection pooling guidance.
- Access to `pg_stat_statements` (extension must be created and listed in
  `shared_preload_libraries`) for query performance analysis — without it
  you are limited to single-query `EXPLAIN ANALYZE` rather than
  aggregate, fleet-wide slow-query identification.

## Step-by-step guidance

### 1. Set up streaming replication (physical, for HA/read-scaling)

On the primary, enable WAL shipping and create a replication role:
```sql
-- postgresql.conf on primary
wal_level = replica
max_wal_senders = 10
wal_keep_size = '2GB'          -- retain enough WAL for replica catch-up
hot_standby = on

-- Create a dedicated, least-privilege replication role
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD '<REPLICATION_PASSWORD>';
```
Add a `pg_hba.conf` entry scoped to the replica's IP, not `0.0.0.0/0`:
```
host    replication     replicator      <REPLICA_IP>/32       scram-sha-256
```
On the replica, take a base backup and configure it as a standby:
```bash
pg_basebackup -h <PRIMARY_HOST> -U replicator -D /var/lib/postgresql/data \
  -Fp -Xs -P -R
```
`-R` writes `postgresql.auto.conf` with `primary_conninfo` and creates
`standby.signal` automatically (PostgreSQL 12+); on older supported
versions you populate `recovery.conf` instead. Verify replication is
flowing from the primary:
```sql
SELECT client_addr, state, sync_state, replay_lag
FROM pg_stat_replication;
```
`sync_state` of `async` is the default; set `synchronous_standby_names`
on the primary if you need synchronous commit guarantees for a specific
replica (at the cost of primary write latency if that replica lags or
disconnects).

### 2. Set up logical replication (selective tables, cross-version, or zero-downtime upgrade)

```sql
-- On the publisher (source)
ALTER SYSTEM SET wal_level = 'logical';   -- restart required
CREATE PUBLICATION orders_pub FOR TABLE orders, order_items;

-- On the subscriber (target) — schema must already exist there
CREATE SUBSCRIPTION orders_sub
  CONNECTION 'host=<PUBLISHER_HOST> dbname=appdb user=replicator password=<REPLICATION_PASSWORD>'
  PUBLICATION orders_pub;
```
Logical replication replicates row-level changes (INSERT/UPDATE/DELETE),
not DDL — schema changes on the publisher must be applied manually on the
subscriber first, in a compatible order, before the corresponding DML
arrives. Monitor lag with:
```sql
SELECT slot_name, confirmed_flush_lsn, pg_current_wal_lsn() - confirmed_flush_lsn AS lag_bytes
FROM pg_replication_slots;
```
An orphaned, unused replication slot holds WAL on disk indefinitely and
will eventually fill the primary's disk — always `DROP SUBSCRIPTION` (or
`ALTER SUBSCRIPTION ... DISABLE` then drop the slot) when decommissioning
a subscriber, never just stop the subscriber process.

### 3. Tune autovacuum and manage bloat

Check dead-tuple ratio and autovacuum activity per table:
```sql
SELECT relname, n_live_tup, n_dead_tup,
       round(n_dead_tup::numeric / GREATEST(n_live_tup, 1), 3) AS dead_ratio,
       last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 20;
```
For a specific hot table (high write/update churn), tune per-table
autovacuum thresholds rather than globally lowering
`autovacuum_vacuum_scale_factor` fleet-wide (which increases I/O pressure
on tables that don't need it):
```sql
ALTER TABLE orders SET (
  autovacuum_vacuum_scale_factor = 0.02,
  autovacuum_vacuum_cost_delay = 2,
  autovacuum_analyze_scale_factor = 0.01
);
```
For existing severe bloat, `VACUUM FULL` reclaims space but takes an
`ACCESS EXCLUSIVE` lock for the duration — schedule it in a maintenance
window, or use `pg_repack` (external extension) for an online rebuild
that avoids blocking reads/writes for the whole operation. Check
transaction ID wraparound risk (a hard outage risk, not just a
performance one) with:
```sql
SELECT datname, age(datfrozenxid) FROM pg_database ORDER BY 2 DESC;
```
An age approaching `autovacuum_freeze_max_age` (default 200M) means
autovacuum will force an aggressive freeze vacuum soon; an age approaching
2^31 risks the database refusing new writes entirely — treat a climbing
value with no corresponding vacuum activity as an urgent operational
issue, not routine noise.

### 4. Size and configure PgBouncer

```ini
# pgbouncer.ini
[databases]
appdb = host=<PRIMARY_HOST> port=5432 dbname=appdb

[pgbouncer]
listen_port = 6432
pool_mode = transaction
max_client_conn = 2000
default_pool_size = 25
reserve_pool_size = 5
```
`default_pool_size` is the number of actual backend connections
PgBouncer holds open per database/user pair — this, not
`max_client_conn`, is what determines load on PostgreSQL's own
`max_connections`. A common sizing heuristic: backend pool size should be
close to `(core_count * 2) + effective_spindle_count` for CPU-bound
workloads, well under `max_connections`, since PostgreSQL's per-connection
memory and context-switch overhead degrades throughput long before
`max_connections` is actually hit. `pool_mode = transaction` is the right
default for most web workloads, but it breaks session-level features
(`SET` persisting across statements, `LISTEN/NOTIFY`, prepared statements
via some drivers) — use `pool_mode = session` for a specific database/user
pair that needs those, not fleet-wide.

### 5. Diagnose and fix a slow query

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE customer_id = 42 AND status = 'pending';
```
Read the plan bottom-up: look for a `Seq Scan` on a large table where an
index on `(customer_id, status)` would let the planner use an `Index
Scan`, and compare `actual time` against `rows` — a large gap between
planner-estimated rows and actual rows usually means stale statistics
(`ANALYZE orders;`) rather than a missing index. With
`pg_stat_statements` enabled, find the worst aggregate offenders across
the whole workload rather than guessing from application logs:
```sql
SELECT query, calls, total_exec_time, mean_exec_time, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
```
Create the composite index matching the query's actual predicate order
and selectivity (most selective / most frequently equality-filtered
column first for a b-tree, unless the query relies on range scans on a
specific column):
```sql
CREATE INDEX CONCURRENTLY idx_orders_customer_status
  ON orders (customer_id, status);
```
Always use `CONCURRENTLY` for index creation on a live production table —
a plain `CREATE INDEX` takes a lock that blocks writes for the whole
build. `CONCURRENTLY` takes roughly twice as long and can leave an
invalid index behind if it fails partway (check
`pg_index.indisvalid`; drop and retry rather than leaving an invalid
index in place, since the planner ignores it but it still costs write
overhead).

### 6. Plan a major-version upgrade

For most fleets, `pg_upgrade` with hard-linking is the standard path and
completes in minutes regardless of database size (it relinks data files
rather than copying them, so it's not simply a data-volume-driven
duration):
```bash
pg_upgrade \
  --old-datadir=/var/lib/postgresql/14/data \
  --new-datadir=/var/lib/postgresql/16/data \
  --old-bindir=/usr/lib/postgresql/14/bin \
  --new-bindir=/usr/lib/postgresql/16/bin \
  --link
```
This requires downtime for the duration of the upgrade run (typically
seconds to a few minutes with `--link`) plus mandatory post-upgrade
`ANALYZE` (statistics are not carried over) before performance is back
to baseline. For workloads that cannot tolerate any downtime window, set
up logical replication to a new-version replica, let it catch up, run
`ANALYZE` on the new instance ahead of time, then cut application traffic
over and drop the old primary — more operational complexity, but the
downtime window shrinks to a connection-string cutover.

## Best practices

- Always run `ANALYZE` (or wait for autoanalyze) immediately after any
  bulk load, `pg_upgrade`, or restore — a planner working from stale or
  default statistics will pick catastrophically bad plans even with
  perfect indexing.
- Alert on replication lag (`replay_lag` for physical, WAL byte lag for
  logical) as a first-class SLO metric, not just on replica
  connectivity — a "connected" replica that's hours behind is often worse
  than a disconnected one, since failover to it silently loses recent
  data.
- Never lower `autovacuum_vacuum_cost_delay` to zero fleet-wide to "make
  vacuum faster" — this removes autovacuum's I/O throttling and can
  starve foreground query I/O during business hours; tune scope and
  scale factor per table instead.
- Prefer `CREATE INDEX CONCURRENTLY` and `DROP INDEX CONCURRENTLY` on any
  table receiving live traffic; reserve the non-concurrent form for
  tables you know are not yet serving traffic.
- Keep `pg_stat_statements` enabled in production — the aggregate,
  fleet-wide visibility it gives into query cost is worth the small
  (typically low single-digit percent) overhead, and it's the only
  practical way to find "slow because it runs 50,000 times a minute"
  queries that no single `EXPLAIN ANALYZE` would reveal.
- Test a major-version upgrade against a realistic data-shaped staging
  copy first, specifically checking for deprecated features, changed
  default settings, and extension version compatibility — validate the
  target configuration itself with
  [postgresql-configuration-validation](../postgresql-configuration-validation/SKILL.md)
  before it reaches production.

## Common pitfalls

- **Symptom:** Replica disk usage grows unboundedly, or the primary's
  `pg_wal` directory fills the disk.
  **Fix:** An inactive/abandoned replication slot (physical or logical)
  holds WAL on the primary indefinitely regardless of `wal_keep_size`.
  Check `pg_replication_slots` for slots with `active = false` and drop
  ones tied to decommissioned replicas/subscribers
  (`SELECT pg_drop_replication_slot('slot_name')`).

- **Symptom:** `n_dead_tup` keeps climbing on a specific table despite
  autovacuum apparently running, and query latency on that table
  degrades over weeks.
  **Fix:** A long-running transaction (an idle-in-transaction session, an
  uncommitted logical replication subscriber, or a long analytical query)
  is holding back the vacuum horizon, preventing autovacuum from
  reclaiming dead tuples newer than that transaction's snapshot. Find it
  with `SELECT pid, state, xact_start, query FROM pg_stat_activity WHERE
  state = 'idle in transaction' ORDER BY xact_start;` and terminate or
  fix the offending session/application code, not just re-run vacuum.

- **Symptom:** PgBouncer in `transaction` pooling mode intermittently
  breaks prepared statements or `SET search_path` seems to randomly stop
  applying.
  **Fix:** In transaction pooling mode, a client's backend connection can
  change between transactions, so anything scoped to a session (prepared
  statements via the simple protocol, `SET` outside a transaction,
  advisory locks held across transactions) is unsafe. Either switch that
  workload's pool to `pool_mode = session`, or use a driver/ORM mode
  that avoids server-side prepared statements against a transaction-mode
  pool.

- **Symptom:** `CREATE INDEX CONCURRENTLY` fails partway (e.g. due to a
  deadlock with a concurrent transaction) and subsequent identical
  `CREATE INDEX` attempts fail with "relation already exists."
  **Fix:** The failed attempt leaves an invalid index behind
  (`pg_index.indisvalid = false`) that still consumes disk and write
  overhead but is never used by the planner. Drop it explicitly
  (`DROP INDEX CONCURRENTLY idx_name;`) before retrying.

- **Symptom:** A `pg_upgrade` run (or any DDL change) is executed directly
  against production with no tested rollback path, and the upgrade
  surfaces an incompatibility only after cutover.
  **Fix:** This is a destructive, hard-to-reverse action if attempted
  without a rehearsal — always dry-run `pg_upgrade --check` first, take a
  verified backup/snapshot immediately before the real run, and rehearse
  the full upgrade against a staging copy with production-shaped data and
  extensions before touching production, with a documented rollback plan
  (e.g. restoring from the pre-upgrade data directory, since `pg_upgrade
  --link` leaves the old cluster's data directory intact but
  unusable once the new cluster has started writing).

## Worked example

**Scenario:** An `orders` table (40M rows, high UPDATE churn on a
`status` column) has degraded from ~5ms to ~400ms for the app's most
common query, and a replica used for reporting is falling behind.

1. Confirm the regression and check statistics freshness:
   ```sql
   EXPLAIN (ANALYZE, BUFFERS)
   SELECT * FROM orders WHERE customer_id = 42 AND status = 'pending';
   -- Seq Scan on orders (actual rows=3 planner estimate=48000)
   ```
   The huge estimate-vs-actual gap points at stale statistics compounded
   by a missing index for this predicate combination.
2. Check bloat and vacuum health on the table:
   ```sql
   SELECT n_live_tup, n_dead_tup, last_autovacuum
   FROM pg_stat_user_tables WHERE relname = 'orders';
   -- n_live_tup=40000000 n_dead_tup=9800000 last_autovacuum=NULL
   ```
   Dead-tuple ratio of ~24% with autovacuum never having completed on
   this table indicates it's losing the race against write volume —
   confirmed by checking for a long-running idle-in-transaction
   reporting session on the replica that was holding back the vacuum
   horizon on the primary via a replication slot's `xmin`.
3. Remediate in order: terminate the offending idle session, tighten
   this table's autovacuum thresholds, then build the missing composite
   index concurrently:
   ```sql
   ALTER TABLE orders SET (autovacuum_vacuum_scale_factor = 0.02);
   CREATE INDEX CONCURRENTLY idx_orders_customer_status ON orders (customer_id, status);
   ANALYZE orders;
   ```
4. Re-run the query: plan now shows `Index Scan using
   idx_orders_customer_status`, actual time back to ~4ms. Replica lag
   drops to near-zero within one autovacuum cycle as the vacuum horizon
   is no longer held back.
5. Add a standing alert on `age(datfrozenxid)` and on
   `n_dead_tup/n_live_tup` ratio per table so the same drift is caught
   before it becomes user-visible next time.

## Cross-references

- [postgresql-high-availability-and-failover](../postgresql-high-availability-and-failover/SKILL.md) — designing the replication topology and failover automation this skill's replication setup feeds into.
- [postgresql-configuration-validation](../postgresql-configuration-validation/SKILL.md) — validating `postgresql.conf` changes (e.g. `max_connections`, `wal_level`) and connection-limit math before applying any tuning from this skill to production.
- [database-schema-migration-with-liquibase-and-flyway](../database-schema-migration-with-liquibase-and-flyway/SKILL.md) — for the DDL changes (e.g. adding the index above via a tracked migration) that should accompany ad hoc tuning changes rather than being applied by hand.
