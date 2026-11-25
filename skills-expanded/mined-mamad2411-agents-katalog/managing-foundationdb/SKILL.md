---
name: managing-foundationdb
description: |
  Use when working with Foundationdb — foundationDB cluster management, layer
  inspection, transaction rate monitoring, and storage engine analysis. Covers
  cluster health via fdbcli status, process roles, coordination state,
  backup/restore status, and data distribution metrics. Read this skill before
  any FoundationDB operations.
connection_type: foundationdb
preload: false
---

# FoundationDB Management Skill

Monitor, analyze, and optimize FoundationDB clusters safely.

## MANDATORY: Discovery-First Pattern

**Always run fdbcli status before any operations. Never assume cluster configuration or layer availability.**

### Phase 1: Discovery

```bash
#!/bin/bash

FDB_CLUSTER="${FDB_CLUSTER_FILE:-/etc/foundationdb/fdb.cluster}"

echo "=== Cluster Status ==="
fdbcli --exec "status details" -C "$FDB_CLUSTER" 2>/dev/null

echo ""
echo "=== Cluster Configuration ==="
fdbcli --exec "configure get" -C "$FDB_CLUSTER" 2>/dev/null || \
    fdbcli --exec "status json" -C "$FDB_CLUSTER" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
cluster = data.get('cluster', {})
config = cluster.get('configuration', {})
print(f\"Redundancy: {config.get('redundancy_mode','?')}\")
print(f\"Storage engine: {config.get('storage_engine','?')}\")
print(f\"Log spill: {config.get('log_spill','?')}\")
" 2>/dev/null
```

**Phase 1 outputs:** Cluster health, process count, redundancy mode, storage engine, transaction rate.

### Phase 2: Analysis

```bash
#!/bin/bash

FDB_CLUSTER="${FDB_CLUSTER_FILE:-/etc/foundationdb/fdb.cluster}"

echo "=== Process Health ==="
fdbcli --exec "status json" -C "$FDB_CLUSTER" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
cluster = data.get('cluster', {})
procs = cluster.get('processes', {})
for pid, p in procs.items():
    roles = [r['role'] for r in p.get('roles', [])]
    print(f\"  {p.get('address','?')}: roles={roles} cpu={p.get('cpu',{}).get('usage_cores','?')} mem={p.get('memory',{}).get('used_bytes',0)//1048576}MB\")
" 2>/dev/null | head -15

echo ""
echo "=== Workload Metrics ==="
fdbcli --exec "status json" -C "$FDB_CLUSTER" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
wl = data.get('cluster', {}).get('workload', {})
ops = wl.get('operations', {})
for op_type, stats in ops.items():
    print(f\"  {op_type}: {stats.get('hz', 0):.0f} ops/sec\")
txns = wl.get('transactions', {})
for t_type, stats in txns.items():
    print(f\"  txn_{t_type}: {stats.get('hz', 0):.0f}/sec\")
" 2>/dev/null

echo ""
echo "=== Data Distribution ==="
fdbcli --exec "status json" -C "$FDB_CLUSTER" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
dd = data.get('cluster', {}).get('data', {})
print(f\"Total KV size: {dd.get('total_kv_size_bytes', 0)//1048576}MB\")
print(f\"Total disk used: {dd.get('total_disk_used_bytes', 0)//1048576}MB\")
print(f\"Moving data: {dd.get('moving_data', {}).get('in_flight_bytes', 0)//1048576}MB\")
print(f\"Partitions: {dd.get('partitions_count', '?')}\")
" 2>/dev/null

echo ""
echo "=== Backup Status ==="
fdbcli --exec "status json" -C "$FDB_CLUSTER" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
layers = data.get('cluster', {}).get('layers', {})
backup = layers.get('backup', {})
if backup:
    print(f\"Backup running: {backup.get('instances_running', 0)}\")
else:
    print('No backup layer detected')
" 2>/dev/null
```

## Output Format

```
FOUNDATIONDB ANALYSIS
=====================
Cluster: [healthy/degraded/unavailable]
Processes: [count] | Redundancy: [mode] | Engine: [type]

ISSUES FOUND:
- [issue with affected process/role]

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

