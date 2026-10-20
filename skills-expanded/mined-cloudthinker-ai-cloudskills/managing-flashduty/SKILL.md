---
name: managing-flashduty
description: |
  Use when working with Flashduty — flashDuty alerting and incident management
  covering alert routing, escalation policy configuration, on-call scheduling,
  collaboration channels, duty management, and integration setup. Use when
  configuring FlashDuty alert escalations, managing on-call rotations, setting
  up collaboration workflows, or reviewing incident resolution metrics.
connection_type: flashduty
preload: false
---

# FlashDuty Management Skill

Manage FlashDuty alerting, escalation policies, on-call schedules, and collaboration workflows.

## API Conventions

### Authentication
All API calls use the `Authorization: Bearer XXXXXX` header — injected automatically. Never hardcode tokens.

### Base URL
`https://api.flashcat.cloud`

### Core Helper Function

```bash
#!/bin/bash

fd_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $FLASHDUTY_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.flashcat.cloud${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $FLASHDUTY_API_KEY" \
            "https://api.flashcat.cloud${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target ≤50 lines per script output

## Alert Management

### List Active Alerts
```bash
fd_api GET "/v1/alerts?status=firing&limit=50" | jq '[.data[] | {
  id, title, severity, status,
  source, service, createdAt,
  assignee, escalationPolicy
}]'
```

### Get Alert Details
```bash
fd_api GET "/v1/alerts/ALERT_ID" | jq '{
  title, severity, status, description,
  labels, annotations,
  timeline: [.events[] | {type, timestamp, actor}]
}'
```

## Escalation Policies

### List Escalation Policies
```bash
fd_api GET "/v1/escalation-policies" | jq '[.data[] | {
  id, name, description,
  steps: [.steps[] | {delayMinutes: .delay, targets: [.targets[] | .name]}]
}]'
```

### Create Escalation Policy
```bash
fd_api POST "/v1/escalation-policies" '{
  "name": "Critical Service Escalation",
  "steps": [
    {"delay": 0, "targets": [{"type": "schedule", "id": "SCHEDULE_ID"}]},
    {"delay": 15, "targets": [{"type": "user", "id": "MANAGER_ID"}]}
  ]
}'
```

## On-Call Schedules

### List Schedules
```bash
fd_api GET "/v1/schedules" | jq '[.data[] | {id, name, timezone, currentOnCall: .currentShift.user}]'
```

### Get Schedule Details
```bash
fd_api GET "/v1/schedules/SCHEDULE_ID" | jq '{
  name, timezone,
  rotations: [.layers[] | {name, rotationType, handoffTime, users: [.users[] | .name]}],
  currentOnCall: .currentShift
}'
```

## Collaboration

### List Channels
```bash
fd_api GET "/v1/channels" | jq '[.data[] | {id, name, type, integration, enabled}]'
```

## Duty Management

### Get Current On-Duty Users
```bash
fd_api GET "/v1/duties/current" | jq '[.data[] | {
  team, schedule: .scheduleName,
  user: .onDutyUser, startTime, endTime
}]'
```

## Common Tasks

1. **Configure escalation chains** — set up multi-step escalation with appropriate delays
2. **Manage on-call rotations** — create and adjust rotation schedules across teams
3. **Set up alert routing** — connect monitoring tools and route by severity and service
4. **Review duty coverage** — verify all time slots have assigned on-call personnel
5. **Analyze response times** — track alert acknowledgment and resolution metrics

## Output Format

Present results as a structured report:
```
Managing Flashduty Report
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

