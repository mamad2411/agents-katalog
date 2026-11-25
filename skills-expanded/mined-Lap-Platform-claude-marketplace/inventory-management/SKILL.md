---
name: inventory-management
description: "Inventory Management API skill. Use when working with Inventory Management for inventory, inventories, feeds. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Inventory Management

## Auth
ApiKey WM_SEC.ACCESS_TOKEN in header

## Base URL
https://marketplace.walmartapis.com

## Setup
1. Set your API key in the appropriate header
2. GET /v3/inventory -- verify access
3. POST /v3/feeds -- create first feeds

## Endpoints

7 endpoints across 4 groups. See references/api-spec.lap for full details.

### inventory
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/inventory | Inventory |
| PUT | /v3/inventory | Update inventory |

### inventories
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/inventories/{sku} | Single Item Inventory by Ship Node |
| PUT | /v3/inventories/{sku} | Update Item Inventory per Ship Node |
| GET | /v3/inventories | Multiple Item Inventory for All Ship Nodes |

### feeds
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/feeds | Bulk Item Inventory Update |

### fulfillment
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/fulfillment/inventory | WFS Inventory |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all inventory?" -> GET /v3/inventory
- "Get inventory details?" -> GET /v3/inventories/{sku}
- "Update a inventory?" -> PUT /v3/inventories/{sku}
- "Create a feed?" -> POST /v3/feeds
- "List all inventories?" -> GET /v3/inventories
- "List all inventory?" -> GET /v3/fulfillment/inventory
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
