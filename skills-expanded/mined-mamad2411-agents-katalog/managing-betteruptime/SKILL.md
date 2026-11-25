---
name: managing-betteruptime
description: |
  Use when working with Betteruptime — better Uptime monitoring, status pages,
  incident management, on-call scheduling, and heartbeat tracking. Covers
  monitor configuration, response time analysis, incident lifecycle, on-call
  rotations, and SLA reporting. Use when managing uptime monitors, reviewing
  incident history, configuring on-call schedules, or analyzing response times
  in Better Uptime.
connection_type: betteruptime
preload: false
---

# Better Uptime Management Skill

Manage and analyze monitors, incidents, status pages, and on-call schedules in Better Uptime.

## API Conventions

### Authentication
All API calls use the `Authorization: Bearer $BETTERUPTIME_API_KEY` header. Never hardcode tokens.

### Base URL
`https://betteruptime.com/api/v2`

### Core Helper Function

```bash
#!/bin/bash

bu_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $BETTERUPTIME_API_KEY" \
            -H "Content-Type: application/json" \
            "https://betteruptime.com/api/v2${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $BETTERUPTIME_API_KEY" \
            -H "Content-Type: application/json" \
            "https://betteruptime.com/api/v2${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Never dump full API responses

## Discovery Phase

### List Monitors

```bash
#!/bin/bash
echo "=== Monitors ==="
bu_api GET "/monitors?per_page=25" \
    | jq -r '.data[] | "\(.attributes.status)\t\(.attributes.monitor_type)\t\(.attributes.url[0:50])\t\(.attributes.pronounceable_name)"' \
    | column -t

echo ""
echo "=== Monitor Status Summary ==="
bu_api GET "/monitors?per_page=100" \
    | jq -r '.data[] | .attributes.status' | sort | uniq -c | sort -rn
```

### Active Incidents

```bash
#!/bin/bash
echo "=== Active Incidents ==="
bu_api GET "/incidents?per_page=20" \
    | jq -r '.data[] | select(.attributes.resolved_at == null) | "\(.attributes.started_at[0:16])\t\(.attributes.call)\t\(.attributes.name[0:60])"' \
    | column -t

echo ""
echo "=== On-Call Now ==="
bu_api GET "/on-call-calendars" \
    | jq -r '.data[] | "\(.attributes.name)\t\(.attributes.current_on_call.name // "nobody")"' | column -t
```

## Analysis Phase

### Monitor Performance

```bash
#!/bin/bash
echo "=== Monitors Down ==="
bu_api GET "/monitors?per_page=50" \
    | jq -r '.data[] | select(.attributes.status == "down") | "\(.attributes.pronounceable_name)\t\(.attributes.url[0:40])\tdown since \(.attributes.last_checked_at[0:16])"' \
    | column -t

echo ""
echo "=== Response Times (slowest) ==="
bu_api GET "/monitors?per_page=50" \
    | jq -r '.data[] | select(.attributes.status == "up") | "\(.attributes.pronounceable_name)\t\(.attributes.response_time_ms // 0)ms"' \
    | sort -t$'\t' -k2 -rn | head -10
```

### Incident History

```bash
#!/bin/bash
echo "=== Recent Incidents ==="
bu_api GET "/incidents?per_page=25" \
    | jq -r '.data[] | "\(.attributes.started_at[0:16])\t\(.attributes.resolved_at[0:16] // "ongoing")\t\(.attributes.name[0:50])"' \
    | column -t

echo ""
echo "=== Incident Duration Stats ==="
bu_api GET "/incidents?per_page=50" \
    | jq '[.data[] | select(.attributes.resolved_at != null) | ((.attributes.resolved_at | fromdateiso8601) - (.attributes.started_at | fromdateiso8601)) / 60] | {avg_minutes: (add / length | . * 10 | round / 10), count: length}'
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
- **JSON:API format**: Responses use `data[].attributes` structure
- **Monitor types**: `status`, `expected_status_code`, `keyword`, `keyword_absence`, `ping`, `tcp`, `udp`, `smtp`, `pop`, `imap`
- **Pagination**: Use `per_page` and check `pagination.next` URL for more pages
- **Heartbeats**: Separate endpoint `/heartbeats` for cron job and service health checks
- **Rate limits**: 200 requests per minute
