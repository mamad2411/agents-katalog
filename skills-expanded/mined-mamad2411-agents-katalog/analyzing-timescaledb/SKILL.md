---
name: analyzing-timescaledb
description: |
  Use when working with Timescaledb — timescaleDB hypertable analysis, chunk
  management, continuous aggregates, compression policies, and time-series
  optimization.
connection_type: timescaledb
preload: false
---

# TimescaleDB Analysis Skill

Analyze and optimize TimescaleDB hypertables with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated hypertable/column names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. Check TimescaleDB version
psql "$TIMESCALE_URI" -c "SELECT extversion FROM pg_extension WHERE extname = 'timescaledb';"

# 2. List hypertables
psql "$TIMESCALE_URI" -c "SELECT hypertable_schema, hypertable_name, num_dimensions, num_chunks, compression_enabled FROM timescaledb_information.hypertables ORDER BY hypertable_name;"

# 3. Get hypertable schema (never assume column names)
psql "$TIMESCALE_URI" -c "\d my_schema.my_hypertable"

# 4. Check dimensions (time column, partition columns)
psql "$TIMESCALE_URI" -c "SELECT * FROM timescaledb_information.dimensions WHERE hypertable_name = 'my_hypertable';"

# 5. Sample data
psql "$TIMESCALE_URI" -c "SELECT * FROM my_schema.my_hypertable ORDER BY time_column DESC LIMIT 5;"
```

**Phase 1 outputs:**
- TimescaleDB version and hypertable list
- Hypertable schemas with confirmed column names
- Dimension info (time column, partitioning)

### Phase 2: Analysis (only after Phase 1)

Only reference hypertables, columns, and chunks confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core TimescaleDB query runner — always use this
tsdb_query() {
    local query="$1"
    psql "${TIMESCALE_URI:-postgres://localhost:5432/tsdb}" -t -A -F$'\t' -c "$query"
}
```

## Anti-Hallucination Rules

- **NEVER reference a hypertable** without confirming via `timescaledb_information.hypertables`
- **NEVER reference column names** without seeing them in `\d` output
- **NEVER assume the time column name** — always check `timescaledb_information.dimensions`
- **NEVER guess chunk intervals** — always read from dimension info
- **NEVER assume compression settings** — check `timescaledb_information.compression_settings`

## Safety Rules

- **READ-ONLY ONLY**: Use only SELECT, EXPLAIN, information views, pg_catalog queries
- **FORBIDDEN**: DROP, ALTER, INSERT, UPDATE, DELETE, add_compression_policy, remove_compression_policy without explicit user request
- **ALWAYS add `LIMIT`** to queries or use time-bounded WHERE clauses
- **Use `EXPLAIN ANALYZE`** carefully — it executes the query
- **Prefer information views** over raw chunk access

## Common Operations

### Hypertable Health Overview

```bash
#!/bin/bash
echo "=== TimescaleDB Version ==="
tsdb_query "SELECT extversion FROM pg_extension WHERE extname = 'timescaledb';"

echo ""
echo "=== Hypertables ==="
tsdb_query "SELECT hypertable_schema, hypertable_name, num_chunks, compression_enabled FROM timescaledb_information.hypertables ORDER BY hypertable_name;"

echo ""
echo "=== Total Hypertable Sizes ==="
tsdb_query "SELECT hypertable_schema || '.' || hypertable_name as hypertable, pg_size_pretty(hypertable_size(format('%I.%I', hypertable_schema, hypertable_name)::regclass)) as total_size, pg_size_pretty(hypertable_data_size(format('%I.%I', hypertable_schema, hypertable_name)::regclass)) as data_size, pg_size_pretty(hypertable_index_size(format('%I.%I', hypertable_schema, hypertable_name)::regclass)) as index_size FROM timescaledb_information.hypertables ORDER BY hypertable_size(format('%I.%I', hypertable_schema, hypertable_name)::regclass) DESC;"
```

### Chunk Management Analysis

```bash
#!/bin/bash
HYPERTABLE="${1:-my_hypertable}"

echo "=== Chunk Summary ==="
tsdb_query "SELECT count(*) as total_chunks, count(*) FILTER (WHERE is_compressed) as compressed_chunks, min(range_start) as oldest_data, max(range_end) as newest_data FROM timescaledb_information.chunks WHERE hypertable_name = '$HYPERTABLE';"

echo ""
echo "=== Recent Chunks (last 10) ==="
tsdb_query "SELECT chunk_name, pg_size_pretty(chunk_size(chunk_schema, chunk_name)) as size, range_start, range_end, is_compressed FROM timescaledb_information.chunks WHERE hypertable_name = '$HYPERTABLE' ORDER BY range_end DESC LIMIT 10;"

echo ""
echo "=== Chunk Sizes Distribution ==="
tsdb_query "SELECT CASE WHEN is_compressed THEN 'compressed' ELSE 'uncompressed' END as state, count(*) as chunks, pg_size_pretty(sum(chunk_size(chunk_schema, chunk_name))) as total_size FROM timescaledb_information.chunks WHERE hypertable_name = '$HYPERTABLE' GROUP BY is_compressed;"
```

### Continuous Aggregates Analysis

```bash
#!/bin/bash
echo "=== Continuous Aggregates ==="
tsdb_query "SELECT view_schema, view_name, materialization_hypertable_schema, materialization_hypertable_name, view_definition FROM timescaledb_information.continuous_aggregates;"

echo ""
echo "=== Continuous Aggregate Policies ==="
tsdb_query "SELECT application_name, hypertable_schema, hypertable_name, schedule_interval, config FROM timescaledb_information.jobs WHERE application_name LIKE '%continuous%' ORDER BY hypertable_name;"

echo ""
echo "=== Job Stats ==="
tsdb_query "SELECT job_id, application_name, last_run_status, last_run_started_at, last_run_duration, next_start FROM timescaledb_information.job_stats ORDER BY last_run_started_at DESC LIMIT 15;"
```

### Compression Analysis

```bash
#!/bin/bash
HYPERTABLE="${1:-my_hypertable}"

echo "=== Compression Settings ==="
tsdb_query "SELECT * FROM timescaledb_information.compression_settings WHERE hypertable_name = '$HYPERTABLE';"

echo ""
echo "=== Compression Ratio ==="
tsdb_query "SELECT pg_size_pretty(before_compression_total_bytes) as before, pg_size_pretty(after_compression_total_bytes) as after, round((1 - after_compression_total_bytes::numeric / before_compression_total_bytes) * 100, 1) as compression_pct FROM hypertable_compression_stats('$HYPERTABLE');" 2>/dev/null || echo "No compression stats available"

echo ""
echo "=== Retention Policies ==="
tsdb_query "SELECT application_name, hypertable_name, schedule_interval, config FROM timescaledb_information.jobs WHERE application_name LIKE '%retention%';"
```

## Output Format

Present results as a structured report:
```
Analyzing Timescaledb Report
════════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Chunk interval sizing**: Too small = many chunks and overhead; too large = slow queries. Match to your query patterns
- **Compression timing**: Compressing too recent data blocks inserts; too old wastes storage
- **Continuous aggregate refresh lag**: Real-time aggregates have overhead; materialized-only have staleness
- **Index on time column**: Hypertables automatically index the time dimension — avoid duplicate indexes
- **Cross-chunk queries**: Queries spanning many chunks can be slow — use time-bounded WHERE clauses
- **Space partitioning**: Hash partitioning adds complexity — only use when data exceeds single-node capacity
