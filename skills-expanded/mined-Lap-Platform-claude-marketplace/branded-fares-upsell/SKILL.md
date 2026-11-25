---
name: branded-fares-upsell
description: "Branded Fares Upsell API skill. Use when working with Branded Fares Upsell for shopping. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Branded Fares Upsell
API version: 1.2.0

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
3. POST /shopping/flight-offers/upselling -- create first upselling

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### shopping
| Method | Path | Description |
|--------|------|-------------|
| POST | /shopping/flight-offers/upselling | Return a list of upsell Flight Offers based on given Flight Offers |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a upselling?" -> POST /shopping/flight-offers/upselling

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
