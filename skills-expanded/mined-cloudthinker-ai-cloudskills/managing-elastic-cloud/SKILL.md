---
name: managing-elastic-cloud
description: |
  Use when working with Elastic Cloud — elastic Cloud (Elasticsearch Service)
  management including deployments, cluster health, index management, ILM
  policies, snapshot repositories, Kibana spaces, and APM configuration. Covers
  cluster performance, shard allocation, disk usage, query latency, and upgrade
  readiness.
connection_type: elastic-cloud
preload: false
---

# Elastic Cloud Management Skill

Monitor and manage Elastic Cloud deployments and Elasticsearch clusters.

## MANDATORY: Discovery-First Pattern

**Always discover deployments and cluster health before querying indices or settings.**

### Phase 1: Discovery

```bash
#!/bin/bash
EC_API="https://api.elastic-cloud.com/api/v1"
EC_AUTH="Authorization: ApiKey ${ELASTIC_CLOUD_API_KEY}"
ES_URL="${ELASTICSEARCH_URL}"
ES_AUTH="-u ${ELASTICSEARCH_USER}:${ELASTICSEARCH_PASSWORD}"

echo "=== Elastic Cloud Deployments ==="
curl -s -H "$EC_AUTH" "$EC_API/deployments" | \
  jq -r '.deployments[] | "\(.name) | ID: \(.id[:12]) | Status: \(.healthy) | Region: \(.resources.elasticsearch[0].region)"'

echo ""
echo "=== Cluster Health ==="
curl -s $ES_AUTH "$ES_URL/_cluster/health" | \
  jq -r '"Status: \(.status)\nNodes: \(.number_of_nodes)\nShards: \(.active_shards) active, \(.unassigned_shards) unassigned\nPending Tasks: \(.number_of_pending_tasks)"'

echo ""
echo "=== Node Stats ==="
curl -s $ES_AUTH "$ES_URL/_cat/nodes?v&h=name,heap.percent,disk.used_percent,cpu,load_1m,node.role" | head -10

echo ""
echo "=== Indices Summary ==="
curl -s $ES_AUTH "$ES_URL/_cat/indices?v&h=index,health,status,docs.count,store.size&s=store.size:desc" | head -15

echo ""
echo "=== ILM Policies ==="
curl -s $ES_AUTH "$ES_URL/_ilm/policy" | \
  jq -r 'to_entries[:5] | .[] | "\(.key) | Phases: \(.value.policy.phases | keys | join(","))"'
```

**Phase 1 outputs:** Deployments, cluster health, nodes, indices, ILM policies

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Shard Allocation ==="
curl -s $ES_AUTH "$ES_URL/_cat/allocation?v&h=node,shards,disk.indices,disk.used,disk.avail,disk.percent"

echo ""
echo "=== Large Indices (>1GB) ==="
curl -s $ES_AUTH "$ES_URL/_cat/indices?v&h=index,docs.count,store.size&bytes=gb&s=store.size:desc" | \
  awk 'NR==1 || $3+0 > 1' | head -10

echo ""
echo "=== Snapshot Repositories ==="
curl -s $ES_AUTH "$ES_URL/_snapshot" | \
  jq -r 'to_entries[] | "\(.key) | Type: \(.value.type)"'

echo ""
echo "=== Latest Snapshots ==="
for repo in $(curl -s $ES_AUTH "$ES_URL/_snapshot" | jq -r 'keys[]'); do
  curl -s $ES_AUTH "$ES_URL/_snapshot/$repo/_all?size=3&sort=start_time&order=desc" | \
    jq -r '.snapshots[:3] | .[] | "\(.snapshot) | State: \(.state) | Indices: \(.indices | length) | Duration: \(.duration_in_millis/1000)s"' 2>/dev/null
done

echo ""
echo "=== Pending Tasks ==="
curl -s $ES_AUTH "$ES_URL/_cluster/pending_tasks" | \
  jq -r '.tasks[:5] | .[] | "Priority: \(.priority) | Source: \(.source[:60]) | Waiting: \(.time_in_queue_millis)ms"'

echo ""
echo "=== Thread Pool Rejections ==="
curl -s $ES_AUTH "$ES_URL/_cat/thread_pool?v&h=node_name,name,active,rejected,completed&s=rejected:desc" | \
  awk 'NR==1 || $4+0 > 0' | head -10
```

## Output Format

```
ELASTIC CLOUD STATUS
====================
Deployment: {name} ({region})
Cluster: {status} | Nodes: {count}
Indices: {count} | Total Size: {size}
Shards: {active} active, {unassigned} unassigned
Disk Usage: {percent}%
Snapshots: Last={time} ({state})
Thread Pool Rejections: {count}
Issues: {list_of_warnings}
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

## Common Pitfalls

- **Cloud API vs Cluster API**: Cloud API manages deployments; cluster API manages Elasticsearch
- **Shard count**: Too many shards degrades performance — aim for 20-40GB per shard
- **Disk watermarks**: Elasticsearch stops allocating at 85% disk — monitor proactively
- **ILM rollover**: Check rollover conditions match data volume — misconfigured ILM causes bloated indices
