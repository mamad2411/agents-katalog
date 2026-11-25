---
name: openfigi-api
description: "OpenFIGI API skill. Use when working with OpenFIGI for mapping, search, filter. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# OpenFIGI API
API version: 2.0.0

## Auth
ApiKey X-OPENFIGI-APIKEY in header

## Base URL
https://api.openfigi.com/v3

## Setup
1. Set your API key in the appropriate header
2. GET /mapping/values/{key} -- verify access
3. POST /mapping -- create first mapping

## Endpoints

4 endpoints across 3 groups. See references/api-spec.lap for full details.

### mapping
| Method | Path | Description |
|--------|------|-------------|
| POST | /mapping | Allows mapping from third-party identifiers to FIGIs. |
| GET | /mapping/values/{key} | Get values for enum-like fields. |

### search
| Method | Path | Description |
|--------|------|-------------|
| POST | /search | Search for FIGIs using key words and other filters. |

### filter
| Method | Path | Description |
|--------|------|-------------|
| POST | /filter | Search for FIGIs using key words and other filters. The results are listed alphabetically by FIGI and include the number of results. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a mapping?" -> POST /mapping
- "Get value details?" -> GET /mapping/values/{key}
- "Create a search?" -> POST /search
- "Create a filter?" -> POST /filter
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
