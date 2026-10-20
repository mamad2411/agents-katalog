---
name: managing-baselime
description: |
  Use when working with Baselime — baselime serverless observability platform
  for AWS Lambda, CloudFlare Workers, and Vercel functions. Covers log and trace
  querying, alert management, service discovery, and performance analysis of
  serverless workloads. Use when investigating serverless function performance,
  querying Baselime events, managing alerts, or analyzing cold start and
  duration metrics.
connection_type: baselime
preload: false
---

# Baselime Monitoring Skill

Query, analyze, and manage Baselime observability data using the Baselime API.

## API Overview

Baselime uses a REST API at `https://api.baselime.io/v1`.

### Core Helper Function

```bash
#!/bin/bash

bl_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" "https://api.baselime.io/v1/${endpoint}" \
            -H "Authorization: Bearer $BASELIME_API_KEY" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "https://api.baselime.io/v1/${endpoint}" \
            -H "Authorization: Bearer $BASELIME_API_KEY"
    fi
}

bl_query() {
    local query_json="$1"
    bl_api POST "query" "$query_json"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover environments, services, and datasets before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Environments ==="
bl_api GET "environments" | jq -r '.[] | "\(.id)\t\(.name)"' | head -10

echo ""
echo "=== Services ==="
bl_api GET "services" | jq -r '.[] | "\(.name)\t\(.type // "unknown")\t\(.runtime // "N/A")"' | head -20

echo ""
echo "=== Datasets ==="
bl_api GET "datasets" | jq -r '.[] | "\(.id)\t\(.name)"' | head -15

echo ""
echo "=== Alerts ==="
bl_api GET "alerts" | jq -r '.[] | "\(.id)\t\(.name)\t\(.enabled)\t\(.threshold // "N/A")"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Lambda Performance (last 1h) ==="
bl_query '{
    "datasets": ["lambda-logs"],
    "calculations": [
        {"operator": "COUNT"},
        {"operator": "P95", "key": "duration"},
        {"operator": "AVG", "key": "duration"}
    ],
    "groupBy": ["@service"],
    "timeframe": "1h",
    "limit": 15
}' | jq -r '.results[] | "\(.group["@service"])\tcount:\(.COUNT)\tp95:\(.P95 // "N/A")ms\tavg:\(.AVG // "N/A")ms"' | head -15

echo ""
echo "=== Error Events ==="
bl_query '{
    "datasets": ["lambda-logs"],
    "filters": [{"key": "@level", "operator": "=", "value": "error"}],
    "calculations": [{"operator": "COUNT"}],
    "groupBy": ["@service"],
    "timeframe": "1h",
    "limit": 15
}' | jq -r '.results[] | "\(.group["@service"])\t\(.COUNT) errors"' | sort -t$'\t' -k2 -rn | head -15

echo ""
echo "=== Cold Starts ==="
bl_query '{
    "datasets": ["lambda-logs"],
    "filters": [{"key": "@initDuration", "operator": "exists"}],
    "calculations": [{"operator": "COUNT"}, {"operator": "AVG", "key": "@initDuration"}],
    "groupBy": ["@service"],
    "timeframe": "1h",
    "limit": 15
}' | jq -r '.results[] | "\(.group["@service"])\tcold_starts:\(.COUNT)\tavg_init:\(.AVG // "N/A")ms"' | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `limit` and `groupBy` for aggregation
- Use calculations with groupBy for service-level summaries
- Filter at query level before post-processing

## Output Format

Present results as a structured report:
```
Managing Baselime Report
════════════════════════
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

