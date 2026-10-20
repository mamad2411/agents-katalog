---
name: managing-calendly
description: |
  Use when working with Calendly — calendly scheduling platform management
  covering event types, scheduled events, invitees, users, and booking
  analytics. Use when monitoring booking rates, analyzing event type
  performance, reviewing upcoming schedules, managing Calendly users and teams,
  or troubleshooting scheduling workflows.
connection_type: calendly
preload: false
---

# Calendly Management Skill

Manage and analyze Calendly scheduling resources including events, event types, and booking analytics.

## API Conventions

### Authentication
All API calls use Bearer personal access token or OAuth token, injected automatically.

### Base URL
`https://api.calendly.com`

### Core Helper Function

```bash
#!/bin/bash

calendly_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $CALENDLY_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.calendly.com${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $CALENDLY_ACCESS_TOKEN" \
            "https://api.calendly.com${endpoint}"
    fi
}
```

## Output Rules
- Target ≤50 lines per script output
- Use `jq` to extract only needed fields
- Never dump full API responses

## Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Current User ==="
USER=$(calendly_api GET "/users/me")
echo "$USER" | jq '{name: .resource.name, email: .resource.email, timezone: .resource.timezone, organization: .resource.current_organization}'
ORG_URI=$(echo "$USER" | jq -r '.resource.current_organization')
USER_URI=$(echo "$USER" | jq -r '.resource.uri')

echo ""
echo "=== Event Types ==="
calendly_api GET "/event_types?user=$USER_URI&count=20" \
    | jq -r '.collection[] | "\(.name[0:30])\t\(.active)\t\(.duration_minutes)min\t\(.kind)\t\(.type)"' \
    | column -t | head -15

echo ""
echo "=== Upcoming Events ==="
calendly_api GET "/scheduled_events?user=$USER_URI&min_start_time=$(date -u +%Y-%m-%dT%H:%M:%SZ)&count=20&status=active" \
    | jq -r '.collection[] | "\(.start_time[0:16])\t\(.name[0:30])\t\(.status)\t\(.event_memberships | length) hosts"' \
    | column -t | head -15
```

## Phase 2: Analysis

### Booking Analytics

```bash
#!/bin/bash
USER_URI=$(calendly_api GET "/users/me" | jq -r '.resource.uri')

echo "=== Event Summary (last 30 days) ==="
calendly_api GET "/scheduled_events?user=$USER_URI&min_start_time=$(date -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)&max_start_time=$(date -u +%Y-%m-%dT%H:%M:%SZ)&count=100" \
    | jq '{
        total_events: (.collection | length),
        by_status: (.collection | group_by(.status) | map({(.[0].status): length}) | add),
        by_type: (.collection | group_by(.name) | map({(.[0].name): length}) | add)
    }'

echo ""
echo "=== Cancelled Events ==="
calendly_api GET "/scheduled_events?user=$USER_URI&status=canceled&min_start_time=$(date -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)&count=20" \
    | jq -r '.collection[] | "\(.start_time[0:16])\t\(.name[0:30])\t\(.cancellation.reason[0:40] // "no reason")"' \
    | head -10

echo ""
echo "=== Events Per Day (last 7 days) ==="
calendly_api GET "/scheduled_events?user=$USER_URI&min_start_time=$(date -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)&max_start_time=$(date -u +%Y-%m-%dT%H:%M:%SZ)&count=100" \
    | jq -r '.collection[] | .start_time[0:10]' | sort | uniq -c | sort -k2
```

### Event Type Health

```bash
#!/bin/bash
USER_URI=$(calendly_api GET "/users/me" | jq -r '.resource.uri')

echo "=== Active Event Types ==="
calendly_api GET "/event_types?user=$USER_URI&active=true&count=20" \
    | jq -r '.collection[] | "\(.name[0:30])\t\(.duration_minutes)min\t\(.slug)\t\(.scheduling_url[0:40])"' \
    | column -t | head -15

echo ""
echo "=== Inactive Event Types ==="
calendly_api GET "/event_types?user=$USER_URI&active=false&count=20" \
    | jq -r '.collection[] | "\(.name[0:30])\t\(.duration_minutes)min"' | head -10
```

## Output Format

```
=== User: <name> (<email>) ===
Timezone: <tz>

--- Event Types ---
Active: <n>  Inactive: <n>

--- Bookings (30d) ---
Total: <n>  Active: <n>  Cancelled: <n>
By Type: <event_type>: <n>

--- Upcoming ---
<date>  <event_name>  <status>
```

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
- **URI-based references**: Calendly uses full URIs (not IDs) for user, org, and event references
- **Pagination**: Use `count` and `page_token`; check `pagination.next_page_token`
- **Date format**: ISO 8601 with timezone for all date parameters
- **Rate limits**: 50 requests/15 seconds per user
- **Organization scope**: Some endpoints require organization URI, not just user URI
