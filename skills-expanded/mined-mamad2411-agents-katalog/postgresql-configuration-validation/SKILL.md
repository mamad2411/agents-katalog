---
name: postgresql-configuration-validation
description: >
  Validates proposed postgresql.conf changes, replication configuration,
  and connection-limit math before they are applied to a production
  PostgreSQL instance — catching restart-required settings applied as
  reload-only, connection-count overcommit against PgBouncer pools, and
  unsafe replication parameter combinations. Use when the user asks to
  "review this postgresql.conf change," "validate max_connections before
  we apply it," "check this replication config is safe," or "will this
  Postgres config change require a restart."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# PostgreSQL Configuration Validation

## Purpose

A PostgreSQL configuration change that looks correct in isolation can
still be unsafe in context: a `max_connections` bump that overcommits
available RAM once `work_mem` is multiplied out, a `wal_level` change
applied with `pg_ctl reload` when it actually requires a full restart, or
a `synchronous_standby_names` entry pointing at a replica name that no
longer exists. This skill is the pre-production gate — it validates a
proposed configuration change against the running instance's actual
capacity and topology before it's applied, so operational tuning work
(covered in
[postgresql-operations-and-performance-tuning](../postgresql-operations-and-performance-tuning/SKILL.md))
doesn't produce an outage instead of an improvement.

## When to use

- Before applying any `postgresql.conf` change (or `ALTER SYSTEM`) to a
  production or shared staging instance, especially `max_connections`,
  `shared_buffers`, `work_mem`, `wal_level`, or anything touching
  replication.
- Before rolling out a new `pg_hba.conf` rule, to confirm it's scoped as
  narrowly as intended and doesn't shadow or conflict with an existing
  rule earlier in file-evaluation order.
- Before enabling or reconfiguring streaming/logical replication, to
  confirm `wal_level`, `max_wal_senders`, `max_replication_slots`, and
  `synchronous_standby_names` are mutually consistent.
- Before changing PgBouncer pool sizes, to confirm the new backend pool
  size (times number of pooler instances/databases) still fits under the
  database's `max_connections` with headroom for superuser/monitoring
  connections.
- As a PR/change-review gate for infrastructure-as-code that manages
  PostgreSQL configuration (e.g. a Terraform/Ansible-managed
  `postgresql.conf` template).

## Prerequisites & environment

- Read access to `pg_settings` on the target instance
  (`SELECT * FROM pg_settings WHERE name = '<param>';`) to check current
  values, `context` (whether a change needs `reload` vs. `postmaster`
  restart vs. cannot change without `initdb`), and `pending_restart`.
  Any role can read `pg_settings`; no superuser needed for read-only
  validation.
- Knowledge of the host's actual RAM/CPU (from the cloud provider
  console, `free -h`, or infra-as-code) to validate memory-related
  settings against real capacity, not just internal consistency.
- The current `pg_hba.conf` and `postgresql.conf` (or the values
  currently loaded, via `SHOW ALL` / `pg_settings`) to diff against the
  proposed change rather than validating the proposed change in a
  vacuum.
- For replication-config validation: the topology (which hosts are
  replicas/subscribers, their names as they appear in
  `synchronous_standby_names` or `pg_stat_replication.application_name`).

## Step-by-step guidance

### 1. Classify every changed parameter by its restart requirement

Query `context` for each parameter before assuming a `reload` is
sufficient:
```sql
SELECT name, setting, unit, context, pending_restart
FROM pg_settings
WHERE name IN ('max_connections', 'shared_buffers', 'wal_level',
               'max_wal_senders', 'work_mem', 'max_worker_processes');
```
- `context = 'postmaster'` (e.g. `max_connections`, `shared_buffers`,
  `wal_level`, `max_wal_senders`, `max_worker_processes`): requires a
  full server **restart** — a `SELECT pg_reload_conf()` or `pg_ctl
  reload` will silently accept the new value into `postgresql.conf` but
  the running instance keeps the old value until restarted. Flag any
  change to a `postmaster`-context parameter explicitly as
  restart-required in the review, since this is the single most common
  "change didn't take effect" surprise.
- `context = 'sighup'` (e.g. most `log_*` settings, `work_mem` is
  actually `user`-context and takes effect per-session): reload is
  sufficient.
- `pending_restart = true` on a currently-loaded row means a value was
  already changed in the config file but the running server hasn't
  picked it up — check this before assuming the file and the running
  instance agree.

### 2. Validate connection-count math end to end, not just `max_connections` in isolation

```sql
SELECT setting::int AS max_connections FROM pg_settings WHERE name = 'max_connections';
SELECT setting::int AS superuser_reserved FROM pg_settings WHERE name = 'superuser_reserved_connections';
SELECT count(*) AS current_connections FROM pg_stat_activity;
```
The number that matters for capacity planning is
`max_connections - superuser_reserved_connections`, and it must be
validated against every connection consumer that talks directly to
Postgres, not just the app's pool: PgBouncer's backend pool size(s)
(summed across every database/user pair PgBouncer maintains, since each
gets its own pool), monitoring agents, replication (`max_wal_senders`
consumes from a separate pool, not `max_connections`, but logical
replication workers do count against `max_connections`), and any
direct/admin connections. A `max_connections` value that's technically
higher than PgBouncer's configured pool size is not sufficient
validation — confirm the sum of all pools plus headroom is still under
the limit, since PgBouncer itself doesn't enforce that for you.

### 3. Validate memory settings against actual host RAM

```sql
SELECT name, setting, unit FROM pg_settings
WHERE name IN ('shared_buffers', 'work_mem', 'maintenance_work_mem', 'max_connections');
```
`work_mem` is **per sort/hash operation, per connection** — a query with
several sort/hash nodes running concurrently across many connections can
multiply far past what looks safe in isolation. Validate:
```
shared_buffers + (work_mem * max_connections * avg_concurrent_ops_per_query) < total_RAM * safety_margin
```
using a conservative `avg_concurrent_ops_per_query` (2–4 is a reasonable
starting assumption for OLTP workloads with moderate query complexity)
rather than assuming 1, since real queries commonly have multiple
sort/hash/aggregate nodes active at once. A `work_mem` bump that looks
reasonable per-connection can still cause an out-of-memory condition
under peak concurrent connections.

### 4. Validate `wal_level` and replication parameters are mutually consistent

```sql
SELECT name, setting FROM pg_settings
WHERE name IN ('wal_level', 'max_wal_senders', 'max_replication_slots', 'max_worker_processes');
```
- `wal_level` must be at least `replica` for physical streaming
  replication, and `logical` for logical replication/subscriptions —
  `logical` is a superset and works for both, but going from `replica` to
  `logical` (or vice versa) is a `postmaster`-context, restart-required
  change (step 1).
- `max_wal_senders` must be ≥ the number of replicas/subscribers plus
  headroom for `pg_basebackup` runs and WAL archiving connections that
  also consume a wal sender slot.
- `max_replication_slots` must be ≥ `max_wal_senders` if slots are used
  (physical replication slots, logical replication slots) since each
  active slot needs a sender.
- If proposing `synchronous_standby_names`, confirm the
  `application_name` values listed actually match a real, currently
  connected standby's `application_name` in `pg_stat_replication` — a
  typo here doesn't error, it just makes every commit on the primary
  block indefinitely waiting for an ACK from a standby that will never
  send one.

### 5. Validate `pg_hba.conf` rule scope and order

`pg_hba.conf` is evaluated top-to-bottom, first match wins — a broad
rule earlier in the file silently shadows a narrower rule added later
for the same connection type. Before adding a rule, check for an
existing broader match above the proposed insertion point:
```sql
SELECT * FROM pg_hba_file_rules ORDER BY line_number;
```
Flag any proposed or existing rule using `0.0.0.0/0` or `trust` auth
method for anything other than a tightly firewalled loopback/internal
health-check use case — a `trust` entry means "no password check," which
is a serious posture problem if the network boundary around it isn't
airtight.

### 6. Validate the change against a non-production instance first when the parameter is `postmaster`-context or otherwise high-blast-radius

For any restart-required parameter, or one that changes replication
topology, apply the change to a staging/replica instance with an
equivalent config first, confirm the instance restarts cleanly and
`pg_settings` shows the intended value, before scheduling the production
change in a maintenance window.

## Best practices

- Treat `context = 'postmaster'` in `pg_settings` as the source of truth
  for "does this need a restart," not memory/documentation — Postgres
  versions occasionally reclassify a parameter's context, and the
  instance you're validating against is the ground truth.
- Validate connection math holistically (app pool + PgBouncer backend
  pools + monitoring + replication workers) against
  `max_connections - superuser_reserved_connections`, never validate
  `max_connections` against a single consumer in isolation.
- Keep a small safety margin (10–20%) below the theoretical memory
  ceiling for `work_mem`-driven settings — real workloads have burstier
  concurrency than steady-state averages suggest.
- Require any `synchronous_standby_names` change to be validated against
  live `pg_stat_replication.application_name` values at apply time, not
  against a topology diagram that may be stale.
- Bake this validation into CI for infra-as-code-managed Postgres config
  (a script asserting no `postmaster`-context param changed without an
  explicit "restart-required" flag in the PR) rather than relying on a
  human reviewer to remember to check `pg_settings.context` every time.

## Common pitfalls

- **Symptom:** A `max_connections` increase is applied via `ALTER SYSTEM`
  and `pg_reload_conf()`, but `SHOW max_connections;` still shows the old
  value and new connections still get rejected at the old ceiling.
  **Fix:** `max_connections` is `postmaster`-context — it only takes
  effect on a full restart. Check `pg_settings.pending_restart = true`
  to confirm the file value is queued but not active, then schedule an
  actual restart.

- **Symptom:** After a `synchronous_standby_names` change, all writes on
  the primary hang and client connections time out.
  **Fix:** The configured `application_name` doesn't match any currently
  connected standby (typo, or the standby's `primary_conninfo` doesn't
  set a matching `application_name`), so the primary waits forever for
  an ACK that never arrives. Validate the name against
  `pg_stat_replication` before applying, and consider
  `synchronous_commit = local` as an emergency mitigation to unblock
  writes while the real standby name is fixed — but treat that as a
  temporary durability trade-off, not a permanent fix.

- **Symptom:** A `work_mem` increase that looked safe per-connection
  causes intermittent out-of-memory kills of the PostgreSQL process
  under peak load.
  **Fix:** `work_mem` is multiplied by concurrent sort/hash operations
  across all active connections, not a single global cap — re-validate
  using `max_connections * work_mem * realistic_concurrent_ops` against
  actual host RAM, and consider `hash_mem_multiplier` and per-role
  `ALTER ROLE ... SET work_mem` for a specific reporting/analytics role
  instead of a blanket global increase.

- **Symptom:** A new `pg_hba.conf` rule intended to restrict a database
  to a specific application IP range has no effect — connections from
  outside that range still succeed.
  **Fix:** An existing broader rule earlier in the file (often a legacy
  `0.0.0.0/0` entry, or a rule for `all` databases) matches first and
  wins, since `pg_hba.conf` is first-match, not most-specific-match.
  Check `pg_hba_file_rules` ordering and move the new narrower rule
  above any broader conflicting rule, then reload (`pg_hba.conf` changes
  are reload-only, no restart needed).

- **Symptom:** A reviewer approves a `wal_level` change from `replica`
  to `minimal` to "reduce WAL volume," and it's applied directly to a
  production primary that has an active streaming replica.
  **Fix:** This is a destructive, high-blast-radius change — `wal_level
  = minimal` breaks streaming and logical replication entirely, and the
  replica will fall permanently out of sync with no way to catch up
  short of a fresh base backup. Never approve a `wal_level` downgrade on
  an instance with any active replica/subscriber without first
  confirming (via `pg_stat_replication`) there are none, and prefer
  leaving `wal_level` at `replica` or `logical` even on standalone
  instances that might grow a replica later, since the WAL volume
  difference is rarely worth the risk.

## Worked example

**Scenario:** A change request proposes bumping `max_connections` from
100 to 400 on a production primary to "fix connection exhaustion errors,"
alongside doubling `work_mem` from 4MB to 8MB. The instance has 16GB RAM
and `shared_buffers` set to 4GB. PgBouncer sits in front with
`default_pool_size = 25` across 3 database/user pairs.

1. Check parameter context:
   ```sql
   SELECT name, context FROM pg_settings WHERE name IN ('max_connections', 'work_mem');
   -- max_connections | postmaster   (restart required)
   -- work_mem        | user         (reload sufficient, but per-session)
   ```
   Flag `max_connections` as restart-required — schedule a maintenance
   window, don't expect a reload to fix the reported exhaustion.
2. Validate whether 400 connections is actually needed: PgBouncer's real
   backend demand is `25 * 3 = 75` connections plus monitoring/admin
   headroom — nowhere near 400. The actual reported "connection
   exhaustion" is traced to application services bypassing PgBouncer and
   connecting directly for a reporting job. Recommendation: fix the
   bypass (route reporting through PgBouncer too) rather than
   quadrupling `max_connections`, which would have masked the real
   problem and multiplied memory risk.
3. Validate the memory math for the requested `work_mem = 8MB` against
   even a corrected, more modest `max_connections = 150`:
   `shared_buffers (4GB) + work_mem (8MB) * 150 * 3 concurrent ops ≈
   4GB + 3.6GB = 7.6GB` — comfortably under 16GB with margin for OS
   cache and other processes. Approved at 150, not 400.
4. Recommendation delivered: set `max_connections = 150` (restart
   required, schedule window), `work_mem = 8MB` (reload sufficient), and
   route the reporting job through PgBouncer instead of a direct
   connection — closing the actual root cause instead of just raising a
   ceiling.

## Cross-references

- [postgresql-operations-and-performance-tuning](../postgresql-operations-and-performance-tuning/SKILL.md) — the operational tuning work (replication, connection pooling, vacuum) whose proposed config changes this skill validates before rollout.
- [postgresql-high-availability-and-failover](../postgresql-high-availability-and-failover/SKILL.md) — validates the `synchronous_standby_names`/replication-slot configuration this skill checks in the context of a full HA topology and failover testing.
- [database-schema-migration-with-liquibase-and-flyway](../database-schema-migration-with-liquibase-and-flyway/SKILL.md) — complementary pre-production gate for schema/DDL changes, as this skill is for engine-config changes.
