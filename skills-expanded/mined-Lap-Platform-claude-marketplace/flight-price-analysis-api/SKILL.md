---
name: flight-price-analysis-api
description: "Flight Price Analysis API skill. Use when working with Flight Price Analysis for analytics. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Flight Price Analysis API
API version: 1.0.1

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /analytics/itinerary-price-metrics -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### analytics
| Method | Path | Description |
|--------|------|-------------|
| GET | /analytics/itinerary-price-metrics | GET itinerary price metric |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all itinerary-price-metrics?" -> GET /analytics/itinerary-price-metrics

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
