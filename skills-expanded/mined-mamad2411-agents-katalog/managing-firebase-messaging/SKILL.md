---
name: managing-firebase-messaging
description: |
  Use when working with Firebase Messaging — firebase Cloud Messaging (FCM)
  management covering message sending, topic subscriptions, device groups, and
  delivery analytics. Use when monitoring message delivery, analyzing
  notification performance, reviewing topic subscriptions, managing device
  tokens, or troubleshooting FCM push notification issues.
connection_type: firebase-messaging
preload: false
---

# Firebase Cloud Messaging Management Skill

Manage and analyze Firebase Cloud Messaging resources including messages, topics, and delivery.

## API Conventions

### Authentication
All API calls use OAuth 2.0 Bearer token from service account, injected automatically.

### Base URL
`https://fcm.googleapis.com/v1/projects/$FIREBASE_PROJECT_ID`

### Core Helper Function

```bash
#!/bin/bash

fcm_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $FIREBASE_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            "https://fcm.googleapis.com/v1/projects/${FIREBASE_PROJECT_ID}${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $FIREBASE_ACCESS_TOKEN" \
            "https://fcm.googleapis.com/v1/projects/${FIREBASE_PROJECT_ID}${endpoint}"
    fi
}

# Instance ID API for topic management
iid_api() {
    local method="$1"
    local endpoint="$2"
    curl -s -X "$method" \
        -H "Authorization: Bearer $FIREBASE_ACCESS_TOKEN" \
        "https://iid.googleapis.com${endpoint}"
}
```

## Output Rules
- Target ≤50 lines per script output
- Use `jq` to extract only needed fields
- Never dump full API responses

## Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Project Configuration ==="
curl -s -H "Authorization: Bearer $FIREBASE_ACCESS_TOKEN" \
    "https://firebase.googleapis.com/v1beta1/projects/${FIREBASE_PROJECT_ID}" \
    | jq '{projectId: .projectId, displayName: .displayName, state: .state}'

echo ""
echo "=== FCM Send Test ==="
RESULT=$(fcm_api POST "/messages:send" '{"message": {"topic": "__test__", "notification": {"title": "test", "body": "test"}, "dry_run": true}}' 2>/dev/null)
echo "$RESULT" | jq '{status: (if .error then "error: \(.error.message)" else "healthy" end)}' 2>/dev/null || echo "FCM API reachable"

echo ""
echo "=== Topic Subscription Check (sample token) ==="
echo "Note: FCM does not have a list-all-topics API. Check specific tokens with IID API."
```

## Phase 2: Analysis

### Delivery Analytics (via BigQuery export)

```bash
#!/bin/bash
echo "=== FCM Delivery Metrics ==="
echo "Note: FCM delivery analytics are available in Firebase Console or via BigQuery export."
echo "Use the Firebase Console > Cloud Messaging > Reports for delivery data."

echo ""
echo "=== Token Validation ==="
# Validate a specific device token
TOKEN="${1:-}"
if [ -n "$TOKEN" ]; then
    iid_api GET "/iid/info/$TOKEN?details=true" \
        | jq '{platform: .platform, app: .application, scope: .rel.topics}'
else
    echo "Provide a device token to validate"
fi

echo ""
echo "=== Topic Management ==="
# Subscribe tokens to a topic
# iid_api POST "/iid/v1:batchAdd" -d '{"to": "/topics/news", "registration_tokens": ["token1"]}'
echo "Use batchAdd/batchRemove IID endpoints for topic management"
```

### Message Health Check

```bash
#!/bin/bash
echo "=== Dry Run Message Validation ==="
for platform in "android" "apns" "webpush"; do
    RESULT=$(fcm_api POST "/messages:send" "{
        \"validate_only\": true,
        \"message\": {
            \"topic\": \"test\",
            \"notification\": {\"title\": \"test\", \"body\": \"test\"},
            \"${platform}\": {}
        }
    }")
    STATUS=$(echo "$RESULT" | jq -r 'if .error then .error.status else "VALID" end')
    echo "$platform: $STATUS"
done

echo ""
echo "=== Service Account Permissions ==="
curl -s -H "Authorization: Bearer $FIREBASE_ACCESS_TOKEN" \
    "https://cloudresourcemanager.googleapis.com/v1/projects/${FIREBASE_PROJECT_ID}:testIamPermissions" \
    -d '{"permissions": ["cloudmessaging.messages.create"]}' \
    | jq '.permissions // ["none"]'
```

## Output Format

```
=== Firebase Project: <name> (<id>) ===
FCM API Status: <healthy|error>

--- Message Validation ---
Android: <valid|error>  APNS: <valid|error>  Web: <valid|error>

--- Notes ---
Delivery analytics: Firebase Console or BigQuery export
Topic management: Use IID batchAdd/batchRemove APIs
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
- **No list API**: FCM does not provide endpoints to list all topics or tokens
- **Dry run**: Use `validate_only: true` to test messages without sending
- **Token expiry**: Device tokens expire and must be refreshed by client apps
- **Rate limits**: 600 requests/minute for message sending
- **v1 API**: Always use FCM v1 API, not legacy HTTP API
