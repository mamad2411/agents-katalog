---
name: managing-better-stack
description: |
  Use when working with Better Stack — better Stack (formerly Logtail) for log
  search, uptime monitoring, incident management, on-call scheduling, and status
  page management. Covers log querying, monitor configuration, heartbeat checks,
  escalation policies, and team management. Use when searching logs, managing
  uptime monitors, handling incidents, or configuring on-call schedules via
  Better Stack API.
connection_type: better-stack
preload: false
---

# Better Stack Management Skill

Manage logs, uptime monitoring, and incidents using the Better Stack API.

## API Conventions

### Authentication
Better Stack API uses Bearer token — injected by connection. Never hardcode tokens.

### Base URLs
- Uptime API: `https://uptime.betterstack.com/api/v2/`
- Logs API: `https://logs.betterstack.com/api/v2/`
- Use connection-injected `BETTERSTACK_BASE_URL`.

### Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `jq` to extract relevant monitor and log fields
- NEVER dump full API responses — always filter and summarize

### Core Helper Function

```bash
#!/bin/bash

bs_uptime_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer ${BETTERSTACK_API_TOKEN}" \
            -H "Content-Type: application/json" \
            "https://uptime.betterstack.com/api/v2${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer ${BETTERSTACK_API_TOKEN}" \
            "https://uptime.betterstack.com/api/v2${endpoint}"
    fi
}

bs_logs_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer ${BETTERSTACK_API_TOKEN}" \
            -H "Content-Type: application/json" \
            "https://logs.betterstack.com/api/v2${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer ${BETTERSTACK_API_TOKEN}" \
            "https://logs.betterstack.com/api/v2${endpoint}"
    fi
}
```

## Parallel Execution

```bash
{
    bs_uptime_api GET "/monitors" &
    bs_uptime_api GET "/incidents" &
    bs_uptime_api GET "/heartbeats" &
    bs_uptime_api GET "/on-call-calendars" &
}
wait
```

## Anti-Hallucination Rules

**NEVER assume monitor IDs, source names, or team IDs. ALWAYS discover first.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Uptime Monitors ==="
bs_uptime_api GET "/monitors" \
    | jq -r '.data[] | "\(.id)\t\(.attributes.monitor_type)\t\(.attributes.status)\t\(.attributes.url // .attributes.ip)"' | head -20

echo ""
echo "=== Log Sources ==="
bs_logs_api GET "/sources" \
    | jq -r '.data[] | "\(.id)\t\(.attributes.name)\t\(.attributes.platform)"' | head -15

echo ""
echo "=== On-Call Calendars ==="
bs_uptime_api GET "/on-call-calendars" \
    | jq -r '.data[] | "\(.id)\t\(.attributes.name)"' | head -10

echo ""
echo "=== Monitor Groups ==="
bs_uptime_api GET "/monitor-groups" \
    | jq -r '.data[] | "\(.id)\t\(.attributes.name)"' | head -10
```

## Common Operations

### Log Search

```bash
#!/bin/bash
echo "=== Recent Logs ==="
bs_logs_api POST "/query" \
    '{"query":"level:error","from":"now-1h","to":"now","batch_size":20}' \
    | jq -r '.data[:20][] | "\(.attributes.timestamp[0:19])\t\(.attributes.level // "info")\t\(.attributes.message[0:80])"'

echo ""
echo "=== Log Volume by Source ==="
bs_logs_api GET "/sources" \
    | jq -r '.data[] | "\(.attributes.name)\t\(.attributes.logs_count // 0) total logs\t\(.attributes.platform)"' | head -15
```

### Uptime Monitor Management

```bash
#!/bin/bash
echo "=== Monitor Status Overview ==="
MONITORS=$(bs_uptime_api GET "/monitors")

echo "$MONITORS" | jq '{
    total: (.data | length),
    up: [.data[] | select(.attributes.status == "up")] | length,
    down: [.data[] | select(.attributes.status == "down")] | length,
    paused: [.data[] | select(.attributes.paused == true)] | length
}'

echo ""
echo "=== Down Monitors ==="
echo "$MONITORS" | jq -r '.data[] | select(.attributes.status == "down") | "\(.attributes.pronounceable_name)\t\(.attributes.url // .attributes.ip)\tdown_since:\(.attributes.last_checked_at)"'

echo ""
echo "=== Monitor Response Times ==="
echo "$MONITORS" | jq -r '.data[] | select(.attributes.status == "up") | "\(.attributes.pronounceable_name)\t\(.attributes.last_response_time // "N/A")ms"' \
    | sort -t$'\t' -k2 -rn | head -15
```

### Incident Management

```bash
#!/bin/bash
echo "=== Open Incidents ==="
bs_uptime_api GET "/incidents?per_page=20" \
    | jq -r '.data[] | select(.attributes.resolved_at == null) | "\(.id)\t\(.attributes.started_at[0:16])\t\(.attributes.cause)\t\(.attributes.name[0:50])"' | head -15

echo ""
echo "=== Recent Resolved Incidents ==="
bs_uptime_api GET "/incidents?per_page=20" \
    | jq -r '.data[] | select(.attributes.resolved_at != null) | "\(.attributes.resolved_at[0:10])\t\(.attributes.duration)s\t\(.attributes.name[0:50])"' | head -10

echo ""
echo "=== Incident Summary ==="
bs_uptime_api GET "/incidents?per_page=100" \
    | jq '{
        total: (.data | length),
        open: [.data[] | select(.attributes.resolved_at == null)] | length,
        resolved: [.data[] | select(.attributes.resolved_at != null)] | length,
        avg_duration_s: ([.data[] | select(.attributes.duration != null) | .attributes.duration] | if length > 0 then add / length | round else 0 end)
    }'
```

### Heartbeat Monitoring

```bash
#!/bin/bash
echo "=== Heartbeat Monitors ==="
bs_uptime_api GET "/heartbeats" \
    | jq -r '.data[] | "\(.id)\t\(.attributes.name)\t\(.attributes.status)\t\(.attributes.period)s interval"' | head -15

echo ""
echo "=== Failing Heartbeats ==="
bs_uptime_api GET "/heartbeats" \
    | jq -r '.data[] | select(.attributes.status == "down") | "\(.attributes.name)\tlast_beat:\(.attributes.last_checked_at // "never")"'
```

### On-Call & Escalation

```bash
#!/bin/bash
echo "=== On-Call Calendars ==="
bs_uptime_api GET "/on-call-calendars" \
    | jq -r '.data[] | "\(.id)\t\(.attributes.name)\t\(.attributes.default_calendar)"'

echo ""
echo "=== Escalation Policies ==="
bs_uptime_api GET "/escalation-policies" \
    | jq -r '.data[] | "\(.id)\t\(.attributes.name)\tsteps:\(.attributes.steps | length)"' | head -10

echo ""
echo "=== Policy Details ==="
bs_uptime_api GET "/escalation-policies" \
    | jq -r '.data[] | "\(.attributes.name):", (.attributes.steps[] | "  Step \(.step_number): wait \(.wait_before)s -> \(.targets | length) targets")'
```

## Output Format

Present results as a structured report:
```
Managing Better Stack Report
════════════════════════════
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

- **Dual APIs**: Uptime and Logs have separate base URLs — use the correct one for each resource type
- **Monitor types**: `status`, `expected_status_code`, `keyword`, `keyword_absence`, `ping`, `tcp`, `udp`, `smtp`, `pop`, `imap`
- **Pagination**: Uses `per_page` and cursor-based pagination — check `pagination.next` for more pages
- **Rate limits**: 250 requests/minute — stagger parallel calls for bulk operations
- **Source tokens**: Log sources have individual source tokens for ingestion — different from API token
- **Incident lifecycle**: Incidents auto-created by monitors — acknowledge or resolve via API
- **Heartbeat URL**: Each heartbeat has a unique URL for pinging — GET request to URL records a heartbeat
- **Status pages**: Managed separately via `/status-pages` endpoint — link monitors to status page resources
