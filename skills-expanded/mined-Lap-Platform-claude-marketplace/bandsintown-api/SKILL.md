---
name: bandsintown-api
description: "Bandsintown API skill. Use when working with Bandsintown for artists. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Bandsintown API
API version: 3.0.0

## Auth
No authentication required.

## Base URL
https://rest.bandsintown.com

## Setup
1. No auth setup needed
2. GET /artists/{artistname}/events -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### artists
| Method | Path | Description |
|--------|------|-------------|
| GET | /artists/{artistname} | Get artist information |
| GET | /artists/{artistname}/events | Get upcoming, past, or all artist events, or events within a date range |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get artist details?" -> GET /artists/{artistname}
- "List all events?" -> GET /artists/{artistname}/events

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
