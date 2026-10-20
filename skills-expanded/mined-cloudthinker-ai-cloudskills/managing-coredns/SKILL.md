---
name: managing-coredns
description: |
  Use when working with Coredns — coreDNS server management, zone configuration,
  plugin chain analysis, query logging, and cache statistics. Covers Corefile
  inspection, health endpoint monitoring, metrics collection, and forwarding
  configuration. Read this skill before any CoreDNS operations — it enforces
  discovery-first patterns, anti-hallucination rules, and safety constraints.
connection_type: coredns
preload: false
---

# CoreDNS Management Skill

Monitor, analyze, and manage CoreDNS servers safely.

## MANDATORY: Discovery-First Pattern

**Always inspect the Corefile and running metrics before making changes. Never guess zone names or plugin chains.**

### Phase 1: Discovery

```bash
#!/bin/bash

COREDNS_METRICS="${COREDNS_METRICS:-http://localhost:9153}"
COREFILE="${COREFILE:-/etc/coredns/Corefile}"

echo "=== CoreDNS Version ==="
coredns -version 2>/dev/null || echo "coredns binary not in PATH — check container/pod"

echo ""
echo "=== Corefile Contents ==="
cat "$COREFILE" 2>/dev/null || \
    kubectl -n kube-system get configmap coredns -o jsonpath='{.data.Corefile}' 2>/dev/null || \
    echo "Corefile not found at $COREFILE"

echo ""
echo "=== Running Process ==="
ps aux | grep '[c]oredns' | awk '{print $1, $2, $11, $12, $13}'

echo ""
echo "=== Health Check ==="
curl -s http://localhost:8080/health 2>/dev/null || echo "Health endpoint not reachable"

echo ""
echo "=== Ready Check ==="
curl -s http://localhost:8181/ready 2>/dev/null || echo "Ready endpoint not reachable"

echo ""
echo "=== DNS Test Query ==="
dig @127.0.0.1 -p 53 version.bind TXT CH +short 2>/dev/null || echo "DNS port not reachable locally"
```

**Phase 1 outputs:** Zone definitions, plugin chain per zone, listening ports, forwarding targets

### Phase 2: Analysis

Only inspect zones and plugins confirmed in Phase 1 Corefile output.

## Anti-Hallucination Rules

- **NEVER assume zone names** — always parse from the Corefile
- **NEVER guess plugin order** — plugin chain order matters and is zone-specific
- **NEVER assume forwarding targets** — extract from `forward` directives
- **NEVER assume metrics port** — default is 9153 but can be configured differently
- **ALWAYS check Kubernetes context** if CoreDNS runs in a cluster

## Safety Rules

- **READ-ONLY by default**: Use metrics endpoint, dig queries, Corefile reading, log inspection
- **FORBIDDEN without explicit request**: Editing Corefile, restarting CoreDNS, deleting zones
- **ALWAYS validate**: Test with `coredns -conf Corefile -dns.port 15353` on a test port before applying
- **Kubernetes awareness**: In k8s, CoreDNS config is in a ConfigMap — edit the ConfigMap, not the file
- **Plugin order matters**: Plugins execute in the order listed — changing order changes behavior

## Core Helper Functions

```bash
#!/bin/bash

COREDNS_METRICS="${COREDNS_METRICS:-http://localhost:9153}"

# Query CoreDNS metrics
coredns_metrics() {
    curl -s "$COREDNS_METRICS/metrics"
}

# Parse zones from Corefile
list_zones() {
    local corefile="${1:-/etc/coredns/Corefile}"
    awk '/^[a-zA-Z0-9.:]+\s*\{/ || /^[a-zA-Z0-9.:]+\s*$/ {
        gsub(/\{/,""); gsub(/\s+/,""); if ($0 != "") print $0
    }' "$corefile" 2>/dev/null
}

# Test DNS resolution
dns_test() {
    local name="$1"
    local type="${2:-A}"
    local server="${3:-127.0.0.1}"
    dig @"$server" "$name" "$type" +short +time=2
}

# Get plugin chain for a zone
zone_plugins() {
    local zone="$1"
    local corefile="${2:-/etc/coredns/Corefile}"
    awk -v zone="$zone" '
        $0 ~ zone { found=1; next }
        found && /\}/ { found=0 }
        found { gsub(/^[ \t]+/, ""); print }
    ' "$corefile" 2>/dev/null
}
```

## Common Operations

### Zone Management

```bash
#!/bin/bash
COREFILE="${COREFILE:-/etc/coredns/Corefile}"

echo "=== Zone Definitions ==="
awk '
    /^[^ \t#].*\{/ {
        zone=$1; plugins=""
        while (getline > 0 && !/^\}/) {
            gsub(/^[ \t]+/, "")
            if ($0 != "" && $0 !~ /^#/) plugins = plugins " " $1
        }
        printf "Zone: %-30s Plugins:%s\n", zone, plugins
    }
' "$COREFILE" 2>/dev/null

echo ""
echo "=== Forward Targets ==="
grep -E '^\s*forward' "$COREFILE" 2>/dev/null | while read _ zone targets; do
    echo "Zone forward: $zone -> $targets"
done

echo ""
echo "=== Zone File References ==="
grep -E '^\s*file\s' "$COREFILE" 2>/dev/null
```

### Plugin Chain Analysis

```bash
#!/bin/bash
COREFILE="${COREFILE:-/etc/coredns/Corefile}"

echo "=== Plugin Chains (execution order) ==="
awk '
    /^[^ \t#].*\{/ { zone=$1; idx=0 }
    /^\s+[a-z]/ && zone {
        gsub(/^[ \t]+/, "")
        plugin=$1
        idx++
        printf "%s [%d] %s\n", zone, idx, plugin
    }
    /^\}/ { zone="" }
' "$COREFILE" 2>/dev/null

echo ""
echo "=== Kubernetes Plugin Config ==="
awk '
    /kubernetes/ { found=1; print "kubernetes plugin found:" }
    found { print "  " $0 }
    found && /\}/ { found=0 }
' "$COREFILE" 2>/dev/null || echo "No kubernetes plugin configured"
```

### Query Logging and Metrics

```bash
#!/bin/bash
echo "=== DNS Query Metrics ==="
coredns_metrics 2>/dev/null | grep -E '^coredns_dns_request' | head -20

echo ""
echo "=== Response Codes ==="
coredns_metrics 2>/dev/null | grep 'coredns_dns_responses_total' | \
    awk -F'[{}]' '{print $2}' | sort | head -20

echo ""
echo "=== Request Duration ==="
coredns_metrics 2>/dev/null | grep 'coredns_dns_request_duration_seconds' | \
    grep -E '_sum|_count' | head -10

echo ""
echo "=== Query Log (if log plugin enabled) ==="
journalctl -u coredns --no-pager -n 50 2>/dev/null || \
    kubectl -n kube-system logs -l k8s-app=kube-dns --tail=50 2>/dev/null || \
    echo "Check container/pod logs for query log"
```

### Cache Statistics

```bash
#!/bin/bash
echo "=== Cache Hit/Miss Rates ==="
coredns_metrics 2>/dev/null | grep 'coredns_cache' | grep -v '^#'

echo ""
echo "=== Cache Size ==="
coredns_metrics 2>/dev/null | grep 'coredns_cache_entries' | \
    awk '{printf "%-60s entries=%s\n", $1, $2}'

echo ""
echo "=== Cache Hit Ratio ==="
coredns_metrics 2>/dev/null | awk '
    /coredns_cache_hits_total/ { hits+=$2 }
    /coredns_cache_misses_total/ { misses+=$2 }
    END {
        total=hits+misses
        if (total > 0) printf "Cache hit rate: %.1f%% (hits=%d misses=%d)\n", hits/total*100, hits, misses
    }
'
```

## Output Format

Present results as a structured report:
```
Managing Coredns Report
═══════════════════════
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

- **Plugin order is critical**: `errors` should come before `log`; `cache` before `forward` — wrong order means plugins are skipped
- **Kubernetes service discovery**: The `kubernetes` plugin must match the cluster domain (default: `cluster.local`)
- **Forward vs proxy**: `proxy` plugin is deprecated — always use `forward`
- **Cache TTL**: Cache plugin respects upstream TTL — setting cache TTL higher than upstream TTL serves stale records
- **Health check ports**: `/health` (8080) and `/ready` (8181) are separate — liveness uses health, readiness uses ready
- **ConfigMap reload**: CoreDNS watches the ConfigMap but may take up to 30 seconds to pick up changes
- **Stub domains in Kubernetes**: Must be configured in the Corefile, not in kube-dns ConfigMap
- **Loop detection**: The `loop` plugin detects forwarding loops — if CoreDNS crashes with loop, check forward targets
