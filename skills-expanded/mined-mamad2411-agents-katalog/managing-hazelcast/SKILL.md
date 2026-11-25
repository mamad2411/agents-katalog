---
name: managing-hazelcast
description: |
  Use when working with Hazelcast — hazelcast cluster management, distributed
  data structure inspection, partition health monitoring, and near-cache
  analysis. Covers member discovery, map/cache statistics, WAN replication
  status, CP subsystem health, and executor service diagnostics. Read this skill
  before any Hazelcast operations.
connection_type: hazelcast
preload: false
---

# Hazelcast Management Skill

Monitor, analyze, and optimize Hazelcast clusters safely.

## MANDATORY: Discovery-First Pattern

**Always check cluster state and member list before inspecting data structures. Never assume map names or partition counts.**

### Phase 1: Discovery

```bash
#!/bin/bash

HZ_URL="${HAZELCAST_URL:-http://localhost:5701}"

echo "=== Cluster State ==="
curl -s "$HZ_URL/hazelcast/rest/cluster" 2>/dev/null || echo "REST API may be disabled"

echo ""
echo "=== Management Center API ==="
MC_URL="${HAZELCAST_MC_URL:-http://localhost:8080}"
curl -s "$MC_URL/rest/clusters" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for cluster in data if isinstance(data, list) else [data]:
    print(f\"Cluster: {cluster.get('name','?')} | Members: {cluster.get('memberCount','?')} | State: {cluster.get('state','?')}\")
" 2>/dev/null || echo "Management Center not available"

echo ""
echo "=== Health Check ==="
curl -s "$HZ_URL/hazelcast/health" 2>/dev/null

echo ""
echo "=== Members via REST ==="
curl -s "$HZ_URL/hazelcast/rest/management/cluster/state" 2>/dev/null

echo ""
echo "=== Using hz-cli if available ==="
if command -v hz-cli &>/dev/null; then
    hz-cli cluster
    hz-cli list-jobs 2>/dev/null || true
else
    echo "hz-cli not found in PATH"
fi
```

**Phase 1 outputs:** Cluster state, member count and addresses, health status, Management Center availability.

### Phase 2: Analysis

```bash
#!/bin/bash

MC_URL="${HAZELCAST_MC_URL:-http://localhost:8080}"
CLUSTER="${1:-dev}"

echo "=== Map Statistics ==="
curl -s "$MC_URL/rest/maps/$CLUSTER" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for m in (data if isinstance(data, list) else []):
    print(f\"Map: {m.get('name','?')} | Entries: {m.get('ownedEntryCount',0)} | Memory: {m.get('ownedEntryMemoryCost',0)//1024}KB | Hits: {m.get('hits',0)}\")
" 2>/dev/null | head -15

echo ""
echo "=== Partition Distribution ==="
curl -s "$MC_URL/rest/clusters/$CLUSTER/partitions" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
member_counts = {}
for p in (data if isinstance(data, list) else []):
    owner = p.get('owner','?')
    member_counts[owner] = member_counts.get(owner, 0) + 1
for member, count in sorted(member_counts.items()):
    print(f\"  {member}: {count} partitions\")
" 2>/dev/null || echo "Partition info not available"

echo ""
echo "=== WAN Replication ==="
curl -s "$MC_URL/rest/wan/$CLUSTER" 2>/dev/null | head -10 || echo "WAN replication not configured"

echo ""
echo "=== CP Subsystem ==="
curl -s "$HZ_URL/hazelcast/rest/cp-subsystem/groups" 2>/dev/null || echo "CP subsystem not enabled"
```

## Output Format

```
HAZELCAST ANALYSIS
==================
Cluster: [name] | State: [active/frozen/passive]
Members: [count] | Partitions: [count]

ISSUES FOUND:
- [issue with affected member/map]

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

