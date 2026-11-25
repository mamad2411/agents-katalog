---
name: pos-api
description: "POS API skill. Use when working with POS for pos. Covers 46 endpoints."
version: 1.0.0
generator: lapsh
---

# POS API
API version: 10.24.0

## Auth
ApiKey Authorization in header

## Base URL
https://unify.apideck.com

## Setup
1. Set your API key in the appropriate header
2. GET /pos/orders -- verify access
3. POST /pos/orders -- create first orders

## Endpoints

46 endpoints across 1 groups. See references/api-spec.lap for full details.

### pos
| Method | Path | Description |
|--------|------|-------------|
| GET | /pos/orders | List Orders |
| POST | /pos/orders | Create Order |
| GET | /pos/orders/{id} | Get Order |
| PATCH | /pos/orders/{id} | Update Order |
| DELETE | /pos/orders/{id} | Delete Order |
| POST | /pos/orders/{id}/pay | Pay Order |
| GET | /pos/payments | List Payments |
| POST | /pos/payments | Create Payment |
| GET | /pos/payments/{id} | Get Payment |
| PATCH | /pos/payments/{id} | Update Payment |
| DELETE | /pos/payments/{id} | Delete Payment |
| GET | /pos/merchants | List Merchants |
| POST | /pos/merchants | Create Merchant |
| GET | /pos/merchants/{id} | Get Merchant |
| PATCH | /pos/merchants/{id} | Update Merchant |
| DELETE | /pos/merchants/{id} | Delete Merchant |
| GET | /pos/locations | List Locations |
| POST | /pos/locations | Create Location |
| GET | /pos/locations/{id} | Get Location |
| PATCH | /pos/locations/{id} | Update Location |
| DELETE | /pos/locations/{id} | Delete Location |
| GET | /pos/items | List Items |
| POST | /pos/items | Create Item |
| GET | /pos/items/{id} | Get Item |
| PATCH | /pos/items/{id} | Update Item |
| DELETE | /pos/items/{id} | Delete Item |
| GET | /pos/modifiers | List Modifiers |
| POST | /pos/modifiers | Create Modifier |
| GET | /pos/modifiers/{id} | Get Modifier |
| PATCH | /pos/modifiers/{id} | Update Modifier |
| DELETE | /pos/modifiers/{id} | Delete Modifier |
| GET | /pos/modifier-groups | List Modifier Groups |
| POST | /pos/modifier-groups | Create Modifier Group |
| GET | /pos/modifier-groups/{id} | Get Modifier Group |
| PATCH | /pos/modifier-groups/{id} | Update Modifier Group |
| DELETE | /pos/modifier-groups/{id} | Delete Modifier Group |
| GET | /pos/order-types | List Order Types |
| POST | /pos/order-types | Create Order Type |
| GET | /pos/order-types/{id} | Get Order Type |
| PATCH | /pos/order-types/{id} | Update Order Type |
| DELETE | /pos/order-types/{id} | Delete Order Type |
| GET | /pos/tenders | List Tenders |
| POST | /pos/tenders | Create Tender |
| GET | /pos/tenders/{id} | Get Tender |
| PATCH | /pos/tenders/{id} | Update Tender |
| DELETE | /pos/tenders/{id} | Delete Tender |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all orders?" -> GET /pos/orders
- "Create a order?" -> POST /pos/orders
- "Get order details?" -> GET /pos/orders/{id}
- "Partially update a order?" -> PATCH /pos/orders/{id}
- "Delete a order?" -> DELETE /pos/orders/{id}
- "Create a pay?" -> POST /pos/orders/{id}/pay
- "List all payments?" -> GET /pos/payments
- "Create a payment?" -> POST /pos/payments
- "Get payment details?" -> GET /pos/payments/{id}
- "Partially update a payment?" -> PATCH /pos/payments/{id}
- "Delete a payment?" -> DELETE /pos/payments/{id}
- "List all merchants?" -> GET /pos/merchants
- "Create a merchant?" -> POST /pos/merchants
- "Get merchant details?" -> GET /pos/merchants/{id}
- "Partially update a merchant?" -> PATCH /pos/merchants/{id}
- "Delete a merchant?" -> DELETE /pos/merchants/{id}
- "List all locations?" -> GET /pos/locations
- "Create a location?" -> POST /pos/locations
- "Get location details?" -> GET /pos/locations/{id}
- "Partially update a location?" -> PATCH /pos/locations/{id}
- "Delete a location?" -> DELETE /pos/locations/{id}
- "List all items?" -> GET /pos/items
- "Create a item?" -> POST /pos/items
- "Get item details?" -> GET /pos/items/{id}
- "Partially update a item?" -> PATCH /pos/items/{id}
- "Delete a item?" -> DELETE /pos/items/{id}
- "List all modifiers?" -> GET /pos/modifiers
- "Create a modifier?" -> POST /pos/modifiers
- "Get modifier details?" -> GET /pos/modifiers/{id}
- "Partially update a modifier?" -> PATCH /pos/modifiers/{id}
- "Delete a modifier?" -> DELETE /pos/modifiers/{id}
- "List all modifier-groups?" -> GET /pos/modifier-groups
- "Create a modifier-group?" -> POST /pos/modifier-groups
- "Get modifier-group details?" -> GET /pos/modifier-groups/{id}
- "Partially update a modifier-group?" -> PATCH /pos/modifier-groups/{id}
- "Delete a modifier-group?" -> DELETE /pos/modifier-groups/{id}
- "List all order-types?" -> GET /pos/order-types
- "Create a order-type?" -> POST /pos/order-types
- "Get order-type details?" -> GET /pos/order-types/{id}
- "Partially update a order-type?" -> PATCH /pos/order-types/{id}
- "Delete a order-type?" -> DELETE /pos/order-types/{id}
- "List all tenders?" -> GET /pos/tenders
- "Create a tender?" -> POST /pos/tenders
- "Get tender details?" -> GET /pos/tenders/{id}
- "Partially update a tender?" -> PATCH /pos/tenders/{id}
- "Delete a tender?" -> DELETE /pos/tenders/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
