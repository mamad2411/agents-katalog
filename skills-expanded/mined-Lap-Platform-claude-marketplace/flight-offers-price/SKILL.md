---
name: flight-offers-price
description: "Flight Offers Price API skill. Use when working with Flight Offers Price for shopping. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Flight Offers Price
API version: 1.3.0

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
3. POST /shopping/flight-offers/pricing -- create first pricing

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### shopping
| Method | Path | Description |
|--------|------|-------------|
| POST | /shopping/flight-offers/pricing | Confirm pricing of given flightOffers. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a pricing?" -> POST /shopping/flight-offers/pricing

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
