---
name: football-prediction-api
description: "Football Prediction API skill. Use when working with Football Prediction for api. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Football Prediction API
API version: 2

## Auth
ApiKey X-RapidApi-Key in header

## Base URL
https://football-prediction-api.p.rapidapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /api/v2/predictions -- verify access

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v2/predictions | This endpoint returns by default the next non-expired football predictions. URL parameters can be specified to show specific date in the past or future or to filter by federation and prediction market name. |
| GET | /api/v2/predictions/{id} | Returns all predictions available for a match id. |
| GET | /api/v2/performance-stats | Returns predictions accuracy in the last 1, 7, 14, 30 days. |
| GET | /api/v2/list-federations | Returns an array of all the available federations. |
| GET | /api/v2/list-markets | Returns an array of all the supported prediction markets |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all predictions?" -> GET /api/v2/predictions
- "Get prediction details?" -> GET /api/v2/predictions/{id}
- "List all performance-stats?" -> GET /api/v2/performance-stats
- "List all list-federations?" -> GET /api/v2/list-federations
- "List all list-markets?" -> GET /api/v2/list-markets
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
