---
name: ga4-measurement-protocol
description: Implement Google Analytics 4 (GA4) Measurement Protocol. Use for server-side tracking or offline event ingestion.
---

# Google Analytics 4 Measurement Protocol

When a user wants to send events from a server, CRM, or offline source to GA4, use the Measurement Protocol.

## Endpoints
- Standard: `https://www.google-analytics.com/mp/collect`
- Debugging: `https://www.google-analytics.com/debug/mp/collect` (returns validation messages)

## Required Query Parameters
- `api_secret`: Generated in the GA4 UI (Admin > Data Streams > Measurement Protocol API secrets).
- `measurement_id`: The GA4 property measurement ID (e.g., `G-XXXXXXX`).

## JSON Body Structure
You must include `client_id` (or `app_instance_id` for apps) and an `events` array.

```json
{
  "client_id": "1234567890.0987654321",
  "events": [{
    "name": "offline_purchase",
    "params": {
      "session_id": "123",
      "engagement_time_msec": "100",
      "value": 45.0,
      "currency": "USD"
    }
  }]
}
```

## Guidelines
1. **Always use the debug endpoint** when developing to validate the payload.
2. The Measurement Protocol **does not create sessions** natively. If you need an event to tie to an existing session, you must pass the `session_id` parameter.
3. Keep payloads under 130KB and no more than 25 events per request.
