---
name: random-lottery-number-generator-api
description: "Random Lottery Number generator API skill. Use when working with Random Lottery Number generator for lottery. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Random Lottery Number generator API
API version: 1.5

## Auth
Bearer bearer

## Base URL
https://api.fungenerators.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /lottery/countries -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### lottery
| Method | Path | Description |
|--------|------|-------------|
| GET | /lottery/countries | Get the complete list of countries supported in the number generation API. |
| GET | /lottery/supported | Get the list of supported lottery games supported in the given country. |
| GET | /lottery/draw | Generate random draw for a given lottery game. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all countries?" -> GET /lottery/countries
- "List all supported?" -> GET /lottery/supported
- "List all draw?" -> GET /lottery/draw
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
