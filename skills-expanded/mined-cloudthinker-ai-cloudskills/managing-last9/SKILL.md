---
name: managing-last9
description: |
  Use when working with Last9 — last9 observability platform for
  high-cardinality metrics, distributed tracing, log management, and SLO-based
  reliability management. Covers metric exploration, trace analysis, log
  querying, SLO tracking, and alert management. Use when querying Last9 metrics,
  investigating service reliability, managing SLOs, or analyzing
  high-cardinality telemetry data.
connection_type: last9
preload: false
---

# Last9 Monitoring Skill

Query, analyze, and manage Last9 observability data using the Last9 API.

## API Overview

Last9 uses a REST API at `https://app.last9.io/api/v1`.

### Core Helper Function

```bash
#!/bin/bash

l9_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" "${LAST9_URL:-https://app.last9.io}/api/v1/${endpoint}" \
            -H "Authorization: Bearer $LAST9_API_KEY" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "${LAST9_URL:-https://app.last9.io}/api/v1/${endpoint}" \
            -H "Authorization: Bearer $LAST9_API_KEY"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover services, SLOs, and data sources before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Services ==="
l9_api GET "services" | jq -r '.data[] | "\(.id)\t\(.name)\t\(.type // "unknown")"' | head -20

echo ""
echo "=== SLOs ==="
l9_api GET "slos" | jq -r '.data[] | "\(.id)\t\(.name)\t\(.target)%\t\(.status)"' | head -15

echo ""
echo "=== Data Sources ==="
l9_api GET "datasources" | jq -r '.data[] | "\(.id)\t\(.name)\t\(.type)"' | head -15

echo ""
echo "=== Alert Rules ==="
l9_api GET "alerts" | jq -r '.data[] | "\(.id)\t\(.name)\t\(.state // "unknown")"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== SLO Status Overview ==="
l9_api GET "slos" | jq -r '.data[] | "\(.name)\ttarget:\(.target)%\tcurrent:\(.currentValue // "N/A")%\tbudget_remaining:\(.errorBudgetRemaining // "N/A")%\tstatus:\(.status)"' | head -15

echo ""
echo "=== Service Health ==="
l9_api GET "services/health?period=1h" \
    | jq -r '.data[] | "\(.name)\tp99:\(.p99Latency // "N/A")ms\terror_rate:\(.errorRate // "N/A")%\tthroughput:\(.throughput // 0)"' \
    | sort -t$'\t' -k3 -rn | head -15

echo ""
echo "=== High Cardinality Metrics ==="
l9_api GET "metrics/top?period=1h&limit=15" \
    | jq -r '.data[] | "\(.metricName)\tcardinality:\(.cardinality)\tseries:\(.activeSeries)"' | head -15

echo ""
echo "=== Firing Alerts ==="
l9_api GET "alerts" | jq -r '.data[] | select(.state == "firing") | "\(.name)\tseverity:\(.severity)\ttriggered:\(.triggeredAt[0:19])"' | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `period` and `limit` parameters
- Focus on SLO-based views for reliability context
- Use service-level health endpoints before drilling into individual metrics

## Output Format

Present results as a structured report:
```
Managing Last9 Report
═════════════════════
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

