---
name: managing-apache-druid-deep
description: |
  Use when working with Apache Druid Deep — apache Druid deep management —
  monitor cluster health, datasources, ingestion tasks, segments, query
  performance, and coordinator/overlord status. Use when debugging ingestion
  failures, inspecting segment distribution, optimizing query latency, or
  auditing cluster capacity.
connection_type: apache-druid
preload: false
---

# Managing Apache Druid (Deep)

Manage and monitor Apache Druid cluster — datasources, ingestion, segments, queries, and cluster health.

## Discovery Phase

```bash
#!/bin/bash

DRUID_API="${DRUID_ROUTER_URL:-http://localhost:8888}"

echo "=== Cluster Health ==="
curl -s "$DRUID_API/status" \
  | jq '{version: .version, memory: .memory}'

echo ""
echo "=== Datasources ==="
curl -s "$DRUID_API/druid/coordinator/v1/datasources?simple" \
  | jq -r '.[] | [.name, .properties.segments.count, .properties.segments.size] | @tsv' | column -t | head -15

echo ""
echo "=== Services ==="
curl -s "$DRUID_API/druid/coordinator/v1/servers?simple" \
  | jq -r '.[] | [.host, .type, .tier, .currSize, .maxSize] | @tsv' | column -t | head -10

echo ""
echo "=== Supervisors ==="
curl -s "$DRUID_API/druid/indexer/v1/supervisor" \
  | jq -r '.[] | [.id, .state // "unknown"] | @tsv' | column -t | head -10

echo ""
echo "=== Load Queue ==="
curl -s "$DRUID_API/druid/coordinator/v1/loadqueue?simple" \
  | jq -r 'to_entries[] | [.key, .value.segmentsToLoad, .value.segmentsToDrop] | @tsv' | column -t | head -10
```

## Analysis Phase

```bash
#!/bin/bash

DRUID_API="${DRUID_ROUTER_URL:-http://localhost:8888}"

echo "=== Running Tasks ==="
curl -s "$DRUID_API/druid/indexer/v1/tasks?state=running" \
  | jq -r '.[] | [.id[:40], .type, .dataSource, .createdTime] | @tsv' | column -t | head -10

echo ""
echo "=== Failed Tasks (Recent) ==="
curl -s "$DRUID_API/druid/indexer/v1/tasks?state=failed&max=10" \
  | jq -r '.[] | [.id[:40], .dataSource, .createdTime, .errorMsg[:50] // ""] | @tsv' | column -t

echo ""
echo "=== Segment Distribution ==="
curl -s "$DRUID_API/druid/coordinator/v1/datasources/$DRUID_DATASOURCE/intervals?simple" \
  | jq -r 'to_entries[:10][] | [.key, .value.count, .value.size] | @tsv' | column -t

echo ""
echo "=== Compaction Status ==="
curl -s "$DRUID_API/druid/coordinator/v1/compaction/status" \
  | jq -r '.latestStatus[] | [.dataSource, .byteCountAwaitingCompaction, .segmentCountAwaitingCompaction] | @tsv' | column -t | head -10

echo ""
echo "=== Query Metrics ==="
curl -s -X POST "$DRUID_API/druid/v2/sql" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT datasource, COUNT(*) AS num_segments, SUM(size) AS total_size, SUM(num_rows) AS total_rows FROM sys.segments WHERE is_published = 1 GROUP BY datasource ORDER BY total_size DESC LIMIT 10"}' \
  | jq -r '.[] | [.datasource, .num_segments, .total_size, .total_rows] | @tsv' | column -t

echo ""
echo "=== Supervisor Status ==="
for SUP_ID in $(curl -s "$DRUID_API/druid/indexer/v1/supervisor" | jq -r '.[:5][].id'); do
  curl -s "$DRUID_API/druid/indexer/v1/supervisor/$SUP_ID/status" \
    | jq -r '[.id, .payload.state, .payload.healthy] | @tsv'
done | column -t
```

## Output Format

```
CLUSTER
Version:     <version>
Services:    <count> nodes

DATASOURCES
Name             Segments   Size
<datasource>     <n>        <bytes>

SUPERVISORS
ID               State       Healthy
<supervisor>     RUNNING     true

RUNNING TASKS
ID               Type        Datasource      Created
<task-id>        <type>      <datasource>    <timestamp>

FAILED TASKS
ID               Datasource      Created         Error
<task-id>        <datasource>    <timestamp>     <message>

COMPACTION
Datasource       Bytes Awaiting   Segments Awaiting
<datasource>     <bytes>          <n>
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

