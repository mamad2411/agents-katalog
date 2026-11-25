---
name: globalwinescore-api-documentation
description: "GlobalWineScore API Documentation API skill. Use when working with GlobalWineScore API Documentation for globalwinescores. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# GlobalWineScore API Documentation
API version: 8234aab51481d37a30757d925b7f4221a659427e

## Auth
ApiKey Authorization in header

## Base URL
https://api.globalwinescore.com

## Setup
1. Set your API key in the appropriate header
2. GET /globalwinescores/latest/ -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### globalwinescores
| Method | Path | Description |
|--------|------|-------------|
| GET | /globalwinescores/latest/ | List all latest GWS |
| GET | /globalwinescores/ | List all historical GWS |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all latest?" -> GET /globalwinescores/latest/
- "List all globalwinescores?" -> GET /globalwinescores/
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
