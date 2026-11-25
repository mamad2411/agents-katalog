---
name: keyserv
description: "KeyServ API skill. Use when working with KeyServ for KeysApi, ProductsApi, SubscriptionsApi. Covers 24 endpoints."
version: 1.0.0
generator: lapsh
---

# KeyServ
API version: 1.4.5

## Auth
ApiKey X-Api-Key in header

## Base URL
https://keyserv.solutions

## Setup
1. Set your API key in the appropriate header
2. GET /v1/KeysApi/Find/{serial} -- verify access
3. POST /v1/ProductsApi/Count -- create first Count

## Endpoints

24 endpoints across 3 groups. See references/api-spec.lap for full details.

### KeysApi
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/KeysApi/Find/{serial} |  |
| GET | /v1/KeysApi/Current/{serial} |  |
| GET | /v1/KeysApi/Custom/{serial} |  |
| GET | /v1/KeysApi/Expiry/{serial} |  |

### ProductsApi
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/ProductsApi/Count |  |
| POST | /v1/ProductsApi/Find |  |
| POST | /v1/ProductsApi/List |  |
| PATCH | /v1/ProductsApi |  |
| POST | /v1/ProductsApi |  |
| POST | /v1/ProductsApi/Save |  |
| DELETE | /v1/ProductsApi/{serial} |  |
| POST | /v1/ProductsApi/{serial} |  |

### SubscriptionsApi
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/SubscriptionsApi/Count |  |
| POST | /v1/SubscriptionsApi/Find |  |
| POST | /v1/SubscriptionsApi/List |  |
| PUT | /v1/SubscriptionsApi |  |
| POST | /v1/SubscriptionsApi |  |
| PATCH | /v1/SubscriptionsApi/Disable |  |
| POST | /v1/SubscriptionsApi/Disable |  |
| PATCH | /v1/SubscriptionsApi/Enable |  |
| POST | /v1/SubscriptionsApi/Enable |  |
| POST | /v1/SubscriptionsApi/Save |  |
| DELETE | /v1/SubscriptionsApi/{serial} |  |
| POST | /v1/SubscriptionsApi/{serial} |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get Find details?" -> GET /v1/KeysApi/Find/{serial}
- "Get Current details?" -> GET /v1/KeysApi/Current/{serial}
- "Get Custom details?" -> GET /v1/KeysApi/Custom/{serial}
- "Get Expiry details?" -> GET /v1/KeysApi/Expiry/{serial}
- "Create a Count?" -> POST /v1/ProductsApi/Count
- "Create a Find?" -> POST /v1/ProductsApi/Find
- "Create a List?" -> POST /v1/ProductsApi/List
- "Create a ProductsApi?" -> POST /v1/ProductsApi
- "Create a Save?" -> POST /v1/ProductsApi/Save
- "Delete a ProductsApi?" -> DELETE /v1/ProductsApi/{serial}
- "Create a Count?" -> POST /v1/SubscriptionsApi/Count
- "Create a Find?" -> POST /v1/SubscriptionsApi/Find
- "Create a List?" -> POST /v1/SubscriptionsApi/List
- "Create a SubscriptionsApi?" -> POST /v1/SubscriptionsApi
- "Create a Disable?" -> POST /v1/SubscriptionsApi/Disable
- "Create a Enable?" -> POST /v1/SubscriptionsApi/Enable
- "Create a Save?" -> POST /v1/SubscriptionsApi/Save
- "Delete a SubscriptionsApi?" -> DELETE /v1/SubscriptionsApi/{serial}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
