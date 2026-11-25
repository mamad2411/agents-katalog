---
name: fulfillmentcom-apiv2
description: "Fulfillment.com APIv2 API skill. Use when working with Fulfillment.com APIv2 for users, returns, orders. Covers 15 endpoints."
version: 1.0.0
generator: lapsh
---

# Fulfillment.com APIv2
API version: 2.0

## Auth
OAuth2 | ApiKey x-api-key in header

## Base URL
https://api.fulfillment.com/v2

## Setup
1. Set your API key in the appropriate header
2. GET /users/me -- verify access
3. POST /orders -- create first orders

## Endpoints

15 endpoints across 7 groups. See references/api-spec.lap for full details.

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/me | About Me |

### returns
| Method | Path | Description |
|--------|------|-------------|
| GET | /returns | List Returns |
| PUT | /returns | Inform us of an RMA |

### orders
| Method | Path | Description |
|--------|------|-------------|
| PUT | /orders/{id}/status | Update Order Status |
| PUT | /orders/{id}/ship | Ship an Order |
| GET | /orders/{id} | Order Details |
| DELETE | /orders/{id} | Cancel an Order |
| GET | /orders | List of Orders |
| POST | /orders | New Order |
| GET | /orders/simple | List of Simplified Orders |

### oauth
| Method | Path | Description |
|--------|------|-------------|
| POST | /oauth/access_token | Generate an Access Token |

### inventory
| Method | Path | Description |
|--------|------|-------------|
| GET | /inventory | List of Item Inventories |
| GET | /inventory/full | List of Inventories |

### track
| Method | Path | Description |
|--------|------|-------------|
| GET | /track/{trackingNumber} | Tracking |

### accounting
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounting | List Order Accounting |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all me?" -> GET /users/me
- "List all returns?" -> GET /returns
- "Get order details?" -> GET /orders/{id}
- "Delete a order?" -> DELETE /orders/{id}
- "List all orders?" -> GET /orders
- "Create a order?" -> POST /orders
- "List all simple?" -> GET /orders/simple
- "Create a access_token?" -> POST /oauth/access_token
- "List all inventory?" -> GET /inventory
- "List all full?" -> GET /inventory/full
- "Get track details?" -> GET /track/{trackingNumber}
- "List all accounting?" -> GET /accounting
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
