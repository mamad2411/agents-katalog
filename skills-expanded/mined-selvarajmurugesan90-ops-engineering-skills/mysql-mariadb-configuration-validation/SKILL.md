---
name: mysql-mariadb-configuration-validation
description: >
  Validates proposed my.cnf changes, replication topology, and connection
  limits before they are applied to a production MySQL/MariaDB instance —
  catching dynamic-vs-static variables applied with the wrong scope,
  GTID-mode mismatches across a replication topology, and connection/
  thread-pool overcommit against ProxySQL pools. Use when the user asks
  to "review this my.cnf change," "validate max_connections before we
  apply it," "check this MySQL replication config is safe," or "will
  this MySQL config change require a restart."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# MySQL/MariaDB Configuration Validation

## Purpose

A MySQL or MariaDB configuration change that looks correct in isolation
can still be unsafe in context: a `SET GLOBAL` change that only affects
new sessions and silently leaves existing connections on the old value,
a `max_connections` bump that overcommits RAM once
`innodb_buffer_pool_size` plus per-connection buffers are accounted for,
or a GTID-mode change applied to one node in a replication topology
without the matching change on its peers, which breaks replication
entirely. This skill is the pre-production gate — it validates a
proposed configuration change against the running instance's actual
capacity and topology before it's applied, so operational tuning work
(covered in
[mysql-mariadb-operations-and-performance-tuning](../mysql-mariadb-operations-and-performance-tuning/SKILL.md))
doesn't produce an outage instead of an improvement.

## When to use

- Before applying any `my.cnf` change (or `SET GLOBAL` / `SET PERSIST`)
  to a production or shared staging instance, especially
  `max_connections`, `innodb_buffer_pool_size`, `gtid_mode`, or anything
  touching replication.
- Before rolling out a new user grant or a change to `skip_name_resolve`/
  `bind_address`, to confirm it doesn't lock out an existing
  application or monitoring connection path.
- Before enabling or reconfiguring replication (async, semi-sync, or
  GTID), to confirm `server_id`, `log_bin`, `gtid_mode`, and
  `enforce_gtid_consistency` are mutually consistent across every node
  in the topology.
- Before changing ProxySQL (or another MySQL-aware pooler) connection
  pool sizes, to confirm the new backend pool size still fits under the
  database's `max_connections` with headroom for replication and
  monitoring connections.
- As a PR/change-review gate for infrastructure-as-code that manages
  MySQL/MariaDB configuration.

## Prerequisites & environment

- Read access to check current values and scope
  (`SHOW VARIABLES LIKE '<param>'`, and whether a variable is dynamic —
  `SHOW GLOBAL VARIABLES` vs. requiring a restart). No elevated
  privilege is needed for read-only validation beyond ordinary
  `SELECT`/`PROCESS` access.
- Knowledge of the host's actual RAM/CPU to validate memory-related
  settings against real capacity, not just internal consistency.
- The current `my.cnf` (or the values currently loaded via `SHOW
  VARIABLES`) to diff against the proposed change rather than
  validating the proposed change in a vacuum.
- For replication-config validation: the topology (which hosts are
  replicas, their `server_id` values, and whether GTID mode is uniform
  across all of them) — mismatched `gtid_mode` between source and
  replica is a common, entirely preventable outage.
- MySQL 8.0+ or MariaDB 10.5+ assumed for `SET PERSIST` /
  `SET GLOBAL ... PERSIST` availability; on older versions a dynamic
  `SET GLOBAL` change does not survive a restart unless also written to
  `my.cnf` by hand — validate which mechanism a proposed change actually
  uses.

## Step-by-step guidance

### 1. Classify every changed parameter by whether it is dynamic and whether it persists

```sql
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SELECT * FROM performance_schema.variables_info
WHERE VARIABLE_NAME IN ('innodb_buffer_pool_size', 'max_connections', 'gtid_mode');
```
`performance_schema.variables_info.VARIABLE_SOURCE` shows whether a
value came from a compiled default, `my.cnf`, a command-line option, or
a persisted `SET PERSIST` — this distinguishes "changed in the config
file but not yet loaded" from "changed live but will revert on restart."
Some variables are dynamic but only partially so:
`innodb_buffer_pool_size` can be resized online (MySQL 5.7.5+/MariaDB
10.5+ support `SET GLOBAL innodb_buffer_pool_size = ...`), but the resize
happens in chunks (`innodb_buffer_pool_chunk_size`) and can take
significant time and I/O for a large pool — treat a large buffer pool
resize as an operationally significant event even though it's
technically dynamic, not a free, instant change.

### 2. Validate connection-count math end to end

```sql
SHOW VARIABLES LIKE 'max_connections';
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';
```
Validate the proposed `max_connections` against every real consumer, not
just the application's pool: ProxySQL's backend connection pool(s)
(summed across every hostgroup/user pair, since each maintains its own),
replication I/O/SQL threads (each replica connection consumes a
`max_connections` slot on the source), monitoring agents, and any direct
administrative connections. Also check `max_user_connections` per
account if set — a per-user cap lower than the intended pool size will
reject connections well before the global `max_connections` ceiling is
reached, which is a common source of confusing, inconsistent connection
errors.

### 3. Validate memory settings against actual host RAM

```sql
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SHOW VARIABLES LIKE '%_buffer_size';   -- sort_buffer_size, join_buffer_size, read_buffer_size, etc.
```
Per-connection buffers (`sort_buffer_size`, `join_buffer_size`,
`read_buffer_size`, `read_rnd_buffer_size`) are allocated **per session,
potentially per operation**, not once globally — validate:
```
innodb_buffer_pool_size + (sum_of_per_connection_buffers * max_connections) < total_RAM * safety_margin
```
using the actual `max_connections` ceiling, not typical concurrent
connection count, since a traffic spike that approaches the configured
ceiling is exactly the scenario this validation needs to survive.
Increasing `sort_buffer_size` fleet-wide to fix one reporting query's
sort performance is a common mistake — prefer a session-scoped `SET
SESSION sort_buffer_size = ...` for that specific workload instead of a
global change that multiplies against every connection.

### 4. Validate replication parameters are mutually consistent across the topology

```sql
SHOW VARIABLES LIKE 'server_id';
SHOW VARIABLES LIKE 'gtid_mode';
SHOW VARIABLES LIKE 'enforce_gtid_consistency';
SHOW VARIABLES LIKE 'log_bin';
```
- Every node in a replication topology must have a **unique**
  `server_id` — a duplicate `server_id` causes replicas to reject or
  silently corrupt replication state, and is a common copy-paste error
  when provisioning a new replica from a template.
- `gtid_mode` must match across source and every replica before GTID
  replication is enabled — a mismatched mode (e.g. source at `ON`,
  replica still at `OFF`) breaks `CHANGE REPLICATION SOURCE TO
  SOURCE_AUTO_POSITION = 1` outright. MySQL's transition supports
  intermediate states (`OFF_PERMISSIVE`, `ON_PERMISSIVE`) specifically
  to allow a rolling migration — validate every node passes through the
  same sequence in the same order, not a subset jumping straight to
  `ON`.
- `log_bin` must be enabled on any node that will act as a source
  (including a replica that might itself have sub-replicas, or that
  needs `log_slave_updates`/`log_replica_updates` for a chained
  topology) — this is a restart-required setting.

### 5. Validate user grants and network-binding changes don't lock out required access

```sql
SHOW GRANTS FOR 'app_user'@'%';
SELECT user, host FROM mysql.user WHERE user = 'app_user';
```
Before tightening a grant's host scope (e.g. from `'app_user'@'%'` to
`'app_user'@'10.0.1.0/255.255.255.0'`), confirm every real connecting
source IP (application hosts, ProxySQL instances, monitoring agents,
CI/migration runners) actually falls inside the proposed scope — check
current connections via `SHOW PROCESSLIST` or
`performance_schema.threads` for real `HOST` values rather than
inferring them from an architecture diagram that may be stale.

### 6. Validate high-blast-radius changes against a non-production instance first

For any restart-required parameter, or one that changes replication
topology or GTID mode, apply the change to a staging/replica instance
with an equivalent configuration first, confirm it comes up cleanly and
`SHOW VARIABLES` reflects the intended value, before scheduling the
production change in a maintenance window.

## Best practices

- Treat `performance_schema.variables_info.VARIABLE_SOURCE` as the
  source of truth for "will this survive a restart," not assumptions —
  a `SET GLOBAL` without a matching `SET PERSIST` or `my.cnf` edit
  reverts silently on the next restart.
- Validate connection math holistically (application pool + ProxySQL
  backend pools + replication threads + monitoring) against
  `max_connections`, and check `max_user_connections` per account
  separately — a lower per-user cap causes errors well before the
  global ceiling is reached.
- Require every node in a replication topology to be validated for a
  unique `server_id` before it's brought online, ideally enforced by
  infra-as-code templating rather than manual entry.
- Roll out a `gtid_mode` transition through MySQL's documented
  intermediate states (`OFF` → `OFF_PERMISSIVE` → `ON_PERMISSIVE` →
  `ON`) across every node in lockstep, never skip a node or a stage.
- Bake this validation into CI for infra-as-code-managed MySQL/MariaDB
  config (asserting no restart-required parameter changed without an
  explicit flag in the PR) rather than relying on a reviewer to check by
  hand every time.

## Common pitfalls

- **Symptom:** `innodb_buffer_pool_size` was changed via `SET GLOBAL`
  and appears updated in `SHOW VARIABLES`, but after the next restart it
  reverts to the old value.
  **Fix:** `SET GLOBAL` alone does not persist across restarts unless
  paired with `SET PERSIST` (8.0+/MariaDB 10.5+) or a corresponding
  `my.cnf` edit. Check `performance_schema.variables_info.VARIABLE_SOURCE`
  to confirm the change's actual persistence mechanism before treating
  it as durable.

- **Symptom:** A newly provisioned replica fails to start replication
  with an error referencing `server_id`, or worse, replicates but
  produces subtly corrupted state.
  **Fix:** The new replica was cloned from a template/snapshot that
  retained the source's `server_id` instead of getting a unique one.
  Validate every node's `server_id` is unique across the entire topology
  as a pre-flight check before starting replication, not after.

- **Symptom:** After enabling GTID mode on the source, replicas that
  were still on `gtid_mode = OFF` stop replicating entirely with a
  fatal error.
  **Fix:** GTID mode was changed on the source without walking every
  replica through the same permissive-mode transition first. Roll back
  to `OFF_PERMISSIVE`/`ON_PERMISSIVE` on all nodes, bring every replica
  through the same sequence in lockstep, and only set `ON` everywhere
  once all nodes confirm the intermediate state, per MySQL's documented
  GTID migration procedure.

- **Symptom:** Connections from a specific application host are
  intermittently rejected with an access-denied error, even though
  `max_connections` is nowhere near its limit and the grant looks
  correct.
  **Fix:** `max_user_connections` for that specific account is set
  lower than the actual concurrent connection count from that host (a
  per-account cap, separate from the global ceiling). Check `SHOW GRANTS`
  and `mysql.user.max_user_connections` for the specific account, not
  just the global variable.

- **Symptom:** A change request proposes tightening `bind_address` and
  revoking `'app_user'@'%'` in favor of a narrower host mask, and it's
  applied directly to production without checking real connecting
  sources first.
  **Fix:** This risks a self-inflicted outage if any real connection
  source (a ProxySQL instance behind a NAT gateway, a CI runner, a
  monitoring agent) falls outside the assumed IP range.
  > **Warning — potentially destructive to availability.** Before
  > tightening network/grant scope on a production account, enumerate
  > actual current connection sources via `performance_schema.threads`
  > or `SHOW PROCESSLIST` over a representative time window (not just an
  > architecture diagram), and apply the narrower grant alongside the
  > old one temporarily, removing the old one only after confirming zero
  > connections still use it.

## Worked example

**Scenario:** A change request proposes bumping `max_connections` from
200 to 800 on a production MySQL 8.0 primary to "fix connection
exhaustion errors," alongside doubling `innodb_buffer_pool_size` from
8GB to 16GB on a host with 32GB RAM, and enabling `gtid_mode` on a
topology that currently has two replicas still running on file/position
replication.

1. Check persistence mechanism and scope for both changes:
   ```sql
   SELECT VARIABLE_NAME, VARIABLE_SOURCE FROM performance_schema.variables_info
   WHERE VARIABLE_NAME IN ('max_connections', 'innodb_buffer_pool_size');
   ```
   `innodb_buffer_pool_size` is dynamically resizable in this version but
   the resize will proceed in `innodb_buffer_pool_chunk_size` increments
   over several minutes under load — schedule it for a lower-traffic
   window even though no restart is required.
2. Validate whether 800 connections is actually needed: ProxySQL's real
   backend demand is calculated at 120 connections across its hostgroups,
   plus 2 replication threads and a handful of monitoring connections —
   nowhere near 800. The real reported exhaustion traces to a batch job
   connecting directly, bypassing ProxySQL. Recommendation: fix the
   bypass and set `max_connections = 300` (headroom, not 4x overcommit).
3. Validate the buffer pool math: `16GB (buffer pool) + (sort_buffer_size
   2MB + join_buffer_size 2MB) * 300 connections ≈ 16GB + 1.2GB = 17.2GB`
   — comfortably under 32GB with margin for OS cache. Approved.
4. For the GTID change: confirm both replicas' current `gtid_mode`
   (`OFF`) and require the full permissive-mode rollout sequence across
   primary and both replicas in lockstep, validated first against a
   staging topology with the same replica count, before scheduling the
   production rollout in a maintenance window.
5. Final recommendation: `max_connections = 300`, buffer pool resize to
   16GB scheduled off-peak, GTID rollout staged through
   `OFF_PERMISSIVE`/`ON_PERMISSIVE` across all three nodes with
   validation at each step — not the originally requested single-shot
   800/GTID-ON change.

## Cross-references

- [mysql-mariadb-operations-and-performance-tuning](../mysql-mariadb-operations-and-performance-tuning/SKILL.md) — the operational tuning work (replication mode, buffer pool sizing, indexing) whose proposed config changes this skill validates before rollout.
- [mysql-mariadb-high-availability-and-replication](../mysql-mariadb-high-availability-and-replication/SKILL.md) — validates the GTID/`server_id` configuration this skill checks in the context of a full Galera/Group Replication HA topology.
- [postgresql-configuration-validation](../postgresql-configuration-validation/SKILL.md) — the equivalent pre-production config-review discipline for PostgreSQL, useful as a comparison when both engines coexist in the same platform.
