---
name: brandlovers-marketplace-api-v1
description: "BrandLovers Marketplace API V1 API skill. Use when working with BrandLovers Marketplace API V1 for products, product, orders. Covers 36 endpoints."
version: 1.0.0
generator: lapsh
---

# BrandLovers Marketplace API V1
API version: 1.0.0

## Auth
ApiKey authorization in header

## Base URL
https://api.brandlovers.com/marketplace/v1

## Setup
1. Set your API key in the appropriate header
2. GET /products -- verify access
3. POST /products -- create first products

## Endpoints

36 endpoints across 6 groups. See references/api-spec.lap for full details.

### products
| Method | Path | Description |
|--------|------|-------------|
| POST | /products | Allows new products from the seller to be loaded into the marketplace |
| GET | /products | Returns a list of products loaded into BrandLovers Marketplace |
| GET | /products/status | Returns seller products status in the marketplace |
| PUT | /products/status | Bulk enable/disable products in the marketplace |
| PUT | /products/prices | Allows bulk update of product prices. |
| PUT | /products/stocks | Bulk product stock update |
| GET | /products/status/selling | Returns products that are successfully listed for sale. |

### product
| Method | Path | Description |
|--------|------|-------------|
| GET | /product/{skuSellerId} | Returns details of a single product using the seller `skuSellerId` |
| PUT | /product/{skuSellerId} | Update product details |
| POST | /product | Create a new product to the marketplace |
| PUT | /product/{skuSellerId}/status | Enable/disable a single product in the Marketplace |
| PUT | /product/{skuSellerId}/stock | Update a single product stock |
| PUT | /product/{skuSellerId}/prices | Allows seller to update prices of a single SKU |

### orders
| Method | Path | Description |
|--------|------|-------------|
| GET | /orders | Returns orders details |
| POST | /orders/shipments/delivered | Bulk update of order shipments |
| GET | /orders/shipments/delivered | Returns list of shipments |
| POST | /orders/shipments/shipped | Bulk update of order shipments |
| GET | /orders/shipments/shipped | Returns a list of shipments shipped |
| GET | /orders/status/approved | Return list of approved orders |
| GET | /orders/status/canceled | Returns lists of canceled orders |
| GET | /orders/status/delivered | Returns a list of orders successfully delivered associated with this seller. |
| GET | /orders/status/new | Returns a list of orders flagged as new. |
| GET | /orders/status/partiallyDelivered | Returns a list of partially deliverd orders |
| GET | /orders/status/partiallySent | Returns a list of orders partially fullfiled |
| GET | /orders/status/sent | Returns a list with orders fully sent |

### order
| Method | Path | Description |
|--------|------|-------------|
| GET | /order/{orderId} | Returns all details of a order |
| POST | /order/{orderId}/shipment/cancel | Confirm shipment canceletion (when requested by the customer) or failure to deliver |
| POST | /order/{orderId}/shipment/delivered | Confirms that a shipment was delivered |
| POST | /order/{orderId}/shipment/exchange | Confirm item exchange |
| POST | /order/{orderId}/shipment/return | Confirm order item return and refund |
| POST | /order/{orderId}/shipment/sent | Update new order to include shipment information |

### tickets
| Method | Path | Description |
|--------|------|-------------|
| GET | /tickets | Get customers trouble tickets |

### ticket
| Method | Path | Description |
|--------|------|-------------|
| POST | /ticket | Creates a new trouble ticket |
| GET | /ticket/{ticketId}/messages | Get trouble ticket messages |
| POST | /ticket/{ticketId}/message | Add new message to trouble ticket |
| PUT | /ticket/{ticketId}/status | Update trouble ticket status |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a product?" -> POST /products
- "List all products?" -> GET /products
- "Get product details?" -> GET /product/{skuSellerId}
- "Update a product?" -> PUT /product/{skuSellerId}
- "Create a product?" -> POST /product
- "List all status?" -> GET /products/status
- "List all selling?" -> GET /products/status/selling
- "List all orders?" -> GET /orders
- "Create a delivered?" -> POST /orders/shipments/delivered
- "List all delivered?" -> GET /orders/shipments/delivered
- "Create a shipped?" -> POST /orders/shipments/shipped
- "List all shipped?" -> GET /orders/shipments/shipped
- "List all approved?" -> GET /orders/status/approved
- "List all canceled?" -> GET /orders/status/canceled
- "List all delivered?" -> GET /orders/status/delivered
- "List all new?" -> GET /orders/status/new
- "List all partiallyDelivered?" -> GET /orders/status/partiallyDelivered
- "List all partiallySent?" -> GET /orders/status/partiallySent
- "List all sent?" -> GET /orders/status/sent
- "Get order details?" -> GET /order/{orderId}
- "Create a cancel?" -> POST /order/{orderId}/shipment/cancel
- "Create a delivered?" -> POST /order/{orderId}/shipment/delivered
- "Create a exchange?" -> POST /order/{orderId}/shipment/exchange
- "Create a return?" -> POST /order/{orderId}/shipment/return
- "Create a sent?" -> POST /order/{orderId}/shipment/sent
- "List all tickets?" -> GET /tickets
- "Create a ticket?" -> POST /ticket
- "List all messages?" -> GET /ticket/{ticketId}/messages
- "Create a message?" -> POST /ticket/{ticketId}/message
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
