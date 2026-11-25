---
name: furkot-trips
description: "Furkot Trips API skill. Use when working with Furkot Trips for trip. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Furkot Trips
API version: 1.0.0

## Auth
OAuth2 | OAuth2

## Base URL
https://trips.furkot.com/pub/api

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /trip -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### trip
| Method | Path | Description |
|--------|------|-------------|
| GET | /trip | list user's trips |
| GET | /trip/{trip_id}/stop | list stops for a trip identified by {trip_id} |
| GET | /trip/{trip_id}/skipped | list of skipped stops for a trip identified by {trip_id} |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all trip?" -> GET /trip
- "List all stop?" -> GET /trip/{trip_id}/stop
- "List all skipped?" -> GET /trip/{trip_id}/skipped
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
