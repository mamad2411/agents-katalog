---
name: seatmap-display
description: "Seatmap Display API skill. Use when working with Seatmap Display for shopping. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Seatmap Display
API version: 1.9.2

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /shopping/seatmaps -- verify access
3. POST /shopping/seatmaps -- create first seatmaps

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### shopping
| Method | Path | Description |
|--------|------|-------------|
| GET | /shopping/seatmaps | Returns all the seat maps of a given order. |
| POST | /shopping/seatmaps | Returns all the seat maps of a given flightOffer. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all seatmaps?" -> GET /shopping/seatmaps
- "Create a seatmap?" -> POST /shopping/seatmaps

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
