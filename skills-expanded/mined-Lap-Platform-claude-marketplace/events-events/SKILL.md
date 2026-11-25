---
name: events-events
description: "Events Events API skill. Use when working with Events Events for events. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Events Events
API version: v3

## Auth
OAuth2 | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /events/v3/events/ -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events/v3/events/ | Retrieve event occurrences |
| GET | /events/v3/events/event-types | Retrieve event types |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all events?" -> GET /events/v3/events/
- "List all event-types?" -> GET /events/v3/events/event-types
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
