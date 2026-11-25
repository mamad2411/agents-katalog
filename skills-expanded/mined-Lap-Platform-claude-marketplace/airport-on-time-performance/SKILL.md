---
name: airport-on-time-performance
description: "Airport On-Time Performance API skill. Use when working with Airport On-Time Performance for airport. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Airport On-Time Performance
API version: 1.0.4

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /airport/predictions/on-time -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### airport
| Method | Path | Description |
|--------|------|-------------|
| GET | /airport/predictions/on-time | Returns a percentage of on-time flight departures from a given airport. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all on-time?" -> GET /airport/predictions/on-time

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
