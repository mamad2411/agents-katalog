---
name: event-notification-api-specification-tpp-endpoints
description: "Event Notification API Specification - TPP Endpoints API skill. Use when working with Event Notification API Specification - TPP Endpoints for event-notifications. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Event Notification API Specification - TPP Endpoints
API version: 4.0.0

## Auth
OAuth2

## Base URL
/open-banking/v4.0

## Setup
1. Configure auth: OAuth2
3. POST /event-notifications -- create first event-notifications

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### event-notifications
| Method | Path | Description |
|--------|------|-------------|
| POST | /event-notifications | Send an event notification |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a event-notification?" -> POST /event-notifications
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
