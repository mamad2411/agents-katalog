---
name: watchtower-update
description: "Auto-update Docker containers using Watchtower."
metadata:
  openclaw:
    emoji: "🗼"
---

# Watchtower Auto-Update

Watchtower runs as a container and automatically updates other running containers when new images are available.

## Tips for AI Agents

- Watchtower polls for image updates at a configurable interval.
- Use labels to include/exclude specific containers from updates.
- Supports notifications via email, Slack, or webhooks on updates.
- Set `WATCHTOWER_CLEANUP=true` to remove old images after updating.
