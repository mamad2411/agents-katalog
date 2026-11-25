---
name: spec
description: "spec API skill. Use when working with spec for subscriptions. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# spec

## Auth
No authentication required.

## Base URL
https://api.ote-godaddy.com

## Setup
1. No auth setup needed
2. GET /v1/subscriptions -- verify access

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/subscriptions | Retrieve a list of Subscriptions for the specified Shopper |
| GET | /v1/subscriptions/productGroups | Retrieve a list of ProductGroups for the specified Shopper |
| DELETE | /v1/subscriptions/{subscriptionId} | Cancel the specified Subscription |
| GET | /v1/subscriptions/{subscriptionId} | Retrieve details for the specified Subscription |
| PATCH | /v1/subscriptions/{subscriptionId} | Update details for the specified Subscription |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all subscriptions?" -> GET /v1/subscriptions
- "List all productGroups?" -> GET /v1/subscriptions/productGroups
- "Delete a subscription?" -> DELETE /v1/subscriptions/{subscriptionId}
- "Get subscription details?" -> GET /v1/subscriptions/{subscriptionId}
- "Partially update a subscription?" -> PATCH /v1/subscriptions/{subscriptionId}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
