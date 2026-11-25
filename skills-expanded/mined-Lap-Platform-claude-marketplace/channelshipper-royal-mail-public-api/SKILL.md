---
name: channelshipper-royal-mail-public-api
description: "ChannelShipper & Royal Mail Public API skill. Use when working with ChannelShipper & Royal Mail Public for version, orders, manifests. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# ChannelShipper & Royal Mail Public API
API version: 1.0.0

## Auth
ApiKey Authorization in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /version -- verify access
3. POST /orders -- create first orders

## Endpoints

14 endpoints across 4 groups. See references/api-spec.lap for full details.

### version
| Method | Path | Description |
|--------|------|-------------|
| GET | /version | Get API version details. |

### orders
| Method | Path | Description |
|--------|------|-------------|
| GET | /orders/{orderIdentifiers} | Retrieve specific orders |
| DELETE | /orders/{orderIdentifiers} | Delete orders |
| PUT | /orders/status | Set order status |
| GET | /orders/{orderIdentifiers}/full | Retrieve details of the specific orders |
| GET | /orders | Retrieve pageable list of orders |
| POST | /orders | Create orders |
| GET | /orders/full | Retrieve pageable list of orders with details |
| GET | /orders/{orderIdentifiers}/label | Return a single PDF file with generated label and/or associated document(s) |

### manifests
| Method | Path | Description |
|--------|------|-------------|
| POST | /manifests | Manifest eligible orders |
| POST | /manifests/retry/{manifestIdentifier} | Retry manifest |
| GET | /manifests/{manifestIdentifier} | Get manifest |

### returns
| Method | Path | Description |
|--------|------|-------------|
| GET | /returns/services | List available return services |
| POST | /returns | Create a return shipment |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all version?" -> GET /version
- "Get order details?" -> GET /orders/{orderIdentifiers}
- "Delete a order?" -> DELETE /orders/{orderIdentifiers}
- "List all full?" -> GET /orders/{orderIdentifiers}/full
- "List all orders?" -> GET /orders
- "Create a order?" -> POST /orders
- "List all full?" -> GET /orders/full
- "List all label?" -> GET /orders/{orderIdentifiers}/label
- "Create a manifest?" -> POST /manifests
- "Get manifest details?" -> GET /manifests/{manifestIdentifier}
- "List all services?" -> GET /returns/services
- "Create a return?" -> POST /returns
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
