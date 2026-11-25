---
name: managing-keydb
description: |
  Use when working with Keydb — keyDB multi-threaded Redis-compatible datastore
  management, active replication monitoring, FLASH storage tier analysis, and
  sub-key expiration inspection. Covers thread configuration, multi-master
  replication, MVCC diagnostics, and memory-to-flash ratio tuning. Read this
  skill before any KeyDB operations.
connection_type: keydb
preload: false
---

# KeyDB Management Skill

Monitor, analyze, and optimize KeyDB instances safely.

## MANDATORY: Discovery-First Pattern

**Always run INFO ALL before any operations. Never assume threading model or active replication topology.**

### Phase 1: Discovery

```bash
#!/bin/bash

keydb_cmd() {
    keydb-cli -h "${KEYDB_HOST:-localhost}" -p "${KEYDB_PORT:-6379}" \
              ${KEYDB_PASSWORD:+-a "$KEYDB_PASSWORD"} \
              --no-auth-warning "$@" 2>/dev/null || \
    redis-cli -h "${KEYDB_HOST:-localhost}" -p "${KEYDB_PORT:-6379}" \
              ${KEYDB_PASSWORD:+-a "$KEYDB_PASSWORD"} \
              --no-auth-warning "$@"
}

echo "=== Server Info ==="
keydb_cmd INFO server | grep -E 'keydb_version|redis_version|uptime_in_days|server_threads|os'

echo ""
echo "=== Threading ==="
keydb_cmd CONFIG GET server-threads 2>/dev/null
keydb_cmd CONFIG GET server-thread-affinity 2>/dev/null

echo ""
echo "=== Memory Overview ==="
keydb_cmd INFO memory | grep -E 'used_memory_human|used_memory_peak_human|maxmemory_human|mem_fragmentation_ratio|maxmemory_policy'

echo ""
echo "=== Keyspace ==="
keydb_cmd INFO keyspace

echo ""
echo "=== Active Replication ==="
keydb_cmd INFO replication | grep -E 'role|connected_slaves|master_link_status|master_host|active_replica'

echo ""
echo "=== FLASH Tier ==="
keydb_cmd CONFIG GET storage-provider 2>/dev/null || echo "FLASH storage not configured"
```

**Phase 1 outputs:** KeyDB version, thread count, memory usage, keyspace, replication topology, FLASH status.

### Phase 2: Analysis

```bash
#!/bin/bash

keydb_cmd() {
    keydb-cli -h "${KEYDB_HOST:-localhost}" -p "${KEYDB_PORT:-6379}" \
              ${KEYDB_PASSWORD:+-a "$KEYDB_PASSWORD"} \
              --no-auth-warning "$@" 2>/dev/null || \
    redis-cli -h "${KEYDB_HOST:-localhost}" -p "${KEYDB_PORT:-6379}" \
              ${KEYDB_PASSWORD:+-a "$KEYDB_PASSWORD"} \
              --no-auth-warning "$@"
}

echo "=== Performance Stats ==="
keydb_cmd INFO stats | grep -E 'instantaneous_ops_per_sec|total_commands_processed|keyspace_hits|keyspace_misses|evicted_keys'

echo ""
echo "=== Multi-Master Status ==="
keydb_cmd INFO replication | grep -E 'active-replica|multi_master'

echo ""
echo "=== Slow Log ==="
keydb_cmd SLOWLOG GET 10

echo ""
echo "=== Client Connections ==="
keydb_cmd CLIENT LIST | awk -F'[ =]' '{for(i=1;i<=NF;i++) if($i=="addr") print $(i+1)}' | \
    cut -d: -f1 | sort | uniq -c | sort -rn | head -10

echo ""
echo "=== Sub-Key Expires ==="
keydb_cmd INFO stats | grep -E 'subkey|expired' | head -5

echo ""
echo "=== Persistence ==="
keydb_cmd INFO persistence | grep -E 'rdb_last_save|rdb_last_bgsave_status|aof_enabled'
```

## Output Format

```
KEYDB ANALYSIS
==============
Version: [version] | Threads: [count] | Mode: [standalone/active-replica]
Memory: [used]/[max] | Keys: [count] | FLASH: [enabled/disabled]

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

