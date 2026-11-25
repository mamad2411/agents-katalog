---
name: aws-elasticache-deep
description: |
  Use when working with Aws Elasticache Deep — aWS ElastiCache deep analysis for
  Redis and Memcached clusters, replication health, failover analysis, and
  performance metrics. Covers node-level metrics, memory utilization, cache hit
  rates, eviction tracking, connection analysis, and engine-specific
  diagnostics.
connection_type: aws
preload: false
---

# AWS ElastiCache Deep Skill

Deep analysis of AWS ElastiCache Redis and Memcached clusters with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-elasticache-deep/` → ElastiCache-specific deep analysis (replication, failover, engine metrics)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for cluster in $clusters; do
  get_cluster_metrics "$cluster" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List replication groups (Redis)
list_replication_groups() {
  aws elasticache describe-replication-groups \
    --output text \
    --query 'ReplicationGroups[].[ReplicationGroupId,Status,ClusterEnabled,AutomaticFailover,MultiAZ,NodeGroups[0].NodeGroupMembers[0].CacheNodeId]'
}

# List cache clusters
list_cache_clusters() {
  aws elasticache describe-cache-clusters --show-cache-node-info \
    --output text \
    --query 'CacheClusters[].[CacheClusterId,Engine,EngineVersion,CacheNodeType,NumCacheNodes,CacheClusterStatus,ReplicationGroupId]'
}

# Get cluster metrics
get_cluster_metrics() {
  local cluster_id=$1 days=${2:-1}
  local end_time start_time
  end_time=$(date -u +"%Y-%m-%dT%H:%M:%S")
  start_time=$(date -u -d "$days days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-${days}d +"%Y-%m-%dT%H:%M:%S")

  aws cloudwatch get-metric-statistics \
    --namespace AWS/ElastiCache --metric-name CPUUtilization \
    --dimensions Name=CacheClusterId,Value="$cluster_id" \
    --start-time "$start_time" --end-time "$end_time" \
    --period $((days * 86400)) --statistics Average Maximum \
    --output text --query "Datapoints[0].[\"$cluster_id\",\"CPU\",Average,Maximum]" &

  aws cloudwatch get-metric-statistics \
    --namespace AWS/ElastiCache --metric-name DatabaseMemoryUsagePercentage \
    --dimensions Name=CacheClusterId,Value="$cluster_id" \
    --start-time "$start_time" --end-time "$end_time" \
    --period $((days * 86400)) --statistics Average Maximum \
    --output text --query "Datapoints[0].[\"$cluster_id\",\"Memory\",Average,Maximum]" &

  aws cloudwatch get-metric-statistics \
    --namespace AWS/ElastiCache --metric-name CacheHitRate \
    --dimensions Name=CacheClusterId,Value="$cluster_id" \
    --start-time "$start_time" --end-time "$end_time" \
    --period $((days * 86400)) --statistics Average \
    --output text --query "Datapoints[0].[\"$cluster_id\",\"HitRate\",Average]" &

  aws cloudwatch get-metric-statistics \
    --namespace AWS/ElastiCache --metric-name Evictions \
    --dimensions Name=CacheClusterId,Value="$cluster_id" \
    --start-time "$start_time" --end-time "$end_time" \
    --period $((days * 86400)) --statistics Sum \
    --output text --query "Datapoints[0].[\"$cluster_id\",\"Evictions\",Sum]" &
  wait
}

# Get replication lag (Redis)
get_replication_lag() {
  local cluster_id=$1
  local end_time start_time
  end_time=$(date -u +"%Y-%m-%dT%H:%M:%S")
  start_time=$(date -u -d "1 hour ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-1H +"%Y-%m-%dT%H:%M:%S")
  aws cloudwatch get-metric-statistics \
    --namespace AWS/ElastiCache --metric-name ReplicationLag \
    --dimensions Name=CacheClusterId,Value="$cluster_id" \
    --start-time "$start_time" --end-time "$end_time" \
    --period 300 --statistics Average Maximum \
    --output text --query 'Datapoints[*].[Timestamp,Average,Maximum]' | sort -k1 | tail -5
}
```

## Common Operations

### 1. Cluster Inventory with Engine Details

```bash
#!/bin/bash
export AWS_PAGER=""
aws elasticache describe-cache-clusters --show-cache-node-info \
  --output text \
  --query 'CacheClusters[].[CacheClusterId,Engine,EngineVersion,CacheNodeType,NumCacheNodes,CacheClusterStatus,PreferredMaintenanceWindow]' | sort -k2
```

### 2. Replication Health (Redis)

```bash
#!/bin/bash
export AWS_PAGER=""
aws elasticache describe-replication-groups \
  --output text \
  --query 'ReplicationGroups[].[ReplicationGroupId,Status,ClusterEnabled,AutomaticFailover,MultiAZ,MemberClusters[]]'

# Check replication lag for all replica nodes
REPLICAS=$(aws elasticache describe-cache-clusters --output text \
  --query 'CacheClusters[?Engine==`redis`].CacheClusterId')
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "1 hour ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-1H +"%Y-%m-%dT%H:%M:%S")
for replica in $REPLICAS; do
  aws cloudwatch get-metric-statistics \
    --namespace AWS/ElastiCache --metric-name ReplicationLag \
    --dimensions Name=CacheClusterId,Value="$replica" \
    --start-time "$START" --end-time "$END" \
    --period 300 --statistics Average Maximum \
    --output text --query "Datapoints[-1].[\"$replica\",Average,Maximum]" &
done
wait
```

### 3. Memory and Eviction Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "1 day ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-1d +"%Y-%m-%dT%H:%M:%S")
CLUSTERS=$(aws elasticache describe-cache-clusters --output text --query 'CacheClusters[].CacheClusterId')
for cluster in $CLUSTERS; do
  {
    mem=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/ElastiCache --metric-name DatabaseMemoryUsagePercentage \
      --dimensions Name=CacheClusterId,Value="$cluster" \
      --start-time "$START" --end-time "$END" \
      --period 86400 --statistics Average Maximum \
      --output text --query 'Datapoints[0].[Average,Maximum]')
    evictions=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/ElastiCache --metric-name Evictions \
      --dimensions Name=CacheClusterId,Value="$cluster" \
      --start-time "$START" --end-time "$END" \
      --period 86400 --statistics Sum \
      --output text --query 'Datapoints[0].Sum')
    printf "%s\tMem:%s\tEvictions:%s\n" "$cluster" "$mem" "${evictions:-0}"
  } &
done
wait
```

### 4. Cache Hit Rate Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "7 days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-7d +"%Y-%m-%dT%H:%M:%S")
CLUSTERS=$(aws elasticache describe-cache-clusters --output text --query 'CacheClusters[].CacheClusterId')
for cluster in $CLUSTERS; do
  {
    hits=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/ElastiCache --metric-name CacheHits \
      --dimensions Name=CacheClusterId,Value="$cluster" \
      --start-time "$START" --end-time "$END" \
      --period 604800 --statistics Sum \
      --output text --query 'Datapoints[0].Sum')
    misses=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/ElastiCache --metric-name CacheMisses \
      --dimensions Name=CacheClusterId,Value="$cluster" \
      --start-time "$START" --end-time "$END" \
      --period 604800 --statistics Sum \
      --output text --query 'Datapoints[0].Sum')
    printf "%s\tHits:%s\tMisses:%s\n" "$cluster" "${hits:-0}" "${misses:-0}"
  } &
done
wait
```

### 5. Connection Count Monitoring

```bash
#!/bin/bash
export AWS_PAGER=""
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "1 day ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-1d +"%Y-%m-%dT%H:%M:%S")
CLUSTERS=$(aws elasticache describe-cache-clusters --output text --query 'CacheClusters[].CacheClusterId')
for cluster in $CLUSTERS; do
  aws cloudwatch get-metric-statistics \
    --namespace AWS/ElastiCache --metric-name CurrConnections \
    --dimensions Name=CacheClusterId,Value="$cluster" \
    --start-time "$START" --end-time "$END" \
    --period 3600 --statistics Average Maximum \
    --output text --query "Datapoints[-1].[\"$cluster\",Average,Maximum]" &
done
wait
```

## Anti-Hallucination Rules

1. **Redis vs Memcached metrics** - ReplicationLag only applies to Redis. CacheHitRate calculation differs between engines. Always check the engine type first.
2. **EngineCPUUtilization vs CPUUtilization** - For Redis, use `EngineCPUUtilization` for the Redis process CPU. `CPUUtilization` includes OS overhead. For Memcached with multiple cores, `CPUUtilization` may underreport per-core usage.
3. **DatabaseMemoryUsagePercentage** - This is Redis-only. For Memcached, use `BytesUsedForCacheItems` divided by `maxmemory`.
4. **Cluster mode enabled vs disabled** - Redis cluster mode (sharded) uses `NodeGroups` with multiple shards. Non-cluster mode has one shard with primary/replicas.
5. **Failover requires Multi-AZ** - Automatic failover only works with Multi-AZ enabled on the replication group. Check `AutomaticFailover` and `MultiAZ` fields.

## Output Format

Present results as a structured report:
```
Aws Elasticache Deep Report
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

- **Node type naming**: ElastiCache uses `cache.` prefix (e.g., `cache.r6g.large`), not the EC2 naming convention.
- **Reserved node pricing**: ElastiCache RIs are separate from EC2 RIs. Check with `describe-reserved-cache-nodes`.
- **Maintenance windows**: During maintenance, nodes may be temporarily unavailable. Check `PreferredMaintenanceWindow`.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Snapshot retention**: Automatic backups (Redis only) retain snapshots for a configurable period. Check `SnapshotRetentionLimit`.
