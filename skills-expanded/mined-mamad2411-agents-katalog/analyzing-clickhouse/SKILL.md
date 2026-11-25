---
name: analyzing-clickhouse
description: |
  Use when working with Clickhouse — clickHouse table analysis, MergeTree
  optimization, query performance tuning, parts management, and cluster health.
connection_type: clickhouse
preload: false
---

# ClickHouse Analysis Skill

Analyze and optimize ClickHouse databases with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated database/table names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List databases
clickhouse-client --query "SHOW DATABASES"

# 2. List tables in a database
clickhouse-client --query "SHOW TABLES FROM my_database"

# 3. Get table schema (never assume column names)
clickhouse-client --query "DESCRIBE TABLE my_database.my_table"

# 4. Table engine and settings
clickhouse-client --query "SELECT engine, engine_full, partition_key, sorting_key, primary_key FROM system.tables WHERE database = 'my_database' AND name = 'my_table'"

# 5. Sample data
clickhouse-client --query "SELECT * FROM my_database.my_table LIMIT 5"
```

**Phase 1 outputs:**
- List of databases and tables
- Table schemas with column names and types
- Engine types and partition/sort keys

### Phase 2: Analysis (only after Phase 1)

Only reference databases, tables, and columns confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core ClickHouse query runner — always use this
ch_query() {
    local query="$1"
    local format="${2:-TabSeparatedWithNames}"
    clickhouse-client --host "${CH_HOST:-localhost}" --port "${CH_PORT:-9000}" \
        --user "${CH_USER:-default}" --password "${CH_PASSWORD:-}" \
        --query "$query" --format "$format"
}

# HTTP API alternative
ch_http() {
    local query="$1"
    curl -s "http://${CH_HOST:-localhost}:8123/?query=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$query'))")&default_format=JSONCompact"
}
```

## Anti-Hallucination Rules

- **NEVER reference a database or table** without confirming via `SHOW DATABASES` / `SHOW TABLES`
- **NEVER reference column names** without seeing them in `DESCRIBE TABLE`
- **NEVER assume table engine** — always check `system.tables`
- **NEVER guess partition keys or sort keys** — always read from table definition
- **NEVER assume cluster name** — check `system.clusters`

## Safety Rules

- **READ-ONLY ONLY**: Use only SELECT, SHOW, DESCRIBE, EXPLAIN, system table queries
- **FORBIDDEN**: DROP, ALTER, INSERT, OPTIMIZE, TRUNCATE without explicit user request
- **ALWAYS add `LIMIT`** to queries on large tables — ClickHouse tables can have billions of rows
- **Use `EXPLAIN`** before running expensive queries
- **Prefer `system.*` tables** for metadata over scanning user data

## Common Operations

### Cluster Health Overview

```bash
#!/bin/bash
echo "=== ClickHouse Version ==="
ch_query "SELECT version()"

echo ""
echo "=== Cluster Nodes ==="
ch_query "SELECT cluster, host_name, port, is_local FROM system.clusters ORDER BY cluster, host_name" 2>/dev/null || echo "Standalone instance"

echo ""
echo "=== Databases & Table Counts ==="
ch_query "SELECT database, count() as tables, sum(total_rows) as total_rows, formatReadableSize(sum(total_bytes)) as total_size FROM system.tables WHERE database NOT IN ('system', 'INFORMATION_SCHEMA', 'information_schema') GROUP BY database ORDER BY sum(total_bytes) DESC"

echo ""
echo "=== Uptime & Memory ==="
ch_query "SELECT uptime() as uptime_seconds, formatReadableSize(totalMemory()) as total_memory"
```

### Table & Parts Analysis

```bash
#!/bin/bash
DB="${1:-default}"
TABLE="${2:-my_table}"

echo "=== Table Info ==="
ch_query "SELECT database, name, engine, partition_key, sorting_key, total_rows, formatReadableSize(total_bytes) as size FROM system.tables WHERE database = '$DB' AND name = '$TABLE'"

echo ""
echo "=== Parts Summary ==="
ch_query "SELECT partition, count() as parts, sum(rows) as rows, formatReadableSize(sum(bytes_on_disk)) as size, min(modification_time) as oldest, max(modification_time) as newest FROM system.parts WHERE database = '$DB' AND table = '$TABLE' AND active GROUP BY partition ORDER BY partition"

echo ""
echo "=== Part Merges in Progress ==="
ch_query "SELECT database, table, elapsed, progress, num_parts, result_part_name FROM system.merges WHERE database = '$DB' AND table = '$TABLE'"
```

### Query Performance Analysis

```bash
#!/bin/bash
echo "=== Slow Queries (last 1h) ==="
ch_query "SELECT query_start_time, query_duration_ms, read_rows, formatReadableSize(read_bytes) as read_size, formatReadableSize(memory_usage) as memory, substring(query, 1, 100) as query_preview FROM system.query_log WHERE type = 'QueryFinish' AND query_duration_ms > 1000 AND event_time > now() - INTERVAL 1 HOUR ORDER BY query_duration_ms DESC LIMIT 20"

echo ""
echo "=== Failed Queries ==="
ch_query "SELECT query_start_time, exception_code, substring(exception, 1, 100) as error, substring(query, 1, 80) as query_preview FROM system.query_log WHERE type = 'ExceptionWhileProcessing' AND event_time > now() - INTERVAL 1 HOUR ORDER BY query_start_time DESC LIMIT 10"

echo ""
echo "=== Current Queries ==="
ch_query "SELECT query_id, elapsed, read_rows, formatReadableSize(memory_usage) as memory, substring(query, 1, 100) as query_preview FROM system.processes ORDER BY elapsed DESC"
```

### MergeTree Optimization Check

```bash
#!/bin/bash
DB="${1:-default}"

echo "=== Tables with Too Many Parts ==="
ch_query "SELECT database, table, count() as parts, sum(rows) as total_rows, formatReadableSize(sum(bytes_on_disk)) as total_size FROM system.parts WHERE active AND database = '$DB' GROUP BY database, table HAVING parts > 100 ORDER BY parts DESC"

echo ""
echo "=== Tables with Wide Partitions ==="
ch_query "SELECT database, table, partition, count() as parts FROM system.parts WHERE active AND database = '$DB' GROUP BY database, table, partition HAVING parts > 50 ORDER BY parts DESC LIMIT 20"

echo ""
echo "=== Mutations in Progress ==="
ch_query "SELECT database, table, mutation_id, command, create_time, parts_to_do FROM system.mutations WHERE is_done = 0"
```

## Output Format

Present results as a structured report:
```
Analyzing Clickhouse Report
═══════════════════════════
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

- **Too many parts**: Excessive parts cause merge pressure and slow inserts — keep parts under a few hundred per table
- **Wrong partition key**: Over-partitioning creates too many parts; under-partitioning creates huge parts
- **FINAL keyword**: `SELECT ... FINAL` deduplicates on read and is slow — avoid on large tables
- **Memory limits**: ClickHouse can OOM on large GROUP BY — check `max_memory_usage` setting
- **Nullable columns**: Nullable columns use extra storage and slower processing — avoid when possible
- **String vs LowCardinality**: Use `LowCardinality(String)` for columns with < 10K distinct values
- **Distributed tables**: Queries on Distributed tables fan out to all shards — filter early
