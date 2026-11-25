---
name: managing-netdata
description: |
  Use when working with Netdata — netdata real-time infrastructure monitoring
  platform for system metrics, application performance, container monitoring,
  and alerting. Covers CPU, memory, disk, network metrics, active alarms, chart
  exploration, and node management. Use when monitoring server health,
  investigating resource utilization, reviewing active alarms, or exploring
  Netdata metrics.
connection_type: netdata
preload: false
---

# Netdata Monitoring Skill

Query, analyze, and manage Netdata monitoring data using the Netdata API.

## API Overview

Netdata uses a REST API at `http://<NETDATA_HOST>:19999/api/v1` (local agent) or Netdata Cloud API.

### Core Helper Function

```bash
#!/bin/bash

nd_api() {
    local endpoint="$1"
    curl -s "${NETDATA_URL:-http://localhost:19999}/api/v1/${endpoint}" \
        ${NETDATA_API_KEY:+-H "Authorization: Bearer $NETDATA_API_KEY"}
}

nd_data() {
    local chart="$1"
    local after="${2:--3600}"
    local points="${3:-1}"
    nd_api "data?chart=${chart}&after=${after}&points=${points}&format=json"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover available charts, nodes, and alarms before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Node Info ==="
nd_api "info" | jq -r '"Hostname: \(.hostname)\nOS: \(.os_name) \(.os_version)\nCPU cores: \(.cores_total)\nRAM: \(.ram_total | . / 1073741824 | . * 10 | round / 10)GB"'

echo ""
echo "=== Chart Categories ==="
nd_api "charts" | jq -r '.charts | keys[]' | cut -d'.' -f1 | sort -u | head -20

echo ""
echo "=== Active Alarms ==="
nd_api "alarms" | jq -r '.alarms | to_entries[] | "\(.value.status)\t\(.value.chart)\t\(.value.info[0:60])"' | head -20

echo ""
echo "=== Monitored Contexts ==="
nd_api "contexts" | jq -r '.contexts | keys[]' | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== CPU Usage (last 1h avg) ==="
nd_data "system.cpu" -3600 1 | jq -r '.data[0] | "User: \(.[1] // 0)%  System: \(.[2] // 0)%  IOWait: \(.[5] // 0)%"'

echo ""
echo "=== Memory Usage ==="
nd_data "system.ram" -3600 1 | jq -r '.data[0] | "Used: \(.[1] // 0)MB  Cached: \(.[3] // 0)MB  Free: \(.[2] // 0)MB"'

echo ""
echo "=== Disk I/O ==="
nd_api "charts" | jq -r '.charts | keys[]' | grep "^disk\." | while read chart; do
    val=$(nd_data "$chart" -3600 1 | jq -r '.data[0] | "\(.[1] // 0) read, \(.[2] // 0) write"')
    echo "$chart: $val"
done | head -10

echo ""
echo "=== Network Traffic ==="
nd_data "system.net" -3600 1 | jq -r '.data[0] | "Received: \(.[1] // 0) kbps  Sent: \(.[2] // 0) kbps"'

echo ""
echo "=== Critical/Warning Alarms ==="
nd_api "alarms" | jq -r '.alarms | to_entries[] | select(.value.status == "CRITICAL" or .value.status == "WARNING") | "\(.value.status)\t\(.value.chart)\t\(.value.info[0:60])"' | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `points=1` for latest value and `head` in output
- Use chart-level queries for aggregated metrics
- Check alarms endpoint for active issues before deep-diving into metrics

## Output Format

Present results as a structured report:
```
Managing Netdata Report
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

