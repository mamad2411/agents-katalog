---
name: flight-availibilities-search
description: "Flight Availibilities Search API skill. Use when working with Flight Availibilities Search for shopping. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Flight Availibilities Search
API version: 1.0.2

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
3. POST /shopping/availability/flight-availabilities -- create first flight-availabilities

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### shopping
| Method | Path | Description |
|--------|------|-------------|
| POST | /shopping/availability/flight-availabilities | Return list of Flight Availabilities based on posted searching criteria. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a flight-availability?" -> POST /shopping/availability/flight-availabilities

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
