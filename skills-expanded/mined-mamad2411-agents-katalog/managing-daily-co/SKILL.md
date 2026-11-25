---
name: managing-daily-co
description: |
  Use when working with Daily Co — daily.co video and audio API platform
  management for real-time video calls, rooms, recordings, and usage analytics.
  Use when monitoring active rooms, analyzing meeting quality, reviewing usage
  and billing, managing room configurations, or troubleshooting Daily.co video
  sessions.
connection_type: daily-co
preload: false
---

# Daily.co Management Skill

Manage and analyze Daily.co video/audio rooms, meetings, recordings, and usage.

## API Conventions

### Authentication
All API calls use Bearer token authentication, injected automatically.

### Base URL
`https://api.daily.co/v1`

### Core Helper Function

```bash
#!/bin/bash

daily_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $DAILY_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.daily.co/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $DAILY_API_KEY" \
            "https://api.daily.co/v1${endpoint}"
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
echo "=== Domain Info ==="
daily_api GET "/" | jq '{domain_name: .domain_name, config: .config}'

echo ""
echo "=== Rooms ==="
daily_api GET "/rooms?limit=30" \
    | jq -r '.data[] | "\(.name)\t\(.privacy)\t\(.created_at[0:10])\tmax_participants:\(.config.max_participants // "unlimited")"' \
    | column -t | head -20

echo ""
echo "=== Active Meetings ==="
daily_api GET "/meetings?active=true&limit=20" \
    | jq -r '.data[] | "\(.room)\t\(.ongoing)\tparticipants:\(.max_participants)\tstarted:\(.start_time[0:16])"' \
    | head -15
```

## Phase 2: Analysis

### Meeting Analytics

```bash
#!/bin/bash
echo "=== Meeting Summary (last 7 days) ==="
daily_api GET "/meetings?timeframe_start=$(date -d '7 days ago' +%s)&timeframe_end=$(date +%s)&limit=100" \
    | jq '{
        total_meetings: (.data | length),
        avg_duration_min: (.data | map(.duration // 0) | if length > 0 then add / length / 60 | floor else 0 end),
        avg_participants: (.data | map(.max_participants // 0) | if length > 0 then add / length | floor else 0 end)
    }'

echo ""
echo "=== Room Usage Breakdown ==="
daily_api GET "/meetings?timeframe_start=$(date -d '7 days ago' +%s)&timeframe_end=$(date +%s)&limit=200" \
    | jq -r '.data[] | .room' | sort | uniq -c | sort -rn | head -15

echo ""
echo "=== Active Recordings ==="
daily_api GET "/recordings?limit=20" \
    | jq -r '.data[] | "\(.room_name)\t\(.duration)s\t\(.status)\t\(.start_ts[0:16])"' \
    | head -15
```

### Room Health

```bash
#!/bin/bash
echo "=== Room Configurations ==="
daily_api GET "/rooms?limit=50" \
    | jq -r '.data[] | "\(.name)\t\(.privacy)\teject_at_room_exp:\(.config.eject_at_room_exp // false)\trecording:\(.config.enable_recording // "none")"' \
    | column -t | head -20

echo ""
echo "=== Rooms Without Expiry ==="
daily_api GET "/rooms?limit=100" \
    | jq -r '.data[] | select(.config.exp == null or .config.exp == 0) | "\(.name)\t\(.privacy)\tcreated:\(.created_at[0:10])"' \
    | head -10
```

## Output Format

```
=== Domain: <domain_name> ===
Rooms: <count>  Active Meetings: <count>

--- Meeting Analytics (7d) ---
Total: <n>  Avg Duration: <n>min  Avg Participants: <n>

--- Room Usage ---
<room_name>: <n> meetings

--- Recordings ---
Total: <n>  Pending: <n>
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
- **Timestamps**: Use Unix epoch seconds for timeframe filters
- **Pagination**: Use `limit` and `starting_after` cursor; default limit is 50
- **Rate limits**: 300 requests/minute for most endpoints
- **Room names**: Must be lowercase, alphanumeric with hyphens only
