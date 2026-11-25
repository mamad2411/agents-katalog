---
name: authentiq-api
description: "Authentiq API skill. Use when working with Authentiq for key, login, scope. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# Authentiq API
API version: 6

## Auth
ApiKey secret in query

## Base URL
https://6-dot-authentiqio.appspot.com/

## Setup
1. Set your API key in the appropriate header
2. GET /key/{PK} -- verify access
3. POST /key -- create first key

## Endpoints

14 endpoints across 3 groups. See references/api-spec.lap for full details.

### key
| Method | Path | Description |
|--------|------|-------------|
| POST | /key | Register a new ID `JWT(sub, devtoken)` |
| DELETE | /key | Revoke an Authentiq ID using email & phone. |
| GET | /key/{PK} | Get public details of an Authentiq ID. |
| POST | /key/{PK} | update properties of an Authentiq ID. |
| HEAD | /key/{PK} | HEAD info on Authentiq ID |
| PUT | /key/{PK} | Update Authentiq ID by replacing the object. |
| DELETE | /key/{PK} | Revoke an Identity (Key) with a revocation secret |

### login
| Method | Path | Description |
|--------|------|-------------|
| POST | /login | push sign-in request |

### scope
| Method | Path | Description |
|--------|------|-------------|
| POST | /scope | scope verification request |
| POST | /scope/{job} | this is a scope confirmation |
| PUT | /scope/{job} | authority updates a JWT with its signature |
| GET | /scope/{job} | get the status / current content of a verification job |
| HEAD | /scope/{job} | HEAD to get the status of a verification job |
| DELETE | /scope/{job} | delete a verification job |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a key?" -> POST /key
- "Get key details?" -> GET /key/{PK}
- "Update a key?" -> PUT /key/{PK}
- "Delete a key?" -> DELETE /key/{PK}
- "Create a login?" -> POST /login
- "Create a scope?" -> POST /scope
- "Update a scope?" -> PUT /scope/{job}
- "Get scope details?" -> GET /scope/{job}
- "Delete a scope?" -> DELETE /scope/{job}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
