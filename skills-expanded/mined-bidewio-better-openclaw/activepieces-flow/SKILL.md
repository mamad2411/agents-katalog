---
name: activepieces-flow
description: No-code workflow automation with Activepieces
version: 1.0.0
tags: [automation, workflow, no-code, zapier-alternative]
---

# Activepieces – Open-Source Zapier Alternative

Activepieces is a no-code automation platform with 200+ integrations,
visual workflow builder, and self-hosting capability.

- **GitHub**: github.com/activepieces/activepieces (15 000+ ⭐)
- **License**: MIT (core)
- **Security**: TypeScript codebase. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{ACTIVEPIECES_URL}}` | Base URL of the Activepieces instance |
| `{{ACTIVEPIECES_API_KEY}}` | API key for programmatic access |

## Usage Examples

### List flows

```bash
curl -s "{{ACTIVEPIECES_URL}}/v1/flows" \
  -H "Authorization: Bearer {{ACTIVEPIECES_API_KEY}}"
```

### Trigger a webhook flow

```bash
curl -s -X POST "{{ACTIVEPIECES_URL}}/v1/webhooks/<flow_id>" \
  -H "Content-Type: application/json" \
  -d '{"event": "new_order", "data": {"id": 123}}'
```

## AI Agent Tips

- Visual builder makes complex workflows accessible to non-developers.
- Supports cron triggers, webhooks, and app-based triggers.
- 200+ pre-built integrations (Slack, Gmail, GitHub, etc.).
- Self-hosted version gives full data control.
