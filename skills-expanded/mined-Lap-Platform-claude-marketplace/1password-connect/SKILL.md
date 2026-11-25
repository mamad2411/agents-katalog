---
name: 1password-connect
description: "1Password Connect API skill. Use when working with 1Password Connect for activity, vaults, heartbeat. Covers 15 endpoints."
version: 1.0.0
generator: lapsh
---

# 1Password Connect
API version: 1.5.7

## Auth
Bearer bearer

## Base URL
http://localhost:8080/v1

## Setup
1. Set Authorization header with your Bearer token
2. GET /activity -- verify access
3. POST /vaults/{vaultUuid}/items -- create first items

## Endpoints

15 endpoints across 5 groups. See references/api-spec.lap for full details.

### activity
| Method | Path | Description |
|--------|------|-------------|
| GET | /activity | Retrieve a list of API Requests that have been made. |

### vaults
| Method | Path | Description |
|--------|------|-------------|
| GET | /vaults | Get all Vaults |
| GET | /vaults/{vaultUuid} | Get Vault details and metadata |
| GET | /vaults/{vaultUuid}/items | Get all items for inside a Vault |
| POST | /vaults/{vaultUuid}/items | Create a new Item |
| GET | /vaults/{vaultUuid}/items/{itemUuid} | Get the details of an Item |
| PUT | /vaults/{vaultUuid}/items/{itemUuid} | Update an Item |
| DELETE | /vaults/{vaultUuid}/items/{itemUuid} | Delete an Item |
| PATCH | /vaults/{vaultUuid}/items/{itemUuid} | Update a subset of Item attributes |
| GET | /vaults/{vaultUuid}/items/{itemUuid}/files | Get all the files inside an Item |
| GET | /vaults/{vaultUuid}/items/{itemUuid}/files/{fileUuid} | Get the details of a File |
| GET | /vaults/{vaultUuid}/items/{itemUuid}/files/{fileUuid}/content | Get the content of a File |

### heartbeat
| Method | Path | Description |
|--------|------|-------------|
| GET | /heartbeat | Ping the server for liveness |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Get state of the server and its dependencies. |

### metrics
| Method | Path | Description |
|--------|------|-------------|
| GET | /metrics | Query server for exposed Prometheus metrics |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all activity?" -> GET /activity
- "List all vaults?" -> GET /vaults
- "Get vault details?" -> GET /vaults/{vaultUuid}
- "List all items?" -> GET /vaults/{vaultUuid}/items
- "Create a item?" -> POST /vaults/{vaultUuid}/items
- "Get item details?" -> GET /vaults/{vaultUuid}/items/{itemUuid}
- "Update a item?" -> PUT /vaults/{vaultUuid}/items/{itemUuid}
- "Delete a item?" -> DELETE /vaults/{vaultUuid}/items/{itemUuid}
- "Partially update a item?" -> PATCH /vaults/{vaultUuid}/items/{itemUuid}
- "List all files?" -> GET /vaults/{vaultUuid}/items/{itemUuid}/files
- "Get file details?" -> GET /vaults/{vaultUuid}/items/{itemUuid}/files/{fileUuid}
- "List all content?" -> GET /vaults/{vaultUuid}/items/{itemUuid}/files/{fileUuid}/content
- "List all heartbeat?" -> GET /heartbeat
- "List all health?" -> GET /health
- "List all metrics?" -> GET /metrics
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
