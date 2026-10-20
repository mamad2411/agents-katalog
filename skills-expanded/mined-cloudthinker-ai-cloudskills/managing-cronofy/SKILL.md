---
name: managing-cronofy
description: |
  Use when working with Cronofy — cronofy calendar API platform management
  covering calendars, events, availability, scheduling, and account sync health.
  Use when monitoring calendar integrations, analyzing scheduling patterns,
  reviewing availability rules, managing connected accounts, or troubleshooting
  Cronofy calendar sync issues.
connection_type: cronofy
preload: false
---

# Cronofy Management Skill

Manage and analyze Cronofy calendar API resources including calendars, events, and scheduling.

## API Conventions

### Authentication
All API calls use Bearer OAuth access token, injected automatically.

### Base URL
`https://api.cronofy.com/v1`

### Core Helper Function

```bash
#!/bin/bash

cronofy_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $CRONOFY_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.cronofy.com/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $CRONOFY_ACCESS_TOKEN" \
            "https://api.cronofy.com/v1${endpoint}"
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
echo "=== Account Info ==="
cronofy_api GET "/account" \
    | jq '{account_id: .account.account_id, email: .account.email, scope: .account.scope}'

echo ""
echo "=== Calendars ==="
cronofy_api GET "/calendars" \
    | jq -r '.calendars[] | "\(.calendar_id[0:16])\t\(.calendar_name[0:30])\t\(.provider_name)\t\(.calendar_primary)\t\(.calendar_readonly)"' \
    | column -t | head -15

echo ""
echo "=== Upcoming Events ==="
cronofy_api GET "/events?from=$(date +%Y-%m-%d)&to=$(date -d '7 days' +%Y-%m-%d)&tzid=Etc/UTC" \
    | jq -r '.events[] | "\(.start.date // .start.time[0:16])\t\(.summary[0:30])\t\(.event_status)\t\(.attendees | length // 0) attendees"' \
    | head -15

echo ""
echo "=== Linked Profiles ==="
cronofy_api GET "/profiles" \
    | jq -r '.profiles[] | "\(.profile_id[0:16])\t\(.profile_name)\t\(.provider_name)\t\(.profile_connected)"' \
    | head -10
```

## Phase 2: Analysis

### Calendar Health

```bash
#!/bin/bash
echo "=== Event Summary (next 7 days) ==="
cronofy_api GET "/events?from=$(date +%Y-%m-%d)&to=$(date -d '7 days' +%Y-%m-%d)&tzid=Etc/UTC" \
    | jq '{
        total_events: (.events | length),
        by_status: (.events | group_by(.event_status) | map({(.[0].event_status): length}) | add),
        all_day: [.events[] | select(.start.date != null)] | length
    }'

echo ""
echo "=== Events Per Day ==="
cronofy_api GET "/events?from=$(date +%Y-%m-%d)&to=$(date -d '7 days' +%Y-%m-%d)&tzid=Etc/UTC" \
    | jq -r '.events[] | (.start.date // .start.time[0:10])' | sort | uniq -c | sort -k2

echo ""
echo "=== Free/Busy Overview ==="
cronofy_api POST "/free_busy" "{\"required_duration\": {\"minutes\": 30}, \"available_periods\": [{\"start\": \"$(date +%Y-%m-%dT%H:%M:%SZ)\", \"end\": \"$(date -d '1 day' +%Y-%m-%dT%H:%M:%SZ)\"}], \"participants\": [{\"members\": [{\"sub\": \"acc_id\"}], \"required\": \"all\"}]}" \
    | jq '{available_slots: (.available_periods | length)}' 2>/dev/null || echo "Free/busy: use availability endpoint for slot queries"
```

### Profile Sync Health

```bash
#!/bin/bash
echo "=== Profile Connection Status ==="
cronofy_api GET "/profiles" \
    | jq -r '.profiles[] | "\(.profile_name)\t\(.provider_name)\tconnected:\(.profile_connected)"' | head -10

echo ""
echo "=== Calendar Sync Summary ==="
cronofy_api GET "/calendars" \
    | jq '{
        total_calendars: (.calendars | length),
        by_provider: (.calendars | group_by(.provider_name) | map({(.[0].provider_name): length}) | add),
        primary: [.calendars[] | select(.calendar_primary == true)] | length,
        readonly: [.calendars[] | select(.calendar_readonly == true)] | length
    }'

echo ""
echo "=== Calendar Permissions ==="
cronofy_api GET "/calendars" \
    | jq -r '.calendars[] | "\(.calendar_name[0:25])\tprimary:\(.calendar_primary)\treadonly:\(.calendar_readonly)\tdeleted:\(.calendar_deleted)"' \
    | head -15
```

## Output Format

```
=== Account: <email> ===
Profiles: <n>  Calendars: <n>

--- Events (7d) ---
Total: <n>  Confirmed: <n>  Tentative: <n>
All-Day: <n>

--- Calendar Sync ---
By Provider: Google: <n>, Microsoft: <n>
Primary: <n>  Read-Only: <n>
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
- **Date format**: Use `YYYY-MM-DD` for date-only events, ISO 8601 for timed events
- **Timezone**: Always specify `tzid` parameter for event queries
- **Event status**: `confirmed`, `tentative`, `cancelled`
- **Rate limits**: 30 requests/minute per access token
- **Pagination**: Events endpoint uses `pages.next_page` for cursor pagination
