---
name: api-title
description: "API title API skill. Use when working with API title for restrooms. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# API title
API version: 0.0.1

## Auth
No authentication required.

## Base URL
https://www.refugerestrooms.org/api

## Setup
1. No auth setup needed
2. GET /v1/restrooms/by_date -- verify access

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### restrooms
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/restrooms/by_date | Search for restroom records updated or created on or after a given date |
| GET | /v1/restrooms/by_location | Search by location. |
| GET | /v1/restrooms/search | Perform full-text search of restroom records. |
| GET | /v1/restrooms | Get all restroom records ordered by date descending. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all by_date?" -> GET /v1/restrooms/by_date
- "List all by_location?" -> GET /v1/restrooms/by_location
- "Search search?" -> GET /v1/restrooms/search
- "List all restrooms?" -> GET /v1/restrooms

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
