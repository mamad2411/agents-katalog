---
name: flight-delay-prediction
description: "Flight Delay Prediction API skill. Use when working with Flight Delay Prediction for travel. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Flight Delay Prediction
API version: 1.0.6

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /travel/predictions/flight-delay -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### travel
| Method | Path | Description |
|--------|------|-------------|
| GET | /travel/predictions/flight-delay | Return the delay segment where the flight is likely to lay. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all flight-delay?" -> GET /travel/predictions/flight-delay

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
