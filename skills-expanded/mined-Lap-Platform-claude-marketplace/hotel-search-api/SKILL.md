---
name: hotel-search-api
description: "Hotel Search API skill. Use when working with Hotel Search for shopping. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Hotel Search API
API version: 3.0.9

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v3

## Setup
1. No auth setup needed
2. GET /shopping/hotel-offers -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### shopping
| Method | Path | Description |
|--------|------|-------------|
| GET | /shopping/hotel-offers | getMultiHotelOffers |
| GET | /shopping/hotel-offers/{offerId} | getOfferPricing |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all hotel-offers?" -> GET /shopping/hotel-offers
- "Get hotel-offer details?" -> GET /shopping/hotel-offers/{offerId}

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
