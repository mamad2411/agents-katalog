---
name: cal_com
display_name: Cal.com
description: Manage bookings, availability, and event types in Cal.com
auth_type: api_key
category: scheduling
---

# Cal.com Integration Skill

## When to use
When the user wants their voice agent to check availability, create bookings, or share
scheduling links via Cal.com during a call.
Common triggers:
- "book an appointment via Cal.com"
- "check availability on Cal.com"
- "send the caller a Cal.com scheduling link"
- "list upcoming bookings"

## What to do

1. **Check connection** via `check_connection("cal_com")`.

2. **If not connected**: Use `secret("cal_com")` in tool scripts. The system
   will automatically emit the correct action card based on the platform
   configuration. Do NOT emit action cards manually.

3. **Discover event types** (Cal.com supports auto-discovery):
   - `api_call("cal_com", "GET", "/event-types")` → list event types with slugs and booking URLs

4. Use the real event type slug or ID in the tool config.

## Example tool configs

### Get a booking link

```json
{
  "name": "cal_com.get_booking_link",
  "description": "Get the Cal.com booking URL for a specific event type",
  "params": [
    {"name": "event_type_slug", "description": "Cal.com event type slug (e.g. '30min')", "type": "string", "required": true}
  ],
  "script": "let key = secret('cal_com');\nlet resp = http_get_h('https://api.cal.com/v2/event-types', {'Authorization': 'Bearer ' + key});\nif (resp.status < 200 || resp.status >= 300) { throw new Error(`Cal.com ${resp.status}: ${resp.body}`); }\nlet types = JSON.parse(resp.body).data;\nlet match = types.find(t => t.slug === event_type_slug);\nif (!match) { return 'Event type not found. Available: ' + types.map(t => t.slug).join(', '); }\nreturn 'https://cal.com/' + match.profile.username + '/' + match.slug;",
  "side_effect": false
}
```

### List upcoming bookings

```json
{
  "name": "cal_com.list_bookings",
  "description": "List upcoming Cal.com bookings",
  "params": [
    {"name": "status", "description": "Booking status filter: upcoming, recurring, past, cancelled (default: upcoming)", "type": "string", "required": false}
  ],
  "script": "let key = secret('cal_com');\nlet s = status || 'upcoming';\nlet resp = http_get_h('https://api.cal.com/v2/bookings?status=' + s + '&take=5', {'Authorization': 'Bearer ' + key});\nif (resp.status >= 200 && resp.status < 300) { return resp.body; }\nthrow new Error(`Cal.com ${resp.status}: ${resp.body}`);",
  "side_effect": false
}
```

## Rules
- NEVER hardcode API keys in tool headers
- NEVER ask for API keys in chat
- Always use `secret("cal_com")` for credentials
- PREFER using `api_call` to discover event type slugs instead of asking
- Cal.com does not support creating bookings via API without attendee confirmation
- For script tools, treat non-2xx HTTP responses as failures and `throw` using `resp.status`/`resp.body`
