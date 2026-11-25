---
name: flight-offers-search
description: "Flight Offers Search API skill. Use when working with Flight Offers Search for shopping. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Flight Offers Search
API version: 2.2.0

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v2

## Setup
1. No auth setup needed
2. GET /shopping/flight-offers -- verify access
3. POST /shopping/flight-offers -- create first flight-offers

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### shopping
| Method | Path | Description |
|--------|------|-------------|
| POST | /shopping/flight-offers | Return list of Flight Offers based on posted searching criteria. |
| GET | /shopping/flight-offers | Return list of Flight Offers based on searching criteria. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a flight-offer?" -> POST /shopping/flight-offers
- "List all flight-offers?" -> GET /shopping/flight-offers

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
