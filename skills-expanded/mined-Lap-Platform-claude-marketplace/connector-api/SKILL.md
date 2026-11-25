---
name: connector-api
description: "Connector API skill. Use when working with Connector for connector. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# Connector API
API version: 10.24.0

## Auth
ApiKey Authorization in header

## Base URL
https://unify.apideck.com

## Setup
1. Set your API key in the appropriate header
2. GET /connector/connectors -- verify access

## Endpoints

10 endpoints across 1 groups. See references/api-spec.lap for full details.

### connector
| Method | Path | Description |
|--------|------|-------------|
| GET | /connector/connectors | List Connectors |
| GET | /connector/connectors/{id} | Get Connector |
| GET | /connector/connectors/{id}/docs/{doc_id} | Get Connector Doc content |
| GET | /connector/connectors/{id}/resources/{resource_id} | Get Connector Resource |
| GET | /connector/connectors/{id}/resources/{resource_id}/unified_api/{api_id}/schema | Get Connector Resource Schema |
| GET | /connector/connectors/{id}/resources/{resource_id}/unified_api/{api_id}/example | Get Connector Resource Example |
| GET | /connector/apis | List APIs |
| GET | /connector/apis/{id} | Get API |
| GET | /connector/apis/{id}/resources/{resource_id} | Get API Resource |
| GET | /connector/apis/{id}/resources/{resource_id}/coverage | Get API Resource Coverage |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all connectors?" -> GET /connector/connectors
- "Get connector details?" -> GET /connector/connectors/{id}
- "Get doc details?" -> GET /connector/connectors/{id}/docs/{doc_id}
- "Get resource details?" -> GET /connector/connectors/{id}/resources/{resource_id}
- "List all schema?" -> GET /connector/connectors/{id}/resources/{resource_id}/unified_api/{api_id}/schema
- "List all example?" -> GET /connector/connectors/{id}/resources/{resource_id}/unified_api/{api_id}/example
- "List all apis?" -> GET /connector/apis
- "Get apis details?" -> GET /connector/apis/{id}
- "Get resource details?" -> GET /connector/apis/{id}/resources/{resource_id}
- "List all coverage?" -> GET /connector/apis/{id}/resources/{resource_id}/coverage
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
