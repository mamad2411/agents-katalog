---
name: managing-onesignal
description: |
  Use when working with Onesignal — oneSignal push notification and messaging
  platform management covering notifications, segments, users, templates, and
  delivery analytics. Use when monitoring notification delivery rates, analyzing
  user engagement, reviewing segment health, managing templates, or
  troubleshooting OneSignal push notification issues.
connection_type: onesignal
preload: false
---

# OneSignal Management Skill

Manage and analyze OneSignal push notification resources including notifications, segments, and delivery metrics.

## API Conventions

### Authentication
All API calls use REST API key and App ID, injected automatically.

### Base URL
`https://onesignal.com/api/v1`

### Core Helper Function

```bash
#!/bin/bash

onesignal_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Basic $ONESIGNAL_REST_API_KEY" \
            -H "Content-Type: application/json" \
            "https://onesignal.com/api/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Basic $ONESIGNAL_REST_API_KEY" \
            "https://onesignal.com/api/v1${endpoint}"
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
echo "=== App Info ==="
onesignal_api GET "/apps/$ONESIGNAL_APP_ID" \
    | jq '{name: .name, players: .players, messageable_players: .messageable_players, gcm_key_set: (.gcm_key != null), apns_configured: (.apns_certificates != null)}'

echo ""
echo "=== Recent Notifications ==="
onesignal_api GET "/notifications?app_id=$ONESIGNAL_APP_ID&limit=20" \
    | jq -r '.notifications[] | "\(.id[0:12])\t\(.successful)\tconv:\(.converted // 0)\t\(.headings.en[0:30] // "no-title")\t\(.completed_at // "pending")"' \
    | column -t | head -20

echo ""
echo "=== Segments ==="
onesignal_api GET "/apps/$ONESIGNAL_APP_ID/segments" \
    | jq -r '.segments[] | "\(.id[0:16])\t\(.name)\t\(.is_active)"' | head -15
```

## Phase 2: Analysis

### Delivery Analytics

```bash
#!/bin/bash
echo "=== Notification Delivery Summary (recent 50) ==="
onesignal_api GET "/notifications?app_id=$ONESIGNAL_APP_ID&limit=50" \
    | jq '{
        total_sent: [.notifications[].successful // 0] | add,
        total_failed: [.notifications[].failed // 0] | add,
        total_converted: [.notifications[].converted // 0] | add,
        avg_delivery_rate: ([.notifications[] | select(.successful != null and .remaining == 0) | (.successful / ((.successful + .failed) // 1) * 100)] | if length > 0 then add / length | floor else 0 end)
    }'

echo ""
echo "=== Failed Notifications ==="
onesignal_api GET "/notifications?app_id=$ONESIGNAL_APP_ID&limit=50" \
    | jq -r '.notifications[] | select(.failed > 0) | "\(.id[0:12])\tsent:\(.successful)\tfailed:\(.failed)\t\(.headings.en[0:30] // "no-title")"' \
    | head -10

echo ""
echo "=== Platform Breakdown ==="
onesignal_api GET "/notifications?app_id=$ONESIGNAL_APP_ID&limit=20" \
    | jq -r '.notifications[0] | .platform_delivery_stats // "N/A"'
```

### User Engagement

```bash
#!/bin/bash
echo "=== Subscriber Summary ==="
onesignal_api GET "/apps/$ONESIGNAL_APP_ID" \
    | jq '{total_players: .players, messageable: .messageable_players, unsubscribed: (.players - .messageable_players)}'

echo ""
echo "=== Top Performing Notifications (by conversion) ==="
onesignal_api GET "/notifications?app_id=$ONESIGNAL_APP_ID&limit=50" \
    | jq -r '.notifications[] | select(.converted > 0) | "\(.converted)\t\(.successful)\t\(.headings.en[0:40] // "no-title")"' \
    | sort -rn | head -10
```

## Output Format

```
=== App: <name> ===
Subscribers: <n>  Messageable: <n>

--- Delivery (recent) ---
Sent: <n>  Failed: <n>  Converted: <n>
Avg Delivery Rate: <n>%

--- Segments ---
Total: <n>  Active: <n>
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
- **App ID required**: Most endpoints need `app_id` as query parameter
- **Two auth keys**: REST API Key for most endpoints, User Auth Key for app management
- **Rate limits**: 1 request/second for notification creation, higher for reads
- **Pagination**: Use `limit` and `offset`; max limit is 50 for notifications
