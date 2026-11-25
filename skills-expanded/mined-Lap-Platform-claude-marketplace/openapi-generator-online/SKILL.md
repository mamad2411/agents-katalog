---
name: openapi-generator-online
description: "OpenAPI Generator Online API skill. Use when working with OpenAPI Generator Online for api. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# OpenAPI Generator Online
API version: 7.12.0

## Auth
No authentication required.

## Base URL
https://api.openapi-generator.tech/

## Setup
1. No auth setup needed
2. GET /api/gen/clients -- verify access
3. POST /api/gen/clients/{language} -- create first clients

## Endpoints

7 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/gen/clients | Gets languages supported by the client generator |
| GET | /api/gen/clients/{language} | Returns options for a client library |
| POST | /api/gen/clients/{language} | Generates a client library |
| GET | /api/gen/download/{fileId} | Downloads a pre-generated file |
| GET | /api/gen/servers | Gets languages supported by the server generator |
| GET | /api/gen/servers/{framework} | Returns options for a server framework |
| POST | /api/gen/servers/{framework} | Generates a server library |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all clients?" -> GET /api/gen/clients
- "Get client details?" -> GET /api/gen/clients/{language}
- "Get download details?" -> GET /api/gen/download/{fileId}
- "List all servers?" -> GET /api/gen/servers
- "Get server details?" -> GET /api/gen/servers/{framework}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
