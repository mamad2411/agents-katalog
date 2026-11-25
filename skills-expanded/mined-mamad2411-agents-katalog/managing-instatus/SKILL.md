---
name: managing-instatus
description: |
  Use when working with Instatus — instatus status page management, component
  monitoring, incident communication, and subscriber notifications. Covers
  status page creation, component health tracking, incident updates, scheduled
  maintenance, and uptime reporting. Use when managing status pages,
  communicating incidents to users, tracking component uptime, or scheduling
  maintenance in Instatus.
connection_type: instatus
preload: false
---

# Instatus Management Skill

Manage and analyze status pages, incidents, components, and subscribers in Instatus.

## API Conventions

### Authentication
All API calls use the `Authorization: Bearer $INSTATUS_API_KEY` header. Never hardcode tokens.

### Base URL
`https://api.instatus.com/v2`

### Core Helper Function

```bash
#!/bin/bash

instatus_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $INSTATUS_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.instatus.com/v2${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $INSTATUS_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.instatus.com/v2${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Never dump full API responses

## Discovery Phase

### List Status Pages and Components

```bash
#!/bin/bash
echo "=== Status Pages ==="
instatus_api GET "/pages" \
    | jq -r '.[] | "\(.id)\t\(.name)\t\(.status)"' | column -t

echo ""
PAGE_ID="${1:?Page ID required}"
echo "=== Components ==="
instatus_api GET "/${PAGE_ID}/components" \
    | jq -r '.[] | "\(.status)\t\(.name)\t\(.group.name // "ungrouped")"' | column -t | head -20
```

### Active Incidents

```bash
#!/bin/bash
PAGE_ID="${1:?Page ID required}"

echo "=== Active Incidents ==="
instatus_api GET "/${PAGE_ID}/incidents?limit=20" \
    | jq -r '.[] | select(.resolved == false) | "\(.started[0:16])\t\(.impact)\t\(.name[0:60])"' \
    | column -t

echo ""
echo "=== Scheduled Maintenance ==="
instatus_api GET "/${PAGE_ID}/maintenances" \
    | jq -r '.[] | select(.status == "scheduled") | "\(.start[0:16])\t\(.end[0:16])\t\(.name[0:50])"' | column -t
```

## Analysis Phase

### Component Health

```bash
#!/bin/bash
PAGE_ID="${1:?Page ID required}"

echo "=== Component Status Summary ==="
instatus_api GET "/${PAGE_ID}/components" \
    | jq -r '.[] | .status' | sort | uniq -c | sort -rn

echo ""
echo "=== Components Not Operational ==="
instatus_api GET "/${PAGE_ID}/components" \
    | jq -r '.[] | select(.status != "OPERATIONAL") | "\(.status)\t\(.name)\t\(.updated_at[0:16])"' | column -t
```

### Incident Detail

```bash
#!/bin/bash
PAGE_ID="${1:?Page ID required}"
INCIDENT_ID="${2:?Incident ID required}"

echo "=== Incident Details ==="
instatus_api GET "/${PAGE_ID}/incidents/${INCIDENT_ID}" \
    | jq '{id, name, impact, status, started, resolved, resolved_at, affected: [.components[].name]}'

echo ""
echo "=== Incident Updates ==="
instatus_api GET "/${PAGE_ID}/incidents/${INCIDENT_ID}/updates" \
    | jq -r '.[] | "\(.created_at[0:16])\t\(.status)\t\(.body[0:80])"' | column -t
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
- **Page-scoped**: Most endpoints require the page ID in the path
- **Impact levels**: `OPERATIONAL`, `UNDERMAINTENANCE`, `DEGRADEDPERFORMANCE`, `PARTIALOUTAGE`, `MAJOROUTAGE`
- **Component groups**: Components can be nested in groups -- check group relationships
- **Subscriber types**: Email, webhook, Slack, and SMS subscribers
- **Pagination**: Use `limit` and `offset` parameters
