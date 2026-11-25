---
name: exchangerate-api
description: "ExchangeRate-API API skill. Use when working with ExchangeRate-API for latest. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# ExchangeRate-API
API version: 4

## Auth
No authentication required.

## Base URL
https://api.exchangerate-api.com/v4

## Setup
1. No auth setup needed
2. GET /latest/{base_currency} -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### latest
| Method | Path | Description |
|--------|------|-------------|
| GET | /latest/{base_currency} | Returns latest exchange rates in parameter-supplied base currency. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get latest details?" -> GET /latest/{base_currency}

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
