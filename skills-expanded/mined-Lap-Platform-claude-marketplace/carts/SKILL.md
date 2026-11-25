---
name: carts
description: "Carts API skill. Use when working with Carts for carts. Covers 21 endpoints."
version: 1.0.0
generator: lapsh
---

# Carts

## Auth
ApiKey X-Auth-Token in header

## Base URL
https://api.bigcommerce.com/stores/{store_hash}/v3

## Setup
1. Set your API key in the appropriate header
2. GET /carts/settings -- verify access
3. POST /carts -- create first carts

## Endpoints

21 endpoints across 1 groups. See references/api-spec.lap for full details.

### carts
| Method | Path | Description |
|--------|------|-------------|
| POST | /carts | Create a Cart |
| POST | /carts/{cartId}/items | Add Cart Line Items |
| POST | /carts/{cartId}/redirect_urls | Create Cart Redirect URL |
| PUT | /carts/{cartId}/items/{itemId} | Update Cart Line Item |
| DELETE | /carts/{cartId}/items/{itemId} | Delete Cart Line Item |
| GET | /carts/{cartId} | Get a Cart |
| PUT | /carts/{cartId} | Update Customer ID |
| DELETE | /carts/{cartId} | Delete a Cart |
| GET | /carts/settings | Get Global Cart Settings |
| PUT | /carts/settings | Update Global Cart Settings |
| GET | /carts/settings/channels/{channel_id} | Get Channel Cart Settings |
| PUT | /carts/settings/channels/{channel_id} | Update Channel Cart Settings |
| GET | /carts/{cart_id}/metafields | Get Cart Metafields |
| POST | /carts/{cart_id}/metafields | Create a Cart Metafield |
| GET | /carts/{cart_id}/metafields/{metafield_id} | Get a Cart Metafield |
| PUT | /carts/{cart_id}/metafields/{metafield_id} | Update a Cart Metafield |
| DELETE | /carts/{cart_id}/metafields/{metafield_id} | Delete a Metafield |
| GET | /carts/metafields | Get All Cart Metafields |
| POST | /carts/metafields | Create multiple Metafields |
| PUT | /carts/metafields | Update multiple Metafields |
| DELETE | /carts/metafields | Delete multiple Metafields |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a cart?" -> POST /carts
- "Create a item?" -> POST /carts/{cartId}/items
- "Create a redirect_url?" -> POST /carts/{cartId}/redirect_urls
- "Update a item?" -> PUT /carts/{cartId}/items/{itemId}
- "Delete a item?" -> DELETE /carts/{cartId}/items/{itemId}
- "Get cart details?" -> GET /carts/{cartId}
- "Update a cart?" -> PUT /carts/{cartId}
- "Delete a cart?" -> DELETE /carts/{cartId}
- "List all settings?" -> GET /carts/settings
- "Get channel details?" -> GET /carts/settings/channels/{channel_id}
- "Update a channel?" -> PUT /carts/settings/channels/{channel_id}
- "List all metafields?" -> GET /carts/{cart_id}/metafields
- "Create a metafield?" -> POST /carts/{cart_id}/metafields
- "Get metafield details?" -> GET /carts/{cart_id}/metafields/{metafield_id}
- "Update a metafield?" -> PUT /carts/{cart_id}/metafields/{metafield_id}
- "Delete a metafield?" -> DELETE /carts/{cart_id}/metafields/{metafield_id}
- "List all metafields?" -> GET /carts/metafields
- "Create a metafield?" -> POST /carts/metafields
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
