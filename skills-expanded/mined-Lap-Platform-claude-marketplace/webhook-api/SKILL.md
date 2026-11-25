---
name: webhook-api
description: "Webhook API skill. Use when working with Webhook for webhook. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# Webhook API
API version: 10.24.0

## Auth
ApiKey Authorization in header

## Base URL
https://unify.apideck.com

## Setup
1. Set your API key in the appropriate header
2. GET /webhook/webhooks -- verify access
3. POST /webhook/webhooks -- create first webhooks

## Endpoints

10 endpoints across 1 groups. See references/api-spec.lap for full details.

### webhook
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhook/webhooks | List webhook subscriptions |
| POST | /webhook/webhooks | Create webhook subscription |
| GET | /webhook/webhooks/{id} | Get webhook subscription |
| PATCH | /webhook/webhooks/{id} | Update webhook subscription |
| DELETE | /webhook/webhooks/{id} | Delete webhook subscription |
| POST | /webhook/webhooks/{id}/execute/{serviceId} | Execute a webhook |
| POST | /webhook/webhooks/{id}/x/{serviceId} | Execute a webhook |
| POST | /webhook/w/{id}/{serviceId} | Resolve and Execute a connection webhook |
| GET | /webhook/w/{id}/{serviceId} | Resolve and Execute a connection webhook |
| GET | /webhook/logs | List event logs |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all webhooks?" -> GET /webhook/webhooks
- "Create a webhook?" -> POST /webhook/webhooks
- "Get webhook details?" -> GET /webhook/webhooks/{id}
- "Partially update a webhook?" -> PATCH /webhook/webhooks/{id}
- "Delete a webhook?" -> DELETE /webhook/webhooks/{id}
- "Get w details?" -> GET /webhook/w/{id}/{serviceId}
- "List all logs?" -> GET /webhook/logs
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
