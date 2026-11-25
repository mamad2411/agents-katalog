---
name: rocketchat-send
description: "Send messages and manage channels using Rocket.Chat at {{ROCKETCHAT_HOST}}:{{ROCKETCHAT_PORT}}."
metadata:
  openclaw:
    emoji: "🚀"
---

# Rocket.Chat Send

Rocket.Chat is available at `http://{{ROCKETCHAT_HOST}}:{{ROCKETCHAT_PORT}}` within the Docker network.

## Send a Message

```bash
curl -X POST "http://{{ROCKETCHAT_HOST}}:{{ROCKETCHAT_PORT}}/api/v1/chat.sendMessage" \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: $ROCKETCHAT_AUTH_TOKEN" \
  -H "X-User-Id: $ROCKETCHAT_USER_ID" \
  -d '{"message": {"rid": "{room_id}", "msg": "Hello from OpenClaw!"}}'
```

## Tips for AI Agents

- Supports channels, direct messages, and threads.
- Use incoming webhooks for simplified bot integration.
- Supports file uploads, emojis, and rich message attachments.
