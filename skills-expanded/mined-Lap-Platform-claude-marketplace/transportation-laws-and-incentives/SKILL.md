---
name: transportation-laws-and-incentives
description: "Transportation Laws and Incentives API skill. Use when working with Transportation Laws and Incentives for v1.{output_format}, {id}.{output_format}, pocs.{output_format}. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Transportation Laws and Incentives
API version: 0.1.0

## Auth
ApiKey api_key in query

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /v1.{output_format} -- verify access

## Endpoints

4 endpoints across 4 groups. See references/api-spec.lap for full details.

### v1.{output_format}
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1.{output_format} | Return a full list of laws and incentives that match your query. |

### {id}.{output_format}
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/{id}.{output_format} | Fetch the details of a specific law given the law's ID. |

### pocs.{output_format}
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/pocs.{output_format} | Get the points of contact for a given jurisdiction. |

### category-list.{output_format}
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/category-list.{output_format} | Return the law categories for a given category type. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get v1.{output_format} details?" -> GET /v1.{output_format}
- "Get pocs.{output_format} details?" -> GET /v1/pocs.{output_format}
- "Get category-list.{output_format} details?" -> GET /v1/category-list.{output_format}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
