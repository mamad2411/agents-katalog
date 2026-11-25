---
name: analyzing-trino
description: |
  Use when working with Trino — trino (Presto) query analysis, catalog
  management, worker health, memory allocation, and query optimization.
connection_type: trino
preload: false
---

# Trino Analysis Skill

Analyze and optimize Trino (formerly Presto) clusters with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated catalog/schema/table names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List catalogs
trino --server "$TRINO_HOST" --execute "SHOW CATALOGS"

# 2. List schemas in a catalog
trino --server "$TRINO_HOST" --execute "SHOW SCHEMAS FROM my_catalog"

# 3. List tables in a schema
trino --server "$TRINO_HOST" --execute "SHOW TABLES FROM my_catalog.my_schema"

# 4. Describe table (never assume column names)
trino --server "$TRINO_HOST" --execute "DESCRIBE my_catalog.my_schema.my_table"

# 5. Sample data
trino --server "$TRINO_HOST" --execute "SELECT * FROM my_catalog.my_schema.my_table LIMIT 5"
```

**Phase 1 outputs:**
- Available catalogs and schemas
- Tables with column definitions
- Sample data to confirm structure

### Phase 2: Analysis (only after Phase 1)

Only reference catalogs, schemas, tables, and columns confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core Trino query runner — always use this
trino_query() {
    local query="$1"
    trino --server "${TRINO_HOST:-localhost:8080}" \
        --user "${TRINO_USER:-trino}" \
        --output-format TSV \
        --execute "$query"
}

# Trino REST API helper
trino_api() {
    local endpoint="$1"
    curl -s -H "X-Trino-User: ${TRINO_USER:-trino}" \
        "http://${TRINO_HOST:-localhost:8080}/v1/$endpoint"
}
```

## Anti-Hallucination Rules

- **NEVER reference a catalog** without confirming via `SHOW CATALOGS`
- **NEVER reference a schema** without confirming via `SHOW SCHEMAS`
- **NEVER reference table or column names** without `DESCRIBE`
- **NEVER assume worker count** — check via cluster info API
- **NEVER guess connector types** — verify catalog configuration

## Safety Rules

- **READ-ONLY ONLY**: Use only SELECT, SHOW, DESCRIBE, EXPLAIN, system table queries
- **FORBIDDEN**: DROP, ALTER, INSERT, CREATE, DELETE without explicit user request
- **ALWAYS add `LIMIT`** to exploration queries
- **Use `EXPLAIN`** before running expensive queries — especially cross-catalog joins
- **Check query cost** via `EXPLAIN (TYPE DISTRIBUTED)` for distributed plan

## Common Operations

### Cluster Health Overview

```bash
#!/bin/bash
echo "=== Cluster Info ==="
trino_api "cluster" | jq '{runningQueries, blockedQueries, queuedQueries, activeWorkers, runningDrivers, totalAvailableProcessors}'

echo ""
echo "=== Worker Nodes ==="
trino_api "node" | jq '.[] | {uri, recentRequests, recentFailures, recentSuccesses, lastResponseTime}'

echo ""
echo "=== Catalogs ==="
trino_query "SHOW CATALOGS"

echo ""
echo "=== Memory Pools ==="
trino_api "cluster/memory" | jq 'to_entries[] | {node: .key, totalBytes: .value.totalBytes, reservedBytes: .value.reservedBytes, freeBytes: (.value.totalBytes - .value.reservedBytes)}'
```

### Query Analysis

```bash
#!/bin/bash
echo "=== Running Queries ==="
trino_api "query" | jq '.[] | select(.state == "RUNNING") | {queryId, state, query: (.query | .[0:80]), elapsedTime, cpuTime, peakMemory: .queryStats.peakTotalMemoryReservation}'

echo ""
echo "=== Recent Failed Queries ==="
trino_api "query" | jq '[.[] | select(.state == "FAILED")] | sort_by(.createTime) | reverse | .[0:10] | .[] | {queryId, state, query: (.query | .[0:60]), errorType, errorCode: .errorCode.name}'

echo ""
echo "=== Query Stats ==="
trino_api "query" | jq '[.[] | select(.state == "FINISHED")] | sort_by(.createTime) | reverse | .[0:10] | .[] | {queryId, query: (.query | .[0:60]), elapsedTime, cpuTime}'
```

### Catalog & Schema Exploration

```bash
#!/bin/bash
CATALOG="${1:-hive}"

echo "=== Schemas in $CATALOG ==="
trino_query "SHOW SCHEMAS FROM $CATALOG"

echo ""
echo "=== Table Stats ==="
trino_query "SELECT table_schema, table_name, table_type FROM $CATALOG.information_schema.tables WHERE table_schema NOT IN ('information_schema') ORDER BY table_schema, table_name LIMIT 50"

echo ""
echo "=== Table Column Details ==="
trino_query "SELECT column_name, data_type, is_nullable FROM $CATALOG.information_schema.columns WHERE table_schema = 'my_schema' AND table_name = 'my_table' ORDER BY ordinal_position"
```

### Memory & Resource Analysis

```bash
#!/bin/bash
echo "=== Memory Usage by Query ==="
trino_api "query" | jq '[.[] | select(.state == "RUNNING")] | .[] | {queryId, query: (.query | .[0:60]), peakMemory: .queryStats.peakTotalMemoryReservation, currentMemory: .queryStats.currentTotalMemoryReservation}'

echo ""
echo "=== Resource Groups ==="
trino_query "SELECT * FROM system.runtime.queries WHERE state = 'RUNNING' ORDER BY created DESC LIMIT 10" 2>/dev/null

echo ""
echo "=== Worker Memory ==="
trino_api "node" | jq '.[] | {uri, heapUsed: .heapUsed, heapAvailable: .heapAvailable, nonHeapUsed: .nonHeapUsed}'
```

## Output Format

Present results as a structured report:
```
Analyzing Trino Report
══════════════════════
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

- **Cross-catalog joins**: Joining across catalogs transfers all data through Trino — very expensive
- **No pushdown**: Some connectors do not push predicates down — check with `EXPLAIN` for `ScanFilterProject`
- **Memory limits**: Queries exceeding per-node memory limits are killed — check peak memory
- **Coordinator bottleneck**: Coordinator handles all metadata — too many concurrent queries cause contention
- **Hive small files**: Many small files in Hive tables cause slow scans — check file counts
- **Dynamic filtering**: Enable dynamic filtering for join-heavy queries to reduce scan sizes
