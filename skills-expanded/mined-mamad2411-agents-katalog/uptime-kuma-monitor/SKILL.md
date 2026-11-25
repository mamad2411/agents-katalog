---
name: uptime-kuma-monitor
description: "Monitor service uptime and configure alerts using Uptime Kuma at {{UPTIME_KUMA_HOST}}:{{UPTIME_KUMA_PORT}}."
metadata:
  openclaw:
    emoji: "💓"
---

# Uptime Kuma Monitor

Uptime Kuma is available at `http://{{UPTIME_KUMA_HOST}}:{{UPTIME_KUMA_PORT}}` within the Docker network.

## Tips for AI Agents

- Access the web UI to add monitors for HTTP, TCP, DNS, Docker, and more.
- Supports notifications via Slack, Discord, Telegram, email, and webhooks.
- Status pages can be shared publicly for transparency.
- Use the Push monitor type to receive heartbeats from your applications.
