---
name: ntfy-publish
description: "Publish topic-based notifications using ntfy at {{NTFY_HOST}}:{{NTFY_PORT}}."
metadata:
  openclaw:
    emoji: "📣"
---

# ntfy Publish

ntfy is available at `http://{{NTFY_HOST}}:{{NTFY_PORT}}` within the Docker network.

## Send a Notification

```bash
curl -X POST "http://{{NTFY_HOST}}:{{NTFY_PORT}}/my-topic" \
  -H "Title: Deployment Complete" \
  -H "Priority: high" \
  -H "Tags: white_check_mark" \
  -d "Application deployed successfully"
```

## Tips for AI Agents

- Subscribe to topics for real-time event notifications.
- Supports attachments, actions (buttons), and scheduled delivery.
- Priority: min, low, default, high, max.
