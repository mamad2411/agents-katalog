---
name: mysql-mariadb-operations-and-performance-tuning
description: >
  Covers day-2 MySQL/MariaDB operations: async, semi-sync, and GTID-based
  replication, InnoDB buffer pool sizing and I/O tuning, index and query
  optimization with EXPLAIN, and MariaDB-specific storage engine choices
  (InnoDB vs. Aria vs. ColumnStore/MyRocks). Use when the user asks to
  "tune MySQL performance," "set up MySQL replication," "why is this
  MySQL query slow," "size the InnoDB buffer pool," "switch a MariaDB
  table's storage engine," or "fix MySQL replication lag."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# MySQL/MariaDB Operations and Performance Tuning

## Purpose

MySQL and MariaDB (a drop-in-compatible fork that has since diverged in
storage engines, replication internals, and some SQL syntax) both default
to configurations sized for a small development box, not a production
workload — an under-sized `innodb_buffer_pool_size` turns every read into
disk I/O, and replication left on plain asynchronous mode with no GTIDs
makes failover a manual, error-prone reconciliation exercise. This skill
covers the recurring operational work of keeping a MySQL/MariaDB fleet
healthy: replication topology and consistency modes, InnoDB buffer pool
and I/O tuning, index/query optimization, and MariaDB-specific storage
engine selection. It assumes a working, already-provisioned instance; for
validating `my.cnf` changes and connection limits before they reach
production, see
[mysql-mariadb-configuration-validation](../mysql-mariadb-configuration-validation/SKILL.md),
and for multi-master clustering (Galera, Group Replication/InnoDB
Cluster) and split-brain prevention, see
[mysql-mariadb-high-availability-and-replication](../mysql-mariadb-high-availability-and-replication/SKILL.md).

## When to use

- Setting up or troubleshooting standard primary-replica replication
  (asynchronous, semi-synchronous, or GTID-based) for read scaling or
  failover readiness.
- Sizing `innodb_buffer_pool_size` and related InnoDB I/O settings for a
  new instance or after a workload/data-size change.
- A query that used to be fast is now slow, or `EXPLAIN` shows a full
  table scan where an index scan is expected.
- Choosing a storage engine on MariaDB for a specific table's access
  pattern (InnoDB for transactional OLTP, Aria for temporary/system
  tables, ColumnStore or MyRocks for analytical/write-heavy workloads).
- Diagnosing replication lag (`Seconds_Behind_Master` /
  `Seconds_Behind_Source` climbing) or a replica that stopped applying
  events.
- Planning connection-limit and thread-pool sizing ahead of a traffic
  increase.

## Prerequisites & environment

- MySQL 8.0+ or MariaDB 10.5+ assumed for the guidance and syntax below.
  Note explicitly where behavior differs: MySQL 8.0 replaced
  `MASTER_*`/`SLAVE_*` SQL keywords and terminology with
  `SOURCE_*`/`REPLICA_*` from 8.0.23 onward (both remain accepted as
  aliases for compatibility); MariaDB kept the original terminology and
  has its own GTID implementation (`gtid_strict_mode`,
  `gtid_current_pos`) that is not wire-compatible with MySQL's GTID sets
  (`gtid_executed`) — the two are not interchangeable in a mixed
  replication topology.
- `REPLICATION SLAVE` (MySQL) / `REPLICATION REPLICA` privilege for
  setting up replication; `PROCESS` and `SELECT` on
  `performance_schema`/`information_schema` for diagnostics.
- Binary logging enabled (`log_bin`) on any instance that will act as a
  replication source — this is off by default on a vanilla install and
  requires a restart to enable.
- For query diagnostics: `performance_schema` enabled (default on in
  recent MySQL/MariaDB) and, ideally, the `sys` schema views
  (`sys.statement_analysis`) or MariaDB's `slow_query_log` with
  `long_query_time` set low enough to actually catch problem queries.
- Enough free disk headroom on the source for binary log retention
  (`binlog_expire_logs_seconds` / `expire_logs_days`) sized to survive a
  replica outage without purging logs the replica still needs.

## Step-by-step guidance

### 1. Choose and configure a replication consistency mode deliberately

**Asynchronous** (the default): the source commits and returns to the
client without waiting for any replica to acknowledge — fastest, but a
source crash immediately after commit can lose transactions that never
reached a replica.

**Semi-synchronous**: the source waits for at least one replica to
acknowledge receipt of the transaction's binlog events (not that it has
applied them) before returning:
```ini
# my.cnf on the source
plugin_load = "rpl_semi_sync_source=semisync_source.so"
rpl_semi_sync_source_enabled = 1
rpl_semi_sync_source_timeout = 10000   # ms; falls back to async if no ACK in time
```
```ini
# my.cnf on the replica
plugin_load = "rpl_semi_sync_replica=semisync_replica.so"
rpl_semi_sync_replica_enabled = 1
```
Semi-sync closes the "lost transaction on source crash" gap for
acknowledged transactions, at the cost of added commit latency
(round-trip to at least one replica). It silently falls back to async if
`rpl_semi_sync_source_timeout` is exceeded — monitor
`Rpl_semi_sync_source_status` so a permanently-fallen-back-to-async
source isn't mistaken for still providing the durability guarantee.

**GTID-based replication** removes the need to track binary log
file/position pairs manually and makes failover/topology changes far
safer:
```ini
# my.cnf, both source and replica
gtid_mode = ON
enforce_gtid_consistency = ON
log_slave_updates = ON
```
```sql
CHANGE REPLICATION SOURCE TO
  SOURCE_HOST = '<SOURCE_HOST>',
  SOURCE_USER = 'repl',
  SOURCE_PASSWORD = '<REPLICATION_PASSWORD>',
  SOURCE_AUTO_POSITION = 1;
START REPLICA;
```
`SOURCE_AUTO_POSITION = 1` lets the replica negotiate its own resume
point from `gtid_executed`, instead of a hand-maintained file/position —
this is what makes promoting any replica to source (in a failover) or
repointing a replica at a new source straightforward, since every
transaction carries a globally unique identifier rather than a
position meaningful only relative to one specific binlog file.

### 2. Monitor replication lag and health correctly

```sql
SHOW REPLICA STATUS\G
-- Seconds_Behind_Source, Replica_IO_Running, Replica_SQL_Running
```
`Seconds_Behind_Source` (MySQL) / `Seconds_Behind_Master` (MariaDB) is
computed from timestamps embedded in binlog events, not real-time
measurement — a replica that has been disconnected and just reconnected
can show a misleadingly small lag briefly before catching up on the
actual backlog. For a more reliable single-writer-vs-replica-position
comparison, use GTID sets:
```sql
SELECT GTID_SUBTRACT(@@GLOBAL.gtid_executed, '<source_gtid_executed>') AS pending_gtids;
```
An empty result means the replica has applied everything the source has
generated as of that check.

### 3. Size the InnoDB buffer pool and related I/O settings

```ini
innodb_buffer_pool_size = 24G      # commonly 60-75% of available RAM on a dedicated DB host
innodb_buffer_pool_instances = 8   # split the pool to reduce mutex contention above a few GB
innodb_log_file_size = 2G          # larger = fewer checkpoints, longer crash recovery
innodb_flush_log_at_trx_commit = 1 # durable (fsync every commit); = 2 trades durability for throughput
innodb_flush_method = O_DIRECT     # avoid double-buffering through the OS page cache
```
`innodb_buffer_pool_size` is the single highest-leverage setting for read
performance — it caches both data and index pages, so an undersized pool
turns index lookups that should be in-memory into random disk reads.
Check the actual hit ratio before assuming a bigger pool is needed:
```sql
SHOW STATUS LIKE 'Innodb_buffer_pool_read%';
-- ratio of Innodb_buffer_pool_reads (disk) to Innodb_buffer_pool_read_requests (logical) should be very low (well under 1%) on a well-sized pool
```
`innodb_flush_log_at_trx_commit = 1` (fsync the redo log on every commit)
is the durable, ACID-compliant default — never change it to `0` or `2`
fleet-wide to "improve throughput" without an explicit, deliberate
decision that losing up to a second of committed transactions on an OS
crash (value `2`) or a MySQL crash (value `0`) is an acceptable trade for
that specific workload.

### 4. Diagnose and fix a slow query

```sql
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 42 AND status = 'pending';
```
Look for `type: ALL` (full table scan) in the classic `EXPLAIN` output,
or a large gap between estimated and actual rows in `EXPLAIN ANALYZE` —
both point at a missing or unused index. Cross-check with the slow query
log or `performance_schema` for aggregate, fleet-wide offenders rather
than guessing from a single query:
```sql
SELECT digest_text, count_star, sum_timer_wait/1000000000000 AS total_sec
FROM performance_schema.events_statements_summary_by_digest
ORDER BY sum_timer_wait DESC LIMIT 20;
```
Add the composite index matching the query's actual predicate order:
```sql
ALTER TABLE orders ADD INDEX idx_orders_customer_status (customer_id, status), ALGORITHM=INPLACE, LOCK=NONE;
```
`ALGORITHM=INPLACE, LOCK=NONE` avoids a full table rebuild/exclusive lock
for a secondary index add on InnoDB in modern versions — always specify
it explicitly for a live production table rather than relying on the
engine's default algorithm choice, and verify with `SHOW PROCESSLIST`
that it isn't blocked waiting behind a long-running transaction holding
metadata locks on the same table.

### 5. Choose MariaDB storage engines by workload, not by default

MariaDB ships several engines beyond InnoDB, each suited to a different
access pattern:
- **InnoDB** — default, transactional, row-level locking, the right
  choice for the overwhelming majority of OLTP tables.
- **Aria** — MariaDB's crash-safe successor to MyISAM, used internally
  for system/temporary tables; occasionally chosen for read-heavy,
  rarely-updated reference tables where InnoDB's transactional overhead
  isn't needed, though InnoDB is still the safer general default.
- **ColumnStore** — a columnar engine for analytical/OLAP workloads
  (large aggregations over wide tables) — a genuinely different storage
  layout from InnoDB's row-oriented B-tree, not a tuning variant of it.
- **MyRocks** (available via a MariaDB/Percona plugin) — an LSM-tree
  engine (RocksDB under the hood) that trades some read latency for
  much better write amplification and compression on write-heavy,
  storage-constrained workloads.
```sql
ALTER TABLE audit_log ENGINE = Aria;
```
Changing engine on an existing table rewrites the entire table (an
`ALGORITHM=COPY` operation under the hood) and takes a full table lock
for the duration on most versions — schedule it in a maintenance window
for any table of meaningful size, and never assume it's an online,
low-impact operation the way a secondary index add can be.

## Best practices

- Enable GTID-based replication (`gtid_mode = ON` / MariaDB's
  `gtid_strict_mode`) on any new topology — the operational cost of
  file/position-based replication (manually computing resume positions
  during failover) is avoidable and error-prone at the exact moment
  (an incident) when mistakes are costliest.
- Treat `innodb_flush_log_at_trx_commit = 1` and
  `sync_binlog = 1` as the production default for any data that must
  survive a crash without loss; only relax them for a specific,
  understood workload (e.g. a replica used purely for disposable
  reporting) with an explicit sign-off, not as a blanket performance
  shortcut.
- Size `innodb_buffer_pool_size` against measured
  `Innodb_buffer_pool_read` hit ratio and actual working-set size, not a
  fixed fraction of RAM chosen once and never revisited as data grows.
- Always specify `ALGORITHM=INPLACE, LOCK=NONE` explicitly for online
  DDL on live tables and verify the engine actually honors it for that
  specific operation (not all `ALTER TABLE` variants support
  `LOCK=NONE`) rather than assuming every schema change is non-blocking.
- Monitor semi-sync's fallback-to-async status
  (`Rpl_semi_sync_source_status`) as a standing alert, not just replica
  connectivity — a source silently running async because every replica
  timed out gives no warning by itself.
- Keep binary log retention (`binlog_expire_logs_seconds`) long enough to
  survive your worst realistic replica outage window, mirroring the same
  reasoning as oplog sizing in
  [mongodb-operations-and-scaling](../mongodb-operations-and-scaling/SKILL.md).

## Common pitfalls

- **Symptom:** `Seconds_Behind_Source` climbs steadily during peak
  write traffic and never fully recovers even overnight.
  **Fix:** Replication apply is commonly single-threaded per default
  configuration on older setups, or multi-threaded replication
  (`replica_parallel_workers` / `slave_parallel_threads`) is enabled but
  set too low, or is bottlenecked by a small number of hot tables that
  serialize regardless of worker count. Increase parallel replica
  workers, confirm `replica_parallel_type = LOGICAL_CLOCK` (MySQL) or the
  MariaDB equivalent for genuine cross-transaction parallelism, and
  investigate whether a few frequently-updated rows/tables are forcing
  serialization regardless of worker count.

- **Symptom:** A query with a `WHERE` clause matching an existing index
  still shows `type: ALL` in `EXPLAIN`.
  **Fix:** The optimizer's cost-based estimate found the index
  non-selective for this table's current statistics (stale after bulk
  load/delete), or the query uses a function/expression on the indexed
  column (`WHERE YEAR(created_at) = 2026`) that prevents index use
  entirely. Run `ANALYZE TABLE orders;` to refresh statistics, and
  rewrite range-friendly predicates (`created_at >= '2026-01-01' AND
  created_at < '2027-01-01'`) instead of wrapping the column in a
  function.

- **Symptom:** Semi-synchronous replication is configured, but a source
  crash still loses a transaction that was supposedly acknowledged.
  **Fix:** `rpl_semi_sync_source_timeout` had elapsed and the source
  fell back to asynchronous mode before the crash, silently, with no
  alert wired to `Rpl_semi_sync_source_status`. Alert on that status
  variable directly, and investigate why the replica couldn't
  acknowledge within the timeout (network latency, replica I/O thread
  lag) rather than only raising the timeout blindly.

- **Symptom:** `innodb_buffer_pool_size` was increased significantly, but
  query latency didn't improve.
  **Fix:** The working set already fit in the old, smaller pool (check
  `Innodb_buffer_pool_read` hit ratio before and after — if it was
  already near 100%, the pool wasn't the bottleneck). The actual
  bottleneck is more likely a missing index (confirm via `EXPLAIN`) or
  lock contention (`SHOW ENGINE INNODB STATUS` for the `TRANSACTIONS`
  section) rather than buffer pool size.

- **Symptom:** Someone runs `ALTER TABLE big_table ENGINE = InnoDB;` (or
  any engine change) directly against a large production table during
  business hours, expecting it to be as non-blocking as a secondary
  index add.
  **Fix:** An engine change is a full `ALGORITHM=COPY` table rewrite that
  takes an exclusive lock for its entire duration, unlike a properly
  specified `LOCK=NONE` index add.
  > **Warning — destructive/blocking action.** Never run an engine
  > change against a live, actively-written production table without
  > scheduling a maintenance window; for large tables, consider an
  > online schema-change tool (`pt-online-schema-change`,
  > `gh-ost`) that performs the rewrite via a shadow table and
  > triggers/binlog replay instead of a blocking in-place copy.

## Worked example

**Scenario:** An `orders` table (60M rows) on a MariaDB 10.6 primary
with one asynchronous replica shows the replica's `Seconds_Behind_Master`
climbing to over 900 seconds during nightly batch imports, and the
application's most common query against `orders` has degraded to
several hundred milliseconds.

1. Confirm the query regression:
   ```sql
   EXPLAIN SELECT * FROM orders WHERE customer_id = 42 AND status = 'pending';
   -- type: ALL, rows: 58000000
   ```
   No usable index exists for this predicate combination.
2. Add the missing composite index online:
   ```sql
   ALTER TABLE orders
     ADD INDEX idx_orders_customer_status (customer_id, status),
     ALGORITHM=INPLACE, LOCK=NONE;
   ANALYZE TABLE orders;
   ```
   Query latency drops from ~350ms to ~4ms; `EXPLAIN` now shows
   `type: ref` using the new index.
3. Investigate replication lag separately: `SHOW REPLICA STATUS\G` shows
   `Replica_SQL_Running_State: system lock`, and
   `slave_parallel_threads` is at its default of `0` (fully serial
   apply). Enable parallel replication and switch to GTID-based
   positioning to make any future failover clean:
   ```ini
   gtid_strict_mode = ON
   slave_parallel_threads = 8
   slave_parallel_mode = optimistic
   ```
4. Re-run the nightly batch import: replica lag during the same import
   window drops from 900s to under 60s with parallel apply enabled.
5. Add a standing alert on `Seconds_Behind_Master` and on
   `Innodb_buffer_pool_read` hit ratio so both classes of regression are
   caught before they're user-visible again, and validate the new
   `slave_parallel_threads`/GTID settings through
   [mysql-mariadb-configuration-validation](../mysql-mariadb-configuration-validation/SKILL.md)
   before rolling the same change out fleet-wide.

## Cross-references

- [mysql-mariadb-configuration-validation](../mysql-mariadb-configuration-validation/SKILL.md) — validates `my.cnf` changes (buffer pool size, replication settings, connection limits) like the ones made here before they reach production.
- [mysql-mariadb-high-availability-and-replication](../mysql-mariadb-high-availability-and-replication/SKILL.md) — multi-master clustering (Galera, Group Replication/InnoDB Cluster) and split-brain prevention, beyond the single-primary replication covered here.
- [database-connection-pooling-strategies](../database-connection-pooling-strategies/SKILL.md) — sizing and configuring ProxySQL in front of a MySQL/MariaDB replication topology like the one tuned here.
- [postgresql-operations-and-performance-tuning](../postgresql-operations-and-performance-tuning/SKILL.md) — the equivalent replication/vacuum/index tuning concerns in PostgreSQL, useful when the two engines coexist in the same platform.
