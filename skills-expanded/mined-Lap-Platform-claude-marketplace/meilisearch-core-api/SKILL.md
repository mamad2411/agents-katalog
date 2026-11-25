---
name: meilisearch-core-api
description: "Meilisearch Core API skill. Use when working with Meilisearch Core for dumps, snapshots, health. Covers 73 endpoints."
version: 1.0.0
generator: lapsh
---

# Meilisearch Core API
API version: 1.7.0

## Auth
Bearer bearer

## Base URL
{protocol}://{domain}:{port}

## Setup
1. Set Authorization header with your Bearer token
2. GET /health -- verify access
3. POST /dumps -- create first dumps

## Endpoints

73 endpoints across 12 groups. See references/api-spec.lap for full details.

### dumps
| Method | Path | Description |
|--------|------|-------------|
| POST | /dumps | Create a Dump |

### snapshots
| Method | Path | Description |
|--------|------|-------------|
| POST | /snapshots | Create a Snapshot |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Get health |

### indexes
| Method | Path | Description |
|--------|------|-------------|
| GET | /indexes | List Indexes |
| POST | /indexes | Create Index |
| GET | /indexes/{indexUid} | Get Index |
| PATCH | /indexes/{indexUid} | Update Index |
| DELETE | /indexes/{indexUid} | Delete Index |
| GET | /indexes/{indexUid}/documents | Get Documents |
| POST | /indexes/{indexUid}/documents | Add or replace documents |
| PUT | /indexes/{indexUid}/documents | Add or update documents |
| DELETE | /indexes/{indexUid}/documents | Delete all documents |
| POST | /indexes/{indexUid}/documents/fetch | Get Documents |
| POST | /indexes/{indexUid}/documents/delete-batch | Delete documents |
| POST | /indexes/{indexUid}/documents/delete | Delete documents |
| GET | /indexes/{indexUid}/documents/{documentId} | Get one document |
| DELETE | /indexes/{indexUid}/documents/{documentId} | Delete one document |
| GET | /indexes/{indexUid}/search | Search |
| POST | /indexes/{indexUid}/search | Search |
| POST | /indexes/{indexUid}/facet-search | Facet Search |
| GET | /indexes/{indexUid}/settings | Get settings |
| PATCH | /indexes/{indexUid}/settings | Update settings |
| DELETE | /indexes/{indexUid}/settings | Reset settings |
| GET | /indexes/{indexUid}/settings/synonyms | Get synonyms |
| PUT | /indexes/{indexUid}/settings/synonyms | Update synonyms |
| DELETE | /indexes/{indexUid}/settings/synonyms | Reset synonyms |
| GET | /indexes/{indexUid}/settings/sortable-attributes | Get sortable attributes |
| PUT | /indexes/{indexUid}/settings/sortable-attributes | Update sortable attributes |
| DELETE | /indexes/{indexUid}/settings/sortable-attributes | Reset sortable attributes |
| GET | /indexes/{indexUid}/settings/stop-words | Get stop-words |
| PUT | /indexes/{indexUid}/settings/stop-words | Update stop-words |
| DELETE | /indexes/{indexUid}/settings/stop-words | Reset stop-words |
| GET | /indexes/{indexUid}/settings/ranking-rules | Get ranking rules |
| PUT | /indexes/{indexUid}/settings/ranking-rules | Update ranking rules |
| DELETE | /indexes/{indexUid}/settings/ranking-rules | Reset ranking rules |
| GET | /indexes/{indexUid}/settings/typo-tolerance | Get typo tolerance configuration |
| PATCH | /indexes/{indexUid}/settings/typo-tolerance | Update typo tolerance settings |
| DELETE | /indexes/{indexUid}/settings/typo-tolerance | Reset typo tolerance settings to the default configuration |
| GET | /indexes/{indexUid}/settings/pagination | Get pagination configuration |
| PATCH | /indexes/{indexUid}/settings/pagination | Update pagination settings |
| DELETE | /indexes/{indexUid}/settings/pagination | Reset pagination settings to the default configuration |
| GET | /indexes/{indexUid}/settings/faceting | Get faceting configuration |
| PATCH | /indexes/{indexUid}/settings/faceting | Update faceting settings |
| DELETE | /indexes/{indexUid}/settings/faceting | Reset faceting settings to the default configuration |
| GET | /indexes/{indexUid}/settings/filterable-attributes | Get Filterable Attributes |
| PUT | /indexes/{indexUid}/settings/filterable-attributes | Update Filterable Attributes |
| DELETE | /indexes/{indexUid}/settings/filterable-attributes | Reset Filterable Attributes |
| GET | /indexes/{indexUid}/settings/distinct-attribute | Get distinct attribute |
| PUT | /indexes/{indexUid}/settings/distinct-attribute | Update distinct attribute |
| DELETE | /indexes/{indexUid}/settings/distinct-attribute | Reset distinct attribute |
| GET | /indexes/{indexUid}/settings/searchable-attributes | Get searchable attributes |
| PUT | /indexes/{indexUid}/settings/searchable-attributes | Update searchable attributes |
| DELETE | /indexes/{indexUid}/settings/searchable-attributes | Reset searchable attributes |
| GET | /indexes/{indexUid}/settings/displayed-attributes | Get displayed attributes |
| PUT | /indexes/{indexUid}/settings/displayed-attributes | Update displayed attributes |
| DELETE | /indexes/{indexUid}/settings/displayed-attributes | Reset displayed attributes |
| GET | /indexes/{indexUid}/stats | Get stat of an index |

### multi-search
| Method | Path | Description |
|--------|------|-------------|
| POST | /multi-search | Multi Search |

### keys
| Method | Path | Description |
|--------|------|-------------|
| GET | /keys | Get API Keys |
| POST | /keys | Create an API Key |
| GET | /keys/{uid_or_key} | Get an API key from its uid or key field. |
| DELETE | /keys/{uid_or_key} | Delete an API key specified by its uid or key field. |
| PATCH | /keys/{uid_or_key} | Update an API key specified by its uid or key field. |

### stats
| Method | Path | Description |
|--------|------|-------------|
| GET | /stats | Get stats of all indexes |

### version
| Method | Path | Description |
|--------|------|-------------|
| GET | /version | Get version of Meilisearch |

### tasks
| Method | Path | Description |
|--------|------|-------------|
| GET | /tasks | Get all tasks |
| DELETE | /tasks | Delete tasks |
| GET | /tasks/:taskUid | Get a task |
| POST | /tasks/cancel | Cancel tasks |

### swap-indexes
| Method | Path | Description |
|--------|------|-------------|
| POST | /swap-indexes | Swap Indexes |

### experimental-features
| Method | Path | Description |
|--------|------|-------------|
| GET | /experimental-features | (EXPERIMENTAL) Get the status of runtime experimental features |
| PATCH | /experimental-features | (EXPERIMENTAL) Set the status of runtime experimental features |

### metrics
| Method | Path | Description |
|--------|------|-------------|
| GET | /metrics | (EXPERIMENTAL) Get prometheus format metrics for observability and monitoring |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a dump?" -> POST /dumps
- "Create a snapshot?" -> POST /snapshots
- "List all health?" -> GET /health
- "List all indexes?" -> GET /indexes
- "Create a indexe?" -> POST /indexes
- "Get indexe details?" -> GET /indexes/{indexUid}
- "Partially update a indexe?" -> PATCH /indexes/{indexUid}
- "Delete a indexe?" -> DELETE /indexes/{indexUid}
- "List all documents?" -> GET /indexes/{indexUid}/documents
- "Create a document?" -> POST /indexes/{indexUid}/documents
- "Create a fetch?" -> POST /indexes/{indexUid}/documents/fetch
- "Create a delete-batch?" -> POST /indexes/{indexUid}/documents/delete-batch
- "Create a delete?" -> POST /indexes/{indexUid}/documents/delete
- "Get document details?" -> GET /indexes/{indexUid}/documents/{documentId}
- "Delete a document?" -> DELETE /indexes/{indexUid}/documents/{documentId}
- "Search search?" -> GET /indexes/{indexUid}/search
- "Create a search?" -> POST /indexes/{indexUid}/search
- "Create a facet-search?" -> POST /indexes/{indexUid}/facet-search
- "List all settings?" -> GET /indexes/{indexUid}/settings
- "List all synonyms?" -> GET /indexes/{indexUid}/settings/synonyms
- "List all sortable-attributes?" -> GET /indexes/{indexUid}/settings/sortable-attributes
- "List all stop-words?" -> GET /indexes/{indexUid}/settings/stop-words
- "List all ranking-rules?" -> GET /indexes/{indexUid}/settings/ranking-rules
- "List all typo-tolerance?" -> GET /indexes/{indexUid}/settings/typo-tolerance
- "List all pagination?" -> GET /indexes/{indexUid}/settings/pagination
- "List all faceting?" -> GET /indexes/{indexUid}/settings/faceting
- "List all filterable-attributes?" -> GET /indexes/{indexUid}/settings/filterable-attributes
- "List all distinct-attribute?" -> GET /indexes/{indexUid}/settings/distinct-attribute
- "List all searchable-attributes?" -> GET /indexes/{indexUid}/settings/searchable-attributes
- "List all displayed-attributes?" -> GET /indexes/{indexUid}/settings/displayed-attributes
- "List all stats?" -> GET /indexes/{indexUid}/stats
- "Create a multi-search?" -> POST /multi-search
- "List all keys?" -> GET /keys
- "Create a key?" -> POST /keys
- "Get key details?" -> GET /keys/{uid_or_key}
- "Delete a key?" -> DELETE /keys/{uid_or_key}
- "Partially update a key?" -> PATCH /keys/{uid_or_key}
- "List all stats?" -> GET /stats
- "List all version?" -> GET /version
- "List all tasks?" -> GET /tasks
- "List all :taskUid?" -> GET /tasks/:taskUid
- "Create a cancel?" -> POST /tasks/cancel
- "Create a swap-indexe?" -> POST /swap-indexes
- "List all experimental-features?" -> GET /experimental-features
- "List all metrics?" -> GET /metrics
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
