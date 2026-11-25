---
name: name-generation-api
description: "Name Generation API skill. Use when working with Name Generation for name. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Name Generation API
API version: 1.5

## Auth
Bearer bearer

## Base URL
https://api.fungenerators.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /name/categories -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### name
| Method | Path | Description |
|--------|------|-------------|
| GET | /name/categories | Get available name generation categories. |
| GET | /name/generate | Generated names in the given category |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all categories?" -> GET /name/categories
- "List all generate?" -> GET /name/generate
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
