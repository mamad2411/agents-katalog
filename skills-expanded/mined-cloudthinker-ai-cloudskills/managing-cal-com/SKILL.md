---
name: managing-cal-com
description: |
  Use when working with Cal Com — cal.com open-source scheduling platform
  management covering event types, bookings, availability, teams, and analytics.
  Use when monitoring booking rates, analyzing event type usage, reviewing team
  availability, managing Cal.com schedules, or troubleshooting scheduling
  issues.
connection_type: cal-com
preload: false
---

# Cal.com Management Skill

Manage and analyze Cal.com scheduling resources including bookings, event types, and availability.

## API Conventions

### Authentication
All API calls use API key as query parameter or Bearer token, injected automatically.

### Base URL
`https://api.cal.com/v1` (cloud) or self-hosted instance URL

### Core Helper Function

```bash
#!/bin/bash

calcom_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Content-Type: application/json" \
            "${CALCOM_BASE_URL:-https://api.cal.com}/v1${endpoint}?apiKey=$CALCOM_API_KEY" \
            -d "$data"
    else
        curl -s -X "$method" \
            "${CALCOM_BASE_URL:-https://api.cal.com}/v1${endpoint}?apiKey=$CALCOM_API_KEY"
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
calcom_api GET "/me" | jq '{id: .user.id, name: .user.name, email: .user.email, timeZone: .user.timeZone}'

echo ""
echo "=== Event Types ==="
calcom_api GET "/event-types" \
    | jq -r '.event_types[] | "\(.id)\t\(.title[0:30])\t\(.length)min\t\(.slug)\t\(.hidden)"' \
    | column -t | head -15

echo ""
echo "=== Upcoming Bookings ==="
calcom_api GET "/bookings?status=upcoming" \
    | jq -r '.bookings[] | "\(.id)\t\(.title[0:30])\t\(.startTime[0:16])\t\(.status)\t\(.attendees[0].email // "?")"' \
    | column -t | head -15

echo ""
echo "=== Schedules (Availability) ==="
calcom_api GET "/schedules" \
    | jq -r '.schedules[] | "\(.id)\t\(.name)\t\(.timeZone)"' | head -10
```

## Phase 2: Analysis

### Booking Analytics

```bash
#!/bin/bash
echo "=== Booking Summary ==="
BOOKINGS=$(calcom_api GET "/bookings")
echo "$BOOKINGS" | jq '{
    total: (.bookings | length),
    by_status: (.bookings | group_by(.status) | map({(.[0].status): length}) | add)
}'

echo ""
echo "=== Bookings by Event Type ==="
echo "$BOOKINGS" | jq -r '.bookings[] | .title' | sort | uniq -c | sort -rn | head -10

echo ""
echo "=== Cancelled Bookings ==="
calcom_api GET "/bookings?status=cancelled" \
    | jq -r '.bookings[] | "\(.id)\t\(.title[0:30])\t\(.startTime[0:16])\t\(.cancellationReason[0:40] // "no reason")"' \
    | head -10

echo ""
echo "=== Bookings Per Day (recent) ==="
echo "$BOOKINGS" | jq -r '.bookings[] | .startTime[0:10]' | sort | uniq -c | sort -k2 | tail -7
```

### Availability & Team Health

```bash
#!/bin/bash
echo "=== Availability Schedules ==="
calcom_api GET "/schedules" \
    | jq -r '.schedules[] | "\(.name)\t\(.timeZone)\t\(.availability | length) slots"' | head -10

echo ""
echo "=== Teams ==="
calcom_api GET "/teams" \
    | jq -r '.teams[] | "\(.id)\t\(.name)\t\(.members | length) members"' | head -10

echo ""
echo "=== Hidden/Disabled Event Types ==="
calcom_api GET "/event-types" \
    | jq -r '.event_types[] | select(.hidden == true) | "\(.id)\t\(.title[0:30])\t\(.length)min"' | head -10
```

## Output Format

```
=== Cal.com User: <name> (<email>) ===

--- Event Types ---
Active: <n>  Hidden: <n>

--- Bookings ---
Total: <n>  Upcoming: <n>  Cancelled: <n>
By Type: <event_type>: <n>

--- Availability ---
Schedules: <n>  Timezone: <tz>
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
- **API key as query param**: Cal.com v1 uses `?apiKey=` not header-based auth
- **Self-hosted**: Ensure correct base URL for self-hosted instances
- **Booking statuses**: `upcoming`, `past`, `cancelled`, `recurring`
- **Rate limits**: 100 requests/minute for cloud; varies for self-hosted
- **Pagination**: Use `limit` and `page` parameters; no cursor pagination
