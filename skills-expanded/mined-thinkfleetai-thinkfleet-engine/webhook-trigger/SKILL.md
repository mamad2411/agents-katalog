---
name: webhook-trigger
description: "Send HTTP requests to webhooks and APIs using curl. Supports GET, POST, PUT, DELETE with headers and JSON payloads."
metadata: {"thinkfleetbot":{"emoji":"🪝","requires":{"bins":["curl","jq"]}}}
---

# Webhook Trigger

Send HTTP requests to any webhook or API endpoint.

## POST JSON

```bash
curl -s -X POST "https://hooks.example.com/webhook" \
  -H "Content-Type: application/json" \
  -d '{"event":"deploy","status":"success"}' | jq .
```

## POST with auth header

```bash
curl -s -X POST "https://api.example.com/notify" \
  -H "Authorization: Bearer $WEBHOOK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello"}' | jq .
```

## GET with query params

```bash
curl -s "https://api.example.com/status?service=web" \
  -H "Authorization: Bearer $API_TOKEN" | jq .
```

## Slack incoming webhook

```bash
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"text":"Deployment complete :rocket:"}'
```

## Discord webhook

```bash
curl -s -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"content":"Build succeeded!"}'
```

## Notes

- Always show the user the URL and payload before sending.
- Use `jq` to format JSON responses.
- For retries: `curl --retry 3 --retry-delay 2`.
