---
name: taxratesio-api
description: "Taxrates.io API skill. Use when working with Taxrates.io for tax. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Taxrates.io API

## Auth
ApiKey Authorization in header

## Base URL
https://api.taxrates.io/api

## Setup
1. Set your API key in the appropriate header
2. GET /v3/tax/rates -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### tax
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/tax/rates | All tax rates |
| GET | /v1/tax/ip | Tax rates by IP address |
| GET | /v1/tax/countrycode | Tax rates by Country Code |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all rates?" -> GET /v3/tax/rates
- "List all ip?" -> GET /v1/tax/ip
- "List all countrycode?" -> GET /v1/tax/countrycode
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
