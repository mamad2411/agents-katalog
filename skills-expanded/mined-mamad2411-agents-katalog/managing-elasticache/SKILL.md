---
name: managing-elasticache
description: |
  Use when working with Elasticache — amazon ElastiCache cluster health, node
  status, replication group management, parameter group analysis, and
  performance monitoring.
connection_type: aws
preload: false
---

# ElastiCache Management Skill

Analyze and manage ElastiCache clusters with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated cluster/node names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List Redis clusters
aws elasticache describe-cache-clusters --output json | jq '.CacheClusters[] | {CacheClusterId, Engine, EngineVersion, CacheNodeType, NumCacheNodes, CacheClusterStatus}'

# 2. List replication groups (Redis)
aws elasticache describe-replication-groups --output json | jq '.ReplicationGroups[] | {ReplicationGroupId, Status, ClusterEnabled, NodeGroups: (.NodeGroups | length)}'

# 3. List Memcached clusters (if applicable)
aws elasticache describe-cache-clusters --show-cache-node-info --output json | jq '.CacheClusters[] | select(.Engine == "memcached")'

# 4. List parameter groups
aws elasticache describe-cache-parameter-groups --output json | jq '.CacheParameterGroups[] | {CacheParameterGroupName, CacheParameterGroupFamily}'
```

**Phase 1 outputs:**
- Cache clusters with engine types and node types
- Replication groups with topology
- Parameter groups in use

### Phase 2: Analysis (only after Phase 1)

Only reference cluster IDs, replication groups, and node types confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core ElastiCache helper — always use this
ec_cmd() {
    aws elasticache "$@" --output json
}

# CloudWatch metric for ElastiCache
ec_metric() {
    local cluster_id="$1" metric="$2" stat="${3:-Average}" period="${4:-300}"
    aws cloudwatch get-metric-statistics \
        --namespace AWS/ElastiCache \
        --metric-name "$metric" \
        --dimensions Name=CacheClusterId,Value="$cluster_id" \
        --start-time "$(date -u -v-1H +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S)" \
        --end-time "$(date -u +%Y-%m-%dT%H:%M:%S)" \
        --period "$period" \
        --statistics "$stat" \
        --output json
}

# Redis CLI helper (if direct access available)
redis_cmd() {
    local endpoint="$1" port="${2:-6379}" cmd="$3"
    redis-cli -h "$endpoint" -p "$port" --tls $cmd
}
```

## Anti-Hallucination Rules

- **NEVER reference a cluster ID** without confirming via `describe-cache-clusters`
- **NEVER reference a replication group** without confirming via `describe-replication-groups`
- **NEVER assume node types** — always check cluster description
- **NEVER guess parameter group names** — always list first
- **NEVER assume engine version** — check cluster metadata

## Safety Rules

- **READ-ONLY ONLY**: Use only describe-*, list-*, CloudWatch get-metric-statistics, Redis INFO/MONITOR
- **FORBIDDEN**: modify-cache-cluster, delete-cache-cluster, create-snapshot, reboot-cache-cluster without explicit user request
- **NEVER run KEYS * on production** — use SCAN instead
- **Monitor memory usage** before any investigation queries

## Common Operations

### Cluster Health Overview

```bash
#!/bin/bash
echo "=== Cache Clusters ==="
ec_cmd describe-cache-clusters --show-cache-node-info | jq '.CacheClusters[] | {CacheClusterId, Engine, EngineVersion, CacheNodeType, NumCacheNodes, CacheClusterStatus, PreferredMaintenanceWindow}'

echo ""
echo "=== Replication Groups ==="
ec_cmd describe-replication-groups | jq '.ReplicationGroups[] | {ReplicationGroupId, Status, ClusterEnabled, AutomaticFailover, MultiAZ, NodeGroups: [.NodeGroups[] | {NodeGroupId, Status, PrimaryEndpoint: .PrimaryEndpoint.Address, Slots}]}'

echo ""
echo "=== Subnet Groups ==="
ec_cmd describe-cache-subnet-groups | jq '.CacheSubnetGroups[] | {CacheSubnetGroupName, VpcId}'
```

### Node & Replication Status

```bash
#!/bin/bash
CLUSTER_ID="${1:-my-cluster}"

echo "=== Node Details ==="
ec_cmd describe-cache-clusters --cache-cluster-id "$CLUSTER_ID" --show-cache-node-info | jq '.CacheClusters[0].CacheNodes[] | {CacheNodeId, CacheNodeStatus, Endpoint: .Endpoint.Address, ParameterGroupStatus}'

echo ""
echo "=== Replication Lag ==="
ec_metric "$CLUSTER_ID" "ReplicationLag" "Maximum" | jq -r '.Datapoints | sort_by(.Timestamp) | .[-5:][] | "\(.Timestamp)\t\(.Maximum)s"'
```

### Performance Metrics

```bash
#!/bin/bash
CLUSTER_ID="${1:-my-cluster}"

echo "=== CPU Utilization ==="
ec_metric "$CLUSTER_ID" "CPUUtilization" "Average" | jq -r '.Datapoints | sort_by(.Timestamp) | .[-5:][] | "\(.Timestamp)\t\(.Average)%"'

echo ""
echo "=== Memory Usage ==="
ec_metric "$CLUSTER_ID" "DatabaseMemoryUsagePercentage" "Average" | jq -r '.Datapoints | sort_by(.Timestamp) | .[-5:][] | "\(.Timestamp)\t\(.Average)%"'

echo ""
echo "=== Cache Hits/Misses ==="
ec_metric "$CLUSTER_ID" "CacheHitRate" "Average" | jq -r '.Datapoints | sort_by(.Timestamp) | .[-5:][] | "\(.Timestamp)\t\(.Average)%"'

echo ""
echo "=== Evictions ==="
ec_metric "$CLUSTER_ID" "Evictions" "Sum" | jq -r '.Datapoints | sort_by(.Timestamp) | .[-5:][] | "\(.Timestamp)\t\(.Sum)"'

echo ""
echo "=== Current Connections ==="
ec_metric "$CLUSTER_ID" "CurrConnections" "Average" | jq -r '.Datapoints | sort_by(.Timestamp) | .[-5:][] | "\(.Timestamp)\t\(.Average)"'
```

### Parameter Group Analysis

```bash
#!/bin/bash
PARAM_GROUP="${1:-default.redis7}"

echo "=== Parameter Group Settings ==="
ec_cmd describe-cache-parameters --cache-parameter-group-name "$PARAM_GROUP" | jq '.Parameters[] | select(.Source != "system") | {ParameterName, ParameterValue, DataType, IsModifiable}'

echo ""
echo "=== Key Parameters ==="
ec_cmd describe-cache-parameters --cache-parameter-group-name "$PARAM_GROUP" | jq '.Parameters[] | select(.ParameterName | test("maxmemory|timeout|tcp-keepalive|notify")) | {ParameterName, ParameterValue}'
```

## Output Format

Present results as a structured report:
```
Managing Elasticache Report
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

- **Eviction pressure**: High eviction rate means memory is full — check maxmemory-policy
- **Replication lag**: Lag spikes indicate overloaded replicas or network issues
- **KEYS command**: Never use KEYS on production — use SCAN with cursor
- **Cluster mode**: Cluster mode enabled vs disabled have different topology — verify before connecting
- **Maintenance windows**: Patching during maintenance windows causes brief unavailability
- **Snapshot overhead**: Creating snapshots on single-node clusters causes latency spikes
