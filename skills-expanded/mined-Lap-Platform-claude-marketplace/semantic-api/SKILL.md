---
name: semantic-api
description: "Semantic API skill. Use when working with Semantic for name, search.json. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Semantic API
API version: 2.0.0

## Auth
ApiKey api-key in query

## Base URL
http://api.nytimes.com/svc/semantic/v2/concept

## Setup
1. Set your API key in the appropriate header
2. GET /search.json -- verify access

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### name
| Method | Path | Description |
|--------|------|-------------|
| GET | /name/{concept-type}/{specific-concept}.json |  |

### search.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /search.json |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search name?" -> GET /name/{concept-type}/{specific-concept}.json
- "Search search.json?" -> GET /search.json
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
