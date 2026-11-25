---
name: managing-honeycomb
description: |
  Use when working with Honeycomb — honeycomb observability platform for
  distributed tracing, event-driven analytics, BubbleUp root cause analysis,
  SLOs, and triggers. Covers querying datasets, analyzing trace spans,
  investigating latency, managing SLOs, and reviewing trigger alerts. Use when
  exploring Honeycomb datasets, debugging slow requests, analyzing service
  dependencies, or managing observability workflows.
connection_type: honeycomb
preload: false
---

# Honeycomb Monitoring Skill

Query, analyze, and manage Honeycomb observability data using the Honeycomb API.

## API Overview

Honeycomb uses a REST API at `https://api.honeycomb.io`.

### Core Helper Function

```bash
#!/bin/bash

hc_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" "https://api.honeycomb.io/1/${endpoint}" \
            -H "X-Honeycomb-Team: $HONEYCOMB_API_KEY" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "https://api.honeycomb.io/1/${endpoint}" \
            -H "X-Honeycomb-Team: $HONEYCOMB_API_KEY"
    fi
}

hc_query() {
    local dataset="$1"
    local query_json="$2"
    hc_api POST "queries/${dataset}" "$query_json"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover datasets, columns, and SLOs before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Auth & Environment ==="
hc_api GET "auth" | jq -r '"Team: \(.team.slug)\nEnvironment: \(.environment.slug)"'

echo ""
echo "=== Available Datasets ==="
hc_api GET "datasets" | jq -r '.[] | "\(.slug)\t\(.last_written_at // "never")[0:10]"' | column -t | head -20

echo ""
echo "=== Columns in Dataset ==="
DATASET="${1:-}"
[ -n "$DATASET" ] && hc_api GET "columns/${DATASET}" \
    | jq -r '.[] | "\(.key_name)\t\(.type)"' | sort | head -30

echo ""
echo "=== SLOs ==="
hc_api GET "slos" | jq -r '.[] | "\(.id)\t\(.name)\t\(.target_per_million/10000)%"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
DATASET="${1:?Dataset slug required}"

echo "=== Request Rate & Latency (last 2h) ==="
hc_api POST "queries/${DATASET}" '{
    "calculations": [
        {"op": "COUNT"},
        {"op": "P95", "column": "duration_ms"},
        {"op": "AVG", "column": "duration_ms"}
    ],
    "time_range": 7200,
    "granularity": 3600
}' | jq -r '.data.results[] | "\(.ts)\tcount:\(.data[0].COUNT)\tp95:\(.data[0].P95 // "N/A")ms\tavg:\(.data[0].AVG // "N/A")ms"' | head -10

echo ""
echo "=== Error Rate by Service ==="
hc_api POST "queries/${DATASET}" '{
    "calculations": [{"op": "COUNT"}],
    "filters": [{"column": "error", "op": "=", "value": true}],
    "breakdowns": ["service.name"],
    "time_range": 3600,
    "limit": 15
}' | jq -r '.data.results[] | "\(.data[0]["service.name"])\t\(.data[0].COUNT) errors"' | sort -t$'\t' -k2 -rn | head -15

echo ""
echo "=== Triggers ==="
hc_api GET "triggers/${DATASET}" | jq -r '.[] | "\(.id)\t\(.name)\t\(.triggered ? "FIRING" : "OK")"' | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `limit` in queries and `head` in output
- Use `breakdowns` for grouping instead of fetching raw events
- Use `granularity` only when time-series trends are specifically needed

## Output Format

Present results as a structured report:
```
Managing Honeycomb Report
═════════════════════════
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

