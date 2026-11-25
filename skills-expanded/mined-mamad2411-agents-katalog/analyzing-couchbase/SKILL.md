---
name: analyzing-couchbase
description: |
  Use when working with Couchbase — couchbase bucket analysis, index advisor,
  N1QL query performance, XDCR status, and cluster health monitoring.
connection_type: couchbase
preload: false
---

# Couchbase Analysis Skill

Analyze and optimize Couchbase clusters with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated bucket/scope/collection names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. Cluster overview
couchbase-cli server-list -c "$CB_HOST" -u "$CB_USER" -p "$CB_PASSWORD"

# 2. List buckets
couchbase-cli bucket-list -c "$CB_HOST" -u "$CB_USER" -p "$CB_PASSWORD"

# 3. List scopes and collections
cbq -e "$CB_HOST" -u "$CB_USER" -p "$CB_PASSWORD" \
    --script="SELECT * FROM system:scopes WHERE \`bucket\` = 'my_bucket';"

# 4. Sample documents (never assume field names)
cbq -e "$CB_HOST" -u "$CB_USER" -p "$CB_PASSWORD" \
    --script="SELECT META().id, * FROM \`my_bucket\`.\`_default\`.\`_default\` LIMIT 5;"

# 5. List indexes
cbq -e "$CB_HOST" -u "$CB_USER" -p "$CB_PASSWORD" \
    --script="SELECT * FROM system:indexes WHERE keyspace_id = 'my_bucket';"
```

**Phase 1 outputs:**
- Cluster node list and services
- Buckets with memory/disk usage
- Scopes, collections, and sample documents

### Phase 2: Analysis (only after Phase 1)

Only reference buckets, scopes, collections, and fields confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core N1QL runner — always use this
cb_query() {
    local query="$1"
    cbq -e "${CB_HOST:-localhost}" -u "${CB_USER:-Administrator}" -p "${CB_PASSWORD}" \
        --script="$query" --quiet
}

# REST API helper
cb_api() {
    local endpoint="$1"
    curl -s -u "${CB_USER:-Administrator}:${CB_PASSWORD}" \
        "http://${CB_HOST:-localhost}:8091$endpoint"
}
```

## Anti-Hallucination Rules

- **NEVER reference a bucket** without confirming via `bucket-list` or REST API
- **NEVER reference field names** without seeing them in sample documents
- **NEVER assume scope/collection names** — always check `system:scopes`
- **NEVER assume index names** — always query `system:indexes`
- **NEVER guess node services** — check cluster topology first

## Safety Rules

- **READ-ONLY ONLY**: Use only SELECT, EXPLAIN, system catalog queries, REST GET endpoints
- **FORBIDDEN**: INSERT, UPSERT, DELETE, DROP, CREATE INDEX, bucket-edit without explicit user request
- **ALWAYS add `LIMIT`** to N1QL queries
- **Use `EXPLAIN`** before running expensive queries
- **Use REST GET endpoints** for cluster info — never POST/PUT/DELETE

## Common Operations

### Cluster Health Overview

```bash
#!/bin/bash
echo "=== Cluster Nodes ==="
cb_api "/pools/nodes" | jq '.nodes[] | {hostname, status, services, clusterMembership, memoryTotal: .memoryTotal, memoryFree: .memoryFree}'

echo ""
echo "=== Bucket Summary ==="
cb_api "/pools/default/buckets" | jq '.[] | {name, bucketType, ramQuota: (.quota.ram/1024/1024|round), ramUsed: (.basicStats.memUsed/1024/1024|round), diskUsed: (.basicStats.diskUsed/1024/1024|round), itemCount: .basicStats.itemCount}'

echo ""
echo "=== Cluster RAM Quota ==="
cb_api "/pools/default" | jq '{memoryQuota: .memoryQuota, indexMemoryQuota: .indexMemoryQuota, ftsMemoryQuota: .ftsMemoryQuota}'
```

### N1QL Performance Analysis

```bash
#!/bin/bash
echo "=== Active Requests ==="
cb_query "SELECT * FROM system:active_requests ORDER BY elapsedTime DESC LIMIT 10;"

echo ""
echo "=== Completed Requests (slow) ==="
cb_query "SELECT statement, elapsedTime, resultCount, errorCount FROM system:completed_requests WHERE elapsedTime > '1s' ORDER BY elapsedTime DESC LIMIT 10;"

echo ""
echo "=== Index Advisor ==="
QUERY="SELECT * FROM \`my_bucket\` WHERE type = 'user' AND status = 'active'"
cb_query "ADVISE $QUERY;"
```

### Index Analysis

```bash
#!/bin/bash
BUCKET="${1:-my_bucket}"

echo "=== Indexes on $BUCKET ==="
cb_query "SELECT name, state, using, index_key, condition, is_primary FROM system:indexes WHERE keyspace_id = '$BUCKET' ORDER BY name;"

echo ""
echo "=== Index Stats ==="
cb_api "/pools/default/buckets/$BUCKET/stats" | jq '.op.samples | {index_num_docs_queued: .index_num_docs_queued[-1], index_num_requests: .index_num_requests[-1], index_resident_percent: .index_resident_percent[-1]}'
```

### XDCR Status

```bash
#!/bin/bash
echo "=== XDCR Remote Clusters ==="
cb_api "/pools/default/remoteClusters" | jq '.[] | {name, hostname, uuid, deleted}'

echo ""
echo "=== XDCR Replications ==="
cb_api "/pools/default/tasks" | jq '[.[] | select(.type == "xdcr") | {id, status, source, target, filterExpression, pauseRequested}]'
```

## Output Format

Present results as a structured report:
```
Analyzing Couchbase Report
══════════════════════════
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

- **Missing primary index**: N1QL queries fail without at least a primary index or a covering secondary index
- **USE KEYS vs scan**: Use `USE KEYS` for direct document access — much faster than scanning
- **Memory quota**: Each bucket has a fixed RAM quota — exceeding it causes evictions
- **XDCR conflict resolution**: Default is revision-based — understand implications for bidirectional replication
- **N1QL vs KV**: Use KV (SDK Get) for single-document access, N1QL for multi-document queries
- **Index replicas**: Production should have index replicas — check with `system:indexes`
