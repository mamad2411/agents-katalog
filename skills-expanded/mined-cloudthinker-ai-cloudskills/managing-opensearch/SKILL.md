---
name: managing-opensearch
description: |
  Use when working with Opensearch — openSearch cluster management including
  index operations, ISM policies, snapshot management, security analytics, and
  performance tuning. Covers cluster health, shard allocation, anomaly
  detection, alerting configuration, and observability pipelines. Read this
  skill before any OpenSearch operations.
connection_type: opensearch
preload: false
---

# OpenSearch Management Skill

Monitor, analyze, and optimize OpenSearch clusters safely.

## MANDATORY: Discovery-First Pattern

**Always run cluster health and list indices before any operations. Never guess index names or field mappings.**

### Phase 1: Discovery

```bash
#!/bin/bash

OS_URL="${OPENSEARCH_URL:-https://localhost:9200}"
CURL_OPTS="-s -k ${OPENSEARCH_USER:+-u $OPENSEARCH_USER:$OPENSEARCH_PASSWORD}"

echo "=== Cluster Health ==="
curl $CURL_OPTS "$OS_URL/_cluster/health?pretty"

echo ""
echo "=== Node Overview ==="
curl $CURL_OPTS "$OS_URL/_cat/nodes?v&h=name,role,version,heap.percent,ram.percent,cpu,load_1m"

echo ""
echo "=== Indices ==="
curl $CURL_OPTS "$OS_URL/_cat/indices?v&h=index,health,status,docs.count,store.size&s=store.size:desc" | head -20

echo ""
echo "=== ISM Policies ==="
curl $CURL_OPTS "$OS_URL/_plugins/_ism/policies" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for p in data.get('policies', []):
    print(f\"Policy: {p['policy']['policy_id']} | States: {len(p['policy'].get('states', []))}\")
" 2>/dev/null

echo ""
echo "=== Plugin List ==="
curl $CURL_OPTS "$OS_URL/_cat/plugins?v"
```

**Phase 1 outputs:** Cluster state, node count, index inventory, ISM policies, installed plugins.

### Phase 2: Analysis

```bash
#!/bin/bash

OS_URL="${OPENSEARCH_URL:-https://localhost:9200}"
CURL_OPTS="-s -k ${OPENSEARCH_USER:+-u $OPENSEARCH_USER:$OPENSEARCH_PASSWORD}"

echo "=== Unassigned Shards ==="
curl $CURL_OPTS "$OS_URL/_cat/shards?v" | grep UNASSIGNED | head -10

echo ""
echo "=== Thread Pool Rejections ==="
curl $CURL_OPTS "$OS_URL/_cat/thread_pool?v&h=node_name,name,active,rejected,completed" | grep -v "0$" | head -15

echo ""
echo "=== Anomaly Detectors ==="
curl $CURL_OPTS "$OS_URL/_plugins/_anomaly_detection/detectors/_search" -H 'Content-Type: application/json' \
    -d '{"query":{"match_all":{}},"size":10}' 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for hit in data.get('hits',{}).get('hits',[]):
    src = hit['_source']
    print(f\"Detector: {src.get('name','?')} | Index: {src.get('indices',['?'])} | Enabled: {src.get('enabled','?')}\")
" 2>/dev/null || echo "No anomaly detectors configured"

echo ""
echo "=== Alerting Monitors ==="
curl $CURL_OPTS "$OS_URL/_plugins/_alerting/monitors/_search" -H 'Content-Type: application/json' \
    -d '{"query":{"match_all":{}},"size":10}' 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for hit in data.get('hits',{}).get('hits',[]):
    src = hit['_source']
    print(f\"Monitor: {src.get('name','?')} | Enabled: {src.get('enabled','?')} | Type: {src.get('monitor_type','?')}\")
" 2>/dev/null || echo "No alerting monitors configured"
```

## Output Format

```
OPENSEARCH ANALYSIS
===================
Cluster: [name] | Status: [green/yellow/red]
Nodes: [count] | Indices: [count] | Unassigned Shards: [count]

ISSUES FOUND:
- [issue with affected resource]

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

