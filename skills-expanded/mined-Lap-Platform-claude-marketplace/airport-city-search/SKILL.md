---
name: airport-city-search
description: "Airport & City Search API skill. Use when working with Airport & City Search for reference-data. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Airport & City Search
API version: 1.2.3

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /reference-data/locations -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### reference-data
| Method | Path | Description |
|--------|------|-------------|
| GET | /reference-data/locations | Returns a list of airports and cities matching a given keyword. |
| GET | /reference-data/locations/{locationId} | Returns a specific airports or cities based on its id. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all locations?" -> GET /reference-data/locations
- "Get location details?" -> GET /reference-data/locations/{locationId}

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
