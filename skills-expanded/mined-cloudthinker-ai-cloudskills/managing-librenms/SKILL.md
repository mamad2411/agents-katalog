---
name: managing-librenms
description: |
  Use when working with Librenms — libreNMS network monitoring platform for
  network devices, servers, SNMP monitoring, alerting, and performance graphing.
  Covers device discovery, port monitoring, alert management, health sensor
  data, and availability reporting. Use when monitoring network devices,
  investigating interface utilization, reviewing alerts, or managing LibreNMS
  device inventory.
connection_type: librenms
preload: false
---

# LibreNMS Monitoring Skill

Query, analyze, and manage LibreNMS monitoring data using the LibreNMS API.

## API Overview

LibreNMS uses a REST API at `https://<LIBRENMS_HOST>/api/v0`.

### Core Helper Function

```bash
#!/bin/bash

lnms_api() {
    local endpoint="$1"
    curl -s "${LIBRENMS_URL}/api/v0/${endpoint}" \
        -H "X-Auth-Token: $LIBRENMS_API_TOKEN"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover devices, device groups, and alert rules before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Device Summary ==="
lnms_api "devices" | jq -r '.devices[] | "\(.device_id)\t\(.hostname)\t\(.os)\t\(.status | if . == 1 then "UP" else "DOWN" end)"' | head -25

echo ""
echo "=== Device Groups ==="
lnms_api "devicegroups" | jq -r '.groups[] | "\(.id)\t\(.name)\t\(.desc[0:40])"' | head -15

echo ""
echo "=== Alert Rules ==="
lnms_api "rules" | jq -r '.rules[] | "\(.id)\t\(.name)\t\(.severity)\t\(.disabled | if . == 0 then "enabled" else "disabled" end)"' | head -15

echo ""
echo "=== Services ==="
lnms_api "services" | jq -r '.services[] | "\(.service_id)\t\(.device_id)\t\(.service_type)\t\(.service_status)"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Active Alerts ==="
lnms_api "alerts?state=1" | jq -r '.alerts[] | "\(.severity)\t\(.hostname)\t\(.rule.name)\t\(.timestamp)"' | head -15

echo ""
echo "=== Down Devices ==="
lnms_api "devices" | jq -r '.devices[] | select(.status == 0) | "\(.hostname)\t\(.os)\t\(.last_polled)"' | head -15

echo ""
echo "=== Port Utilization (top by traffic) ==="
lnms_api "ports?columns=port_id,ifName,ifAlias,ifInOctets_rate,ifOutOctets_rate,device_id" \
    | jq -r '.ports[] | select(.ifInOctets_rate > 0) | "\(.device_id)\t\(.ifName)\tin:\(.ifInOctets_rate / 1000000 * 8 | . * 10 | round / 10)Mbps\tout:\(.ifOutOctets_rate / 1000000 * 8 | . * 10 | round / 10)Mbps"' \
    | sort -t$'\t' -k3 -rn | head -15

echo ""
echo "=== Health Sensors (Warnings) ==="
lnms_api "resources/sensors" \
    | jq -r '.sensors[] | select(.sensor_current > .sensor_limit or .sensor_current < .sensor_limit_low) | "\(.device_id)\t\(.sensor_descr)\tcurrent:\(.sensor_current)\tlimit:\(.sensor_limit)"' | head -10

echo ""
echo "=== Device Availability ==="
lnms_api "devices" | jq -r '.devices[] | "\(.hostname)\tuptime:\(.uptime / 86400 | floor)d\t\(.status | if . == 1 then "UP" else "DOWN" end)"' | sort -t$'\t' -k2 -rn | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `columns` parameter and `head` in output
- Device status: 0=DOWN, 1=UP
- Alert states: 0=OK, 1=ACTIVE, 2=ACKNOWLEDGED
- Use device groups to scope queries to specific infrastructure segments

## Output Format

Present results as a structured report:
```
Managing Librenms Report
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

