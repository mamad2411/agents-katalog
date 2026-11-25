---
name: location-score
description: "Location Score API skill. Use when working with Location Score for location. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Location Score
API version: 1.0.3

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /location/analytics/category-rated-areas -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### location
| Method | Path | Description |
|--------|------|-------------|
| GET | /location/analytics/category-rated-areas | GET category rated areas |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all category-rated-areas?" -> GET /location/analytics/category-rated-areas

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
