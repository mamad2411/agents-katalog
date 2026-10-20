---
name: managing-apache-hbase
description: |
  Use when working with Apache Hbase — apache HBase cluster management, region
  server health monitoring, table analysis, and compaction management. Covers
  RegionServer load balancing, HDFS integration health, WAL status, namespace
  inspection, and coprocessor diagnostics. Read this skill before any HBase
  operations.
connection_type: hbase
preload: false
---

# Apache HBase Management Skill

Monitor, analyze, and optimize HBase clusters safely.

## MANDATORY: Discovery-First Pattern

**Always check cluster status and list tables before any scan or get operations. Never assume table names or column family configurations.**

### Phase 1: Discovery

```bash
#!/bin/bash

HBASE_HOST="${HBASE_MASTER:-localhost}"

echo "=== Cluster Status ==="
echo "status 'detailed'" | hbase shell -n 2>/dev/null | head -30

echo ""
echo "=== HBase Version ==="
echo "version" | hbase shell -n 2>/dev/null

echo ""
echo "=== Namespaces ==="
echo "list_namespace" | hbase shell -n 2>/dev/null

echo ""
echo "=== Tables ==="
echo "list" | hbase shell -n 2>/dev/null

echo ""
echo "=== Master UI API ==="
curl -s "http://$HBASE_HOST:16010/api/v1/admin/cluster-status" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Live servers: {len(data.get('liveNodes', []))}\")
print(f\"Dead servers: {len(data.get('deadNodes', []))}\")
print(f\"Regions: {data.get('regionsCount', '?')}\")
" 2>/dev/null || echo "Master REST API not available"
```

**Phase 1 outputs:** Cluster health, live/dead RegionServers, namespace list, table inventory.

### Phase 2: Analysis

```bash
#!/bin/bash

HBASE_HOST="${HBASE_MASTER:-localhost}"
TABLE="${1:-my_table}"

echo "=== Table Description ==="
echo "describe '$TABLE'" | hbase shell -n 2>/dev/null

echo ""
echo "=== Region Count per Table ==="
echo "list" | hbase shell -n 2>/dev/null | grep -v "^$\|TABLE\|row(s)" | while read tbl; do
    count=$(echo "list_regions '$tbl'" | hbase shell -n 2>/dev/null | grep -c "REGION")
    echo "  $tbl: $count regions"
done 2>/dev/null | head -15

echo ""
echo "=== Region Server Load ==="
curl -s "http://$HBASE_HOST:16010/api/v1/admin/cluster-status" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for node in data.get('liveNodes', []):
    print(f\"  {node.get('name','?')}: regions={node.get('regionsCount',0)} requests={node.get('requestsPerSecond',0)}/s\")
" 2>/dev/null || echo "REST API not available"

echo ""
echo "=== Compaction Queue ==="
echo "status 'simple'" | hbase shell -n 2>/dev/null | grep -i compaction

echo ""
echo "=== Replication Status ==="
echo "status 'replication'" | hbase shell -n 2>/dev/null | head -10 || echo "Replication not configured"
```

## Output Format

```
HBASE ANALYSIS
==============
Cluster: [status] | Live RS: [count] | Dead RS: [count]
Tables: [count] | Total Regions: [count]

ISSUES FOUND:
- [issue with affected table/region]

RECOMMENDATIONS:
- [actionable recommendation]
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

