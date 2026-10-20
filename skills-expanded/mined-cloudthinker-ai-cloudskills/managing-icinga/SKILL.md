---
name: managing-icinga
description: |
  Use when working with Icinga — icinga infrastructure monitoring platform for
  host and service monitoring, cluster management, alerting, and performance
  data analysis. Covers host/service status, check result review, notification
  management, downtime scheduling, and configuration object management via
  Icinga 2 API. Use when checking monitoring status, investigating alerts,
  managing downtimes, or querying Icinga objects.
connection_type: icinga
preload: false
---

# Icinga Monitoring Skill

Query, analyze, and manage Icinga monitoring data using the Icinga 2 API.

## API Overview

Icinga 2 uses a REST API at `https://<ICINGA_HOST>:5665/v1`.

### Core Helper Function

```bash
#!/bin/bash

icinga_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -k -X "$method" "https://${ICINGA_HOST}:5665/v1/${endpoint}" \
            -H "Authorization: Basic $(echo -n "${ICINGA_USER}:${ICINGA_PASS}" | base64)" \
            -H "Accept: application/json" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -k -X "$method" "https://${ICINGA_HOST}:5665/v1/${endpoint}" \
            -H "Authorization: Basic $(echo -n "${ICINGA_USER}:${ICINGA_PASS}" | base64)" \
            -H "Accept: application/json"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover hosts, host groups, and services before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Icinga Status ==="
icinga_api GET "status/IcingaApplication" | jq -r '.results[0].status.icingaapplication.app | "Version: \(.version)\nNode: \(.node_name)"'

echo ""
echo "=== Host Groups ==="
icinga_api GET "objects/hostgroups" | jq -r '.results[] | "\(.name)\t\(.attrs.display_name)"' | head -15

echo ""
echo "=== Hosts ==="
icinga_api GET "objects/hosts" | jq -r '.results[] | "\(.name)\t\(.attrs.state | if . == 0 then "UP" elif . == 1 then "DOWN" else "UNREACHABLE" end)\t\(.attrs.address)"' | head -25

echo ""
echo "=== Service Groups ==="
icinga_api GET "objects/servicegroups" | jq -r '.results[] | "\(.name)"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Host Problems ==="
icinga_api POST "objects/hosts" '{"filter": "host.state != 0"}' \
    | jq -r '.results[] | "\(if .attrs.state == 1 then "DOWN" else "UNREACHABLE" end)\t\(.name)\t\(.attrs.last_check_result.output[0:60])"' | head -15

echo ""
echo "=== Service Problems ==="
icinga_api POST "objects/services" '{"filter": "service.state != 0"}' \
    | jq -r '.results[] | "\(if .attrs.state == 1 then "WARNING" elif .attrs.state == 2 then "CRITICAL" else "UNKNOWN" end)\t\(.name)\t\(.attrs.last_check_result.output[0:50])"' | head -20

echo ""
echo "=== Status Summary ==="
echo "Hosts:"
icinga_api GET "status/CIB" | jq -r '.results[0].status | "  UP: \(.num_hosts_up)  DOWN: \(.num_hosts_down)  UNREACHABLE: \(.num_hosts_unreachable)"'
echo "Services:"
icinga_api GET "status/CIB" | jq -r '.results[0].status | "  OK: \(.num_services_ok)  WARN: \(.num_services_warning)  CRIT: \(.num_services_critical)  UNKNOWN: \(.num_services_unknown)"'

echo ""
echo "=== Active Downtimes ==="
icinga_api GET "objects/downtimes" | jq -r '.results[] | "\(.attrs.host_name)\t\(.attrs.service_name // "HOST")\t\(.attrs.author)\t\(.attrs.comment)"' | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use API filters and `head` in output
- Host states: 0=UP, 1=DOWN, 2=UNREACHABLE
- Service states: 0=OK, 1=WARNING, 2=CRITICAL, 3=UNKNOWN
- Use `filter` parameter in POST body for server-side filtering

## Output Format

Present results as a structured report:
```
Managing Icinga Report
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

