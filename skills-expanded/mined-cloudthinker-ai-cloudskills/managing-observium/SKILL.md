---
name: managing-observium
description: |
  Use when working with Observium — observium network monitoring platform for
  auto-discovery of network devices, SNMP-based monitoring, traffic analysis,
  and alerting. Covers device inventory, port utilization, health sensors, alert
  review, and syslog analysis. Use when monitoring network infrastructure,
  investigating device health, analyzing bandwidth utilization, or reviewing
  Observium alerts.
connection_type: observium
preload: false
---

# Observium Monitoring Skill

Query, analyze, and manage Observium monitoring data using the Observium API.

## API Overview

Observium uses a REST API at `https://<OBSERVIUM_HOST>/api/v0`.

### Core Helper Function

```bash
#!/bin/bash

obs_api() {
    local endpoint="$1"
    curl -s "${OBSERVIUM_URL}/api/v0/${endpoint}" \
        -u "${OBSERVIUM_USER}:${OBSERVIUM_PASS}" \
        -H "Accept: application/json"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover devices, device groups, and ports before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Devices ==="
obs_api "devices" | jq -r '.devices | to_entries[] | "\(.value.device_id)\t\(.value.hostname)\t\(.value.os)\t\(.value.status | if . == "1" then "UP" else "DOWN" end)"' | head -25

echo ""
echo "=== Device Groups ==="
obs_api "groups/device" | jq -r '.groups | to_entries[] | "\(.value.group_id)\t\(.value.group_name)"' | head -15

echo ""
echo "=== Port Count by Device ==="
obs_api "ports" | jq -r '[.ports | to_entries[].value | .device_id] | group_by(.) | map({device: .[0], ports: length}) | sort_by(-.ports)[] | "\(.device)\t\(.ports) ports"' | head -15

echo ""
echo "=== Alert Checks ==="
obs_api "alerts/checks" | jq -r '.checks | to_entries[] | "\(.value.alert_test_id)\t\(.value.alert_name)\t\(.value.entity_type)"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Active Alerts ==="
obs_api "alerts" | jq -r '.alerts | to_entries[] | "\(.value.severity)\t\(.value.device_hostname // "unknown")\t\(.value.alert_message[0:60])"' | head -15

echo ""
echo "=== Down Devices ==="
obs_api "devices" | jq -r '.devices | to_entries[] | select(.value.status != "1") | "\(.value.hostname)\t\(.value.os)\t\(.value.last_polled)"' | head -15

echo ""
echo "=== Top Ports by Traffic ==="
obs_api "ports" | jq -r '.ports | to_entries[] | select(.value.ifOperStatus == "up") | "\(.value.device_id)\t\(.value.ifName)\tin:\((.value.ifInOctets_rate // 0) / 125000 | . * 10 | round / 10)Mbps\tout:\((.value.ifOutOctets_rate // 0) / 125000 | . * 10 | round / 10)Mbps"' | sort -t$'\t' -k3 -rn | head -15

echo ""
echo "=== Health Sensors ==="
obs_api "sensors" | jq -r '.sensors | to_entries[] | select(.value.sensor_alert == "1") | "\(.value.device_id)\t\(.value.sensor_descr)\tcurrent:\(.value.sensor_value)\tlimit:\(.value.sensor_limit)"' | head -10

echo ""
echo "=== Recent Syslog ==="
obs_api "syslog?limit=15" | jq -r '.syslog[] | "\(.timestamp[0:19])\t\(.device_hostname)\t\(.msg[0:60])"' | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `limit` parameter and `head` in output
- Device status: 0=DOWN, 1=UP
- Use device groups for scoping to infrastructure segments
- Port rates are in bytes/sec — divide by 125000 for Mbps

## Output Format

Present results as a structured report:
```
Managing Observium Report
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

