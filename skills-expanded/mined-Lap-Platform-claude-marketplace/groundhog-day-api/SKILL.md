---
name: groundhog-day-api
description: "Groundhog Day API skill. Use when working with Groundhog Day for api. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Groundhog Day API
API version: 1.2.1

## Auth
No authentication required.

## Base URL
https://virtserver.swaggerhub.com/pcraig3/groundhog-day-api/1.2.1

## Setup
1. No auth setup needed
2. GET /api/v1 -- verify access

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1 | Root |
| GET | /api/v1/groundhogs | Get all groundhogs |
| GET | /api/v1/groundhogs/{slug} | Get a groundhog by slug |
| GET | /api/v1/predictions | Get predictions for a given year |
| GET | /api/v1/spec | Get JSON schema |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all api?" -> GET /api/v1
- "List all groundhogs?" -> GET /api/v1/groundhogs
- "Get groundhog details?" -> GET /api/v1/groundhogs/{slug}
- "List all predictions?" -> GET /api/v1/predictions
- "List all spec?" -> GET /api/v1/spec

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
