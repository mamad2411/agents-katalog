---
name: orders
description: "Orders API skill. Use when working with Orders for checkout. Covers 9 endpoints."
version: 1.0.0
generator: lapsh
---

# Orders
API version: 2.25

## Auth
OAuth2

## Base URL
https://api-m.sandbox.paypal.com

## Setup
1. Configure auth: OAuth2
2. GET /v2/checkout/orders/{id} -- verify access
3. POST /v2/checkout/orders -- create first orders

## Endpoints

9 endpoints across 1 groups. See references/api-spec.lap for full details.

### checkout
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/checkout/orders | Create order |
| GET | /v2/checkout/orders/{id} | Show order details |
| PATCH | /v2/checkout/orders/{id} | Update order |
| POST | /v2/checkout/orders/{id}/confirm-payment-source | Confirm the Order |
| POST | /v2/checkout/orders/{id}/authorize | Authorize payment for order |
| POST | /v2/checkout/orders/{id}/capture | Capture payment for order |
| POST | /v2/checkout/orders/{id}/track | Add tracking information for an Order. |
| PATCH | /v2/checkout/orders/{id}/trackers/{tracker_id} | Update or cancel tracking information for an order |
| POST | /v2/checkout/orders/order-update-callback | Receive updated order information via callback URL |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a order?" -> POST /v2/checkout/orders
- "Get order details?" -> GET /v2/checkout/orders/{id}
- "Partially update a order?" -> PATCH /v2/checkout/orders/{id}
- "Create a confirm-payment-source?" -> POST /v2/checkout/orders/{id}/confirm-payment-source
- "Create a authorize?" -> POST /v2/checkout/orders/{id}/authorize
- "Create a capture?" -> POST /v2/checkout/orders/{id}/capture
- "Create a track?" -> POST /v2/checkout/orders/{id}/track
- "Partially update a tracker?" -> PATCH /v2/checkout/orders/{id}/trackers/{tracker_id}
- "Create a order-update-callback?" -> POST /v2/checkout/orders/order-update-callback
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
