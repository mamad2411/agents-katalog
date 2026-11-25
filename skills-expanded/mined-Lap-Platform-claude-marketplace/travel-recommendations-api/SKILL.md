---
name: travel-recommendations-api
description: "Travel Recommendations API skill. Use when working with Travel Recommendations for reference-data. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Travel Recommendations API
API version: 1.0.4

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /reference-data/recommended-locations -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### reference-data
| Method | Path | Description |
|--------|------|-------------|
| GET | /reference-data/recommended-locations | GET recommended destinations |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all recommended-locations?" -> GET /reference-data/recommended-locations

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
