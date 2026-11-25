---
name: calorieninjas
description: "CalorieNinjas API skill. Use when working with CalorieNinjas for nutrition. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# CalorieNinjas
API version: 1.0.0

## Auth
ApiKey api_key in header

## Base URL
api.calorieninjas.com

## Setup
1. Set your API key in the appropriate header
2. GET /v1/nutrition -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### nutrition
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/nutrition | Get nutrition text for an input string containing food and beverage words. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search nutrition?" -> GET /v1/nutrition
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
