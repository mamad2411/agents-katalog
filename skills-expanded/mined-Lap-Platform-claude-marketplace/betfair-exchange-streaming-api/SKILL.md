---
name: betfair-exchange-streaming-api
description: "Betfair: Exchange Streaming API skill. Use when working with Betfair: Exchange Streaming for request. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Betfair: Exchange Streaming API
API version: 1.0.1423

## Auth
No authentication required.

## Base URL
http://stream-api.betfair.com:443/api

## Setup
1. No auth setup needed
3. POST /request -- create first request

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### request
| Method | Path | Description |
|--------|------|-------------|
| POST | /request | This is a socket protocol delimited by CRLF (not http) |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a request?" -> POST /request

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
