---
name: managing-logdna
description: |
  Use when working with Logdna — logDNA (now Mezmo) log management platform for
  log aggregation, search, alerting, and analysis. Covers log querying, view
  management, alert configuration, and usage monitoring. Use when searching
  LogDNA logs, investigating application issues through log data, managing views
  and alerts, or analyzing log ingestion volume.
connection_type: logdna
preload: false
---

# LogDNA Monitoring Skill

Query, analyze, and manage LogDNA log data using the LogDNA API.

## API Overview

LogDNA uses a REST API at `https://api.logdna.com`.

### Core Helper Function

```bash
#!/bin/bash

logdna_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" "https://api.logdna.com/v1/${endpoint}" \
            -u "${LOGDNA_SERVICE_KEY}:" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "https://api.logdna.com/v1/${endpoint}" \
            -u "${LOGDNA_SERVICE_KEY}:"
    fi
}

logdna_v2() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" "https://api.logdna.com/v2/${endpoint}" \
            -H "Authorization: Bearer $LOGDNA_SERVICE_KEY" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "https://api.logdna.com/v2/${endpoint}" \
            -H "Authorization: Bearer $LOGDNA_SERVICE_KEY"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover available apps, hosts, and log levels before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Usage Info ==="
logdna_api GET "usage/host" | jq -r '.[] | "\(.name)\t\(.lines) lines"' | sort -t$'\t' -k2 -rn | head -20

echo ""
echo "=== Available Apps ==="
logdna_api GET "usage/app" | jq -r '.[] | "\(.name)\t\(.lines) lines"' | sort -t$'\t' -k2 -rn | head -20

echo ""
echo "=== Views ==="
logdna_api GET "config/view" | jq -r '.[] | "\(.name)\t\(.query // "no query")"' | head -15

echo ""
echo "=== Alerts ==="
logdna_api GET "config/alert" | jq -r '.[] | "\(.name)\t\(.channels[0].type // "unknown")"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
QUERY="${1:-level:error}"
FROM="${2:-$(date -d '1 hour ago' +%s)}"
TO="${3:-$(date +%s)}"

echo "=== Log Search: ${QUERY} ==="
logdna_api GET "export?query=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${QUERY}'))")&from=${FROM}&to=${TO}&size=50" \
    | jq -r '.lines[] | "\(._ts[0:19])\t\(._app)\t\(._line[0:80])"' | head -20

echo ""
echo "=== Log Volume by Host ==="
logdna_api GET "usage/host" | jq -r '.[] | "\(.name)\t\(.lines)"' | sort -t$'\t' -k2 -rn | head -15

echo ""
echo "=== Log Volume by Level ==="
logdna_api GET "usage/level" | jq -r '.[] | "\(.name)\t\(.lines)"' | sort -t$'\t' -k2 -rn | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `size` parameter and `head` in output
- Filter at API level with `query` parameter before post-processing
- Use usage endpoints for volume analysis instead of counting raw log lines

## Output Format

Present results as a structured report:
```
Managing Logdna Report
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

