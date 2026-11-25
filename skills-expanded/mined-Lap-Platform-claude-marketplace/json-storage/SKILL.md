---
name: json-storage
description: "JSON storage API skill. Use when working with JSON storage for bin. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# JSON storage
API version: 0.1

## Auth
No authentication required.

## Base URL
https://extendsclass.com/api/json-storage

## Setup
1. No auth setup needed
2. GET /bin/{id} -- verify access
3. POST /bin -- create first bin

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### bin
| Method | Path | Description |
|--------|------|-------------|
| GET | /bin/{id} | Return a json bin |
| PUT | /bin/{id} | Update a json bin |
| PATCH | /bin/{id} | Partially update a json bin with JSON Merge Patch |
| DELETE | /bin/{id} | Delete a json bin |
| POST | /bin | Create a json bin |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get bin details?" -> GET /bin/{id}
- "Update a bin?" -> PUT /bin/{id}
- "Partially update a bin?" -> PATCH /bin/{id}
- "Delete a bin?" -> DELETE /bin/{id}
- "Create a bin?" -> POST /bin

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
