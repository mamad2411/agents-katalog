---
name: truanon-private-api
description: "TruAnon Private API skill. Use when working with TruAnon Private for api. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# TruAnon Private API

## Auth
Bearer token

## Base URL
https://staging.truanon.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /api/get_profile -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/get_profile | Get Profile |
| GET | /api/request_token | Get Token |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all get_profile?" -> GET /api/get_profile
- "List all request_token?" -> GET /api/request_token
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
