---
name: managing-dragonfly
description: |
  Use when working with Dragonfly — dragonfly in-memory datastore management,
  multi-threaded performance analysis, memory efficiency monitoring, and
  compatibility checks. Covers thread utilization, snapshot operations, memory
  usage per thread, replication status, and Redis/Memcached protocol
  compatibility. Read this skill before any Dragonfly operations.
connection_type: dragonfly
preload: false
---

# Dragonfly Management Skill

Monitor, analyze, and optimize Dragonfly instances safely.

## MANDATORY: Discovery-First Pattern

**Always run INFO ALL before any operations. Never assume threading model or memory layout.**

### Phase 1: Discovery

```bash
#!/bin/bash

df_cmd() {
    redis-cli -h "${DRAGONFLY_HOST:-localhost}" -p "${DRAGONFLY_PORT:-6379}" \
              ${DRAGONFLY_PASSWORD:+-a "$DRAGONFLY_PASSWORD"} \
              --no-auth-warning "$@"
}

echo "=== Server Info ==="
df_cmd INFO server | grep -E 'dragonfly_version|redis_version|uptime_in_days|tcp_port|os|used_threads'

echo ""
echo "=== Memory Overview ==="
df_cmd INFO memory | grep -E 'used_memory_human|used_memory_peak_human|maxmemory_human|mem_fragmentation_ratio'

echo ""
echo "=== Keyspace ==="
df_cmd INFO keyspace

echo ""
echo "=== Database Size ==="
df_cmd DBSIZE

echo ""
echo "=== Clients ==="
df_cmd INFO clients | grep -E 'connected_clients|blocked_clients'

echo ""
echo "=== Replication ==="
df_cmd INFO replication | grep -E 'role|connected_slaves|master_link_status'
```

**Phase 1 outputs:** Dragonfly version, thread count, memory usage, keyspace, client count.

### Phase 2: Analysis

```bash
#!/bin/bash

df_cmd() {
    redis-cli -h "${DRAGONFLY_HOST:-localhost}" -p "${DRAGONFLY_PORT:-6379}" \
              ${DRAGONFLY_PASSWORD:+-a "$DRAGONFLY_PASSWORD"} \
              --no-auth-warning "$@"
}

echo "=== Performance Stats ==="
df_cmd INFO stats | grep -E 'instantaneous_ops_per_sec|total_commands_processed|keyspace_hits|keyspace_misses|evicted_keys'

echo ""
echo "=== Hit Rate ==="
df_cmd INFO stats | awk -F: '
    /keyspace_hits/ { hits=$2 }
    /keyspace_misses/ { misses=$2 }
    END {
        total = hits + misses
        if (total > 0) printf "Hit rate: %.1f%%\n", hits/total*100
    }'

echo ""
echo "=== Slow Log ==="
df_cmd SLOWLOG GET 10 2>/dev/null || echo "Slowlog not available"

echo ""
echo "=== Snapshot Status ==="
df_cmd INFO persistence | grep -E 'rdb_|aof_|save_|snapshot'

echo ""
echo "=== Key Type Distribution (sample) ==="
df_cmd SCAN 0 COUNT 200 | tail -n +2 | while read key; do
    df_cmd TYPE "$key"
done | sort | uniq -c | sort -rn
```

## Output Format

```
DRAGONFLY ANALYSIS
==================
Version: [version] | Threads: [count]
Memory: [used]/[max] | Keys: [count] | Ops/sec: [count]

ISSUES FOUND:
- [issue with affected component]

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

