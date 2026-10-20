---
name: analyzing-singlestore
description: |
  Use when working with Singlestore — singleStore (MemSQL) workspace management,
  pipeline status, query tuning, memory analysis, and cluster health.
connection_type: singlestore
preload: false
---

# SingleStore Analysis Skill

Analyze and optimize SingleStore clusters with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated database/table names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. Cluster info
singlestore -h "$SS_HOST" -P "$SS_PORT" -u "$SS_USER" -p"$SS_PASSWORD" -e "SHOW CLUSTER STATUS;"

# 2. List databases
singlestore -h "$SS_HOST" -P "$SS_PORT" -u "$SS_USER" -p"$SS_PASSWORD" -e "SHOW DATABASES;"

# 3. List tables
singlestore -h "$SS_HOST" -P "$SS_PORT" -u "$SS_USER" -p"$SS_PASSWORD" -e "SHOW TABLES FROM my_database;"

# 4. Describe table (never assume column names)
singlestore -h "$SS_HOST" -P "$SS_PORT" -u "$SS_USER" -p"$SS_PASSWORD" -e "DESCRIBE my_database.my_table;"

# 5. Table types (rowstore vs columnstore)
singlestore -h "$SS_HOST" -P "$SS_PORT" -u "$SS_USER" -p"$SS_PASSWORD" -e "SELECT TABLE_NAME, TABLE_TYPE, ENGINE FROM information_schema.tables WHERE TABLE_SCHEMA = 'my_database';"
```

**Phase 1 outputs:**
- Cluster topology and node roles
- Databases and tables
- Table schemas with storage engine types

### Phase 2: Analysis (only after Phase 1)

Only reference databases, tables, and columns confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core SingleStore query runner — always use this
ss_query() {
    local query="$1"
    mysql -h "${SS_HOST:-localhost}" -P "${SS_PORT:-3306}" \
        -u "${SS_USER:-root}" -p"${SS_PASSWORD}" \
        -N -B -e "$query"
}
```

## Anti-Hallucination Rules

- **NEVER reference a database or table** without confirming via SHOW commands
- **NEVER reference column names** without running DESCRIBE
- **NEVER assume rowstore vs columnstore** — always check table engine
- **NEVER guess pipeline names** — always list via `SHOW PIPELINES`
- **NEVER assume shard key** — always check table definition

## Safety Rules

- **READ-ONLY ONLY**: Use only SELECT, SHOW, EXPLAIN, PROFILE, information_schema queries
- **FORBIDDEN**: DROP, ALTER, INSERT, UPDATE, DELETE, START/STOP PIPELINE without explicit user request
- **ALWAYS add `LIMIT`** to user table queries
- **Use `EXPLAIN`** before running expensive queries

## Common Operations

### Cluster Health Overview

```bash
#!/bin/bash
echo "=== Cluster Status ==="
ss_query "SHOW CLUSTER STATUS;"

echo ""
echo "=== Aggregators ==="
ss_query "SHOW AGGREGATORS;"

echo ""
echo "=== Leaves ==="
ss_query "SHOW LEAVES;"

echo ""
echo "=== Memory Usage ==="
ss_query "SELECT @@maximum_memory, @@maximum_table_memory;"
ss_query "SELECT DATABASE_NAME, SUM(MEMORY_USE)/1024/1024 as memory_mb FROM information_schema.TABLE_STATISTICS GROUP BY DATABASE_NAME ORDER BY memory_mb DESC;"
```

### Pipeline Status

```bash
#!/bin/bash
DB="${1:-my_database}"

echo "=== Pipelines ==="
ss_query "USE $DB; SHOW PIPELINES;"

echo ""
echo "=== Pipeline Status ==="
ss_query "USE $DB; SELECT * FROM information_schema.PIPELINES_CURSORS;" 2>/dev/null

echo ""
echo "=== Pipeline Errors ==="
ss_query "USE $DB; SELECT PIPELINE_NAME, BATCH_ID, PARTITION, BATCH_STATE FROM information_schema.PIPELINES_BATCHES_SUMMARY WHERE BATCH_STATE = 'Error' LIMIT 10;" 2>/dev/null
```

### Query Performance

```bash
#!/bin/bash
echo "=== Resource Pool Status ==="
ss_query "SHOW RESOURCE POOLS;"

echo ""
echo "=== Plancache ==="
ss_query "SELECT DATABASE_NAME, SUBSTR(QUERY_TEXT, 1, 80) as query, EXECUTION_COUNT, AVG_RUNTIME, AVG_ROWS_RETURNED FROM information_schema.MV_PLANCACHE ORDER BY AVG_RUNTIME DESC LIMIT 15;"

echo ""
echo "=== Running Queries ==="
ss_query "SHOW PROCESSLIST;" | head -20
```

### Memory & Storage Analysis

```bash
#!/bin/bash
echo "=== Database Sizes ==="
ss_query "SELECT TABLE_SCHEMA, SUM(DATA_LENGTH + INDEX_LENGTH)/1024/1024 as size_mb, COUNT(*) as tables FROM information_schema.tables GROUP BY TABLE_SCHEMA ORDER BY size_mb DESC;"

echo ""
echo "=== Columnstore Segments ==="
ss_query "SELECT DATABASE_NAME, TABLE_NAME, SUM(ROWS_COUNT) as total_rows, COUNT(*) as segments FROM information_schema.COLUMNAR_SEGMENTS GROUP BY DATABASE_NAME, TABLE_NAME ORDER BY total_rows DESC LIMIT 15;" 2>/dev/null

echo ""
echo "=== Memory by Table ==="
ss_query "SELECT DATABASE_NAME, TABLE_NAME, MEMORY_USE/1024/1024 as memory_mb, ROWS as row_count FROM information_schema.TABLE_STATISTICS ORDER BY MEMORY_USE DESC LIMIT 15;"
```

## Output Format

Present results as a structured report:
```
Analyzing Singlestore Report
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

- **Rowstore vs Columnstore**: Rowstore is for OLTP, columnstore for analytics — wrong choice hurts performance
- **Shard key selection**: Poor shard keys cause data skew and cross-partition queries
- **Memory limits**: SingleStore is in-memory first — monitor memory usage closely
- **Pipeline errors**: Kafka pipelines can stall silently — check pipeline batch errors
- **Hash vs Reference tables**: Reference tables are replicated to all nodes — only for small lookup tables
- **Columnstore sorting**: Columnstore tables benefit from sorted inserts — check segment metadata
