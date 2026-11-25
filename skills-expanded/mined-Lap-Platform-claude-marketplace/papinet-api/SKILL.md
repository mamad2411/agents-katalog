---
name: papinet-api
description: "papiNet API skill. Use when working with papiNet for orders. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# papiNet API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://papinet.papinet.io

## Setup
1. No auth setup needed
2. GET /orders -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### orders
| Method | Path | Description |
|--------|------|-------------|
| GET | /orders | List `orders` |
| GET | /orders/{orderId} | Get an `order` |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all orders?" -> GET /orders
- "Get order details?" -> GET /orders/{orderId}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
