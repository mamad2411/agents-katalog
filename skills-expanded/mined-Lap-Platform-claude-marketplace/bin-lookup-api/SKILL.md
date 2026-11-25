---
name: bin-lookup-api
description: "BIN Lookup API skill. Use when working with BIN Lookup for {bin}, balance. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# BIN Lookup API
API version: 1.0.0-oas3

## Auth
ApiKey api_key in query

## Base URL
https://api.bintable.com/v1

## Setup
1. Set your API key in the appropriate header
2. GET /balance -- verify access

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### {bin}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{bin} | Lookup for bin |

### balance
| Method | Path | Description |
|--------|------|-------------|
| GET | /balance | Check Balance |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all balance?" -> GET /balance
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
