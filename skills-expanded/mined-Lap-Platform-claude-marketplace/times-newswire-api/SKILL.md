---
name: times-newswire-api
description: "Times Newswire API skill. Use when working with Times Newswire for content, content.json. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Times Newswire API
API version: 3.0.0

## Auth
ApiKey api-key in query

## Base URL
http://api.nytimes.com/svc/news/v3

## Setup
1. Set your API key in the appropriate header
2. GET /content.json -- verify access

## Endpoints

3 endpoints across 2 groups. See references/api-spec.lap for full details.

### content
| Method | Path | Description |
|--------|------|-------------|
| GET | /content/{source}/{section}.json |  |
| GET | /content/{source}/{section}/{time-period}.json |  |

### content.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /content.json |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get content details?" -> GET /content/{source}/{section}.json
- "Get content details?" -> GET /content/{source}/{section}/{time-period}.json
- "List all content.json?" -> GET /content.json
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
