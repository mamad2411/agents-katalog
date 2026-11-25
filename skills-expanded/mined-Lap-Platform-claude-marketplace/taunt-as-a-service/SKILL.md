---
name: taunt-as-a-service
description: "Taunt as a service API skill. Use when working with Taunt as a service for taunt. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Taunt as a service
API version: 1.5

## Auth
ApiKey X-Fungenerators-Api-Secret in header

## Base URL
https://api.fungenerators.com/

## Setup
1. Set your API key in the appropriate header
2. GET /taunt/categories -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### taunt
| Method | Path | Description |
|--------|------|-------------|
| GET | /taunt/categories | Get available taunt generation categories. |
| GET | /taunt/generate | Generated taunts in the given category |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all categories?" -> GET /taunt/categories
- "List all generate?" -> GET /taunt/generate
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
