---
name: hotel-name-autocomplete
description: "Hotel Name Autocomplete API skill. Use when working with Hotel Name Autocomplete for reference-data. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Hotel Name Autocomplete
API version: 1.0.3

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /reference-data/locations/hotel -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### reference-data
| Method | Path | Description |
|--------|------|-------------|
| GET | /reference-data/locations/hotel | Returns a list of hotels matching a given keyword. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all hotel?" -> GET /reference-data/locations/hotel

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
