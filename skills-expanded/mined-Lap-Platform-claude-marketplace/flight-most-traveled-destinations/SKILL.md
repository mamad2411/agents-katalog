---
name: flight-most-traveled-destinations
description: "Flight Most Traveled Destinations API skill. Use when working with Flight Most Traveled Destinations for travel. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Flight Most Traveled Destinations
API version: 1.1.1

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /travel/analytics/air-traffic/traveled -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### travel
| Method | Path | Description |
|--------|------|-------------|
| GET | /travel/analytics/air-traffic/traveled | Returns a list of air traffic reports. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all traveled?" -> GET /travel/analytics/air-traffic/traveled

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
