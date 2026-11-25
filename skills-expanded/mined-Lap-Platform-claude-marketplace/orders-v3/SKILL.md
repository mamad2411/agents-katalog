---
name: orders-v3
description: "Orders V3 API skill. Use when working with Orders V3 for orders. Covers 21 endpoints."
version: 1.0.0
generator: lapsh
---

# Orders V3

## Auth
ApiKey X-Auth-Token in header

## Base URL
https://api.bigcommerce.com/stores/{store_hash}/v3

## Setup
1. Set your API key in the appropriate header
2. GET /orders/payment_actions/refunds -- verify access
3. POST /orders/{order_id}/payment_actions/capture -- create first capture

## Endpoints

21 endpoints across 1 groups. See references/api-spec.lap for full details.

### orders
| Method | Path | Description |
|--------|------|-------------|
| POST | /orders/{order_id}/payment_actions/capture | Capture order payment |
| POST | /orders/{order_id}/payment_actions/void | Void |
| GET | /orders/{order_id}/transactions | Get Transactions |
| POST | /orders/{order_id}/payment_actions/refund_quotes | Create a Refund Quote |
| POST | /orders/{order_id}/payment_actions/refunds | Create a Refund |
| GET | /orders/{order_id}/payment_actions/refunds | Get Refunds for Order |
| GET | /orders/payment_actions/refunds/{refund_id} | Get a Refund |
| GET | /orders/payment_actions/refunds | Get All Refunds |
| GET | /orders/{order_id}/metafields | Get Order Metafields |
| POST | /orders/{order_id}/metafields | Create Metafields |
| GET | /orders/{order_id}/metafields/{metafield_id} | Get a Metafield |
| PUT | /orders/{order_id}/metafields/{metafield_id} | Update a Metafield |
| DELETE | /orders/{order_id}/metafields/{metafield_id} | Delete a Metafield |
| GET | /orders/settings | Get Global Order Settings |
| PUT | /orders/settings | Update Global Order Settings |
| GET | /orders/settings/channels/{channel_id} | Get Channel Order Settings |
| PUT | /orders/settings/channels/{channel_id} | Update Channel Order Settings |
| GET | /orders/metafields | Get All Order Metafields |
| POST | /orders/metafields | Create multiple Metafields |
| PUT | /orders/metafields | Update multiple Metafields |
| DELETE | /orders/metafields | Delete Multiple Metafields |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a capture?" -> POST /orders/{order_id}/payment_actions/capture
- "Create a void?" -> POST /orders/{order_id}/payment_actions/void
- "List all transactions?" -> GET /orders/{order_id}/transactions
- "Create a refund_quote?" -> POST /orders/{order_id}/payment_actions/refund_quotes
- "Create a refund?" -> POST /orders/{order_id}/payment_actions/refunds
- "List all refunds?" -> GET /orders/{order_id}/payment_actions/refunds
- "Get refund details?" -> GET /orders/payment_actions/refunds/{refund_id}
- "List all refunds?" -> GET /orders/payment_actions/refunds
- "List all metafields?" -> GET /orders/{order_id}/metafields
- "Create a metafield?" -> POST /orders/{order_id}/metafields
- "Get metafield details?" -> GET /orders/{order_id}/metafields/{metafield_id}
- "Update a metafield?" -> PUT /orders/{order_id}/metafields/{metafield_id}
- "Delete a metafield?" -> DELETE /orders/{order_id}/metafields/{metafield_id}
- "List all settings?" -> GET /orders/settings
- "Get channel details?" -> GET /orders/settings/channels/{channel_id}
- "Update a channel?" -> PUT /orders/settings/channels/{channel_id}
- "List all metafields?" -> GET /orders/metafields
- "Create a metafield?" -> POST /orders/metafields
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
