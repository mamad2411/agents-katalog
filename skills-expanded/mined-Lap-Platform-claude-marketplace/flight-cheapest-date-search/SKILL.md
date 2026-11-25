---
name: flight-cheapest-date-search
description: "Flight Cheapest Date Search API skill. Use when working with Flight Cheapest Date Search for shopping. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Flight Cheapest Date Search
API version: 1.0.6

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /shopping/flight-dates -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### shopping
| Method | Path | Description |
|--------|------|-------------|
| GET | /shopping/flight-dates | Find the cheapest flight dates from an origin to a destination. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all flight-dates?" -> GET /shopping/flight-dates

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
