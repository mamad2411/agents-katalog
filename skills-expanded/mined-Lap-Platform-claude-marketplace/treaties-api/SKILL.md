---
name: treaties-api
description: "Treaties API skill. Use when working with Treaties for api. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Treaties API
API version: v1

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /api/GovernmentOrganisation -- verify access

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/BusinessItem/{id} | Returns business item by ID. |
| GET | /api/GovernmentOrganisation | Returns all government organisations. |
| GET | /api/SeriesMembership | Returns all series memberships. |
| GET | /api/Treaty | Returns a list of treaties. |
| GET | /api/Treaty/{id} | Returns a treaty by ID. |
| GET | /api/Treaty/{id}/BusinessItems | Returns business items belonging to the treaty with ID. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get BusinessItem details?" -> GET /api/BusinessItem/{id}
- "List all GovernmentOrganisation?" -> GET /api/GovernmentOrganisation
- "List all SeriesMembership?" -> GET /api/SeriesMembership
- "List all Treaty?" -> GET /api/Treaty
- "Get Treaty details?" -> GET /api/Treaty/{id}
- "List all BusinessItems?" -> GET /api/Treaty/{id}/BusinessItems

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
