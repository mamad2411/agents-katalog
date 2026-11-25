---
name: managing-manageengine-opmanager
description: |
  Use when working with Manageengine Opmanager — manageEngine OpManager network
  monitoring platform for routers, switches, firewalls, servers, and virtual
  infrastructure. Covers device discovery, interface monitoring, alert
  management, performance dashboards, and report generation. Use when monitoring
  network device health, investigating interface utilization, reviewing alarms,
  or managing OpManager device inventory.
connection_type: manageengine-opmanager
preload: false
---

# ManageEngine OpManager Monitoring Skill

Query, analyze, and manage OpManager monitoring data using the OpManager REST API.

## API Overview

OpManager uses a REST API at `https://<OPMANAGER_HOST>/api/json`.

### Core Helper Function

```bash
#!/bin/bash

opm_api() {
    local endpoint="$1"
    local params="${2:-}"
    curl -s "${OPMANAGER_URL}/api/json/${endpoint}?apiKey=${OPMANAGER_API_KEY}&${params}"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover devices, categories, and alarm profiles before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Device Summary ==="
opm_api "device/listDevices" | jq -r '.data[] | "\(.deviceId)\t\(.deviceName)\t\(.ipAddress)\t\(.status)"' | head -25

echo ""
echo "=== Device Categories ==="
opm_api "device/getCategories" | jq -r '.data[] | "\(.categoryId)\t\(.categoryName)\tdevices:\(.deviceCount // 0)"' | head -15

echo ""
echo "=== Business Views ==="
opm_api "businessview/listBusinessViews" | jq -r '.data[] | "\(.bvId)\t\(.bvName)"' | head -15

echo ""
echo "=== Alarm Profiles ==="
opm_api "alarm/listAlarmProfiles" | jq -r '.data[] | "\(.profileId)\t\(.profileName)\t\(.severity)"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Active Alarms ==="
opm_api "alarm/listAlarms" "severity=critical&status=active" \
    | jq -r '.data[] | "\(.severity)\t\(.deviceName)\t\(.message[0:60])\t\(.modTime)"' | head -15

echo ""
echo "=== Down Devices ==="
opm_api "device/listDevices" "status=down" \
    | jq -r '.data[] | "\(.deviceName)\t\(.ipAddress)\t\(.category)\t\(.lastPollTime)"' | head -15

echo ""
echo "=== Interface Utilization (Top) ==="
opm_api "interface/listInterfaces" "sortBy=utilization&sortOrder=desc&limit=15" \
    | jq -r '.data[] | "\(.deviceName)\t\(.ifName)\tin:\(.rxUtil // 0)%\tout:\(.txUtil // 0)%"' | head -15

echo ""
echo "=== Alarm Summary ==="
opm_api "alarm/getAlarmSummary" | jq -r '"Critical: \(.critical // 0)\nWarning: \(.warning // 0)\nInfo: \(.info // 0)\nCleared: \(.cleared // 0)"'

echo ""
echo "=== Device Health (CPU/Memory) ==="
opm_api "device/getDeviceHealth" "limit=15" \
    | jq -r '.data[] | "\(.deviceName)\tcpu:\(.cpuUtil // "N/A")%\tmem:\(.memUtil // "N/A")%\tdisk:\(.diskUtil // "N/A")%"' | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `status`, `severity`, and `limit` parameters
- Alarm severity: critical, warning, info, clear
- Device status: up, down, unknown, maintenance
- Use alarm summary endpoint for quick overview before drilling into individual alarms

## Output Format

Present results as a structured report:
```
Managing Manageengine Opmanager Report
══════════════════════════════════════
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

