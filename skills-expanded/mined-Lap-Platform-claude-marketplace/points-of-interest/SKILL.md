---
name: points-of-interest
description: "Points of Interest API skill. Use when working with Points of Interest for reference-data. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Points of Interest
API version: 1.1.1

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /reference-data/locations/pois -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### reference-data
| Method | Path | Description |
|--------|------|-------------|
| GET | /reference-data/locations/pois | Returns points of interest for a given location and radius. |
| GET | /reference-data/locations/pois/{poisId} | Retieve one point of interest by its Id. |
| GET | /reference-data/locations/pois/by-square | Returns points of interest for a given area |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all pois?" -> GET /reference-data/locations/pois
- "Get pois details?" -> GET /reference-data/locations/pois/{poisId}
- "List all by-square?" -> GET /reference-data/locations/pois/by-square

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
