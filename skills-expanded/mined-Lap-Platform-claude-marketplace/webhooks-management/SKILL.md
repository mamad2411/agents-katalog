---
name: webhooks-management
description: "Webhooks Management API skill. Use when working with Webhooks Management for notifications. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# Webhooks Management
API version: 1.11

## Auth
OAuth2

## Base URL
https://api-m.sandbox.paypal.com

## Setup
1. Configure auth: OAuth2
2. GET /v1/notifications/webhooks -- verify access
3. POST /v1/notifications/webhooks -- create first webhooks

## Endpoints

16 endpoints across 1 groups. See references/api-spec.lap for full details.

### notifications
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/notifications/webhooks | Create webhook |
| GET | /v1/notifications/webhooks | List webhooks |
| GET | /v1/notifications/webhooks/{webhook_id} | Show webhook details |
| PATCH | /v1/notifications/webhooks/{webhook_id} | Update webhook |
| DELETE | /v1/notifications/webhooks/{webhook_id} | Delete webhook |
| GET | /v1/notifications/webhooks/{webhook_id}/event-types | List event subscriptions for webhook |
| POST | /v1/notifications/webhooks-lookup | Create webhook lookup |
| GET | /v1/notifications/webhooks-lookup | List webhook lookups |
| GET | /v1/notifications/webhooks-lookup/{webhook_lookup_id} | Show webhook lookup details |
| DELETE | /v1/notifications/webhooks-lookup/{webhook_lookup_id} | Delete webhook lookup |
| POST | /v1/notifications/verify-webhook-signature | Verify webhook signature |
| GET | /v1/notifications/webhooks-event-types | List available events |
| GET | /v1/notifications/webhooks-events | List event notifications |
| GET | /v1/notifications/webhooks-events/{event_id} | Show event notification details |
| POST | /v1/notifications/webhooks-events/{event_id}/resend | Resend event notification |
| POST | /v1/notifications/simulate-event | Simulate webhook event |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a webhook?" -> POST /v1/notifications/webhooks
- "List all webhooks?" -> GET /v1/notifications/webhooks
- "Get webhook details?" -> GET /v1/notifications/webhooks/{webhook_id}
- "Partially update a webhook?" -> PATCH /v1/notifications/webhooks/{webhook_id}
- "Delete a webhook?" -> DELETE /v1/notifications/webhooks/{webhook_id}
- "List all event-types?" -> GET /v1/notifications/webhooks/{webhook_id}/event-types
- "Create a webhooks-lookup?" -> POST /v1/notifications/webhooks-lookup
- "List all webhooks-lookup?" -> GET /v1/notifications/webhooks-lookup
- "Get webhooks-lookup details?" -> GET /v1/notifications/webhooks-lookup/{webhook_lookup_id}
- "Delete a webhooks-lookup?" -> DELETE /v1/notifications/webhooks-lookup/{webhook_lookup_id}
- "Create a verify-webhook-signature?" -> POST /v1/notifications/verify-webhook-signature
- "List all webhooks-event-types?" -> GET /v1/notifications/webhooks-event-types
- "List all webhooks-events?" -> GET /v1/notifications/webhooks-events
- "Get webhooks-event details?" -> GET /v1/notifications/webhooks-events/{event_id}
- "Create a resend?" -> POST /v1/notifications/webhooks-events/{event_id}/resend
- "Create a simulate-event?" -> POST /v1/notifications/simulate-event
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
