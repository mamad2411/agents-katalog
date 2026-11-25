---
name: safe-place
description: "Safe Place API skill. Use when working with Safe Place for safety. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Safe Place
API version: 1.0.1

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /safety/safety-rated-locations -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### safety
| Method | Path | Description |
|--------|------|-------------|
| GET | /safety/safety-rated-locations | Returns safety rating for a given location and radius. |
| GET | /safety/safety-rated-locations/{safety-rated-locationId} | Retieve safety information of a location by its Id. |
| GET | /safety/safety-rated-locations/by-square | Returns the safety rating of a given area |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all safety-rated-locations?" -> GET /safety/safety-rated-locations
- "Get safety-rated-location details?" -> GET /safety/safety-rated-locations/{safety-rated-locationId}
- "List all by-square?" -> GET /safety/safety-rated-locations/by-square

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
