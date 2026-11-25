---
name: airportsapi
description: "airportsapi API skill. Use when working with airportsapi for airportsapi. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# airportsapi
API version: v1

## Auth
OAuth2

## Base URL
https://airport-web.appspot.com/_ah/api

## Setup
1. Configure auth: OAuth2
2. GET /airportsapi/v1/airports/{icao_code} -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### airportsapi
| Method | Path | Description |
|--------|------|-------------|
| GET | /airportsapi/v1/airports/{icao_code} |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get airport details?" -> GET /airportsapi/v1/airports/{icao_code}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
