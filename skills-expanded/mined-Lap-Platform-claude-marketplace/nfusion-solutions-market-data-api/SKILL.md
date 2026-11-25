---
name: nfusion-solutions-market-data-api
description: "nFusion Solutions Market Data API skill. Use when working with nFusion Solutions Market Data for api. Covers 19 endpoints."
version: 1.0.0
generator: lapsh
---

# nFusion Solutions Market Data API
API version: 1

## Auth
ApiKey token in query

## Base URL
https://api.nfusionsolutions.biz

## Setup
1. Set your API key in the appropriate header
2. GET /api/v1/Currencies/rate/supported -- verify access
3. POST /api/v1/Currencies/adjustments -- create first adjustments

## Endpoints

19 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/Currencies/rate/supported | Get list of currencies supported by the rate endpoint |
| GET | /api/v1/Currencies/summary/supported | Get list of currency pairs supported by the Summary endpoint |
| GET | /api/v1/Currencies/history/supported | Get list of currency pairs supported by the history endpoint |
| GET | /api/v1/Currencies/rate | Get latest mid rate for requested currency pairs |
| GET | /api/v1/Currencies/summary | Get latest Summary for requested currency pairs |
| GET | /api/v1/Currencies/history | Get historical prices for requested currency pairs |
| GET | /api/v1/Currencies/adjustments | Read the currency adjustments |
| POST | /api/v1/Currencies/adjustments | Update the currency adjustments |
| GET | /api/v1/Metals/supported/currency | Get list of currencies supported by metals endpoints for currency conversion |
| GET | /api/v1/Metals/spot/supported | Get list of symbols supported by the spot endpoints |
| GET | /api/v1/Metals/spot/summary | Get latest Spot Summary for requested metals |
| GET | /api/v1/Metals/spot/history | Get historical Spot prices for requested metals |
| GET | /api/v1/Metals/spot/ratio/summary | Get latest Spot Summary for requested metal ratios |
| GET | /api/v1/Metals/spot/ratio/history | Get historical Spot Ratio prices for requested metals |
| GET | /api/v1/Metals/benchmark/supported | Get list of symbols supported by the benchmark endpoints |
| GET | /api/v1/Metals/benchmark/summary | Get latest Benchmark prices for requested metals |
| GET | /api/v1/Metals/benchmark/history | Get historical benchmark prices for requested metals |
| GET | /api/v1/Metals/adjustments | Read the spot adjustments |
| POST | /api/v1/Metals/adjustments | Update the spot adjustments |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all supported?" -> GET /api/v1/Currencies/rate/supported
- "List all supported?" -> GET /api/v1/Currencies/summary/supported
- "List all supported?" -> GET /api/v1/Currencies/history/supported
- "List all rate?" -> GET /api/v1/Currencies/rate
- "List all summary?" -> GET /api/v1/Currencies/summary
- "List all history?" -> GET /api/v1/Currencies/history
- "List all adjustments?" -> GET /api/v1/Currencies/adjustments
- "Create a adjustment?" -> POST /api/v1/Currencies/adjustments
- "List all currency?" -> GET /api/v1/Metals/supported/currency
- "List all supported?" -> GET /api/v1/Metals/spot/supported
- "List all summary?" -> GET /api/v1/Metals/spot/summary
- "List all history?" -> GET /api/v1/Metals/spot/history
- "List all summary?" -> GET /api/v1/Metals/spot/ratio/summary
- "List all history?" -> GET /api/v1/Metals/spot/ratio/history
- "List all supported?" -> GET /api/v1/Metals/benchmark/supported
- "List all summary?" -> GET /api/v1/Metals/benchmark/summary
- "List all history?" -> GET /api/v1/Metals/benchmark/history
- "List all adjustments?" -> GET /api/v1/Metals/adjustments
- "Create a adjustment?" -> POST /api/v1/Metals/adjustments
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
