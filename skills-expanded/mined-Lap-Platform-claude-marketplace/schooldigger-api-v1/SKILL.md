---
name: schooldigger-api-v1
description: "SchoolDigger API V1 API skill. Use when working with SchoolDigger API V1 for districts, rankings, schools. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# SchoolDigger API V1
API version: v1

## Auth
ApiKey appKey in query

## Base URL
https://api.schooldigger.com

## Setup
1. Set your API key in the appropriate header
2. GET /v1/districts -- verify access

## Endpoints

6 endpoints across 3 groups. See references/api-spec.lap for full details.

### districts
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/districts | Returns a list of districts |
| GET | /v1/districts/{id} | Returns a detailed record for one district |

### rankings
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/rankings/schools/{st} | Returns a SchoolDigger school ranking list |
| GET | /v1/rankings/districts/{st} | Returns a SchoolDigger district ranking list |

### schools
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/schools | Returns a list of schools |
| GET | /v1/schools/{id} | Returns a detailed record for one school |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search districts?" -> GET /v1/districts
- "Get district details?" -> GET /v1/districts/{id}
- "Get school details?" -> GET /v1/rankings/schools/{st}
- "Get district details?" -> GET /v1/rankings/districts/{st}
- "Search schools?" -> GET /v1/schools
- "Get school details?" -> GET /v1/schools/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
