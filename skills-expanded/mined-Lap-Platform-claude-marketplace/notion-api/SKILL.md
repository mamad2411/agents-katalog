---
name: notion-api
description: "Notion API skill. Use when working with Notion for users, search, blocks. Covers 22 endpoints."
version: 1.0.0
generator: lapsh
---

# Notion API
API version: 2.0.0

## Auth
Bearer bearer | Bearer basic

## Base URL
https://api.notion.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/users -- verify access
3. POST /v1/search -- create first search

## Endpoints

22 endpoints across 7 groups. See references/api-spec.lap for full details.

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/users/{user_id} | Retrieve a user |
| GET | /v1/users | List all users |
| GET | /v1/users/me | Retrieve your token's bot user |

### search
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/search | Search by title |

### blocks
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/blocks/{block_id}/children | Retrieve block children |
| PATCH | /v1/blocks/{block_id}/children | Append block children |
| GET | /v1/blocks/{block_id} | Retrieve a block |
| PATCH | /v1/blocks/{block_id} | Update a block |
| DELETE | /v1/blocks/{block_id} | Delete a block |

### pages
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/pages/{page_id} | Retrieve a page |
| PATCH | /v1/pages/{page_id} | Update page properties |
| POST | /v1/pages | Create a page |
| GET | /v1/pages/{page_id}/properties/{property_id} | Retrieve a page property item |
| POST | /v1/pages/{page_id}/move | Move a page |

### comments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/comments | Retrieve comments |
| POST | /v1/comments | Create comment |

### data_sources
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/data_sources/{data_source_id}/query | Query a data source |
| GET | /v1/data_sources/{data_source_id} | Retrieve a data source |
| PATCH | /v1/data_sources/{data_source_id} | Update a data source |
| POST | /v1/data_sources | Create a data source |
| GET | /v1/data_sources/{data_source_id}/templates | List templates in a data source |

### databases
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/databases/{database_id} | Retrieve a database |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get user details?" -> GET /v1/users/{user_id}
- "List all users?" -> GET /v1/users
- "List all me?" -> GET /v1/users/me
- "Create a search?" -> POST /v1/search
- "List all children?" -> GET /v1/blocks/{block_id}/children
- "Get block details?" -> GET /v1/blocks/{block_id}
- "Partially update a block?" -> PATCH /v1/blocks/{block_id}
- "Delete a block?" -> DELETE /v1/blocks/{block_id}
- "Get page details?" -> GET /v1/pages/{page_id}
- "Partially update a page?" -> PATCH /v1/pages/{page_id}
- "Create a page?" -> POST /v1/pages
- "Get property details?" -> GET /v1/pages/{page_id}/properties/{property_id}
- "List all comments?" -> GET /v1/comments
- "Create a comment?" -> POST /v1/comments
- "Create a query?" -> POST /v1/data_sources/{data_source_id}/query
- "Get data_source details?" -> GET /v1/data_sources/{data_source_id}
- "Partially update a data_source?" -> PATCH /v1/data_sources/{data_source_id}
- "Create a data_source?" -> POST /v1/data_sources
- "List all templates?" -> GET /v1/data_sources/{data_source_id}/templates
- "Get database details?" -> GET /v1/databases/{database_id}
- "Create a move?" -> POST /v1/pages/{page_id}/move
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
