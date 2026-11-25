---
name: huginn-automate
description: Event-driven automation with Huginn agents
version: 1.0.0
tags: [automation, events, monitoring, self-hosted]
---

# Huginn – Event-Driven Automation

Huginn creates agents that monitor the web and take automated actions —
like IFTTT/Zapier but fully self-hosted.

- **GitHub**: github.com/huginn/huginn (45 000+ ⭐)
- **License**: MIT
- **Security**: Mature project (10+ years). Ruby codebase. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{HUGINN_URL}}` | Base URL of the Huginn instance |
| `{{HUGINN_API_TOKEN}}` | User API token |

## Usage Examples

### List agents

```bash
curl -s "{{HUGINN_URL}}/api/agents" \
  -H "Authorization: Token {{HUGINN_API_TOKEN}}"
```

### Trigger an agent run

```bash
curl -s -X POST "{{HUGINN_URL}}/api/agents/<agent_id>/run" \
  -H "Authorization: Token {{HUGINN_API_TOKEN}}"
```

## AI Agent Tips

- Agents can watch websites, parse emails, send notifications, and trigger webhooks.
- Chain agents together to build complex automation pipelines.
- Supports scheduling via cron-like intervals.
- Self-hosted — all data stays on your server.
