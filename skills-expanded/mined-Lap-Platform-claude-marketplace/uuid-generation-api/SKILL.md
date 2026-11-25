---
name: uuid-generation-api
description: "UUID Generation API skill. Use when working with UUID Generation for uuid. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# UUID Generation API
API version: 1.5

## Auth
ApiKey X-Fungenerators-Api-Secret in header

## Base URL
https://api.fungenerators.com

## Setup
1. Set your API key in the appropriate header
2. GET /uuid -- verify access
3. POST /uuid -- create first uuid

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### uuid
| Method | Path | Description |
|--------|------|-------------|
| GET | /uuid | Generate a random UUID (v4). |
| POST | /uuid | Parse a UUID string and return its version and check whether it is valid. |
| GET | /uuid/version/{version} | Generate a random UUID (v4). |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all uuid?" -> GET /uuid
- "Create a uuid?" -> POST /uuid
- "Get version details?" -> GET /uuid/version/{version}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
