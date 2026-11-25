---
name: word-associations-api
description: "Word Associations API skill. Use when working with Word Associations for json. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Word Associations API
API version: 1.0

## Auth
ApiKey apikey in query

## Base URL
https://api.wordassociations.net/associations/v1.0

## Setup
1. Set your API key in the appropriate header
2. GET /json/search -- verify access
3. POST /json/search -- create first search

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### json
| Method | Path | Description |
|--------|------|-------------|
| GET | /json/search | Gets associations with the given word or phrase. |
| POST | /json/search | Gets associations with the given word or phrase. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all search?" -> GET /json/search
- "Create a search?" -> POST /json/search
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
