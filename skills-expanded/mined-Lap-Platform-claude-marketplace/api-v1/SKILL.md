---
name: api-v1
description: "API V1 API skill. Use when working with API V1 for api. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# API V1
API version: v1

## Auth
ApiKey apiKey in header

## Base URL
https://{defaultHost}

## Setup
1. Set your API key in the appropriate header
2. GET /api/v1/scans -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/scans | Retrieves all scans |
| GET | /api/v1/scans/{id} | Retrieves a project scan result |
| GET | /api/v1/scans/{id}/files/{file_id} | Retrieves a file object, containing information about dependencies in the file |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all scans?" -> GET /api/v1/scans
- "Get scan details?" -> GET /api/v1/scans/{id}
- "Get file details?" -> GET /api/v1/scans/{id}/files/{file_id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
