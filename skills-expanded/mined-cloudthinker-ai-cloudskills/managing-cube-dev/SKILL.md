---
name: managing-cube-dev
description: |
  Use when working with Cube Dev — cube.dev semantic layer management — monitor
  deployments, data models, pre-aggregations, query performance, and API health.
  Use when inspecting cube schemas, debugging slow queries, reviewing
  pre-aggregation builds, or auditing API usage.
connection_type: cube-dev
preload: false
---

# Managing Cube.dev

Manage and monitor Cube.dev semantic layer — data models, pre-aggregations, queries, and deployments.

## Discovery Phase

```bash
#!/bin/bash

CUBE_API="${CUBE_API_URL:-http://localhost:4000}/cubejs-api/v1"
AUTH="Authorization: $CUBE_API_TOKEN"

echo "=== Cube Meta (Models) ==="
curl -s -H "$AUTH" "$CUBE_API/meta" \
  | jq -r '.cubes[] | [.name, .type, (.measures | length), (.dimensions | length)] | @tsv' | column -t | head -15

echo ""
echo "=== Cube Measures ==="
curl -s -H "$AUTH" "$CUBE_API/meta" \
  | jq -r '.cubes[:5][] | .measures[] | [.name, .type, .aggType // ""] | @tsv' | column -t | head -15

echo ""
echo "=== Cube Dimensions ==="
curl -s -H "$AUTH" "$CUBE_API/meta" \
  | jq -r '.cubes[:5][] | .dimensions[] | [.name, .type] | @tsv' | column -t | head -15

echo ""
echo "=== Pre-Aggregations ==="
curl -s -H "$AUTH" "$CUBE_API/pre-aggregations" \
  | jq -r '.preAggregations[] | [.preAggregationName, .tableName, .refreshKey, .status] | @tsv' | column -t | head -10
```

## Analysis Phase

```bash
#!/bin/bash

CUBE_API="${CUBE_API_URL:-http://localhost:4000}/cubejs-api/v1"
AUTH="Authorization: $CUBE_API_TOKEN"

echo "=== Pre-Aggregation Build Status ==="
curl -s -H "$AUTH" "$CUBE_API/pre-aggregations/jobs" \
  | jq -r '.[] | [.table, .status, .duration // 0, .addedToQueue] | @tsv' | column -t | head -10

echo ""
echo "=== Query Sample (test) ==="
curl -s -H "$AUTH" "$CUBE_API/load" \
  -G --data-urlencode "query=$(echo '{"measures":["Orders.count"],"timeDimensions":[{"dimension":"Orders.createdAt","granularity":"day","dateRange":"last 7 days"}]}' 2>/dev/null)" \
  | jq '{annotation: .annotation, dataLength: (.data | length), slowQuery: .slowQuery}'

echo ""
echo "=== SQL Compilation Check ==="
curl -s -H "$AUTH" "$CUBE_API/sql" \
  -G --data-urlencode "query=$(echo '{"measures":["Orders.count"]}')" \
  | jq '{sql: .sql.sql[0][:100], preAggregation: .sql.preAggregationType // "none"}'

echo ""
echo "=== Pre-Aggregation Partitions ==="
curl -s -H "$AUTH" "$CUBE_API/pre-aggregations/partitions" \
  | jq -r '.preAggregationPartitions[:5][] | [.preAggregationName, (.partitions | length), .refreshKey] | @tsv' | column -t

echo ""
echo "=== API Health ==="
curl -s -H "$AUTH" "${CUBE_API_URL:-http://localhost:4000}/readyz" \
  | jq '.'
```

## Output Format

```
CUBES (Models)
Name             Type    Measures   Dimensions
<cube-name>      cube    <n>        <n>

PRE-AGGREGATIONS
Name                Table           Status     Refresh Key
<preagg-name>       <table>         <status>   <key>

BUILD JOBS
Table            Status      Duration   Queued
<table>          completed   <ms>       <timestamp>

API HEALTH
Status:          ready
Slow Queries:    <bool>
```

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

