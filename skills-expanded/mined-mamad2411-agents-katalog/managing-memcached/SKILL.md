---
name: managing-memcached
description: |
  Use when working with Memcached — memcached instance monitoring, slab
  allocation analysis, hit ratio optimization, and connection management. Covers
  memory utilization, eviction rates, item distribution across slabs, connection
  pool health, and multi-instance topology. Read this skill before any Memcached
  operations.
connection_type: memcached
preload: false
---

# Memcached Management Skill

Monitor, analyze, and optimize Memcached instances safely.

## MANDATORY: Discovery-First Pattern

**Always run stats commands before inspecting specific slabs or items. Never assume slab classes or item counts.**

### Phase 1: Discovery

```bash
#!/bin/bash

MC_HOST="${MEMCACHED_HOST:-localhost}"
MC_PORT="${MEMCACHED_PORT:-11211}"

mc_cmd() {
    echo "$1" | nc -q2 "$MC_HOST" "$MC_PORT" 2>/dev/null || \
    echo "$1" | nc -w2 "$MC_HOST" "$MC_PORT" 2>/dev/null
}

echo "=== General Stats ==="
mc_cmd "stats" | grep -E 'version|uptime|curr_connections|total_connections|curr_items|total_items|bytes |limit_maxbytes|evictions|get_hits|get_misses|cmd_get|cmd_set'

echo ""
echo "=== Hit Ratio ==="
mc_cmd "stats" | awk -F' ' '
    /get_hits/ { hits=$3 }
    /get_misses/ { misses=$3 }
    END {
        total = hits + misses
        if (total > 0) printf "Hit ratio: %.1f%% (%s hits, %s misses)\n", hits/total*100, hits, misses
        else print "No gets recorded yet"
    }'

echo ""
echo "=== Memory Usage ==="
mc_cmd "stats" | awk -F' ' '
    /^STAT bytes / { used=$3 }
    /limit_maxbytes/ { limit=$3 }
    END {
        if (limit > 0) printf "Memory: %dMB / %dMB (%.1f%%)\n", used/1048576, limit/1048576, used/limit*100
    }'

echo ""
echo "=== Slab Overview ==="
mc_cmd "stats slabs" | grep -E 'chunk_size|used_chunks|total_chunks|mem_requested' | head -20
```

**Phase 1 outputs:** Version, connection count, item count, hit ratio, memory utilization, slab allocation.

### Phase 2: Analysis

```bash
#!/bin/bash

MC_HOST="${MEMCACHED_HOST:-localhost}"
MC_PORT="${MEMCACHED_PORT:-11211}"

mc_cmd() {
    echo "$1" | nc -q2 "$MC_HOST" "$MC_PORT" 2>/dev/null || \
    echo "$1" | nc -w2 "$MC_HOST" "$MC_PORT" 2>/dev/null
}

echo "=== Slab Efficiency ==="
mc_cmd "stats slabs" | awk -F'[: ]' '
    /used_chunks/ { slab=$2; used[$2]=$4 }
    /total_chunks/ { total[$2]=$4 }
    END {
        for (s in used) {
            if (total[s] > 0) printf "Slab %s: %s/%s chunks used (%.0f%%)\n", s, used[s], total[s], used[s]/total[s]*100
        }
    }' | sort -t: -k1 -n

echo ""
echo "=== Eviction Stats ==="
mc_cmd "stats items" | grep -E 'evicted|outofmemory|crawler' | head -15

echo ""
echo "=== Connection Analysis ==="
mc_cmd "stats" | grep -E 'curr_connections|listen_disabled|conn_yields|rejected_connections'

echo ""
echo "=== Growth Trends ==="
mc_cmd "stats" | grep -E 'total_items|evictions|reclaimed|expired_unfetched'
```

## Output Format

```
MEMCACHED ANALYSIS
==================
Version: [version] | Uptime: [days]d
Memory: [used]/[limit] | Items: [count] | Hit Ratio: [pct]%

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

