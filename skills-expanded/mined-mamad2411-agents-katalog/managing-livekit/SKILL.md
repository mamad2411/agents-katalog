---
name: managing-livekit
description: |
  Use when working with Livekit — liveKit real-time video and audio
  infrastructure management for WebRTC-based video conferencing, live streaming,
  and data channels. Use when monitoring active rooms, analyzing participant
  quality, reviewing egress/ingress status, managing room configurations, or
  troubleshooting LiveKit sessions.
connection_type: livekit
preload: false
---

# LiveKit Management Skill

Manage and analyze LiveKit real-time video/audio rooms, participants, and media pipelines.

## API Conventions

### Authentication
API calls use API Key and Secret to generate JWT tokens, injected automatically.

### Base URL
`https://<your-livekit-host>` (connection-provided)

### Core Helper Function

```bash
#!/bin/bash

livekit_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $LIVEKIT_TOKEN" \
            -H "Content-Type: application/json" \
            "${LIVEKIT_URL}${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $LIVEKIT_TOKEN" \
            "${LIVEKIT_URL}${endpoint}"
    fi
}

# Alternative: use livekit-cli if available
lk_cli() {
    livekit-cli --url "$LIVEKIT_URL" --api-key "$LIVEKIT_API_KEY" --api-secret "$LIVEKIT_API_SECRET" "$@"
}
```

## Output Rules
- Target ≤50 lines per script output
- Use `jq` to extract only needed fields
- Never dump full API responses

## Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Active Rooms ==="
lk_cli list-rooms 2>/dev/null \
    | jq -r '.rooms[] | "\(.name)\t\(.num_participants) participants\t\(.creation_time)"' \
    | head -20

echo ""
echo "=== Room Details ==="
ROOMS=$(lk_cli list-rooms 2>/dev/null | jq -r '.rooms[].name' | head -5)
for room in $ROOMS; do
    echo "--- Room: $room ---"
    lk_cli list-participants --room "$room" 2>/dev/null \
        | jq -r '.participants[] | "\(.identity)\t\(.state)\ttracks:\(.tracks | length)"' | head -5
done

echo ""
echo "=== Active Egresses ==="
lk_cli list-egress 2>/dev/null \
    | jq -r '.items[] | "\(.egress_id[0:12])\t\(.room_name)\t\(.status)\t\(.started_at)"' \
    | head -10
```

## Phase 2: Analysis

### Room & Participant Quality

```bash
#!/bin/bash
echo "=== Participant Summary ==="
ROOMS=$(lk_cli list-rooms 2>/dev/null | jq -r '.rooms[].name')
TOTAL_PARTICIPANTS=0
for room in $ROOMS; do
    COUNT=$(lk_cli list-participants --room "$room" 2>/dev/null | jq '.participants | length')
    TOTAL_PARTICIPANTS=$((TOTAL_PARTICIPANTS + COUNT))
    echo "$room: $COUNT participants"
done | head -15
echo "Total participants across all rooms: $TOTAL_PARTICIPANTS"

echo ""
echo "=== Track Quality ==="
for room in $(echo "$ROOMS" | head -3); do
    lk_cli list-participants --room "$room" 2>/dev/null \
        | jq -r '.participants[] | .tracks[] | "\(.sid[0:12])\t\(.type)\t\(.width // "-")x\(.height // "-")\t\(.muted)"'
done | head -15
```

### Egress & Ingress Status

```bash
#!/bin/bash
echo "=== Egress Jobs ==="
lk_cli list-egress 2>/dev/null \
    | jq -r '.items[] | "\(.egress_id[0:12])\t\(.room_name)\t\(.status)\tstarted:\(.started_at)"' \
    | head -15

echo ""
echo "=== Egress Status Breakdown ==="
lk_cli list-egress 2>/dev/null \
    | jq -r '.items[] | .status' | sort | uniq -c | sort -rn

echo ""
echo "=== Ingress Endpoints ==="
lk_cli list-ingress 2>/dev/null \
    | jq -r '.items[] | "\(.ingress_id[0:12])\t\(.room_name)\t\(.state)\t\(.input_type)"' \
    | head -10
```

## Output Format

```
=== LiveKit Server: <url> ===
Active Rooms: <n>  Total Participants: <n>

--- Room Details ---
<room_name>: <n> participants, <n> tracks

--- Egress/Ingress ---
Active Egresses: <n>  Active Ingresses: <n>

--- Quality ---
Tracks: <n> video, <n> audio  Muted: <n>
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
- **JWT tokens expire**: Generate fresh tokens for each API call session
- **Twirp protocol**: LiveKit uses Twirp (protobuf over HTTP); CLI abstracts this
- **Room auto-delete**: Empty rooms are deleted automatically after timeout
- **Track types**: `AUDIO`, `VIDEO`, `DATA` — filter accordingly
