---
name: mattermost-post
description: "Post messages and manage channels using Mattermost at {{MATTERMOST_HOST}}:{{MATTERMOST_PORT}}."
metadata:
  openclaw:
    emoji: "💬"
---

# Mattermost Post

Mattermost is available at `http://{{MATTERMOST_HOST}}:{{MATTERMOST_PORT}}` within the Docker network.

## Post a Message

```bash
curl -X POST "http://{{MATTERMOST_HOST}}:{{MATTERMOST_PORT}}/api/v4/posts" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MATTERMOST_TOKEN" \
  -d '{"channel_id": "{channel_id}", "message": "Hello from OpenClaw!"}'
```

## Tips for AI Agents

- Use incoming webhooks for simplified integration.
- Supports Markdown, file attachments, and interactive messages.
- Bot accounts are recommended for automated posting.
