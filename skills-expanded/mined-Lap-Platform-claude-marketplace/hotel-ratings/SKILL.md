---
name: hotel-ratings
description: "Hotel Ratings API skill. Use when working with Hotel Ratings for e-reputation. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Hotel Ratings
API version: 1.0.2

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v2

## Setup
1. No auth setup needed
2. GET /e-reputation/hotel-sentiments -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### e-reputation
| Method | Path | Description |
|--------|------|-------------|
| GET | /e-reputation/hotel-sentiments | Get sentiments by Amadeus Hotel Ids |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all hotel-sentiments?" -> GET /e-reputation/hotel-sentiments

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
