---
name: managing-groundcover
description: |
  Use when working with Groundcover — groundcover eBPF-based Kubernetes
  observability platform for APM, infrastructure monitoring, log management, and
  network analysis without code instrumentation. Covers service map discovery,
  golden signal metrics, log querying, alert management, and Kubernetes workload
  analysis. Use when monitoring Kubernetes services, investigating performance
  issues, querying container logs, or managing groundcover alerts.
connection_type: groundcover
preload: false
---

# Groundcover Monitoring Skill

Query, analyze, and manage groundcover observability data using the groundcover API.

## API Overview

Groundcover uses a REST API at `https://app.groundcover.com/api/v1`.

### Core Helper Function

```bash
#!/bin/bash

gc_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" "${GROUNDCOVER_URL:-https://app.groundcover.com}/api/v1/${endpoint}" \
            -H "Authorization: Bearer $GROUNDCOVER_API_KEY" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "${GROUNDCOVER_URL:-https://app.groundcover.com}/api/v1/${endpoint}" \
            -H "Authorization: Bearer $GROUNDCOVER_API_KEY"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover clusters, namespaces, and services before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Clusters ==="
gc_api GET "clusters" | jq -r '.data[] | "\(.id)\t\(.name)\t\(.status)"' | head -10

echo ""
echo "=== Namespaces ==="
gc_api GET "namespaces" | jq -r '.data[] | "\(.namespace)\t\(.cluster)\tworkloads:\(.workloadCount // 0)"' | head -20

echo ""
echo "=== Services ==="
gc_api GET "services?period=1h" | jq -r '.data[] | "\(.name)\t\(.namespace)\t\(.protocol // "unknown")"' | head -20

echo ""
echo "=== Alert Rules ==="
gc_api GET "alerts" | jq -r '.data[] | "\(.id)\t\(.name)\t\(.state // "unknown")"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Service Golden Signals (last 1h) ==="
gc_api GET "services/metrics?period=1h" \
    | jq -r '.data[] | "\(.name)\t\(.namespace)\tp99:\(.p99Latency // 0)ms\terror%:\(.errorRate // 0)\treqs:\(.requestRate // 0)/s"' \
    | sort -t$'\t' -k4 -rn | head -15

echo ""
echo "=== Kubernetes Workload Health ==="
gc_api GET "workloads?period=1h" \
    | jq -r '.data[] | "\(.name)\t\(.namespace)\t\(.kind)\tready:\(.readyReplicas)/\(.replicas)\tcpu:\(.cpuUsage // "N/A")"' | head -15

echo ""
echo "=== Recent Error Logs ==="
gc_api POST "logs/search" '{"query":"level:error","from":"now-1h","to":"now","limit":20}' \
    | jq -r '.data[] | "\(.timestamp[0:19])\t\(.namespace)/\(.pod)\t\(.message[0:70])"' | head -15

echo ""
echo "=== Network Issues ==="
gc_api GET "network/anomalies?period=1h" \
    | jq -r '.data[] | "\(.source) -> \(.destination)\t\(.anomalyType)\t\(.severity)"' | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `period` and `limit` parameters
- Use golden signals (latency, error rate, throughput) for service-level overview
- Leverage namespace scoping to narrow queries

## Output Format

Present results as a structured report:
```
Managing Groundcover Report
═══════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

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

