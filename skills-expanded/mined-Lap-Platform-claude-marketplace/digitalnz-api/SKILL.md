---
name: digitalnz-api
description: "DigitalNZ API skill. Use when working with DigitalNZ for records.{format}, records. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# DigitalNZ API
API version: 3

## Auth
ApiKey api_key in query

## Base URL
https://api.digitalnz.org

## Setup
1. Set your API key in the appropriate header
2. GET /records.{format} -- verify access

## Endpoints

3 endpoints across 2 groups. See references/api-spec.lap for full details.

### records.{format}
| Method | Path | Description |
|--------|------|-------------|
| GET | /records.{format} | Run queries against DigitalNZ metadata search service. |

### records
| Method | Path | Description |
|--------|------|-------------|
| GET | /records/{record_id}.{format} | View metadata associated with a single record. |
| GET | /records/{record_id}/more_like_this.{format} | The "More Like This" call returns similar records to the specified ID. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get records.{format} details?" -> GET /records.{format}
- "Get record details?" -> GET /records/{record_id}.{format}
- "Get more_like_this.{format} details?" -> GET /records/{record_id}/more_like_this.{format}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
