---
name: api-webhook
description: "Send webhook events to external endpoints using curl."
metadata:
  openclaw:
    emoji: "🪝"
---

# API Webhook

Send webhook events to notify external services of events.

## Send Webhook

```bash
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Secret: $WEBHOOK_SECRET" \
  -d '{"event": "task.completed", "payload": {"task_id": "123", "status": "success"}}'
```

## Tips for AI Agents

- Include a signature header for webhook verification.
- Use retry logic for failed deliveries.
- Log webhook responses for debugging.
