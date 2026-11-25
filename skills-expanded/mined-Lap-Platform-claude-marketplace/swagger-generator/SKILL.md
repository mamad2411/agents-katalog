---
name: swagger-generator
description: "Swagger Generator API skill. Use when working with Swagger Generator for gen. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Swagger Generator
API version: 2.4.49

## Auth
No authentication required.

## Base URL
https://generator.swagger.io/api

## Setup
1. No auth setup needed
2. GET /gen/servers -- verify access
3. POST /gen/servers/{framework} -- create first servers

## Endpoints

7 endpoints across 1 groups. See references/api-spec.lap for full details.

### gen
| Method | Path | Description |
|--------|------|-------------|
| GET | /gen/download/{fileId} | Downloads a pre-generated file |
| GET | /gen/servers | Gets languages supported by the server generator |
| GET | /gen/servers/{framework} | Returns options for a server framework |
| POST | /gen/servers/{framework} | Generates a server library |
| GET | /gen/clients/{language} | Returns options for a client library |
| POST | /gen/clients/{language} | Generates a client library |
| GET | /gen/clients | Gets languages supported by the client generator |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get download details?" -> GET /gen/download/{fileId}
- "List all servers?" -> GET /gen/servers
- "Get server details?" -> GET /gen/servers/{framework}
- "Get client details?" -> GET /gen/clients/{language}
- "List all clients?" -> GET /gen/clients

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
