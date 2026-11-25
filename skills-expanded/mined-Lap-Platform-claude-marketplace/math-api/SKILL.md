---
name: math-api
description: "Math API skill. Use when working with Math for media. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Math API
API version: 1.0.0

## Auth
ApiKey cookie in header

## Base URL
https://wikimedia.org/api/rest_v1

## Setup
1. Set your API key in the appropriate header
2. GET /media/math/formula/{hash} -- verify access
3. POST /media/math/check/{type} -- create first check

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### media
| Method | Path | Description |
|--------|------|-------------|
| POST | /media/math/check/{type} | Check and normalize a TeX formula. |
| GET | /media/math/formula/{hash} | Get a previously-stored formula |
| GET | /media/math/render/{format}/{hash} | Get rendered formula in the given format. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get formula details?" -> GET /media/math/formula/{hash}
- "Get render details?" -> GET /media/math/render/{format}/{hash}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
