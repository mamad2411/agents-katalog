---
name: managing-crowdstrike
description: |
  Use when working with Crowdstrike — crowdStrike Falcon endpoint detection and
  response, threat intelligence, host management, and incident investigation.
  Covers detection queries, host inventory, IOC searches, real-time response
  sessions, and vulnerability assessment. Use when investigating security
  incidents, reviewing endpoint health, analyzing threat detections, or managing
  CrowdStrike Falcon sensors.
connection_type: crowdstrike
preload: false
---

# CrowdStrike Falcon Management Skill

Manage and analyze CrowdStrike Falcon detections, hosts, incidents, and threat intelligence.

## API Conventions

### Authentication
All API calls use OAuth2 bearer tokens via `Authorization: Bearer $CROWDSTRIKE_ACCESS_TOKEN` -- injected automatically. Never hardcode tokens.

### Base URL
`https://api.crowdstrike.com`

### Core Helper Function

```bash
#!/bin/bash

cs_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $CROWDSTRIKE_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.crowdstrike.com${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $CROWDSTRIKE_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.crowdstrike.com${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Always filter by relevant time range to avoid huge response sets
- Never dump full API responses

## Discovery Phase

```bash
#!/bin/bash
echo "=== Host Inventory Summary ==="
cs_api GET "/devices/queries/devices-scroll/v1?limit=5000" \
    | jq '.meta.pagination.total as $total | "Total managed hosts: \($total)"' -r

echo ""
echo "=== Recent Detections (last 24h) ==="
cs_api GET "/detects/queries/detects/v1?filter=created_timestamp:>'$(date -u -v-1d +%Y-%m-%dT%H:%M:%SZ)'&limit=100" \
    | jq '.meta.pagination.total as $total | "Detections (24h): \($total)"' -r

echo ""
echo "=== Active Incidents ==="
cs_api GET "/incidents/queries/incidents/v1?filter=status:['20','25']&limit=50" \
    | jq '.meta.pagination.total as $total | "Open incidents: \($total)"' -r
```

## Analysis Phase

### Detection Overview

```bash
#!/bin/bash
echo "=== Critical/High Detections ==="
IDS=$(cs_api GET "/detects/queries/detects/v1?filter=max_severity_displayname:['Critical','High']+created_timestamp:>'$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)'&limit=20" | jq -r '.resources[:20] | join(",")')

if [ -n "$IDS" ]; then
    cs_api POST "/detects/entities/summaries/GET/v1" "{\"ids\":[$(echo "$IDS" | sed 's/,/","/g' | sed 's/^/"/;s/$/"/')]}" \
        | jq -r '.resources[] | "\(.created_timestamp[0:16])\t\(.max_severity_displayname)\t\(.status)\t\(.device.hostname)\t\(.detection_id)"' \
        | column -t | head -20
fi

echo ""
echo "=== Detection Count by Severity ==="
cs_api GET "/detects/aggregates/detects/GET/v1" \
    -d '{"date_ranges":[{"from":"'"$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)"'","to":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"}],"field":"max_severity_displayname","type":"terms"}' \
    | jq -r '.resources[].buckets[] | "\(.label): \(.count)"'
```

### Host Health

```bash
#!/bin/bash
echo "=== Hosts by Platform ==="
cs_api POST "/devices/aggregates/devices/GET/v1" \
    '[{"type":"terms","field":"platform_name"}]' \
    | jq -r '.resources[].buckets[] | "\(.label): \(.count)"'

echo ""
echo "=== Hosts with Stale Sensors (>7 days) ==="
cs_api GET "/devices/queries/devices/v1?filter=last_seen:<='$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)'&limit=10" \
    | jq '.meta.pagination.total as $total | "Stale sensors: \($total)"' -r

echo ""
echo "=== Sensor Versions ==="
cs_api POST "/devices/aggregates/devices/GET/v1" \
    '[{"type":"terms","field":"agent_version","size":10}]' \
    | jq -r '.resources[].buckets[] | "\(.label): \(.count)"' | head -10
```

### Incident Investigation

```bash
#!/bin/bash
INCIDENT_ID="${1:?Incident ID required}"

echo "=== Incident Details ==="
cs_api POST "/incidents/entities/incidents/GET/v1" "{\"ids\":[\"$INCIDENT_ID\"]}" \
    | jq '.resources[0] | {
        incident_id: .incident_id,
        status: .status,
        severity: .fine_score,
        start: .start,
        end: .end,
        hosts: (.hosts | length),
        tactics: .tactics,
        techniques: .techniques
    }'

echo ""
echo "=== Associated Detections ==="
cs_api GET "/incidents/queries/behaviors/v1?filter=incident_id:'$INCIDENT_ID'" \
    | jq -r '.resources[:10][]'
```

## Output Format

Present results as a structured report:
```
Managing Crowdstrike Report
═══════════════════════════
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

## Common Pitfalls

- **Two-step entity lookup**: Query endpoints return IDs only -- must call entity endpoints to get details
- **FQL syntax**: Filter queries use Falcon Query Language with single quotes for values
- **Rate limits**: 6000 requests/min for most endpoints -- stagger parallel calls
- **Pagination**: Default limit varies by endpoint -- always specify `limit` parameter
- **OAuth2 token refresh**: Tokens expire after 30 minutes -- refresh via `/oauth2/token`
