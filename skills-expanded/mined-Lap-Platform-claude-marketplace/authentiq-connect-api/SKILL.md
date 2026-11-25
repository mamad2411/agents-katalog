---
name: authentiq-connect-api
description: "Authentiq Connect API skill. Use when working with Authentiq Connect for authorize, token, userinfo. Covers 9 endpoints."
version: 1.0.0
generator: lapsh
---

# Authentiq Connect API
API version: 1.0

## Auth
OAuth2 | ApiKey Authorization in header | OAuth2 | OAuth2 | OAuth2

## Base URL
https://connect.authentiq.io/

## Setup
1. Set your API key in the appropriate header
2. GET /authorize -- verify access
3. POST /token -- create first token

## Endpoints

9 endpoints across 5 groups. See references/api-spec.lap for full details.

### authorize
| Method | Path | Description |
|--------|------|-------------|
| GET | /authorize | Authenticate a user |

### token
| Method | Path | Description |
|--------|------|-------------|
| POST | /token | Obtain an ID Token |

### userinfo
| Method | Path | Description |
|--------|------|-------------|
| GET | /userinfo | Retrieve a user profile |

### client
| Method | Path | Description |
|--------|------|-------------|
| GET | /client | List clients |
| POST | /client | Register a client |
| GET | /client/{client_id} | View a client |
| PUT | /client/{client_id} | Update a client |
| DELETE | /client/{client_id} | Delete a client |

### {client_id}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{client_id}/iframe | Include a session iframe |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all authorize?" -> GET /authorize
- "Create a token?" -> POST /token
- "List all userinfo?" -> GET /userinfo
- "List all client?" -> GET /client
- "Create a client?" -> POST /client
- "Get client details?" -> GET /client/{client_id}
- "Update a client?" -> PUT /client/{client_id}
- "Delete a client?" -> DELETE /client/{client_id}
- "List all iframe?" -> GET /{client_id}/iframe
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
