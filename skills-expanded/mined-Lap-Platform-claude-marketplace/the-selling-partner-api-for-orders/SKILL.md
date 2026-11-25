---
name: the-selling-partner-api-for-orders
description: "The Selling Partner API for Orders API skill. Use when working with The Selling Partner API for Orders for orders. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# The Selling Partner API for Orders
API version: 2026-01-01

## Auth
No authentication required.

## Base URL
https://sellingpartnerapi-na.amazon.com

## Setup
1. No auth setup needed
2. GET /orders/2026-01-01/orders -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### orders
| Method | Path | Description |
|--------|------|-------------|
| GET | /orders/2026-01-01/orders | Returns orders that are created or updated during the time period that you specify. You can filter the response for specific types of orders. |
| GET | /orders/2026-01-01/orders/{orderId} | Returns the order that you specify. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all orders?" -> GET /orders/2026-01-01/orders
- "Get order details?" -> GET /orders/2026-01-01/orders/{orderId}

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
