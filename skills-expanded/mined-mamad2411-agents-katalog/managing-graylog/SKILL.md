---
name: managing-graylog
description: |
  Use when working with Graylog — graylog centralized log management platform
  for log collection, search, dashboards, alerting, and pipeline processing.
  Covers log querying with Lucene syntax, stream management, alert condition
  configuration, dashboard review, and input/output management. Use when
  searching Graylog logs, managing streams and pipelines, investigating
  incidents, or configuring alert rules.
connection_type: graylog
preload: false
---

# Graylog Monitoring Skill

Query, analyze, and manage Graylog log data using the Graylog REST API.

## API Overview

Graylog uses a REST API at `https://<GRAYLOG_HOST>/api`.

### Core Helper Function

```bash
#!/bin/bash

gl_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" "${GRAYLOG_URL}/api/${endpoint}" \
            -H "Authorization: Bearer $GRAYLOG_API_TOKEN" \
            -H "Content-Type: application/json" \
            -H "Accept: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "${GRAYLOG_URL}/api/${endpoint}" \
            -H "Authorization: Bearer $GRAYLOG_API_TOKEN" \
            -H "Accept: application/json"
    fi
}

gl_search() {
    local query="$1"
    local range="${2:-3600}"
    local limit="${3:-50}"
    gl_api GET "search/universal/relative?query=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${query}'))")&range=${range}&limit=${limit}&sort=timestamp:desc"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover streams, inputs, and indices before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== System Overview ==="
gl_api GET "system" | jq -r '"Cluster ID: \(.cluster_id)\nNode ID: \(.node_id)\nVersion: \(.version)\nStatus: \(.lifecycle)"'

echo ""
echo "=== Streams ==="
gl_api GET "streams" | jq -r '.streams[] | "\(.id)\t\(.title)\t\(.disabled)"' | head -20

echo ""
echo "=== Inputs ==="
gl_api GET "system/inputs" | jq -r '.inputs[] | "\(.id)\t\(.title)\t\(.type)\t\(.global)"' | head -15

echo ""
echo "=== Index Sets ==="
gl_api GET "system/indices/index_sets" | jq -r '.index_sets[] | "\(.id)\t\(.title)\t\(.total_number_of_indices) indices"' | head -10

echo ""
echo "=== Alert Conditions ==="
gl_api GET "alerts/conditions" | jq -r '.conditions[] | "\(.id)\t\(.title)\t\(.type)"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
QUERY="${1:-level:3 OR level:4}"

echo "=== Log Search: ${QUERY} ==="
gl_search "$QUERY" 3600 30 | jq -r '.messages[] | "\(.message.timestamp[0:19])\t\(.message.source)\t\(.message.message[0:80])"' | head -20

echo ""
echo "=== Message Count by Source (last 1h) ==="
gl_api GET "search/universal/relative/terms?field=source&query=*&range=3600&size=15" \
    | jq -r '.terms | to_entries[] | "\(.key)\t\(.value)"' | sort -t$'\t' -k2 -rn | head -15

echo ""
echo "=== Recent Alerts ==="
gl_api GET "streams/alerts?since=$(date -d '24 hours ago' +%s)&limit=15" \
    | jq -r '.[] | "\(.triggered_at[0:19])\t\(.condition_id)\t\(.description[0:60])"' | head -15

echo ""
echo "=== Node Health ==="
gl_api GET "system/cluster" | jq -r '.[] | "\(.node_id[0:8])\t\(.hostname)\t\(.lifecycle)\t\(.is_leader)"' | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `limit` parameter and `terms` aggregation endpoint
- Use Lucene query syntax for log search (e.g., `source:nginx AND level:3`)
- Prefer terms aggregation for volume breakdowns over counting raw messages

## Output Format

Present results as a structured report:
```
Managing Graylog Report
═══════════════════════
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

