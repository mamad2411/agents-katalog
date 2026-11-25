---
name: ecosystem-api
description: "Ecosystem API skill. Use when working with Ecosystem for ecosystems. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# Ecosystem API
API version: 0.0.6

## Auth
No authentication required.

## Base URL
https://api.apideck.com

## Setup
1. No auth setup needed
2. GET /ecosystems/{ecosystem_id}/listings -- verify access

## Endpoints

12 endpoints across 1 groups. See references/api-spec.lap for full details.

### ecosystems
| Method | Path | Description |
|--------|------|-------------|
| GET | /ecosystems/{ecosystem_id} | Get ecosystem |
| GET | /ecosystems/{ecosystem_id}/listings | List listings |
| GET | /ecosystems/{ecosystem_id}/listings/{id} | Get listing |
| GET | /ecosystems/{ecosystem_id}/categories | List categories |
| GET | /ecosystems/{ecosystem_id}/categories/{id} | Get category |
| GET | /ecosystems/{ecosystem_id}/categories/{id}/listings | List category listings |
| GET | /ecosystems/{ecosystem_id}/collections | List collections |
| GET | /ecosystems/{ecosystem_id}/collections/{id} | Get collection |
| GET | /ecosystems/{ecosystem_id}/collections/{id}/listings | List collection listings |
| GET | /ecosystems/{ecosystem_id}/products | List products |
| GET | /ecosystems/{ecosystem_id}/products/{id} | Get product |
| GET | /ecosystems/{ecosystem_id}/products/{id}/listings | List product listings |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get ecosystem details?" -> GET /ecosystems/{ecosystem_id}
- "List all listings?" -> GET /ecosystems/{ecosystem_id}/listings
- "Get listing details?" -> GET /ecosystems/{ecosystem_id}/listings/{id}
- "List all categories?" -> GET /ecosystems/{ecosystem_id}/categories
- "Get category details?" -> GET /ecosystems/{ecosystem_id}/categories/{id}
- "List all listings?" -> GET /ecosystems/{ecosystem_id}/categories/{id}/listings
- "List all collections?" -> GET /ecosystems/{ecosystem_id}/collections
- "Get collection details?" -> GET /ecosystems/{ecosystem_id}/collections/{id}
- "List all listings?" -> GET /ecosystems/{ecosystem_id}/collections/{id}/listings
- "List all products?" -> GET /ecosystems/{ecosystem_id}/products
- "Get product details?" -> GET /ecosystems/{ecosystem_id}/products/{id}
- "List all listings?" -> GET /ecosystems/{ecosystem_id}/products/{id}/listings

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
