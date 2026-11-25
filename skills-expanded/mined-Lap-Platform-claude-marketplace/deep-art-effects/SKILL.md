---
name: deep-art-effects
description: "Deep Art Effects API skill. Use when working with Deep Art Effects for noauth. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Deep Art Effects
API version: 2017-02-10T16:24:46Z

## Auth
ApiKey x-api-key in header | ApiKey Authorization in header

## Base URL
https://api.deeparteffects.com/v1

## Setup
1. Set your API key in the appropriate header
2. GET /noauth/result -- verify access
3. POST /noauth/upload -- create first upload

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### noauth
| Method | Path | Description |
|--------|------|-------------|
| GET | /noauth/result |  |
| GET | /noauth/styles |  |
| POST | /noauth/upload |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all result?" -> GET /noauth/result
- "List all styles?" -> GET /noauth/styles
- "Create a upload?" -> POST /noauth/upload
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
