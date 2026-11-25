---
name: managing-aerospike
description: |
  Use when working with Aerospike — aerospike cluster management, namespace
  utilization, set analysis, and secondary index monitoring. Covers node health,
  storage engine statistics, migration tracking, UDF management, and XDR
  cross-datacenter replication status. Read this skill before any Aerospike
  operations.
connection_type: aerospike
preload: false
---

# Aerospike Management Skill

Monitor, analyze, and optimize Aerospike clusters safely.

## MANDATORY: Discovery-First Pattern

**Always check cluster health and list namespaces before any data operations. Never assume namespace names or set configurations.**

### Phase 1: Discovery

```bash
#!/bin/bash

AS_HOST="${AEROSPIKE_HOST:-localhost}"
AS_PORT="${AEROSPIKE_PORT:-3000}"

echo "=== Cluster Status ==="
asadm -e "info" 2>/dev/null || \
    asinfo -h "$AS_HOST" -p "$AS_PORT" -v "status" 2>/dev/null || \
    curl -s "http://$AS_HOST:8081/v1/cluster" 2>/dev/null

echo ""
echo "=== Node Info ==="
asinfo -h "$AS_HOST" -p "$AS_PORT" -v "build" 2>/dev/null
asinfo -h "$AS_HOST" -p "$AS_PORT" -v "node" 2>/dev/null
asinfo -h "$AS_HOST" -p "$AS_PORT" -v "statistics" 2>/dev/null | tr ';' '\n' | grep -E 'cluster_size|uptime|objects|sub_objects'

echo ""
echo "=== Namespaces ==="
asinfo -h "$AS_HOST" -p "$AS_PORT" -v "namespaces" 2>/dev/null

echo ""
echo "=== Namespace Details ==="
for ns in $(asinfo -h "$AS_HOST" -p "$AS_PORT" -v "namespaces" 2>/dev/null | tr ';' '\n'); do
    echo "--- Namespace: $ns ---"
    asinfo -h "$AS_HOST" -p "$AS_PORT" -v "namespace/$ns" 2>/dev/null | tr ';' '\n' | \
        grep -E 'type|objects|memory_used|device_used|repl-factor|high-water|stop-writes|evicted|expired'
done

echo ""
echo "=== Sets ==="
asinfo -h "$AS_HOST" -p "$AS_PORT" -v "sets" 2>/dev/null | tr ';' '\n' | head -20
```

**Phase 1 outputs:** Cluster size, node versions, namespaces with storage type and capacity, set inventory.

### Phase 2: Analysis

```bash
#!/bin/bash

AS_HOST="${AEROSPIKE_HOST:-localhost}"
AS_PORT="${AEROSPIKE_PORT:-3000}"

echo "=== Storage Engine Stats ==="
for ns in $(asinfo -h "$AS_HOST" -p "$AS_PORT" -v "namespaces" 2>/dev/null | tr ';' '\n'); do
    echo "--- $ns ---"
    asinfo -h "$AS_HOST" -p "$AS_PORT" -v "namespace/$ns" 2>/dev/null | tr ';' '\n' | \
        grep -E 'device_available_pct|device_free_pct|memory_free_pct|cache_read_pct|defrag|migrate'
done

echo ""
echo "=== Migration Status ==="
asinfo -h "$AS_HOST" -p "$AS_PORT" -v "statistics" 2>/dev/null | tr ';' '\n' | grep -E 'migrate'

echo ""
echo "=== Secondary Indexes ==="
asinfo -h "$AS_HOST" -p "$AS_PORT" -v "sindex" 2>/dev/null | tr ';' '\n' | head -10

echo ""
echo "=== XDR Status ==="
asinfo -h "$AS_HOST" -p "$AS_PORT" -v "statistics/xdr" 2>/dev/null | tr ';' '\n' | \
    grep -E 'xdr_ship|xdr_read|xdr_hotkey|xdr_active' | head -10 || echo "XDR not configured"

echo ""
echo "=== UDFs ==="
asinfo -h "$AS_HOST" -p "$AS_PORT" -v "udf-list" 2>/dev/null || echo "No UDFs registered"
```

## Output Format

```
AEROSPIKE ANALYSIS
==================
Cluster Size: [nodes] | Version: [build]
Namespaces: [count] | Total Objects: [count]

ISSUES FOUND:
- [issue with affected namespace/node]

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

