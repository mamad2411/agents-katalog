---
name: gotify-notify
description: "Send push notifications using Gotify at {{GOTIFY_HOST}}:{{GOTIFY_PORT}}."
metadata:
  openclaw:
    emoji: "🔔"
---

# Gotify Notifications

Gotify is available at `http://{{GOTIFY_HOST}}:{{GOTIFY_PORT}}` within the Docker network.

## Send a Notification

```bash
curl -X POST "http://{{GOTIFY_HOST}}:{{GOTIFY_PORT}}/message?token=$GOTIFY_APP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Alert", "message": "Service health check failed", "priority": 8}'
```

## Tips for AI Agents

- Priority levels: 1-3 (low), 4-7 (normal), 8-10 (high/urgent).
- Create separate application tokens for different notification sources.
- Supports Markdown formatting in message bodies.
