---
name: managing-opsgenie
description: |
  Use when working with Opsgenie — opsGenie alert management, on-call schedule
  queries, escalation policy configuration, integration management, and incident
  response. Covers alert lifecycle, team management, routing rules, maintenance
  windows, and notification policies. Use when managing alerts, reviewing
  on-call schedules, configuring escalations, or analyzing incident response via
  OpsGenie API.
connection_type: opsgenie
preload: false
---

# OpsGenie Management Skill

Manage alerts, on-call schedules, and escalation policies using the OpsGenie API.

## API Conventions

### Authentication
OpsGenie API uses `GenieKey` authorization header — injected by connection. Never hardcode keys.

### Base URL
- US: `https://api.opsgenie.com/v2/`
- EU: `https://api.eu.opsgenie.com/v2/`
- Use connection-injected `OPSGENIE_BASE_URL`.

### Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `jq` to extract alert and schedule fields
- NEVER dump full alert payloads — extract key fields only

### Core Helper Function

```bash
#!/bin/bash

opsgenie_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: GenieKey ${OPSGENIE_API_KEY}" \
            -H "Content-Type: application/json" \
            "${OPSGENIE_BASE_URL}/v2${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: GenieKey ${OPSGENIE_API_KEY}" \
            "${OPSGENIE_BASE_URL}/v2${endpoint}"
    fi
}
```

## Parallel Execution

```bash
{
    opsgenie_api GET "/alerts?limit=20&order=desc&sort=createdAt" &
    opsgenie_api GET "/schedules" &
    opsgenie_api GET "/teams" &
}
wait
```

## Anti-Hallucination Rules

**NEVER assume alert IDs, schedule names, team names, or integration IDs. ALWAYS discover first.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Teams ==="
opsgenie_api GET "/teams" | jq -r '.data[] | "\(.id)\t\(.name)"' | head -15

echo ""
echo "=== Schedules ==="
opsgenie_api GET "/schedules" | jq -r '.data[] | "\(.id)\t\(.name)\t\(.enabled)"' | head -15

echo ""
echo "=== Escalation Policies ==="
opsgenie_api GET "/escalations" | jq -r '.data[] | "\(.id)\t\(.name)"' | head -15

echo ""
echo "=== Integrations ==="
opsgenie_api GET "/integrations" | jq -r '.data[] | "\(.id)\t\(.type)\t\(.name)\t\(.enabled)"' | head -15
```

## Common Operations

### Alert Management

```bash
#!/bin/bash
echo "=== Open Alerts ==="
opsgenie_api GET "/alerts?limit=20&order=desc&sort=createdAt&query=status%3Aopen" \
    | jq -r '.data[] | "\(.tinyId)\t\(.priority)\t\(.status)\t\(.createdAt[0:16])\t\(.message[0:60])"' | head -20

echo ""
echo "=== Alert Count by Priority ==="
for priority in P1 P2 P3 P4 P5; do
    count=$(opsgenie_api GET "/alerts/count?query=status%3Aopen%20AND%20priority%3A${priority}" \
        | jq '.data.count')
    echo "$priority: $count"
done

echo ""
echo "=== Unacknowledged Alerts ==="
opsgenie_api GET "/alerts?limit=10&query=status%3Aopen%20AND%20acknowledged%3Afalse&order=desc" \
    | jq -r '.data[] | "\(.tinyId)\t\(.priority)\t\(.message[0:60])"'
```

### On-Call Schedules

```bash
#!/bin/bash
echo "=== Current On-Call ==="
SCHEDULES=$(opsgenie_api GET "/schedules" | jq -r '.data[].id')

for schedule_id in $SCHEDULES; do
    {
        name=$(opsgenie_api GET "/schedules/${schedule_id}" | jq -r '.data.name')
        oncall=$(opsgenie_api GET "/schedules/${schedule_id}/on-calls" \
            | jq -r '.data.onCallParticipants[] | .name' 2>/dev/null | head -3 | tr '\n' ', ')
        echo "$name: ${oncall%,}"
    } &
done
wait

echo ""
echo "=== Schedule Timeline (next 7 days) ==="
FROM=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TO=$(date -u -d '7 days' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v+7d +%Y-%m-%dT%H:%M:%SZ)

SCHEDULE_ID="${1:-}"
if [ -n "$SCHEDULE_ID" ]; then
    opsgenie_api GET "/schedules/${SCHEDULE_ID}/timeline?interval=7&intervalUnit=days" \
        | jq -r '.data.finalTimeline.rotations[].periods[] | "\(.startDate[0:16])\t\(.endDate[0:16])\t\(.recipient.name)"' | head -15
fi
```

### Escalation Policies

```bash
#!/bin/bash
echo "=== Escalation Policies ==="
opsgenie_api GET "/escalations" \
    | jq -r '.data[] | "\(.name)\trules:\(.rules | length)"'

echo ""
echo "=== Policy Details ==="
opsgenie_api GET "/escalations" \
    | jq -r '.data[] | "\(.name):", (.rules[] | "  Step \(.delay.timeAmount)m: \(.recipient.type)=\(.recipient.name // .recipient.id)")'
```

### Integration Management

```bash
#!/bin/bash
echo "=== Active Integrations ==="
opsgenie_api GET "/integrations" \
    | jq -r '.data[] | select(.enabled == true) | "\(.type)\t\(.name)\t\(.id)"' | head -20

echo ""
echo "=== Disabled Integrations ==="
opsgenie_api GET "/integrations" \
    | jq -r '.data[] | select(.enabled == false) | "\(.type)\t\(.name)\t\(.id)"' | head -10

echo ""
echo "=== Integration Types ==="
opsgenie_api GET "/integrations" \
    | jq -r '[.data[].type] | group_by(.) | map("\(.[0]): \(length)") | .[]'
```

### Team & Routing Management

```bash
#!/bin/bash
echo "=== Teams & Members ==="
TEAMS=$(opsgenie_api GET "/teams")
echo "$TEAMS" | jq -r '.data[] | "\(.name)\tmembers:\(.members | length)"'

echo ""
echo "=== Routing Rules ==="
TEAM_ID="${1:-}"
if [ -n "$TEAM_ID" ]; then
    opsgenie_api GET "/teams/${TEAM_ID}/routing-rules" \
        | jq -r '.data[] | "\(.name)\torder:\(.order)\t\(.criteria.type // "match-all")"' | head -10
fi

echo ""
echo "=== Maintenance Windows ==="
opsgenie_api GET "/maintenance" \
    | jq -r '.data[] | "\(.id)\t\(.status)\t\(.description[0:50])"' | head -10
```

## Output Format

Present results as a structured report:
```
Managing Opsgenie Report
════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Query encoding**: Alert queries use URL-encoded OpsGenie Query Language — `status%3Aopen%20AND%20priority%3AP1`
- **Priority format**: `P1` (critical) through `P5` (informational) — uppercase P required
- **GenieKey header**: Use `Authorization: GenieKey <key>` — NOT Bearer or Basic auth
- **Rate limits**: 3000 requests/min for paid plans — stagger parallel calls for bulk operations
- **Alert tiny ID vs ID**: Use `tinyId` for human-readable reference, `id` (UUID) for API calls
- **Pagination**: Use `offset` parameter — default limit is 20, max 100 per page
- **Time format**: ISO 8601 with timezone — `2024-01-15T10:00:00Z`
- **EU vs US**: Different base URLs — EU data residency requires `api.eu.opsgenie.com`
