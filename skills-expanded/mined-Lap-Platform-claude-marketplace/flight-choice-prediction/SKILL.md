---
name: flight-choice-prediction
description: "Flight Choice Prediction API skill. Use when working with Flight Choice Prediction for shopping. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Flight Choice Prediction
API version: 2.0.2

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v2

## Setup
1. No auth setup needed
3. POST /shopping/flight-offers/prediction -- create first prediction

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### shopping
| Method | Path | Description |
|--------|------|-------------|
| POST | /shopping/flight-offers/prediction | Predict the choice of flight offers. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a prediction?" -> POST /shopping/flight-offers/prediction

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
