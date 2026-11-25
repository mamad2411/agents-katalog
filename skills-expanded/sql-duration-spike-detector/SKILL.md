---
name: sql-duration-spike-detector
version: 1.0.0
description: >
  Detects SQL queries with sudden duration spikes BEFORE they hit the slow query threshold.
  Compares recent (24h) vs baseline (7d) average execution time using performance_schema
  digest statistics. Finds "invisible performance killers" — queries that silently degrade
  without triggering any alert.
allowed-tools: db_query, db_get_status, db_get_variable
---

# SQL Duration Spike Detector (Pre-Threshold Early Warning)

## Overview

Most monitoring systems only catch queries that exceed a fixed threshold (e.g., `long_query_time = 1s`). But the real danger often comes from queries that **haven't crossed the threshold yet** — a query that normally takes 5ms suddenly jumping to 50ms. At 10,000 QPS, that's a 10x load increase that **no alert catches**.

This skill detects these "invisible killers" by analyzing SQL performance **trends** rather than absolute thresholds:

- Compare each query's recent average (24h) against its baseline (7d)
- Flag queries with duration increase > 5x as "spikes"
- Analyze root cause: data growth, index degradation, or lock contention
- Recommend fixes before the query becomes a full-blown incident

**Real-world result**: This capability is a **"from 0 to 1" improvement** — previously impossible for humans to detect manually across hundreds of queries.

Key capabilities:
- Detect duration spikes at the SQL digest level (parameterized queries)
- Calculate **spike ratio** (recent avg / baseline avg)
- Classify root cause: data growth, index saturation, lock contention, plan change
- Prioritize by impact (spike ratio × execution frequency)
- Output actionable recommendations

## When to Use

Apply this skill when:
- User asks "any SQL performance degradation recently?"
- Proactive weekly performance review
- After data migration or bulk load
- Application latency increases but no slow queries appear
- Capacity planning — identify queries approaching breaking point
- Post-index-change verification

## Required MCP Server

| Tool | Purpose | Example |
|------|---------|---------|
| `db_query` | Query performance_schema digest tables | `db_query("SELECT ... FROM events_statements_summary_by_digest")` |
| `db_get_status` | Get performance counters | `db_get_status("Innodb_row_lock_waits")` |
| `db_get_variable` | Check version and config | `db_get_variable("version")` |

### Requirements

- **MySQL 5.7+** with `performance_schema` enabled
- `performance_schema.events_statements_summary_by_digest` populated
- Consumers: `SET GLOBAL performance_schema_digests_size = 10000` (default 200 may be too low)

### Required MySQL Privileges

- `SELECT` on `performance_schema.*`

## Diagnostic Workflow

### Step 1: Collect Baseline and Recent Performance

```sql
-- Get all SQL digests with their performance stats
-- This single query compares current cumulative stats
SELECT
  DIGEST AS digest_hash,
  LEFT(DIGEST_TEXT, 200) AS sql_template,
  COUNT_STAR AS total_executions,
  ROUND(SUM_TIMER_WAIT / 1000000000000, 3) AS total_time_sec,
  ROUND(AVG_TIMER_WAIT / 1000000000, 3) AS avg_time_ms,
  ROUND(MAX_TIMER_WAIT / 1000000000, 3) AS max_time_ms,
  ROUND(SUM_ROWS_EXAMINED / NULLIF(COUNT_STAR, 0), 0) AS avg_rows_examined,
  ROUND(SUM_ROWS_SENT / NULLIF(COUNT_STAR, 0), 0) AS avg_rows_sent,
  SUM_NO_INDEX_USED AS no_index_count,
  SUM_SORT_ROWS AS total_sort_rows,
  SUM_CREATED_TMP_TABLES AS tmp_table_count,
  FIRST_SEEN,
  LAST_SEEN
FROM performance_schema.events_statements_summary_by_digest
WHERE DIGEST_TEXT IS NOT NULL
  AND COUNT_STAR > 10  -- minimum sample size
  AND AVG_TIMER_WAIT > 1000000  -- at least 1ms average
ORDER BY AVG_TIMER_WAIT DESC
LIMIT 100;
```

### Step 2: Compare with Historical Baseline

If historical data is available (stored from previous checks), compare:

```sql
-- If you have a baseline table from previous check:
-- Compare current avg_time vs baseline avg_time for each digest

-- Otherwise, use the FIRST_SEEN and LAST_SEEN timestamps
-- to estimate if a query has been running long enough for trend analysis

-- For MySQL 8.0+, you can use the built-in history:
SELECT * FROM performance_schema.events_statements_history_long
WHERE DIGEST = '{digest_hash}'
ORDER BY TIMER_START DESC
LIMIT 50;
```

**If no historical data is available**, this skill operates in **single-snapshot mode**:
- Flag queries with suspiciously high `avg_time_ms` relative to `rows_sent`
- Calculate efficiency: `avg_rows_examined / avg_rows_sent`
- Identify queries with `no_index_count > 0`

### Step 2b: MariaDB / MySQL 5.6 Fallback (No performance_schema)

If `performance_schema` is OFF or not available (e.g., MariaDB 10.1), use the slow query log for trend analysis:

```sql
-- Check if performance_schema is available
SHOW VARIABLES LIKE 'performance_schema';

-- Fallback: Compare slow query patterns across time windows
-- Get slow queries from last 24 hours
SELECT
  LEFT(sql_text, 200) AS sql_template,
  COUNT(*) AS exec_count,
  ROUND(AVG(TIME_TO_SEC(query_time)), 3) AS avg_time_sec,
  ROUND(MAX(TIME_TO_SEC(query_time)), 3) AS max_time_sec,
  ROUND(AVG(rows_examined), 0) AS avg_rows_examined,
  ROUND(AVG(rows_sent), 0) AS avg_rows_sent,
  MIN(start_time) AS first_seen,
  MAX(start_time) AS last_seen
FROM mysql.slow_log
WHERE start_time > DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY LEFT(sql_text, 200)
HAVING COUNT(*) > 5
ORDER BY avg_time_sec DESC
LIMIT 50;

-- Compare with previous 7 days baseline
SELECT
  LEFT(sql_text, 200) AS sql_template,
  COUNT(*) AS baseline_count,
  ROUND(AVG(TIME_TO_SEC(query_time)), 3) AS baseline_avg_sec
FROM mysql.slow_log
WHERE start_time BETWEEN DATE_SUB(NOW(), INTERVAL 7 DAY) AND DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY LEFT(sql_text, 200)
HAVING COUNT(*) > 5
ORDER BY baseline_avg_sec DESC
LIMIT 50;
```

Cross-reference the two results: any SQL appearing in both with `avg_time_sec` significantly higher in the recent window indicates a spike.

### Step 3: Identify Spikes

For each query, calculate:

| Metric | Calculation | Alert Threshold |
|--------|------------|-----------------|
| **Spike Ratio** | `recent_avg_ms / baseline_avg_ms` | > 5x = spike |
| **Efficiency Degradation** | `recent_examined/sent / baseline_examined/sent` | > 3x = degraded |
| **Frequency Change** | `recent_count / baseline_count` | > 2x = suspicious |
| **Sort Overhead** | `total_sort_rows / COUNT_STAR` | High = missing index |

### Step 4: Root Cause Classification

For each spiked query, determine the likely cause:

```
IF avg_rows_examined increased proportionally to spike:
  → Cause: DATA_GROWTH
  → Fix: Partition, archive, or add index for growing table
  → Check: SELECT TABLE_ROWS FROM information_schema.TABLES

ELSE IF no_index_count > 0 OR avg_rows_examined >> avg_rows_sent:
  → Cause: INDEX_MISS
  → Fix: Add appropriate index
  → Check: SHOW INDEX FROM {table}

ELSE IF total_sort_rows is high OR tmp_table_count is high:
  → Cause: SORT_TMP_TABLE
  → Fix: Add ORDER BY columns to index (covering index)

ELSE IF lock-related wait detected:
  → Cause: LOCK_CONTENTION
  → Fix: Check concurrent transactions, optimize isolation level
  → Check: SHOW STATUS LIKE 'Innodb_row_lock%'
```

### Step 5: Prioritize by Impact

```
impact_score = spike_ratio × execution_frequency × avg_time_ms
```

Sort by impact_score descending. Focus on:
1. High spike ratio (> 10x) + high frequency (> 100/min)
2. Medium spike (5-10x) + high frequency
3. High spike + low frequency (less urgent)

## Output Templates

### Spike Detection Report

```
⚡ SQL Duration Spike Detection Report
══════════════════════════════════════
📋 Instance: {host}:{port}
   Baseline Period: {start} ~ {end} ({days} days)
   Analysis Time: {timestamp}
   SQL Digests Analyzed: {total}
   Spikes Detected: {count}

🔴 HIGH IMPACT SPIKES (action required)
───────────────────────────────────────

  1. Spike: ↑14.7x (3.2ms → 47ms)
  ┌─────────────────────────────────────────────────┐
  │ SQL: SELECT ... FROM order_detail WHERE status=? │
  │                                                 │
  │ Baseline: 3.2ms avg, 1.2M rows examined         │
  │ Recent:   47ms avg, 3.8M rows examined (↑3.2x)  │
  │ Executions: ~2,400/day                          │
  │ Impact: ~112 extra seconds/day of DB load       │
  │                                                 │
  │ Root Cause: DATA_GROWTH 📈                      │
  │   order_detail grew from 1.2M → 3.8M rows      │
  │   Current index (status) no longer selective     │
  │                                                 │
  │ ✅ Fix: Extend to covering index                 │
  │   ALTER TABLE order_detail ADD INDEX             │
  │     idx_status_created (status, created_at);     │
  │   Expected: 47ms → <5ms                         │
  └─────────────────────────────────────────────────┘

  2. Spike: ↑12.8x (1.8ms → 23ms)
     SQL: UPDATE user_session SET last_active=? WHERE user_id=?
     Root Cause: LOCK_CONTENTION 🔒
     → Connection pool leak causing lock wait
     → Fix: Check app pool config (287/300 connections used)

🟡 MODERATE SPIKES (monitor)
  3. Spike: ↑3.5x (12ms → 42ms)
     SQL: SELECT COUNT(*) FROM large_table WHERE ...
     Root Cause: DATA_GROWTH — table approaching 10M rows

📊 Summary
  | # | SQL Pattern | Baseline | Current | Spike | Cause | Priority |
  |---|------------|----------|---------|-------|-------|----------|
  | 1 | order_detail SELECT | 3.2ms | 47ms | ↑14.7x | Data Growth | Critical |
  | 2 | user_session UPDATE | 1.8ms | 23ms | ↑12.8x | Lock Contention | High |
  | 3 | large_table COUNT | 12ms | 42ms | ↑3.5x | Data Growth | Monitor |

💡 Key Insight:
  These queries haven't triggered slow_query_log (threshold: 1s),
  but they're consuming 10x more resources than a week ago.
  Without this check, they'd go unnoticed until causing an outage.
```

### Single-Snapshot Mode (No Baseline)

```
⚡ SQL Efficiency Report (Single Snapshot)
══════════════════════════════════════════
📋 Instance: {host}:{port}
   Note: No historical baseline available — showing absolute efficiency analysis

🔴 Low Efficiency Queries (rows_examined >> rows_sent)
  | SQL | Examined | Returned | Efficiency | Suggested Fix |
  |-----|----------|----------|------------|---------------|
  | SELECT ... FROM orders WHERE status=? | 2.4M | 380 | 0.016% | Add index |
  | SELECT ... FROM users WHERE email LIKE ? | 890K | 12 | 0.001% | Full-text search |

📊 Statistics
  Total Digests: {count}
  Full Table Scans: {count}
  Using Temporary Tables: {count}
  Using Filesort: {count}

💡 Recommendation:
  Top 2 queries account for 85% of unnecessary row scans.
  Adding suggested indexes could reduce total DB load by ~40%.
```

## Example Usage

**User**: "Any SQL performance degradation on db-prod-01?"

**AI**:
```
⚡ SQL Spike Detection — db-prod-01:3306

Found 2 queries with significant duration spikes:

🔴 1. SELECT ... FROM order_detail WHERE status=?
   3.2ms → 47ms (↑14.7x) over the last 7 days
   Cause: Table grew from 1.2M → 3.8M rows, index selectivity dropped
   Fix: ALTER TABLE order_detail ADD INDEX (status, created_at)
   Expected: 47ms → <5ms

🔴 2. UPDATE user_session SET last_active=? WHERE user_id=?
   1.8ms → 23ms (↑12.8x)
   Cause: Lock contention from connection pool leak (287/300)
   Fix: Check application connection pool configuration

Neither query triggers slow_query_log (threshold: 1s),
but combined they're adding ~200s/day of extra DB load.
```

## Best Practices

### Establish Baseline

For best results, run this check **weekly** and store results:

```sql
-- Create baseline storage table
CREATE TABLE IF NOT EXISTS dbops.sql_baseline (
  check_date DATE,
  digest_hash VARCHAR(64),
  sql_template TEXT,
  avg_time_ms DECIMAL(10,3),
  avg_rows_examined BIGINT,
  avg_rows_sent BIGINT,
  exec_count BIGINT,
  PRIMARY KEY (check_date, digest_hash)
);

-- Store current snapshot (run weekly)
INSERT INTO dbops.sql_baseline
SELECT CURDATE(), DIGEST, LEFT(DIGEST_TEXT, 200),
  ROUND(AVG_TIMER_WAIT / 1000000000, 3),
  ROUND(SUM_ROWS_EXAMINED / COUNT_STAR, 0),
  ROUND(SUM_ROWS_SENT / COUNT_STAR, 0),
  COUNT_STAR
FROM performance_schema.events_statements_summary_by_digest
WHERE DIGEST_TEXT IS NOT NULL;

-- Compare current vs last week
SELECT cur.sql_template, cur.avg_time_ms, prev.avg_time_ms,
  ROUND(cur.avg_time_ms / prev.avg_time_ms, 1) AS spike_ratio
FROM dbops.sql_baseline cur
JOIN dbops.sql_baseline prev ON cur.digest_hash = prev.digest_hash
WHERE cur.check_date = CURDATE() AND prev.check_date = DATE_SUB(CURDATE(), INTERVAL 7 DAY)
  AND cur.avg_time_ms / prev.avg_time_ms > 5;
```

### Spike Investigation Checklist

1. ✅ Check table row count growth (`information_schema.TABLES.TABLE_ROWS`)
2. ✅ Check if index statistics are stale (`ANALYZE TABLE {table}`)
3. ✅ Check for recent schema changes
4. ✅ Check for query plan changes (`EXPLAIN`)
5. ✅ Check lock contention (`Innodb_row_lock_waits`)

### Performance Schema Sizing

```sql
-- Ensure enough digest capacity
SHOW VARIABLES LIKE 'performance_schema_digests_size';
-- Recommended: 10000+ for production

-- Check if digests are being lost
SHOW STATUS LIKE 'Performance_schema_digest_lost';
-- If > 0, increase performance_schema_digests_size
```

## Quick Reference

| Action | Query |
|--------|-------|
| All SQL digest stats | `SELECT ... FROM performance_schema.events_statements_summary_by_digest` |
| Queries using full scan | `WHERE SUM_NO_INDEX_USED > 0` |
| Queries with temp tables | `WHERE SUM_CREATED_TMP_TABLES > 0` |
| Reset digest stats | `TRUNCATE performance_schema.events_statements_summary_by_digest` |
| Check digest capacity | `SHOW VARIABLES LIKE 'performance_schema_digests_size'` |
| Check lost digests | `SHOW STATUS LIKE 'Performance_schema_digest_lost'` |

**Use this skill to find "invisible" performance killers — queries that are silently slowing down before they trigger any alert.**
