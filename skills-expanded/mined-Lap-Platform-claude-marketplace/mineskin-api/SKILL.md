---
name: mineskin-api
description: "MineSkin API skill. Use when working with MineSkin for generate, get, validate. Covers 9 endpoints."
version: 1.0.0
generator: lapsh
---

# MineSkin API
API version: 1.0.0

## Auth
Bearer bearer

## Base URL
https://api.mineskin.org

## Setup
1. Set Authorization header with your Bearer token
2. GET /get/delay -- verify access
3. POST /generate/url -- create first url

## Endpoints

9 endpoints across 3 groups. See references/api-spec.lap for full details.

### generate
| Method | Path | Description |
|--------|------|-------------|
| POST | /generate/url |  |
| POST | /generate/upload |  |
| POST | /generate/user |  |

### get
| Method | Path | Description |
|--------|------|-------------|
| GET | /get/delay |  |
| GET | /get/id/{id} | Deprecated. Use /get/uuid instead. |
| GET | /get/uuid/{uuid} |  |
| GET | /get/list/{page} |  |

### validate
| Method | Path | Description |
|--------|------|-------------|
| GET | /validate/name/{name} |  |
| GET | /validate/uuid/{uuid} |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a url?" -> POST /generate/url
- "Create a upload?" -> POST /generate/upload
- "Create a user?" -> POST /generate/user
- "List all delay?" -> GET /get/delay
- "Get id details?" -> GET /get/id/{id}
- "Get uuid details?" -> GET /get/uuid/{uuid}
- "Get list details?" -> GET /get/list/{page}
- "Get name details?" -> GET /validate/name/{name}
- "Get uuid details?" -> GET /validate/uuid/{uuid}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
