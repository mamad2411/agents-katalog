---
name: database-connection-pooling-strategies
description: >
  Cross-database connection pooling patterns and tooling: PgBouncer for
  PostgreSQL, ProxySQL for MySQL/MariaDB, and the shared design questions
  (transaction vs. session vs. statement pooling modes, backend pool
  sizing, failover-aware routing) that apply regardless of the
  underlying database engine. Use when the user asks to "size a
  connection pool," "choose between transaction and session pooling,"
  "set up ProxySQL for MySQL," "why do prepared statements break under
  pooling," or "route reads/writes through a proxy during failover."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# Database Connection Pooling Strategies

## Purpose

Every relational database has a real, finite cost per open connection —
memory, a backend process/thread, and context-switch overhead — which
means "just let every application instance open its own connections"
stops scaling long before the database's actual query-processing
capacity is exhausted. A connection pooler sits between application and
database specifically to decouple the number of *client-facing*
connections (which can be very large — thousands of application threads)
from the number of *backend* connections the database actually has to
serve (which should stay well under the database's practical capacity).
This skill covers the pooling-mode decision that generalizes across
engines (transaction vs. session vs. statement pooling), and the two
dominant tools that implement it for the two most common relational
engines — **PgBouncer** for PostgreSQL and **ProxySQL** for MySQL/
MariaDB — plus the failover-aware routing patterns that make a pooler
also useful as an application-transparent HA layer, not just a
connection multiplexer.

## When to use

- Sizing a new connection pool for an application ahead of launch, or
  re-sizing one after "too many connections"/"connection exhausted"
  errors.
- Choosing a pooling mode (transaction, session, or statement) for a
  specific workload, and understanding what application behavior each
  mode breaks.
- Diagnosing prepared statements, session-level `SET` variables, or
  advisory locks behaving unexpectedly under a pooled connection.
- Setting up ProxySQL in front of a MySQL/MariaDB replication or Galera
  topology for read/write splitting or failover-aware routing.
- Deciding whether to add a pooler at all for a given workload/database
  engine, versus relying on the database's own native connection
  handling (e.g. PostgreSQL's process-per-connection model vs. MySQL's
  thread-per-connection model have different practical connection
  ceilings before a pooler becomes necessary).

## Prerequisites & environment

- A target database's actual connection-handling model understood
  before sizing anything: PostgreSQL forks an OS process per
  connection (higher per-connection memory/context-switch cost, lower
  practical `max_connections` ceiling before performance degrades);
  MySQL/MariaDB use a thread per connection (generally cheaper per
  connection, higher realistic ceiling, but still finite).
- PgBouncer 1.18+ or ProxySQL 2.x assumed for the configuration syntax
  below.
- Network connectivity from every application host to the pooler, and
  from the pooler to every database backend (primary and replicas) —
  the pooler becomes a new single point of failure unless it's itself
  deployed redundantly (typically as a sidecar per application host, or
  as a small fleet behind a load balancer).
- Visibility into current connection counts and pool utilization on the
  target database (`pg_stat_activity` for PostgreSQL,
  `SHOW STATUS LIKE 'Threads_connected'` for MySQL/MariaDB) to size
  against real demand rather than a guess.
- For failover-aware routing: an understanding of the underlying HA
  topology (see
  [postgresql-high-availability-and-failover](../postgresql-high-availability-and-failover/SKILL.md)
  or
  [mysql-mariadb-high-availability-and-replication](../mysql-mariadb-high-availability-and-replication/SKILL.md))
  since the pooler's routing configuration must track which node is
  currently primary, not assume a static hostname.

## Step-by-step guidance

### 1. Choose a pooling mode deliberately — this decision determines what breaks

- **Session pooling**: a client holds its backend connection for the
  entire duration of its session (until it disconnects). Safest —
  everything session-scoped (`SET` variables, prepared statements,
  advisory locks, temp tables) behaves exactly as it would without a
  pooler — but gives the least connection-multiplexing benefit, since
  one idle client still holds one backend connection.
- **Transaction pooling**: a backend connection is assigned to a client
  only for the duration of a single transaction, returned to the pool
  immediately on commit/rollback. The dominant mode for high-
  concurrency web workloads (many short transactions, most connections
  idle between requests) since it multiplexes far more client
  connections onto far fewer backend ones — but breaks anything that
  must persist *across* transactions on the same backend connection:
  session-level `SET`, `LISTEN/NOTIFY`, advisory locks held across
  transactions, and (depending on client library) server-side prepared
  statements.
- **Statement pooling**: a backend connection is held only for a single
  statement, even within a transaction — the most aggressive
  multiplexing, but incompatible with multi-statement transactions
  entirely (each statement could land on a different backend
  connection) and rarely appropriate for typical application workloads;
  mostly relevant for specific analytical/reporting proxy scenarios.

Pick per workload, not fleet-wide by default: a typical stateless web
application backend is the canonical transaction-pooling case; a
migration runner or a session relying on temp tables/advisory locks
needs session pooling even if the rest of the fleet uses transaction
mode.

### 2. Configure PgBouncer for PostgreSQL

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
reserve_pool_timeout = 3
```
`default_pool_size` — the actual backend connections PgBouncer holds
open per database/user pair — is what determines load on PostgreSQL's
`max_connections`, not `max_client_conn`. Size it against
`(core_count * 2) + effective_spindle_count` as a starting heuristic for
CPU-bound OLTP workloads, well under `max_connections`, then validate
against measured PostgreSQL-side connection counts and query latency
rather than trusting the heuristic blindly. `reserve_pool_size` gives a
small burst allowance above `default_pool_size` for transient spikes,
activated only after `reserve_pool_timeout` of queueing — a safety
valve, not a substitute for correct baseline sizing.

### 3. Configure ProxySQL for MySQL/MariaDB

```sql
-- ProxySQL admin interface (port 6032) — configure backend servers
INSERT INTO mysql_servers (hostgroup_id, hostname, port) VALUES (10, '<PRIMARY_HOST>', 3306);
INSERT INTO mysql_servers (hostgroup_id, hostname, port) VALUES (20, '<REPLICA_HOST>', 3306);

-- Query rule: route SELECTs to the replica hostgroup, everything else to primary
INSERT INTO mysql_query_rules (rule_id, active, match_pattern, destination_hostgroup, apply)
VALUES (100, 1, '^SELECT.*FOR UPDATE$', 10, 1),
       (200, 1, '^SELECT', 20, 1);

LOAD MYSQL SERVERS TO RUNTIME;
LOAD MYSQL QUERY RULES TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
SAVE MYSQL QUERY RULES TO DISK;
```
ProxySQL is meaningfully more than a connection pool — it's a
query-aware proxy that can route based on query pattern (the `SELECT ...
FOR UPDATE` rule above deliberately routes locking reads to the primary
hostgroup even though it matches `^SELECT`, since a replica's data may
be stale for a read that's about to inform a write). Configure
per-hostgroup connection pool sizing similarly to PgBouncer's
`default_pool_size`:
```sql
UPDATE mysql_servers SET max_connections = 50 WHERE hostgroup_id = 10;
LOAD MYSQL SERVERS TO RUNTIME;
```
Every configuration change must be explicitly `LOAD`ed to runtime and
`SAVE`d to disk — a change left only in the in-memory admin tables
without both steps is lost on ProxySQL restart, a common source of
"the config change didn't survive a restart" confusion.

### 4. Route around failover without an application-side connection-string change

Both poolers can track which backend is currently the writable primary
and update routing without the application knowing a failover happened:
```ini
# PgBouncer: paired with a healthcheck/failover manager (e.g. Patroni)
# that rewrites the [databases] host entry via a reload, or via a
# virtual IP/DNS layer PgBouncer connects through instead of a static host
```
```sql
-- ProxySQL: mysql_replication_hostgroups lets ProxySQL detect the
-- current primary automatically via read_only status, not a static config entry
INSERT INTO mysql_replication_hostgroups (writer_hostgroup, reader_hostgroup, check_type)
VALUES (10, 20, 'read_only');
LOAD MYSQL SERVERS TO RUNTIME;
```
With `mysql_replication_hostgroups` configured, ProxySQL periodically
checks each backend's `read_only` variable and automatically moves a
newly-promoted primary into the writer hostgroup — this is what makes a
MySQL/MariaDB failover (whether via Orchestrator, Galera's own
membership, or manual promotion) transparent to the application, which
only ever talks to ProxySQL's stable endpoint.

### 5. Size and monitor pool utilization on an ongoing basis

```sql
-- PgBouncer admin console
SHOW POOLS;
SHOW STATS;
```
```sql
-- ProxySQL stats schema
SELECT * FROM stats_mysql_connection_pool;
```
Watch for a pool consistently at its `default_pool_size`/
`max_connections` ceiling with client connections queueing
(`cl_waiting` in PgBouncer's `SHOW POOLS`, or growing queue depth in
ProxySQL's connection pool stats) — this is the actual signal that a
pool needs resizing, not application-reported "connection timeout"
errors alone, which can also be caused by a genuinely overloaded
database backend that more pooled connections would only make worse.

## Best practices

- Default new stateless web workloads to transaction pooling, and treat
  session pooling as an explicit, narrow exception for specific
  connections/workloads that need session-scoped features — not the
  reverse.
- Size backend pools against measured database-side connection/CPU
  capacity, not client-side connection count — the pooler's entire
  purpose is decoupling those two numbers.
- Always route application traffic through the pooler's stable
  endpoint, never a specific database node's hostname directly, so a
  planned or unplanned failover doesn't require an application
  redeploy/config change.
- For ProxySQL, always pair `LOAD ... TO RUNTIME` with `SAVE ... TO
  DISK` for every configuration change — a change that only reaches
  runtime is lost on the next restart.
- Monitor pool-level queueing metrics (not just application-observed
  latency) as the primary signal for resizing — a pool at its ceiling
  with queued clients is a clear, direct signal; elevated application
  latency alone could have several other causes.
- Deploy the pooler itself with redundancy appropriate to the
  workload's availability requirement — a single PgBouncer/ProxySQL
  instance is a new single point of failure sitting in front of an
  otherwise-HA database.

## Common pitfalls

- **Symptom:** Under transaction pooling, prepared statements
  intermittently fail, or `SET search_path`/`SET NAMES` appears to
  randomly stop taking effect.
  **Fix:** In transaction pooling mode, a client's backend connection
  can change between transactions, so anything scoped to a session
  (server-side prepared statements via some drivers, a `SET` issued
  outside a transaction, advisory locks held across transactions) is
  unsafe. Either switch that specific workload's pool to session mode,
  or configure the client driver to avoid server-side prepared
  statements against a transaction-pooled connection (many modern
  drivers support a client-side/"simple query" prepared-statement mode
  specifically for this).

- **Symptom:** ProxySQL's query routing rules appear correct in the
  admin tables but have no effect on actual traffic.
  **Fix:** The rules were inserted into the admin schema but never
  promoted to runtime. Always run `LOAD MYSQL QUERY RULES TO RUNTIME;`
  (and the equivalent for servers/variables) after any change, and
  `SAVE ... TO DISK` so the change survives a ProxySQL restart.

- **Symptom:** Application connection errors ("too many clients
  already" or ProxySQL connection timeouts) occur even though the pool
  size looks generously configured.
  **Fix:** Check `SHOW POOLS`/`stats_mysql_connection_pool` for actual
  queueing before assuming the pool is undersized — a pool that's
  correctly sized can still queue if the *database itself* is the
  bottleneck (slow queries holding connections open longer than
  expected), in which case adding more pooled connections just pushes
  more concurrent load onto an already-overloaded backend rather than
  fixing the underlying slowness.

- **Symptom:** After a database failover, the application keeps sending
  writes to the old (now-demoted) primary for a period, causing errors
  or, worse, split-brain-style writes to a node that should be
  read-only.
  **Fix:** The pooler's routing configuration wasn't wired to detect
  the failover automatically (a static `[databases]` host entry in
  PgBouncer with no reload triggered by the failover manager, or
  ProxySQL without `mysql_replication_hostgroups` configured to detect
  `read_only` status changes). Wire the pooler's routing to the actual
  HA mechanism's failover signal (a Patroni/etcd-triggered PgBouncer
  reload, or ProxySQL's automatic replication-hostgroup detection)
  rather than a static configuration that requires manual updating.

- **Symptom:** Someone reconfigures a production pooler's pool size or
  routing rules directly via the admin interface during an incident,
  without saving to disk, "just to test something quickly."
  **Fix:** This is a risky, easy-to-forget action — the change works
  until the next restart, then silently reverts, which can reintroduce
  the original problem at an unpredictable time and confuse whoever is
  debugging it later.
  > **Warning — avoid untracked production config drift.** Treat pooler
  > configuration (pool sizes, routing rules, hostgroup membership) as
  > infrastructure-as-code reviewed the same way as database
  > configuration itself — see
  > [postgresql-configuration-validation](../postgresql-configuration-validation/SKILL.md)
  > and
  > [mysql-mariadb-configuration-validation](../mysql-mariadb-configuration-validation/SKILL.md)
  > — rather than ad hoc admin-console changes made directly against
  > production without a corresponding tracked, reviewed change.

## Worked example

**Scenario:** A checkout service on MySQL/MariaDB with a primary and
two read replicas currently has every application instance connecting
directly to the primary for all reads and writes, and is hitting
`max_connections` during traffic spikes. The team introduces ProxySQL
for pooling and read/write splitting.

1. Deploy ProxySQL as a small redundant fleet (2 instances behind an
   internal load balancer, not a single instance) and register backends:
   ```sql
   INSERT INTO mysql_servers (hostgroup_id, hostname, port) VALUES (10, '<PRIMARY_HOST>', 3306);
   INSERT INTO mysql_servers (hostgroup_id, hostname, port) VALUES (20, '<REPLICA1_HOST>', 3306);
   INSERT INTO mysql_servers (hostgroup_id, hostname, port) VALUES (20, '<REPLICA2_HOST>', 3306);
   INSERT INTO mysql_replication_hostgroups (writer_hostgroup, reader_hostgroup, check_type)
     VALUES (10, 20, 'read_only');
   LOAD MYSQL SERVERS TO RUNTIME; SAVE MYSQL SERVERS TO DISK;
   ```
2. Add query rules routing non-locking `SELECT`s to the reader
   hostgroup, everything else (writes, `SELECT ... FOR UPDATE`) to the
   writer hostgroup, `LOAD`ed and `SAVE`d.
3. Size each hostgroup's connection pool against measured backend
   capacity: `max_connections = 60` for the writer hostgroup (well under
   the primary's `max_connections = 300`, leaving headroom for
   replication threads and monitoring), `max_connections = 40` per
   replica for the reader hostgroup.
4. Repoint application connection strings at ProxySQL's stable endpoint
   instead of the primary's hostname directly.
5. Load-test a simulated primary failover (promote a replica, confirm
   its `read_only` flips to `OFF`) and verify ProxySQL's automatic
   replication-hostgroup detection moves it into the writer hostgroup
   within the configured check interval, with zero application
   connection-string changes required.
6. Monitor `stats_mysql_connection_pool` for queueing over the following
   week's peak traffic; connection-exhaustion errors on the primary
   stop recurring, and read load is now measurably distributed across
   both replicas instead of concentrated on the primary.

## Cross-references

- [postgresql-operations-and-performance-tuning](../postgresql-operations-and-performance-tuning/SKILL.md) — PgBouncer sizing and pool-mode guidance in the context of broader PostgreSQL operational tuning.
- [mysql-mariadb-operations-and-performance-tuning](../mysql-mariadb-operations-and-performance-tuning/SKILL.md) — the MySQL/MariaDB-side connection and replication concepts (thread-per-connection model, replica lag) that ProxySQL routing decisions here depend on.
- [mysql-mariadb-high-availability-and-replication](../mysql-mariadb-high-availability-and-replication/SKILL.md) — the Galera/Group Replication failover mechanics that ProxySQL's `mysql_replication_hostgroups` automatic routing tracks.
- [postgresql-configuration-validation](../postgresql-configuration-validation/SKILL.md) — validates the `max_connections`/pooler-sizing math this skill's pool configurations depend on before rollout.
