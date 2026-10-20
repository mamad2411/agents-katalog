---
name: cal-schedule
description: "Manage scheduling and bookings using Cal.com at {{CALCOM_HOST}}:{{CALCOM_PORT}}."
metadata:
  openclaw:
    emoji: "📅"
---

# Cal.com Scheduling

Cal.com is available at `http://{{CALCOM_HOST}}:{{CALCOM_PORT}}` within the Docker network.

## List Bookings

```bash
curl -X GET "http://{{CALCOM_HOST}}:{{CALCOM_PORT}}/api/v1/bookings?apiKey=$CALCOM_API_KEY"
```

## Create Event Type

```bash
curl -X POST "http://{{CALCOM_HOST}}:{{CALCOM_PORT}}/api/v1/event-types?apiKey=$CALCOM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "30min Meeting", "slug": "30min", "length": 30}'
```

## Tips for AI Agents

- Use event types to define meeting templates.
- Webhook integrations notify on booking changes.
- Supports round-robin and collective scheduling.
