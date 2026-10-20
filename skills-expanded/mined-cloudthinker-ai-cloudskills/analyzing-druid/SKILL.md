---
name: analyzing-druid
description: |
  Use when working with Druid — apache Druid datasource analysis, ingestion task
  management, supervisor status, segment management, and query performance.
connection_type: druid
preload: false
---

# Druid Analysis Skill

Analyze and optimize Apache Druid clusters with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated datasource/column names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List datasources
curl -s "http://$DRUID_ROUTER:8888/druid/v2/datasources"

# 2. Get datasource details
curl -s "http://$DRUID_ROUTER:8888/druid/v2/datasources/my_datasource"

# 3. Get datasource schema (columns)
curl -s "http://$DRUID_ROUTER:8888/druid/v2/datasources/my_datasource?full" | jq '.dimensions, .metrics'

# 4. Cluster health
curl -s "http://$DRUID_COORDINATOR:8081/druid/coordinator/v1/cluster"

# 5. SQL-based discovery
curl -s -X POST "http://$DRUID_ROUTER:8888/druid/v2/sql" \
    -H "Content-Type: application/json" \
    -d '{"query": "SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '\''druid'\'' LIMIT 50"}'
```

**Phase 1 outputs:**
- Available datasources
- Dimensions and metrics per datasource
- Cluster topology

### Phase 2: Analysis (only after Phase 1)

Only reference datasources, dimensions, and metrics confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Druid SQL query helper — always use this
druid_sql() {
    local query="$1"
    curl -s -X POST "http://${DRUID_ROUTER:-localhost}:8888/druid/v2/sql" \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$query\"}"
}

# Druid REST API helper
druid_api() {
    local endpoint="$1"
    local service="${2:-router}"
    local port=8888
    [ "$service" = "coordinator" ] && port=8081
    [ "$service" = "overlord" ] && port=8090
    curl -s "http://${DRUID_ROUTER:-localhost}:${port}${endpoint}"
}
```

## Anti-Hallucination Rules

- **NEVER reference a datasource** without confirming via datasources API
- **NEVER reference dimension/metric names** without checking datasource schema
- **NEVER assume segment granularity** — always check datasource config
- **NEVER guess supervisor IDs** — always list via overlord API
- **NEVER assume ingestion spec format** — always check supervisor spec

## Safety Rules

- **READ-ONLY ONLY**: Use only GET endpoints, SELECT SQL queries
- **FORBIDDEN**: POST to ingestion, supervisor shutdown, datasource delete, segment disable without explicit user request
- **ALWAYS add time filters** to Druid queries — full datasource scans are expensive
- **Use SQL API** for queries — native JSON queries are complex and error-prone

## Common Operations

### Cluster Health Overview

```bash
#!/bin/bash
echo "=== Cluster Health ==="
druid_api "/status" "coordinator"

echo ""
echo "=== Datasources ==="
druid_sql "SELECT TABLE_NAME, COUNT(*) as column_count FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'druid' GROUP BY TABLE_NAME ORDER BY TABLE_NAME"

echo ""
echo "=== Servers ==="
druid_api "/druid/coordinator/v1/servers?simple" "coordinator" | jq '.[] | {host, type, tier, currSize, maxSize}'

echo ""
echo "=== Load Queue ==="
druid_api "/druid/coordinator/v1/loadqueue?simple" "coordinator" | jq 'to_entries[] | {server: .key, segmentsToLoad: .value.segmentsToLoad, segmentsToDrop: .value.segmentsToDrop}'
```

### Datasource Analysis

```bash
#!/bin/bash
DATASOURCE="${1:-my_datasource}"

echo "=== Datasource Info ==="
druid_api "/druid/v2/datasources/$DATASOURCE?full" | jq '{dimensions, metrics, segments: (.segments | {count: length, totalSize: (map(.size) | add)})}'

echo ""
echo "=== Segment Summary ==="
druid_sql "SELECT datasource, COUNT(*) as segments, SUM(size) / 1024 / 1024 as total_mb, SUM(num_rows) as total_rows, MIN(start) as min_time, MAX(\"end\") as max_time FROM sys.segments WHERE datasource = '$DATASOURCE' AND is_active = 1 GROUP BY datasource"

echo ""
echo "=== Segment Size Distribution ==="
druid_sql "SELECT DATE_TRUNC('DAY', start) as day, COUNT(*) as segments, SUM(size)/1024/1024 as mb, SUM(num_rows) as rows FROM sys.segments WHERE datasource = '$DATASOURCE' AND is_active = 1 GROUP BY 1 ORDER BY 1 DESC LIMIT 14"
```

### Ingestion & Supervisor Status

```bash
#!/bin/bash
echo "=== Active Supervisors ==="
druid_api "/druid/indexer/v1/supervisor" "overlord" | jq '.[]'

echo ""
echo "=== Supervisor Status ==="
for SUP in $(druid_api "/druid/indexer/v1/supervisor" "overlord" | jq -r '.[]'); do
    echo "--- $SUP ---"
    druid_api "/druid/indexer/v1/supervisor/$SUP/status" "overlord" | jq '{id, state: .payload.state, healthy: .payload.healthy, detailedState: .payload.detailedState}'
done

echo ""
echo "=== Running Tasks ==="
druid_api "/druid/indexer/v1/tasks?state=running" "overlord" | jq '.[] | {id, type, dataSource, createdTime, statusCode: .status}'
```

### Query Performance

```bash
#!/bin/bash
echo "=== Recent Queries ==="
druid_sql "SELECT query_id, datasource, duration, result_rows, error FROM sys.queries ORDER BY start_time DESC LIMIT 15" 2>/dev/null

echo ""
echo "=== Server Metrics ==="
druid_api "/druid/coordinator/v1/servers?full" "coordinator" | jq '.[] | {host, type, currSize, maxSize, segments: (.segments | length)}'
```

## Output Format

Present results as a structured report:
```
Analyzing Druid Report
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

- **No time filter**: Druid queries without time filters scan entire datasources — always include `__time` filter
- **High cardinality dimensions**: Dimensions with millions of unique values slow queries — check cardinality
- **Segment compaction**: Too many small segments hurt query performance — check if auto-compaction is configured
- **Ingestion lag**: Kafka supervisors can fall behind — monitor consumer lag
- **Rollup granularity**: Wrong rollup granularity either wastes storage or loses precision
- **Memory tuning**: Druid processes have separate JVM heaps — monitor for OOMs
