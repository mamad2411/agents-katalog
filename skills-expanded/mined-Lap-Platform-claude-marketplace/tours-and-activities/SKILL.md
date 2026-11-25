---
name: tours-and-activities
description: "Tours and Activities API skill. Use when working with Tours and Activities for shopping. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Tours and Activities
API version: 1.0.2

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /shopping/activities -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### shopping
| Method | Path | Description |
|--------|------|-------------|
| GET | /shopping/activities | Returns Activities around a given location |
| GET | /shopping/activities/by-square | Returns Activities around a given location |
| GET | /shopping/activities/{activityId} | Retrieve one activity by its id |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all activities?" -> GET /shopping/activities
- "List all by-square?" -> GET /shopping/activities/by-square
- "Get activity details?" -> GET /shopping/activities/{activityId}

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
