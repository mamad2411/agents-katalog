---
name: airport-nearest-relevant
description: "Airport Nearest Relevant API skill. Use when working with Airport Nearest Relevant for reference-data. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Airport Nearest Relevant
API version: 1.1.2

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /reference-data/locations/airports -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### reference-data
| Method | Path | Description |
|--------|------|-------------|
| GET | /reference-data/locations/airports | Returns a list of relevant airports near to a given point. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all airports?" -> GET /reference-data/locations/airports

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
