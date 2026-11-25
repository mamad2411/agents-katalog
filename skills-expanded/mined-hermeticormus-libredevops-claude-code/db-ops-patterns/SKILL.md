---
name: db-ops-patterns
description: "Database operations patterns: reading EXPLAIN ANALYZE, connection pool sizing, autovacuum tuning for high-write tables, PostgreSQL replication setup and monitoring, Flyway migrations, Redis patterns, and pg_stat_statements queries. Use when tuning or operating PostgreSQL or Redis in production."
---

# DB Ops Patterns

PostgreSQL query optimization, indexing, VACUUM tuning, pgBouncer, replication, and migration patterns.

## EXPLAIN ANALYZE Reading Guide

```sql
-- Example slow query
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE o.status = 'completed'
  AND o.created_at > NOW() - INTERVAL '30 days'
GROUP BY u.id, u.name
ORDER BY order_count DESC
LIMIT 10;

/*
Limit  (cost=45231.23..45231.26 rows=10 width=40) (actual time=3421.234..3421.235 rows=10 loops=1)
  ->  Sort  (cost=45231.23..45481.23 rows=100000 width=40) (actual time=3421.233..3421.234 rows=10)
        Sort Key: (count(o.id)) DESC
        Sort Method: top-N heapsort  Memory: 26kB
        ->  HashAggregate  (cost=39231.23..41231.23 rows=100000 width=40) (actual time=3214.123..3312.456)
              ->  Hash Join  (cost=5123.45..35231.23 rows=400000 width=16) (actual time=123.456..2987.654)
                    Hash Cond: (o.user_id = u.id)
                    Buffers: shared hit=1234 read=45678    <-- 45678 reads = disk I/O
                    ->  Seq Scan on orders  (cost=0.00..28123.45 rows=400000 width=12)  <-- PROBLEM
                          Filter: ((status = 'completed') AND (created_at > ...))
                          Rows Removed by Filter: 1200000  <-- Scanning 1.6M rows, keeping 400K
                    ->  Hash  (cost=4123.45..4123.45 rows=80000 width=12)
                          ->  Seq Scan on users  (cost=0.00..4123.45 rows=80000 width=12)
Planning Time: 2.345 ms
Execution Time: 3422.456 ms     <-- 3.4 seconds!
*/

-- Fix: composite index on orders for this query pattern
CREATE INDEX CONCURRENTLY idx_orders_status_created_user
ON orders (status, created_at, user_id)
WHERE status = 'completed';  -- Partial: only index completed orders

-- Or if other statuses also queried:
CREATE INDEX CONCURRENTLY idx_orders_status_created
ON orders (status, created_at DESC)
INCLUDE (user_id);  -- Cover user_id to avoid heap fetch
```

## Connection Pool Sizing Formula

```
DB Max Connections = (num_cores * 2) + num_disk_spindles

For Fargate 2 vCPU: max_connections = 5 (safe default)
pgBouncer pool_size per app = max_connections / num_app_instances

Example:
  RDS db.r6g.xlarge (4 vCPU): max_connections ≈ 200 (RDS sets this automatically)
  3 app servers, each needing 30 connections = 90 total
  pgBouncer: default_pool_size = 30 per app server
              max_client_conn = 500 (can have many waiting clients)
```

```ini
# pgBouncer config for 3-server app -> RDS
[databases]
myapp_prod = host=myapp.cluster-ro.us-east-1.rds.amazonaws.com port=5432 dbname=myapp

[pgbouncer]
pool_mode = transaction
max_client_conn = 500
default_pool_size = 30
reserve_pool_size = 10
server_idle_timeout = 300
server_lifetime = 3600
tcp_keepalive = 1
tcp_keepidle = 10
tcp_keepintvl = 10
```

## Autovacuum Tuning for High-Write Tables

```sql
-- Tables with high write volume need more aggressive autovacuum
-- Default thresholds are designed for average tables

-- Check which tables need tuning
SELECT
  schemaname || '.' || tablename AS table_name,
  n_live_tup AS live_rows,
  n_dead_tup AS dead_rows,
  round(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
  last_autovacuum,
  last_autoanalyze
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY dead_pct DESC NULLS LAST;

-- Tune autovacuum for orders table (high write volume)
ALTER TABLE orders SET (
  autovacuum_vacuum_scale_factor = 0.01,     -- 1% dead rows triggers vacuum (not 20%)
  autovacuum_vacuum_threshold = 100,         -- minimum 100 dead rows
  autovacuum_analyze_scale_factor = 0.005,   -- 0.5% changes triggers analyze
  autovacuum_analyze_threshold = 50,
  autovacuum_vacuum_cost_delay = 2,          -- Less throttling = faster vacuum
  autovacuum_vacuum_cost_limit = 400         -- Default 200, allow more work per pass
);

-- Emergency: Run manual vacuum without locking
VACUUM (VERBOSE, ANALYZE) orders;

-- For extreme bloat, VACUUM FULL (locks table -- schedule maintenance window)
-- Better: use pg_repack (no table lock)
-- pg_repack -d mydb -t orders
```

## Replication Setup and Monitoring

```sql
-- Primary: grant replication permission
CREATE USER replicator REPLICATION LOGIN PASSWORD 'strong-password';

-- Primary postgresql.conf
-- wal_level = replica           (or logical for logical replication)
-- max_wal_senders = 10
-- wal_keep_size = 1024          (keep 1GB of WAL segments)
-- hot_standby = on
-- synchronous_standby_names = 'replica01'  (for synchronous)

-- Primary pg_hba.conf
-- host  replication  replicator  10.0.0.0/24  scram-sha-256

-- Replica: recovery.conf / postgresql.conf (PG 12+)
-- primary_conninfo = 'host=primary port=5432 user=replicator sslmode=require'
-- recovery_target_timeline = 'latest'
-- hot_standby = on

-- Monitor replication health (run on primary)
SELECT
  application_name,
  client_addr,
  state,
  write_lag,
  flush_lag,
  replay_lag,
  CASE WHEN sync_state = 'sync' THEN 'SYNCHRONOUS' ELSE 'ASYNC' END AS mode
FROM pg_stat_replication
ORDER BY replay_lag DESC NULLS LAST;

-- Monitor from replica
SELECT
  now() - pg_last_xact_replay_timestamp() AS lag_interval,
  pg_is_in_recovery() AS is_replica,
  pg_last_wal_receive_lsn() AS received_lsn,
  pg_last_wal_replay_lsn() AS replayed_lsn;
```

## Flyway Migration Pattern

```sql
-- V1__create_users_table.sql
CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,
    email       VARCHAR(255) NOT NULL UNIQUE,
    name        VARCHAR(255) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- V2__add_users_status.sql
-- Safe: add nullable column first (no table lock in PG 11+)
ALTER TABLE users ADD COLUMN status VARCHAR(20);
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;

-- V3__backfill_users_status.sql (idempotent)
UPDATE users
SET status = 'active'
WHERE status IS NULL;

-- V4__add_users_status_constraint.sql
ALTER TABLE users ALTER COLUMN status SET DEFAULT 'active';
ALTER TABLE users ALTER COLUMN status SET NOT NULL;

-- Create index concurrently cannot run inside transaction (Flyway workaround)
-- V5__add_status_index.sql with @MixedMode or runInTransaction=false
-- flyway.mixed=true in flyway.conf

-- R__current_schema_stats.sql (repeatable migration for views/functions)
CREATE OR REPLACE FUNCTION get_active_users()
RETURNS TABLE(id bigint, email text, name text) AS $$
  SELECT id, email, name FROM users WHERE status = 'active' AND deleted_at IS NULL;
$$ LANGUAGE sql;
```

```yaml
# Flyway in Docker Compose (run before app startup)
version: "3.8"
services:
  migrate:
    image: flyway/flyway:9
    command: -url=jdbc:postgresql://db:5432/myapp -user=myapp -password=${DB_PASSWORD} migrate
    volumes:
      - ./migrations:/flyway/sql
    depends_on:
      db:
        condition: service_healthy
    networks: [backend]

  app:
    image: myapp:latest
    depends_on:
      migrate:
        condition: service_completed_successfully
    networks: [backend]
```

## Redis Patterns

```python
# Redis for session storage, cache-aside, distributed locks
import redis
import json
import hashlib
from functools import wraps
from datetime import timedelta

r = redis.Redis.from_url(os.environ['REDIS_URL'], decode_responses=True)

# Cache-aside pattern with TTL
def cache(ttl_seconds=300, key_prefix=""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Build deterministic cache key
            key = f"{key_prefix}:{func.__name__}:{hashlib.md5(str(args + tuple(sorted(kwargs.items()))).encode()).hexdigest()}"
            cached = r.get(key)
            if cached:
                return json.loads(cached)
            result = func(*args, **kwargs)
            r.setex(key, timedelta(seconds=ttl_seconds), json.dumps(result))
            return result
        return wrapper
    return decorator

@cache(ttl_seconds=60, key_prefix="user")
def get_user_profile(user_id: int) -> dict:
    return db.query("SELECT * FROM users WHERE id = %s", (user_id,))

# Distributed lock with automatic expiry
def with_lock(lock_name: str, timeout_seconds: int = 30):
    lock = r.lock(lock_name, timeout=timeout_seconds)
    if lock.acquire(blocking=False):
        try:
            yield lock
        finally:
            lock.release()
    else:
        raise Exception(f"Could not acquire lock: {lock_name}")
```

## pg_stat_statements Analysis Queries

```sql
-- Top 10 queries by total execution time
SELECT
  LEFT(query, 80) AS query_preview,
  calls,
  round(total_exec_time::numeric, 2) AS total_ms,
  round(mean_exec_time::numeric, 2) AS avg_ms,
  round(stddev_exec_time::numeric, 2) AS stddev_ms,
  round(rows::numeric / calls, 2) AS avg_rows,
  round(shared_blks_hit::numeric / NULLIF(shared_blks_hit + shared_blks_read, 0) * 100, 2) AS cache_hit_pct
FROM pg_stat_statements
WHERE calls > 10
ORDER BY total_exec_time DESC
LIMIT 10;

-- Queries with low cache hit rate (I/O bound queries)
SELECT
  LEFT(query, 80) AS query_preview,
  calls,
  round(mean_exec_time::numeric, 2) AS avg_ms,
  shared_blks_read AS disk_reads,
  round(shared_blks_hit::numeric / NULLIF(shared_blks_hit + shared_blks_read, 0) * 100, 2) AS cache_hit_pct
FROM pg_stat_statements
WHERE shared_blks_read > 1000 AND calls > 5
ORDER BY shared_blks_read DESC
LIMIT 10;

-- Reset statistics after optimizations
SELECT pg_stat_statements_reset();
```
