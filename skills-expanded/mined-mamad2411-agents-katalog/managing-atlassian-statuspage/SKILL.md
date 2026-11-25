---
name: managing-atlassian-statuspage
description: |
  Use when working with Atlassian Statuspage — atlassian Statuspage management,
  component monitoring, incident communication, scheduled maintenance, and
  subscriber notifications. Covers page configuration, component group
  management, incident lifecycle, metric tracking, and uptime reporting. Use
  when managing public or private status pages, communicating outages,
  scheduling maintenance, or reviewing component uptime in Atlassian Statuspage.
connection_type: atlassian-statuspage
preload: false
---

# Atlassian Statuspage Management Skill

Manage and analyze status pages, components, incidents, and maintenance in Atlassian Statuspage.

## API Conventions

### Authentication
All API calls use the `Authorization: OAuth $STATUSPAGE_API_KEY` header. Never hardcode tokens.

### Base URL
`https://api.statuspage.io/v1`

### Core Helper Function

```bash
#!/bin/bash

sp_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.statuspage.io/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.statuspage.io/v1${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Never dump full API responses

## Discovery Phase

### List Pages and Components

```bash
#!/bin/bash
echo "=== Status Pages ==="
sp_api GET "/pages" \
    | jq -r '.[] | "\(.id)\t\(.name)\t\(.status_indicator)"' | column -t

PAGE_ID="${1:?Page ID required}"
echo ""
echo "=== Components ==="
sp_api GET "/pages/${PAGE_ID}/components" \
    | jq -r '.[] | "\(.status)\t\(.name)\t\(.group_id // "ungrouped")"' | column -t | head -25
```

### Active Incidents

```bash
#!/bin/bash
PAGE_ID="${1:?Page ID required}"

echo "=== Unresolved Incidents ==="
sp_api GET "/pages/${PAGE_ID}/incidents/unresolved" \
    | jq -r '.[] | "\(.created_at[0:16])\t\(.impact)\t\(.status)\t\(.name[0:60])"' | column -t

echo ""
echo "=== Upcoming Maintenance ==="
sp_api GET "/pages/${PAGE_ID}/incidents/upcoming" \
    | jq -r '.[] | "\(.scheduled_for[0:16])\t\(.scheduled_until[0:16])\t\(.name[0:50])"' | column -t
```

## Analysis Phase

### Component Health

```bash
#!/bin/bash
PAGE_ID="${1:?Page ID required}"

echo "=== Component Status Summary ==="
sp_api GET "/pages/${PAGE_ID}/components" \
    | jq -r '.[] | .status' | sort | uniq -c | sort -rn

echo ""
echo "=== Components Not Operational ==="
sp_api GET "/pages/${PAGE_ID}/components" \
    | jq -r '.[] | select(.status != "operational") | "\(.status)\t\(.name)\t\(.updated_at[0:16])"' | column -t

echo ""
echo "=== Component Groups ==="
sp_api GET "/pages/${PAGE_ID}/component-groups" \
    | jq -r '.[] | "\(.name)\t\(.components | length) components"' | column -t
```

### Incident Detail

```bash
#!/bin/bash
PAGE_ID="${1:?Page ID required}"
INCIDENT_ID="${2:?Incident ID required}"

echo "=== Incident Details ==="
sp_api GET "/pages/${PAGE_ID}/incidents/${INCIDENT_ID}" \
    | jq '{id, name, impact, status, created_at, resolved_at, shortlink, affected: [.components[].name]}'

echo ""
echo "=== Incident Updates ==="
sp_api GET "/pages/${PAGE_ID}/incidents/${INCIDENT_ID}" \
    | jq -r '.incident_updates[] | "\(.created_at[0:16])\t\(.status)\t\(.body[0:80])"' | column -t
```

## Output Format
- Use tab-separated columns with `column -t`
- Limit lists to 15-25 items
- Show summaries before details

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
- **Page-scoped**: All component and incident endpoints require the page ID
- **Component statuses**: `operational`, `degraded_performance`, `partial_outage`, `major_outage`, `under_maintenance`
- **Incident statuses**: `investigating`, `identified`, `monitoring`, `resolved`, `postmortem`
- **Impact levels**: `none`, `minor`, `major`, `critical`
- **Unresolved vs all**: Use `/incidents/unresolved` for active incidents, `/incidents` for all
- **Rate limits**: 60 requests per minute per API key
- **Subscriber count**: Check `/pages/{page_id}/subscribers/count` instead of listing all subscribers
