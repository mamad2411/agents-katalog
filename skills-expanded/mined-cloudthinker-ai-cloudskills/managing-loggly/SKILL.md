---
name: managing-loggly
description: |
  Use when working with Loggly — loggly cloud log management platform for log
  search, analysis, alerting, and dashboards. Covers log querying with Lucene
  syntax, field exploration, alert management, and usage analysis. Use when
  searching Loggly logs, investigating application errors, managing alert
  configurations, or analyzing log volume patterns.
connection_type: loggly
preload: false
---

# Loggly Monitoring Skill

Query, analyze, and manage Loggly log data using the Loggly API.

## API Overview

Loggly uses a REST API at `https://<SUBDOMAIN>.loggly.com/apiv2`.

### Core Helper Function

```bash
#!/bin/bash

loggly_api() {
    local endpoint="$1"
    curl -s "https://${LOGGLY_SUBDOMAIN}.loggly.com/apiv2/${endpoint}" \
        -H "Authorization: Bearer $LOGGLY_API_TOKEN"
}

loggly_search() {
    local query="$1"
    local from="${2:--1h}"
    local to="${3:-now}"
    local rsid
    rsid=$(loggly_api "search?q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${query}'))")&from=${from}&until=${to}&size=50" | jq -r '.rsid.id')
    [ -n "$rsid" ] && loggly_api "events?rsid=${rsid}"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover available fields, source groups, and alerts before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Available Fields ==="
loggly_api "fields" | jq -r '.[] | "\(.name)\t\(.type)"' | sort | head -25

echo ""
echo "=== Source Groups ==="
loggly_api "source-groups" | jq -r '.sourcegroups[] | "\(.id)\t\(.name)"' | head -15

echo ""
echo "=== Saved Searches ==="
loggly_api "saved-searches" | jq -r '.savedsearches[] | "\(.id)\t\(.name)\t\(.query)"' | head -15

echo ""
echo "=== Alerts ==="
loggly_api "alerts" | jq -r '.alerts[] | "\(.id)\t\(.name)\t\(.status)"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Error Logs (last 1h) ==="
loggly_search "syslog.severity:error OR level:error" "-1h" "now" \
    | jq -r '.events[] | "\(.timestamp[0:19])\t\(.event.json.message[0:80] // .event.raw[0:80])"' | head -20

echo ""
echo "=== Log Volume by Level ==="
loggly_api "fields/json.level?from=-1h&until=now&facet_size=10" \
    | jq -r '.json.level[] | "\(.term)\t\(.count)"' | sort -t$'\t' -k2 -rn | head -10

echo ""
echo "=== Log Volume by Source ==="
loggly_api "fields/syslog.appName?from=-1h&until=now&facet_size=15" \
    | jq -r '.syslog.appName[] | "\(.term)\t\(.count)"' | sort -t$'\t' -k2 -rn | head -15

echo ""
echo "=== Active Alerts ==="
loggly_api "alerts" | jq -r '.alerts[] | select(.status == "active") | "\(.name)\t\(.query)\t\(.threshold)"' | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `size` parameter and facet queries for aggregation
- Use Lucene query syntax for filtering (e.g., `level:error AND app:myservice`)
- Use field facets for volume breakdowns instead of counting raw events

## Output Format

Present results as a structured report:
```
Managing Loggly Report
══════════════════════
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

