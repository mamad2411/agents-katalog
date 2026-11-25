---
name: trip-purpose-prediction
description: "Trip Purpose Prediction API skill. Use when working with Trip Purpose Prediction for travel. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Trip Purpose Prediction
API version: 1.1.4

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /travel/predictions/trip-purpose -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### travel
| Method | Path | Description |
|--------|------|-------------|
| GET | /travel/predictions/trip-purpose | Returns the forecast purpose of a trip |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all trip-purpose?" -> GET /travel/predictions/trip-purpose

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
