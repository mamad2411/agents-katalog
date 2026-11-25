---
name: movie-reviews-api
description: "Movie Reviews API skill. Use when working with Movie Reviews for reviews, critics. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Movie Reviews API
API version: 2.0.0

## Auth
ApiKey api-key in query

## Base URL
http://api.nytimes.com/svc/movies/v2

## Setup
1. Set your API key in the appropriate header
2. GET /reviews/search.json -- verify access

## Endpoints

3 endpoints across 2 groups. See references/api-spec.lap for full details.

### reviews
| Method | Path | Description |
|--------|------|-------------|
| GET | /reviews/{resource-type}.json |  |
| GET | /reviews/search.json |  |

### critics
| Method | Path | Description |
|--------|------|-------------|
| GET | /critics/{resource-type}.json |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get review details?" -> GET /reviews/{resource-type}.json
- "Search search.json?" -> GET /reviews/search.json
- "Get critic details?" -> GET /critics/{resource-type}.json
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
