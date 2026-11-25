---
name: saas-telephony
description: "Make voice calls and send SMS/MMS via the ThinkFleetBot SaaS telephony API. Check if telephony is enabled for the current agent."
metadata: {"thinkfleetbot":{"emoji":"📞","requires":{"bins":["curl","jq"],"env":["SAAS_API_URL","SAAS_API_KEY"]}}}
---

# SaaS Telephony

Make voice calls and send text messages through the ThinkFleetBot SaaS API.

## Check If Telephony Is Enabled

```bash
# Check agent's telephony status
curl -s "$SAAS_API_URL/api/agents/me/telephony" \
  -H "Authorization: Bearer $SAAS_API_KEY" | jq '{enabled: .enabled, phone_number: .phone_number, capabilities: .capabilities}'
```

If `enabled: false`, telephony is not configured for this agent. Do not attempt calls or messages.

## Send SMS

```bash
curl -s -X POST "$SAAS_API_URL/api/messaging/sms" \
  -H "Authorization: Bearer $SAAS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+15551234567",
    "body": "Your order has been shipped!"
  }' | jq .
```

## Send MMS (with media)

```bash
curl -s -X POST "$SAAS_API_URL/api/messaging/mms" \
  -H "Authorization: Bearer $SAAS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+15551234567",
    "body": "Here is your receipt",
    "media_url": "https://example.com/receipt.pdf"
  }' | jq .
```

## Initiate Voice Call

```bash
curl -s -X POST "$SAAS_API_URL/api/messaging/voice" \
  -H "Authorization: Bearer $SAAS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+15551234567",
    "prompt": "Hello, this is a reminder about your appointment tomorrow at 3pm. Press 1 to confirm or 2 to reschedule."
  }' | jq .
```

## Check Message/Call Status

```bash
# Check SMS status
curl -s "$SAAS_API_URL/api/messaging/sms/{MESSAGE_ID}" \
  -H "Authorization: Bearer $SAAS_API_KEY" | jq '{status, delivered_at, error}'

# Check call status
curl -s "$SAAS_API_URL/api/messaging/voice/{CALL_ID}" \
  -H "Authorization: Bearer $SAAS_API_KEY" | jq '{status, duration, recording_url}'
```

## List Recent Messages

```bash
curl -s "$SAAS_API_URL/api/messaging/history?limit=20" \
  -H "Authorization: Bearer $SAAS_API_KEY" | jq '.data[] | {id, type, to, status, created_at}'
```

## Notes

- Always check if telephony is enabled before attempting to send messages or make calls.
- Confirm the recipient phone number with the user before sending.
- Phone numbers must be in E.164 format: `+1XXXXXXXXXX`.
- Voice calls use the `prompt` field to define what the AI says. Keep prompts conversational and clear.
- Message delivery is async — check status after sending if confirmation is needed.
- Rate limits apply. Don't send bulk messages without checking the plan's limits.
- Never log or store phone numbers in plain text outside the SaaS platform.
