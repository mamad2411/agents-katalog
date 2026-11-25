---
name: managing-coralogix
description: |
  Use when working with Coralogix — coralogix observability platform for log
  analytics, metrics, tracing, security, and alerting. Covers log querying with
  DataPrime, metric exploration, alert management, parsing rules, and data usage
  insights. Use when searching Coralogix logs, investigating application errors,
  managing alert rules, or analyzing log ingestion patterns.
connection_type: coralogix
preload: false
---

# Coralogix Monitoring Skill

Query, analyze, and manage Coralogix observability data using the Coralogix API.

## API Overview

Coralogix uses regional API endpoints. Set `CORALOGIX_DOMAIN` to your region (e.g., `coralogix.com`, `eu2.coralogix.com`).

### Core Helper Function

```bash
#!/bin/bash

cx_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    local url="https://ng-api-http.${CORALOGIX_DOMAIN}${endpoint}"
    if [ -n "$data" ]; then
        curl -s -X "$method" "$url" \
            -H "Authorization: Bearer $CORALOGIX_API_KEY" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "$url" \
            -H "Authorization: Bearer $CORALOGIX_API_KEY"
    fi
}

cx_logs() {
    local query="$1"
    local from="${2:-now-1h}"
    local to="${3:-now}"
    cx_api POST "/api/v1/dataprime/query" \
        "{\"query\":\"${query}\",\"metadata\":{\"startDate\":\"${from}\",\"endDate\":\"${to}\",\"limit\":100}}"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover applications, subsystems, and alert configurations before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Team Info ==="
cx_api GET "/api/v1/teams" | jq -r '.[] | "\(.teamId)\t\(.teamName)"' | head -10

echo ""
echo "=== Applications ==="
cx_logs "source logs | distinct applicationName | limit 30" \
    | jq -r '.results[].applicationName' | sort | head -30

echo ""
echo "=== Subsystems ==="
cx_logs "source logs | distinct subsystemName | limit 30" \
    | jq -r '.results[].subsystemName' | sort | head -30

echo ""
echo "=== Active Alerts ==="
cx_api GET "/api/v1/external/alerts" \
    | jq -r '.[] | "\(.id)\t\(.name)\t\(.is_active)\t\(.severity)"' | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Log Volume by Severity (last 1h) ==="
cx_logs "source logs | stats count() by severity | sort -count" \
    | jq -r '.results[] | "\(.severity)\t\(.count)"' | head -10

echo ""
echo "=== Error Logs by Application ==="
cx_logs "source logs | filter severity == 'error' | stats count() by applicationName | sort -count" \
    | jq -r '.results[] | "\(.applicationName)\t\(.count) errors"' | head -15

echo ""
echo "=== Recent Error Messages ==="
cx_logs "source logs | filter severity == 'error' | select timestamp, applicationName, text | limit 15" \
    | jq -r '.results[] | "\(.timestamp[0:19])\t\(.applicationName)\t\(.text[0:80])"' | head -15

echo ""
echo "=== Alert Status Summary ==="
cx_api GET "/api/v1/external/alerts" \
    | jq -r 'group_by(.is_active) | .[] | "\(if .[0].is_active then "Active" else "Inactive" end): \(length)"'
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use DataPrime aggregations and `limit` clauses
- Use `stats count() by` for grouping in DataPrime queries
- Filter at query level with `filter` before applying `select`

## Output Format

Present results as a structured report:
```
Managing Coralogix Report
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

