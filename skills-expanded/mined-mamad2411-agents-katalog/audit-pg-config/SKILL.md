---
name: audit-pg-config
description: Audit Postgres server config — shared_buffers, work_mem, max_connections vs pgbouncer pool, autovacuum tuning, WAL retention.
---

# audit-pg-config

> Sanity-check a Postgres config against the workload. Output: parameter-by-parameter findings + concrete change suggestions.

## Procedure

1. **Memory.**
   - `shared_buffers` — 25% of RAM is a common starting point; over 40% and you start fighting the OS page cache.
   - `work_mem` — per-operation, *per-connection*. `work_mem × max_connections × parallel_workers` can OOM a host. Lean on the smaller side; raise per-session for ETL.
   - `maintenance_work_mem` — for autovacuum + CREATE INDEX. 1-2GB on hosts with > 32GB RAM is reasonable.
2. **Connections.**
   - `max_connections` — high values (> 200) waste memory; pair with `pgbouncer` in `transaction` mode and let the bouncer hold the pool.
   - Hard floor: enough headroom for `pg_stat_statements`, monitoring agents, and admin sessions.
3. **WAL + checkpoints.**
   - `wal_compression = on` — cheap CPU for less WAL bytes (helps replicas).
   - `max_wal_size` / `min_wal_size` — too small triggers checkpoints too often (latency spikes).
   - `checkpoint_completion_target = 0.9` — spreads checkpoint IO over time.
4. **Autovacuum.**
   - `autovacuum_vacuum_scale_factor` — default 0.2 means vacuum kicks in at 20% dead tuples; large tables benefit from a much lower per-table setting (e.g. 0.05).
   - `autovacuum_max_workers` — raise above the default 3 for many-tabled clusters.
   - `autovacuum_analyze_scale_factor` — analyze runs less than vacuum; on hot tables, tune down.
5. **Statistics.**
   - `default_statistics_target` — 100 is the default; 500-1000 for skew-y joins where the planner makes bad row-estimates.
   - `track_io_timing = on` — needed for `pg_stat_statements` to show meaningful IO numbers.
6. **Replication.**
   - `hot_standby_feedback = on` if long-running replica reads exist (prevents replication conflicts).
   - `wal_keep_size` (PG 13+) replaces `wal_keep_segments`; ensure replicas can catch up without falling off.
7. **Logging.**
   - `log_min_duration_statement = '500ms'` (or workload-specific). Cheaper than waiting for a customer ticket.
   - `log_lock_waits = on` — diagnose lock-storm incidents.

## Output

```text
audit-pg-config

Host:    db.refund-prod
Version: 16.3
RAM:     64GB

Memory
  ✓ shared_buffers = 16GB (25% of RAM).
  ✗ work_mem = 256MB; with max_connections=300 worst-case 75GB. Lower to 64MB
    (per-session bump for ETL).

Connections
  ✗ max_connections = 300 without a pgbouncer. Add pgbouncer in transaction mode;
    drop max_connections to ~120.

Autovacuum
  ✓ autovacuum on.
  ⚠ refunds table dead-tuple ratio 38% (per pg_stat_user_tables). Per-table
    autovacuum_vacuum_scale_factor = 0.05; consider HOT-only tuning.

WAL
  ✓ max_wal_size = 4GB.

Logging
  ✗ log_min_duration_statement = -1 (off). Recommend 500ms.

Recommendation: 4 changes; mem + connections are the highest leverage.
```

## Anti-patterns to avoid

- Raising `max_connections` without `pgbouncer`. Linear memory cost per backend.
- Turning autovacuum off "for now". You will not turn it back on; bloat will eat you.
- Setting `fsync = off` on production. Data loss on crash.
- Cargo-culted `shared_buffers = 4GB` on a 256GB host. Match the workload, not the wiki.
