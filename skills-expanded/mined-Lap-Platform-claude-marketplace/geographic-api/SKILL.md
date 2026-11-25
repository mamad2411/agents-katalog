---
name: geographic-api
description: "Geographic API skill. Use when working with Geographic for query.json. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Geographic API
API version: 1.0.0

## Auth
ApiKey api-key in query

## Base URL
http://api.nytimes.com/svc/semantic/v2/geocodes

## Setup
1. Set your API key in the appropriate header
2. GET /query.json -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### query.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /query.json | Geographic API |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search query.json?" -> GET /query.json
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
