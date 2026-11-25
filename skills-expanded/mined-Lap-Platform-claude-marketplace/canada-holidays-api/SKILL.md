---
name: canada-holidays-api
description: "Canada Holidays API skill. Use when working with Canada Holidays for api. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Canada Holidays API
API version: 1.8.0

## Auth
No authentication required.

## Base URL
https://canada-holidays.ca

## Setup
1. No auth setup needed
2. GET /api/v1 -- verify access

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1 | root |
| GET | /api/v1/holidays | Get all holidays |
| GET | /api/v1/provinces | Get all provinces |
| GET | /api/v1/provinces/{provinceId} | Get a province or territory by abbreviation |
| GET | /api/v1/holidays/{holidayId} | Get a holiday by id |
| GET | /api/v1/spec | Get JSON schema |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all api?" -> GET /api/v1
- "List all holidays?" -> GET /api/v1/holidays
- "List all provinces?" -> GET /api/v1/provinces
- "Get province details?" -> GET /api/v1/provinces/{provinceId}
- "Get holiday details?" -> GET /api/v1/holidays/{holidayId}
- "List all spec?" -> GET /api/v1/spec

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
