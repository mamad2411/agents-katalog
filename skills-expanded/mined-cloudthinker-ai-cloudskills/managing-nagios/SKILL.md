---
name: managing-nagios
description: |
  Use when working with Nagios — nagios infrastructure monitoring platform for
  host and service monitoring, alerting, event handling, and availability
  reporting. Covers host status review, service check results, notification
  management, downtime scheduling, and performance data analysis. Use when
  checking Nagios host/service status, investigating alerts, scheduling
  downtime, or reviewing monitoring configurations.
connection_type: nagios
preload: false
---

# Nagios Monitoring Skill

Query, analyze, and manage Nagios monitoring data using the Nagios API (Core or XI).

## API Overview

Nagios XI uses a REST API at `https://<NAGIOS_HOST>/nagiosxi/api/v1`. Nagios Core uses the CGI interface or Livestatus.

### Core Helper Function

```bash
#!/bin/bash

nagios_api() {
    local endpoint="$1"
    local params="${2:-}"
    curl -s "${NAGIOS_URL}/nagiosxi/api/v1/${endpoint}?apikey=${NAGIOS_API_KEY}&${params}"
}

# For Nagios Core with Livestatus
nagios_ls() {
    local query="$1"
    echo "$query" | unixcat "${NAGIOS_LIVESTATUS_SOCKET:-/var/nagios/rw/live}"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover hostgroups, hosts, and servicegroups before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Host Groups ==="
nagios_api "objects/hostgrouplist" | jq -r '.hostgrouplist[] | "\(.hostgroup_name)\thosts:\(.members | length)"' | head -15

echo ""
echo "=== Hosts ==="
nagios_api "objects/hoststatus" "records=25" | jq -r '.hoststatus[] | "\(.host_name)\t\(.status_text)\t\(.address)\t\(.last_check[0:16])"' | head -25

echo ""
echo "=== Service Groups ==="
nagios_api "objects/servicegrouplist" | jq -r '.servicegrouplist[] | "\(.servicegroup_name)"' | head -15

echo ""
echo "=== Contact Groups ==="
nagios_api "objects/contactgrouplist" | jq -r '.contactgrouplist[] | "\(.contactgroup_name)"' | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Host Problems ==="
nagios_api "objects/hoststatus" "hoststatus_types=12" \
    | jq -r '.hoststatus[] | "\(.status_text)\t\(.host_name)\t\(.status_information[0:60])"' | head -15

echo ""
echo "=== Service Problems ==="
nagios_api "objects/servicestatus" "servicestatus_types=28" \
    | jq -r '.servicestatus[] | "\(.status_text)\t\(.host_name)/\(.service_description)\t\(.status_information[0:50])"' | head -20

echo ""
echo "=== Status Summary ==="
nagios_api "objects/hoststatus" | jq -r '[.hoststatus[] | .status_text] | group_by(.) | map({status: .[0], count: length})[] | "\(.status): \(.count)"'
nagios_api "objects/servicestatus" | jq -r '[.servicestatus[] | .status_text] | group_by(.) | map({status: .[0], count: length})[] | "\(.status): \(.count)"'

echo ""
echo "=== Scheduled Downtimes ==="
nagios_api "objects/downtimedata" | jq -r '.downtimedata[] | "\(.host_name)\t\(.service_description // "HOST")\t\(.start_time[0:16])-\(.end_time[0:16])\t\(.author)"' | head -10

echo ""
echo "=== Recent Notifications ==="
nagios_api "objects/notificationlist" "records=15" \
    | jq -r '.notificationlist[] | "\(.start_time[0:16])\t\(.host_name)\t\(.service_description // "HOST")\t\(.notification_type)"' | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `records` parameter and filter by status types
- Status types bitmask: 1=OK/UP, 2=WARNING/DOWN, 4=CRITICAL/UNREACHABLE, 8=UNKNOWN, 16=PENDING
- Use `hoststatus_types` and `servicestatus_types` to filter at API level

## Output Format

Present results as a structured report:
```
Managing Nagios Report
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

