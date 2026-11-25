---
name: managing-bandwidth
description: |
  Use when working with Bandwidth — bandwidth communications platform management
  for voice calls, SMS/MMS messaging, phone number ordering, and 911 services.
  Use when managing phone number inventory, analyzing message delivery,
  monitoring call quality, reviewing usage, or troubleshooting Bandwidth
  messaging and voice issues.
connection_type: bandwidth
preload: false
---

# Bandwidth Management Skill

Manage and analyze Bandwidth voice, messaging, and phone number resources.

## API Conventions

### Authentication
All API calls use HTTP Basic Auth with API credentials, injected automatically.

### Base URLs
- Messaging: `https://messaging.bandwidth.com/api/v2/users/$BW_ACCOUNT_ID`
- Voice: `https://voice.bandwidth.com/api/v2/accounts/$BW_ACCOUNT_ID`
- Numbers: `https://dashboard.bandwidth.com/api/accounts/$BW_ACCOUNT_ID`

### Core Helper Function

```bash
#!/bin/bash

bw_msg_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -u "$BW_API_USER:$BW_API_PASSWORD" \
            -H "Content-Type: application/json" \
            "https://messaging.bandwidth.com/api/v2/users/${BW_ACCOUNT_ID}${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -u "$BW_API_USER:$BW_API_PASSWORD" \
            "https://messaging.bandwidth.com/api/v2/users/${BW_ACCOUNT_ID}${endpoint}"
    fi
}

bw_dash_api() {
    local method="$1"
    local endpoint="$2"
    curl -s -X "$method" \
        -u "$BW_API_USER:$BW_API_PASSWORD" \
        "https://dashboard.bandwidth.com/api/accounts/${BW_ACCOUNT_ID}${endpoint}"
}
```

## Output Rules
- Target ≤50 lines per script output
- Use `jq` or `xmllint` to extract only needed fields
- Never dump full API responses

## Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Account Sites ==="
bw_dash_api GET "/sites" \
    | xmllint --xpath '//Site' - 2>/dev/null | head -20

echo ""
echo "=== Phone Numbers (TNs) ==="
bw_dash_api GET "/tns?size=20" \
    | xmllint --xpath '//TelephoneNumber' - 2>/dev/null | head -20

echo ""
echo "=== Messaging Applications ==="
bw_dash_api GET "/applications" \
    | xmllint --xpath '//Application/ApplicationId|//Application/AppName' - 2>/dev/null | head -15
```

## Phase 2: Analysis

### Message Delivery Health

```bash
#!/bin/bash
echo "=== Recent Message Status ==="
bw_msg_api GET "/messages?from=$(date -u -d '1 day ago' +%Y-%m-%dT%H:%M:%SZ)&to=$(date -u +%Y-%m-%dT%H:%M:%SZ)&size=100" \
    | jq -r '.messages[] | "\(.time[0:16])\t\(.direction)\t\(.messageStatus)\t\(.to[0])"' \
    | head -20

echo ""
echo "=== Delivery Status Breakdown ==="
bw_msg_api GET "/messages?from=$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)&to=$(date -u +%Y-%m-%dT%H:%M:%SZ)&size=500" \
    | jq -r '.messages[] | .messageStatus' | sort | uniq -c | sort -rn
```

### Number Inventory

```bash
#!/bin/bash
echo "=== Active Orders ==="
bw_dash_api GET "/orders?status=COMPLETE&size=10" \
    | xmllint --xpath '//Order' - 2>/dev/null | head -20

echo ""
echo "=== Disconnect Orders ==="
bw_dash_api GET "/disconnects?size=10" \
    | xmllint --xpath '//DisconnectTelephoneNumberOrder' - 2>/dev/null | head -15
```

## Output Format

```
=== Account: <id> ===
Sites: <count>  Phone Numbers: <count>

--- Messaging Health (24h) ---
Delivered: <n>  Failed: <n>  Queued: <n>

--- Number Inventory ---
Active Numbers: <n>
Recent Orders: <n>
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
- **Dashboard API returns XML**: Use `xmllint` not `jq` for number management endpoints
- **Messaging API returns JSON**: Use `jq` for message-related endpoints
- **Rate limits**: 1 request/second for number ordering, higher for messaging
- **Number format**: Use 10-digit format for US numbers (no +1 prefix in dashboard API)
