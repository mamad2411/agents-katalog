---
name: analyzing-redshift
description: |
  Use when working with Redshift — amazon Redshift query performance, WLM
  configuration, table design analysis, vacuum/analyze status, and cluster
  health.
connection_type: redshift
preload: false
---

# Redshift Analysis Skill

Analyze and optimize Redshift clusters with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated schema/table names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List schemas
psql "$REDSHIFT_URI" -c "SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('information_schema', 'pg_catalog') ORDER BY schema_name;"

# 2. List tables in a schema
psql "$REDSHIFT_URI" -c "SELECT tablename, tabletype FROM pg_catalog.svv_tables WHERE table_schema = 'public' ORDER BY tablename;"

# 3. Get table schema (never assume column names)
psql "$REDSHIFT_URI" -c "\d public.my_table"

# 4. Table design (dist/sort keys)
psql "$REDSHIFT_URI" -c "SELECT tablename, diststyle, sortkey1 FROM pg_catalog.svv_table_info WHERE schema = 'public' ORDER BY tablename;"

# 5. Sample data
psql "$REDSHIFT_URI" -c "SELECT * FROM public.my_table LIMIT 5;"
```

**Phase 1 outputs:**
- Schemas and tables
- Column names and data types
- Distribution style and sort keys

### Phase 2: Analysis (only after Phase 1)

Only reference schemas, tables, and columns confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core Redshift query runner — always use this
rs_query() {
    local query="$1"
    psql "${REDSHIFT_URI}" -t -A -F$'\t' -c "$query"
}

# AWS CLI helper for Redshift
rs_aws() {
    aws redshift "$@" --output json
}
```

## Anti-Hallucination Rules

- **NEVER reference a schema or table** without confirming via `svv_tables` or `information_schema`
- **NEVER reference column names** without seeing them in table description
- **NEVER assume distribution style** — always check `svv_table_info`
- **NEVER guess sort keys** — always verify from table definition
- **NEVER assume WLM queue configuration** — always query system tables

## Safety Rules

- **READ-ONLY ONLY**: Use only SELECT, EXPLAIN, system table queries
- **FORBIDDEN**: DROP, ALTER, INSERT, UPDATE, DELETE, VACUUM, ANALYZE without explicit user request
- **ALWAYS add `LIMIT`** to queries on user tables
- **Use `EXPLAIN`** before running expensive queries
- **Query system tables** (STL_, STV_, SVV_) for metadata

## Common Operations

### Cluster Health Overview

```bash
#!/bin/bash
echo "=== Cluster Info ==="
rs_query "SELECT host, version() as version;"

echo ""
echo "=== Node Slices ==="
rs_query "SELECT node, slice, type FROM stv_slices ORDER BY node, slice;"

echo ""
echo "=== Disk Usage ==="
rs_query "SELECT owner, host, diskno, used, capacity, ROUND(used::float/capacity*100, 1) as pct_used FROM stv_partitions WHERE part_begin = 0 ORDER BY pct_used DESC;"

echo ""
echo "=== Table Sizes ==="
rs_query "SELECT schema, \"table\", size as size_mb, tbl_rows, diststyle, sortkey1 FROM svv_table_info ORDER BY size DESC LIMIT 20;"
```

### Query Performance Analysis

```bash
#!/bin/bash
echo "=== Slow Queries (last 24h) ==="
rs_query "SELECT query, TRIM(querytxt) as query_text, starttime, endtime, DATEDIFF(second, starttime, endtime) as duration_sec, aborted FROM stl_query WHERE starttime > DATEADD(hour, -24, GETDATE()) AND userid > 1 ORDER BY duration_sec DESC LIMIT 20;"

echo ""
echo "=== Queue Wait Times ==="
rs_query "SELECT query, service_class, total_queue_time/1000000.0 as queue_sec, total_exec_time/1000000.0 as exec_sec FROM stl_wlm_query WHERE starttime > DATEADD(hour, -24, GETDATE()) ORDER BY total_queue_time DESC LIMIT 15;"

echo ""
echo "=== Disk-Based Queries (spilled to disk) ==="
rs_query "SELECT query, segment, step, rows, bytes, label FROM stl_disk_full_scan WHERE starttime > DATEADD(hour, -24, GETDATE()) ORDER BY bytes DESC LIMIT 10;" 2>/dev/null
```

### WLM Configuration

```bash
#!/bin/bash
echo "=== WLM Configuration ==="
rs_query "SELECT service_class, num_query_tasks, query_working_mem, max_execution_time, user_group_wild_card, query_group_wild_card FROM stv_wlm_classification_config ORDER BY service_class;"

echo ""
echo "=== WLM Queue Status ==="
rs_query "SELECT service_class, num_queued_queries, num_executing_queries, num_executed_queries FROM stv_wlm_service_class_state ORDER BY service_class;"

echo ""
echo "=== Concurrency Scaling ==="
rs_query "SELECT service_class, query_priority, concurrency_scaling FROM svv_wlm_query_queue_state ORDER BY service_class;" 2>/dev/null
```

### Table Design Analysis

```bash
#!/bin/bash
echo "=== Tables with Skewed Distribution ==="
rs_query "SELECT schema, \"table\", diststyle, skew_rows, skew_sortkey1 FROM svv_table_info WHERE skew_rows > 2.0 ORDER BY skew_rows DESC LIMIT 15;"

echo ""
echo "=== Vacuum Status ==="
rs_query "SELECT schema, \"table\", empty, unsorted, stats_off, tbl_rows FROM svv_table_info WHERE unsorted > 5 OR stats_off > 5 ORDER BY unsorted DESC LIMIT 20;"

echo ""
echo "=== Tables Needing ANALYZE ==="
rs_query "SELECT schema, \"table\", stats_off FROM svv_table_info WHERE stats_off > 10 ORDER BY stats_off DESC LIMIT 20;"
```

## Output Format

Present results as a structured report:
```
Analyzing Redshift Report
═════════════════════════
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

- **Distribution key skew**: Poor dist key choice causes data skew — check `skew_rows` in svv_table_info
- **Sort key staleness**: Unsorted regions degrade query performance — check unsorted percentage
- **WLM queue contention**: Too many queues or wrong concurrency causes queueing — monitor queue wait times
- **COPY vs INSERT**: Use COPY for bulk loads — INSERT is single-row and very slow
- **Encoding**: Column compression encoding affects scan speed — check with `ANALYZE COMPRESSION`
- **Leader node queries**: Some functions run only on leader node — avoid in large distributed queries
- **Commit queue**: Frequent small commits block writes — batch operations where possible
