---
name: search-services
description: "Search Services API skill. Use when working with Search Services for search. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Search Services
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://api.archive.org/

## Setup
1. No auth setup needed
2. GET /search/v1/scrape -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search/v1/scrape | Scrape search results from Internet Archive, allowing a scrolling cursor |
| GET | /search/v1/organic | Return relevance-based results from search queries |
| GET | /search/v1/fields | Fields that can be requested |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search scrape?" -> GET /search/v1/scrape
- "Search organic?" -> GET /search/v1/organic
- "List all fields?" -> GET /search/v1/fields

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
