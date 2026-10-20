---
name: chatwoot-support
description: Customer support with Chatwoot
version: 1.0.0
tags: [support, chat, customer-service, self-hosted]
---

# Chatwoot – Customer Support Platform

Chatwoot is an open-source customer engagement platform with
live chat, email, social media, and API channel support.

- **GitHub**: github.com/chatwoot/chatwoot (22 000+ ⭐)
- **License**: MIT
- **Security**: GDPR compliant. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{CHATWOOT_URL}}` | Base URL |
| `{{CHATWOOT_API_TOKEN}}` | User or bot API access token |

## Usage Examples

### List conversations

```bash
curl -s "{{CHATWOOT_URL}}/api/v1/accounts/<account_id>/conversations" \
  -H "api_access_token: {{CHATWOOT_API_TOKEN}}"
```

### Send a message

```bash
curl -s -X POST "{{CHATWOOT_URL}}/api/v1/accounts/<account_id>/conversations/<conv_id>/messages" \
  -H "api_access_token: {{CHATWOOT_API_TOKEN}}" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello! How can I help?", "message_type": "outgoing"}'
```

## AI Agent Tips

- Supports live chat widget, email, WhatsApp, Facebook, Twitter, and API.
- Bot integration via webhooks and API channels.
- Canned responses and automation rules for efficiency.
- Self-hosted for full data control — or use managed cloud.
