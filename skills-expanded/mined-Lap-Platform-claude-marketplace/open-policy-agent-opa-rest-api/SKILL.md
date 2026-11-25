---
name: open-policy-agent-opa-rest-api
description: "Open Policy Agent (OPA) REST API skill. Use when working with Open Policy Agent (OPA) REST for policies, data, root. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# Open Policy Agent (OPA) REST API
API version: 0.28.0

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /v1/policies -- verify access
3. POST /v1/data/{path} -- create first data

## Endpoints

16 endpoints across 7 groups. See references/api-spec.lap for full details.

### policies
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/policies | List policies |
| GET | /v1/policies/{id} | Get a policy module |
| PUT | /v1/policies/{id} | Create or update a policy module |
| DELETE | /v1/policies/{id} | Delete a policy module |

### data
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/data/{path} | Get a document |
| PUT | /v1/data/{path} | Create or overwrite a document |
| PATCH | /v1/data/{path} | Update a document |
| DELETE | /v1/data/{path} | Delete a document |
| POST | /v1/data/{path} | Get a document (with input) |
| POST | /v0/data/{path} | Get a document (with webhook) |

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Execute a simple query |

### query
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/query | Execute an ad-hoc query (simple) |
| POST | /v1/query | Execute an ad-hoc query (complex) |

### compile
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/compile | Compile |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health |

### config
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/config | Get configurations |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all policies?" -> GET /v1/policies
- "Get policy details?" -> GET /v1/policies/{id}
- "Update a policy?" -> PUT /v1/policies/{id}
- "Delete a policy?" -> DELETE /v1/policies/{id}
- "Get data details?" -> GET /v1/data/{path}
- "Update a data?" -> PUT /v1/data/{path}
- "Partially update a data?" -> PATCH /v1/data/{path}
- "Delete a data?" -> DELETE /v1/data/{path}
- "Search query?" -> GET /v1/query
- "Create a query?" -> POST /v1/query
- "Create a compile?" -> POST /v1/compile
- "List all health?" -> GET /health
- "List all config?" -> GET /v1/config

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
