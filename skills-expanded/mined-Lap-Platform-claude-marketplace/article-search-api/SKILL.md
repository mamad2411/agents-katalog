---
name: article-search-api
description: "Article Search API skill. Use when working with Article Search for articlesearch.json. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Article Search API
API version: 1.0.0

## Auth
ApiKey api-key in query

## Base URL
http://api.nytimes.com/svc/search/v2

## Setup
1. Set your API key in the appropriate header
2. GET /articlesearch.json -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### articlesearch.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /articlesearch.json | Article Search |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search articlesearch.json?" -> GET /articlesearch.json
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
