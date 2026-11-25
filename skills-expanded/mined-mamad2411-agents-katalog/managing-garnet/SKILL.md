---
name: managing-garnet
description: |
  Use when working with Garnet — microsoft Garnet cache-store management, RESP
  protocol compatibility analysis, performance benchmarking, and cluster
  configuration. Covers server health, memory usage, storage tier inspection,
  checkpoint status, and client connection diagnostics. Read this skill before
  any Garnet operations.
connection_type: garnet
preload: false
---

# Garnet Management Skill

Monitor, analyze, and optimize Microsoft Garnet instances safely.

## MANDATORY: Discovery-First Pattern

**Always run INFO and PING before any operations. Never assume feature compatibility with Redis commands.**

### Phase 1: Discovery

```bash
#!/bin/bash

garnet_cmd() {
    redis-cli -h "${GARNET_HOST:-localhost}" -p "${GARNET_PORT:-6379}" \
              ${GARNET_PASSWORD:+-a "$GARNET_PASSWORD"} \
              --no-auth-warning "$@"
}

echo "=== Server Info ==="
garnet_cmd INFO server 2>/dev/null | grep -E 'garnet_version|redis_version|uptime_in_seconds|tcp_port|os' || \
    garnet_cmd INFO 2>/dev/null | head -20

echo ""
echo "=== Connectivity ==="
garnet_cmd PING

echo ""
echo "=== Memory Overview ==="
garnet_cmd INFO memory 2>/dev/null | grep -E 'used_memory|maxmemory'

echo ""
echo "=== Keyspace ==="
garnet_cmd INFO keyspace 2>/dev/null
garnet_cmd DBSIZE

echo ""
echo "=== Clients ==="
garnet_cmd INFO clients 2>/dev/null | grep -E 'connected_clients|blocked_clients'

echo ""
echo "=== Supported Commands Check ==="
for cmd in SCAN TYPE TTL OBJECT CLUSTER MODULE; do
    result=$(garnet_cmd COMMAND INFO "$cmd" 2>/dev/null)
    if echo "$result" | grep -q "ERR\|nil"; then
        echo "  $cmd: NOT SUPPORTED"
    else
        echo "  $cmd: supported"
    fi
done
```

**Phase 1 outputs:** Garnet version, memory usage, keyspace, client count, command compatibility.

### Phase 2: Analysis

```bash
#!/bin/bash

garnet_cmd() {
    redis-cli -h "${GARNET_HOST:-localhost}" -p "${GARNET_PORT:-6379}" \
              ${GARNET_PASSWORD:+-a "$GARNET_PASSWORD"} \
              --no-auth-warning "$@"
}

echo "=== Performance Stats ==="
garnet_cmd INFO stats 2>/dev/null | grep -E 'instantaneous_ops_per_sec|total_commands_processed|keyspace_hits|keyspace_misses'

echo ""
echo "=== Hit Rate ==="
garnet_cmd INFO stats 2>/dev/null | awk -F: '
    /keyspace_hits/ { hits=$2 }
    /keyspace_misses/ { misses=$2 }
    END {
        total = hits + misses
        if (total > 0) printf "Hit rate: %.1f%%\n", hits/total*100
        else print "No gets recorded"
    }'

echo ""
echo "=== Replication ==="
garnet_cmd INFO replication 2>/dev/null | grep -E 'role|connected_slaves'

echo ""
echo "=== Key Type Sample ==="
garnet_cmd SCAN 0 COUNT 100 2>/dev/null | tail -n +2 | while read key; do
    type=$(garnet_cmd TYPE "$key" 2>/dev/null)
    echo "$type"
done | sort | uniq -c | sort -rn 2>/dev/null || echo "SCAN not available"

echo ""
echo "=== Persistence/Checkpoint ==="
garnet_cmd INFO persistence 2>/dev/null | head -10 || echo "Persistence info not available"
```

## Output Format

```
GARNET ANALYSIS
===============
Version: [version] | Protocol: RESP
Memory: [used]/[max] | Keys: [count] | Ops/sec: [count]

ISSUES FOUND:
- [issue or compatibility gap]

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

