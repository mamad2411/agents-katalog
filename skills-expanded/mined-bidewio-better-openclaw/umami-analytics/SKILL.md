---
name: umami-analytics
description: "Track website analytics with privacy-focused Umami at {{UMAMI_HOST}}:{{UMAMI_PORT}}."
metadata:
  openclaw:
    emoji: "📉"
---

# Umami Analytics

Umami is available at `http://{{UMAMI_HOST}}:{{UMAMI_PORT}}` within the Docker network.

## Query Stats

```bash
curl "http://{{UMAMI_HOST}}:{{UMAMI_PORT}}/api/websites/{website_id}/stats?startAt=1704067200000&endAt=1704153600000" \
  -H "Authorization: Bearer $UMAMI_TOKEN"
```

## Tips for AI Agents

- Umami is GDPR-compliant by default — no cookies needed.
- Use the API to programmatically query page views, visitors, and events.
- Lightweight tracking script with minimal performance impact.
