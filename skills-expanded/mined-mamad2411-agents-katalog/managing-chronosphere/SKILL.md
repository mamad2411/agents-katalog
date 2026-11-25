---
name: managing-chronosphere
description: |
  Use when working with Chronosphere — chronosphere cloud-native observability
  platform for metrics, tracing, and alerting at scale. Covers PromQL-based
  metric queries, trace analysis, monitor management, dashboards, and control
  plane configuration. Use when querying Chronosphere metrics, investigating
  service performance, managing alerting rules, or analyzing distributed traces.
connection_type: chronosphere
preload: false
---

# Chronosphere Monitoring Skill

Query, analyze, and manage Chronosphere observability data using the Chronosphere API.

## API Overview

Chronosphere uses a REST API at your tenant URL: `https://<TENANT>.chronosphere.io/api`.

### Core Helper Function

```bash
#!/bin/bash

chrono_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    local url="${CHRONOSPHERE_URL}/api/v1/${endpoint}"
    if [ -n "$data" ]; then
        curl -s -X "$method" "$url" \
            -H "Authorization: Bearer $CHRONOSPHERE_API_TOKEN" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "$url" \
            -H "Authorization: Bearer $CHRONOSPHERE_API_TOKEN"
    fi
}

chrono_query() {
    local promql="$1"
    local time="${2:-$(date +%s)}"
    chrono_api GET "query?query=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${promql}'))")&time=${time}"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover available metrics, services, and monitors before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Available Metric Namespaces ==="
chrono_api GET "label/__name__/values" | jq -r '.data[]' | cut -d'_' -f1 | sort -u | head -20

echo ""
echo "=== Monitors ==="
chrono_api GET "config/monitors" | jq -r '.monitors[] | "\(.slug)\t\(.name)\t\(.state // "unknown")"' | head -20

echo ""
echo "=== Dashboards ==="
chrono_api GET "config/dashboards" | jq -r '.dashboards[] | "\(.slug)\t\(.name)"' | head -20

echo ""
echo "=== Collections (Metric Groupings) ==="
chrono_api GET "config/collections" | jq -r '.collections[] | "\(.slug)\t\(.name)"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== CPU Usage by Service (top 15) ==="
chrono_query 'avg by (service) (rate(process_cpu_seconds_total[5m]) * 100)' \
    | jq -r '.data.result[] | "\(.metric.service)\t\(.value[1])%"' | sort -t$'\t' -k2 -rn | head -15

echo ""
echo "=== Request Rate by Service ==="
chrono_query 'sum by (service) (rate(http_requests_total[5m]))' \
    | jq -r '.data.result[] | "\(.metric.service)\t\(.value[1]) req/s"' | sort -t$'\t' -k2 -rn | head -15

echo ""
echo "=== Error Rate by Service ==="
chrono_query 'sum by (service) (rate(http_requests_total{status=~"5.."}[5m])) / sum by (service) (rate(http_requests_total[5m])) * 100' \
    | jq -r '.data.result[] | "\(.metric.service)\t\(.value[1])%"' | sort -t$'\t' -k2 -rn | head -15

echo ""
echo "=== Firing Monitors ==="
chrono_api GET "config/monitors" | jq -r '.monitors[] | select(.state == "firing") | "\(.slug)\t\(.name)"' | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use PromQL aggregation and `head` in output
- Use `avg by`, `sum by` for grouping instead of raw series
- Prefer instant queries over range queries unless trend analysis is needed

## Output Format

Present results as a structured report:
```
Managing Chronosphere Report
════════════════════════════
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

