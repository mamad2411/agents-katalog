---
name: managing-opsgenie-deep
description: |
  Use when working with Opsgenie Deep — advanced OpsGenie management covering
  routing rules, integration configurations, on-call analytics, alert policy
  tuning, notification rules, team structures, and escalation optimization. Use
  when performing deep OpsGenie configuration, analyzing on-call workload
  distribution, tuning alert noise reduction, or building sophisticated routing
  workflows.
connection_type: opsgenie
preload: false
---

# OpsGenie Advanced Management Skill

Deep management of OpsGenie routing rules, integrations, on-call analytics, and alert policies.

## API Conventions

### Authentication
All API calls use the `Authorization: GenieKey XXXXXX` header — injected automatically. Never hardcode tokens.

### Base URL
`https://api.opsgenie.com`

### Core Helper Function

```bash
#!/bin/bash

og_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: GenieKey $OPSGENIE_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.opsgenie.com${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: GenieKey $OPSGENIE_API_KEY" \
            "https://api.opsgenie.com${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target ≤50 lines per script output
- Always filter by relevant time range to avoid huge response sets

## Routing Rules Management

### List Team Routing Rules
```bash
og_api GET "/v2/teams/TEAM_ID/routing-rules" | jq '[.data[] | {
  id, name, order,
  timezone,
  criteria: .criteria,
  notify: .notify
}]'
```

### Create a Routing Rule
```bash
og_api POST "/v2/teams/TEAM_ID/routing-rules" '{
  "name": "High Priority to Primary",
  "order": 0,
  "criteria": {
    "type": "match-all-conditions",
    "conditions": [{"field": "priority", "operation": "equals", "expectedValue": "P1"}]
  },
  "notify": {"type": "escalation", "id": "ESCALATION_ID"}
}'
```

## Integration Management

### List All Integrations
```bash
og_api GET "/v2/integrations" | jq '[.data[] | {id, name, type, enabled, teamId: .ownerTeam.id}]'
```

### Get Integration Details
```bash
og_api GET "/v2/integrations/INTEGRATION_ID" | jq '.data | {name, type, enabled, allowConfigurationAccess, suppressNotifications}'
```

## On-Call Analytics

### Get On-Call Schedule Timeline
```bash
og_api GET "/v2/schedules/SCHEDULE_ID/timeline?interval=1&intervalUnit=months" | jq '.data | {
  schedule: .name,
  rotations: [.finalTimeline.rotations[] | {
    name,
    periods: [.periods[] | {user: .recipient.name, start: .startDate, end: .endDate}]
  }]
}'
```

### Who Is Currently On-Call
```bash
og_api GET "/v2/schedules/SCHEDULE_ID/on-calls" | jq '.data | {
  parent: .parent.name,
  onCallParticipants: [.onCallParticipants[] | {name, type}]
}'
```

## Alert Policy Management

### List Alert Policies
```bash
og_api GET "/v2/policies/alert" | jq '[.data[] | {id, name, type, enabled, order}]'
```

### Analyze Alert Volume by Team
```bash
og_api GET "/v2/alerts?limit=100&sort=createdAt&order=desc" | jq '
  [.data[] | {team: .ownerTeamId, priority: .priority, status: .status}]
  | group_by(.team) | map({team: .[0].team, count: length, priorities: (group_by(.priority) | map({(.[0].priority): length}) | add)})
'
```

## Notification Rules

### List User Notification Rules
```bash
og_api GET "/v2/users/USER_ID/notification-rules" | jq '[.data[] | {
  id, name, actionType, enabled,
  steps: [.steps[] | {contact: .contact, sendAfter: .sendAfter}]
}]'
```

## Common Tasks

1. **Audit routing rules** — verify all teams have proper routing for P1-P5 priorities
2. **Analyze on-call burden** — check schedule coverage and rotation fairness
3. **Tune alert policies** — adjust deduplication, suppression, and auto-close rules
4. **Review integrations** — ensure all monitoring tools are properly connected
5. **Optimize notification rules** — configure escalating notification channels per severity

## Output Format

Present results as a structured report:
```
Managing Opsgenie Deep Report
═════════════════════════════
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

