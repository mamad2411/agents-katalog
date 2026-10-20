---
name: managing-checkmk
description: |
  Use when working with Checkmk — checkmk infrastructure and application
  monitoring platform for hosts, services, network devices, and cloud resources.
  Covers host/service status, event console, rule management, agent deployment,
  and WATO configuration. Use when checking Checkmk monitoring status,
  investigating service problems, managing host configurations, or reviewing
  monitoring rules.
connection_type: checkmk
preload: false
---

# Checkmk Monitoring Skill

Query, analyze, and manage Checkmk monitoring data using the Checkmk REST API.

## API Overview

Checkmk uses a REST API at `https://<CMK_HOST>/<SITE>/check_mk/api/1.0`.

### Core Helper Function

```bash
#!/bin/bash

cmk_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    local url="${CHECKMK_URL}/check_mk/api/1.0/${endpoint}"
    if [ -n "$data" ]; then
        curl -s -X "$method" "$url" \
            -H "Authorization: Bearer ${CHECKMK_USER} ${CHECKMK_SECRET}" \
            -H "Content-Type: application/json" \
            -H "Accept: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "$url" \
            -H "Authorization: Bearer ${CHECKMK_USER} ${CHECKMK_SECRET}" \
            -H "Accept: application/json"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover hosts, folders, and host groups before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Site Version ==="
cmk_api GET "version" | jq -r '"Version: \(.versions.checkmk)\nEdition: \(.edition)"'

echo ""
echo "=== Folders ==="
cmk_api GET "domain-types/folder_config/collections/all" \
    | jq -r '.value[] | "\(.id)\t\(.title)"' | head -15

echo ""
echo "=== Hosts ==="
cmk_api GET "domain-types/host_config/collections/all" \
    | jq -r '.value[] | "\(.id)\t\(.title)\t\(.extensions.folder // "/")"' | head -25

echo ""
echo "=== Host Groups ==="
cmk_api GET "domain-types/host_group_config/collections/all" \
    | jq -r '.value[] | "\(.id)\t\(.title)"' | head -15

echo ""
echo "=== Contact Groups ==="
cmk_api GET "domain-types/contact_group_config/collections/all" \
    | jq -r '.value[] | "\(.id)\t\(.title)"' | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Host Problems ==="
cmk_api GET "domain-types/host/collections/all?query=%7B%22op%22%3A%22!%3D%22%2C%22left%22%3A%22state%22%2C%22right%22%3A%220%22%7D" \
    | jq -r '.value[] | "\(.extensions.state | if . == 1 then "DOWN" elif . == 2 then "UNREACH" else "UNKNOWN" end)\t\(.title)\t\(.extensions.last_check // "N/A")"' | head -15

echo ""
echo "=== Service Problems ==="
cmk_api GET "domain-types/service/collections/all?query=%7B%22op%22%3A%22!%3D%22%2C%22left%22%3A%22state%22%2C%22right%22%3A%220%22%7D" \
    | jq -r '.value[] | "\(.extensions.state | if . == 1 then "WARN" elif . == 2 then "CRIT" else "UNKNOWN" end)\t\(.extensions.host_name)/\(.title)\t\(.extensions.plugin_output[0:50])"' | head -20

echo ""
echo "=== Status Summary ==="
cmk_api GET "domain-types/host/collections/all" | jq -r '[.value[].extensions.state] | group_by(.) | map({state: (.[0] | if . == 0 then "UP" elif . == 1 then "DOWN" else "UNREACH" end), count: length})[] | "\(.state): \(.count)"'

echo ""
echo "=== Scheduled Downtimes ==="
cmk_api GET "domain-types/downtime/collections/all" \
    | jq -r '.value[] | "\(.extensions.host_name)\t\(.extensions.service_description // "HOST")\t\(.extensions.author)\t\(.extensions.comment[0:40])"' | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use query filters and `head` in output
- Host states: 0=UP, 1=DOWN, 2=UNREACHABLE
- Service states: 0=OK, 1=WARNING, 2=CRITICAL, 3=UNKNOWN
- Use Livestatus query expressions in `query` parameter for server-side filtering

## Output Format

Present results as a structured report:
```
Managing Checkmk Report
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

