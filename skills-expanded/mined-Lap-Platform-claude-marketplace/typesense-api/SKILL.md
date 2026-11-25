---
name: typesense-api
description: "Typesense API skill. Use when working with Typesense for collections, synonym_sets, curation_sets. Covers 79 endpoints."
version: 1.0.0
generator: lapsh
---

# Typesense API
API version: 30.0

## Auth
ApiKey X-TYPESENSE-API-KEY in header

## Base URL
http://localhost:8108

## Setup
1. Set your API key in the appropriate header
2. GET /collections -- verify access
3. POST /collections -- create first collections

## Endpoints

79 endpoints across 18 groups. See references/api-spec.lap for full details.

### collections
| Method | Path | Description |
|--------|------|-------------|
| GET | /collections | List all collections |
| POST | /collections | Create a new collection |
| GET | /collections/{collectionName} | Retrieve a single collection |
| PATCH | /collections/{collectionName} | Update a collection |
| DELETE | /collections/{collectionName} | Delete a collection |
| POST | /collections/{collectionName}/documents | Index a document |
| PATCH | /collections/{collectionName}/documents | Update documents with conditional query |
| DELETE | /collections/{collectionName}/documents | Delete a bunch of documents |
| GET | /collections/{collectionName}/documents/search | Search for documents in a collection |
| GET | /collections/{collectionName}/documents/export | Export all documents in a collection |
| POST | /collections/{collectionName}/documents/import | Import documents into a collection |
| GET | /collections/{collectionName}/documents/{documentId} | Retrieve a document |
| PATCH | /collections/{collectionName}/documents/{documentId} | Update a document |
| DELETE | /collections/{collectionName}/documents/{documentId} | Delete a document |

### synonym_sets
| Method | Path | Description |
|--------|------|-------------|
| GET | /synonym_sets | List all synonym sets |
| GET | /synonym_sets/{synonymSetName} | Retrieve a synonym set |
| PUT | /synonym_sets/{synonymSetName} | Create or update a synonym set |
| DELETE | /synonym_sets/{synonymSetName} | Delete a synonym set |
| GET | /synonym_sets/{synonymSetName}/items | List items in a synonym set |
| GET | /synonym_sets/{synonymSetName}/items/{itemId} | Retrieve a synonym set item |
| PUT | /synonym_sets/{synonymSetName}/items/{itemId} | Create or update a synonym set item |
| DELETE | /synonym_sets/{synonymSetName}/items/{itemId} | Delete a synonym set item |

### curation_sets
| Method | Path | Description |
|--------|------|-------------|
| GET | /curation_sets | List all curation sets |
| GET | /curation_sets/{curationSetName} | Retrieve a curation set |
| PUT | /curation_sets/{curationSetName} | Create or update a curation set |
| DELETE | /curation_sets/{curationSetName} | Delete a curation set |
| GET | /curation_sets/{curationSetName}/items | List items in a curation set |
| GET | /curation_sets/{curationSetName}/items/{itemId} | Retrieve a curation set item |
| PUT | /curation_sets/{curationSetName}/items/{itemId} | Create or update a curation set item |
| DELETE | /curation_sets/{curationSetName}/items/{itemId} | Delete a curation set item |

### conversations
| Method | Path | Description |
|--------|------|-------------|
| GET | /conversations/models | List all conversation models |
| POST | /conversations/models | Create a conversation model |
| GET | /conversations/models/{modelId} | Retrieve a conversation model |
| PUT | /conversations/models/{modelId} | Update a conversation model |
| DELETE | /conversations/models/{modelId} | Delete a conversation model |

### keys
| Method | Path | Description |
|--------|------|-------------|
| GET | /keys | Retrieve (metadata about) all keys. |
| POST | /keys | Create an API Key |
| GET | /keys/{keyId} | Retrieve (metadata about) a key |
| DELETE | /keys/{keyId} | Delete an API key given its ID. |

### aliases
| Method | Path | Description |
|--------|------|-------------|
| GET | /aliases | List all aliases |
| PUT | /aliases/{aliasName} | Create or update a collection alias |
| GET | /aliases/{aliasName} | Retrieve an alias |
| DELETE | /aliases/{aliasName} | Delete an alias |

### debug
| Method | Path | Description |
|--------|------|-------------|
| GET | /debug | Print debugging information |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Checks if Typesense server is ready to accept requests. |

### operations
| Method | Path | Description |
|--------|------|-------------|
| GET | /operations/schema_changes | Get the status of in-progress schema change operations |
| POST | /operations/snapshot | Creates a point-in-time snapshot of a Typesense node's state and data in the specified directory. |
| POST | /operations/vote | Triggers a follower node to initiate the raft voting process, which triggers leader re-election. |
| POST | /operations/cache/clear | Clear the cached responses of search requests in the LRU cache. |
| POST | /operations/db/compact | Compacting the on-disk database |

### config
| Method | Path | Description |
|--------|------|-------------|
| POST | /config | Toggle Slow Request Log |

### multi_search
| Method | Path | Description |
|--------|------|-------------|
| POST | /multi_search | send multiple search requests in a single HTTP request |

### analytics
| Method | Path | Description |
|--------|------|-------------|
| POST | /analytics/events | Create an analytics event |
| GET | /analytics/events | Retrieve analytics events |
| POST | /analytics/flush | Flush in-memory analytics to disk |
| GET | /analytics/status | Get analytics subsystem status |
| POST | /analytics/rules | Create analytics rule(s) |
| GET | /analytics/rules | Retrieve analytics rules |
| PUT | /analytics/rules/{ruleName} | Upserts an analytics rule |
| GET | /analytics/rules/{ruleName} | Retrieves an analytics rule |
| DELETE | /analytics/rules/{ruleName} | Delete an analytics rule |

### metrics.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /metrics.json | Get current RAM, CPU, Disk & Network usage metrics. |

### stats.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /stats.json | Get stats about API endpoints. |

### stopwords
| Method | Path | Description |
|--------|------|-------------|
| GET | /stopwords | Retrieves all stopwords sets. |
| PUT | /stopwords/{setId} | Upserts a stopwords set. |
| GET | /stopwords/{setId} | Retrieves a stopwords set. |
| DELETE | /stopwords/{setId} | Delete a stopwords set. |

### presets
| Method | Path | Description |
|--------|------|-------------|
| GET | /presets | Retrieves all presets. |
| GET | /presets/{presetId} | Retrieves a preset. |
| PUT | /presets/{presetId} | Upserts a preset. |
| DELETE | /presets/{presetId} | Delete a preset. |

### stemming
| Method | Path | Description |
|--------|------|-------------|
| GET | /stemming/dictionaries | List all stemming dictionaries |
| GET | /stemming/dictionaries/{dictionaryId} | Retrieve a stemming dictionary |
| POST | /stemming/dictionaries/import | Import a stemming dictionary |

### nl_search_models
| Method | Path | Description |
|--------|------|-------------|
| GET | /nl_search_models | List all NL search models |
| POST | /nl_search_models | Create a NL search model |
| GET | /nl_search_models/{modelId} | Retrieve a NL search model |
| PUT | /nl_search_models/{modelId} | Update a NL search model |
| DELETE | /nl_search_models/{modelId} | Delete a NL search model |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all collections?" -> GET /collections
- "Create a collection?" -> POST /collections
- "Get collection details?" -> GET /collections/{collectionName}
- "Partially update a collection?" -> PATCH /collections/{collectionName}
- "Delete a collection?" -> DELETE /collections/{collectionName}
- "Create a document?" -> POST /collections/{collectionName}/documents
- "List all search?" -> GET /collections/{collectionName}/documents/search
- "List all synonym_sets?" -> GET /synonym_sets
- "Get synonym_set details?" -> GET /synonym_sets/{synonymSetName}
- "Update a synonym_set?" -> PUT /synonym_sets/{synonymSetName}
- "Delete a synonym_set?" -> DELETE /synonym_sets/{synonymSetName}
- "List all items?" -> GET /synonym_sets/{synonymSetName}/items
- "Get item details?" -> GET /synonym_sets/{synonymSetName}/items/{itemId}
- "Update a item?" -> PUT /synonym_sets/{synonymSetName}/items/{itemId}
- "Delete a item?" -> DELETE /synonym_sets/{synonymSetName}/items/{itemId}
- "List all curation_sets?" -> GET /curation_sets
- "Get curation_set details?" -> GET /curation_sets/{curationSetName}
- "Update a curation_set?" -> PUT /curation_sets/{curationSetName}
- "Delete a curation_set?" -> DELETE /curation_sets/{curationSetName}
- "List all items?" -> GET /curation_sets/{curationSetName}/items
- "Get item details?" -> GET /curation_sets/{curationSetName}/items/{itemId}
- "Update a item?" -> PUT /curation_sets/{curationSetName}/items/{itemId}
- "Delete a item?" -> DELETE /curation_sets/{curationSetName}/items/{itemId}
- "List all export?" -> GET /collections/{collectionName}/documents/export
- "Create a import?" -> POST /collections/{collectionName}/documents/import
- "Get document details?" -> GET /collections/{collectionName}/documents/{documentId}
- "Partially update a document?" -> PATCH /collections/{collectionName}/documents/{documentId}
- "Delete a document?" -> DELETE /collections/{collectionName}/documents/{documentId}
- "List all models?" -> GET /conversations/models
- "Create a model?" -> POST /conversations/models
- "Get model details?" -> GET /conversations/models/{modelId}
- "Update a model?" -> PUT /conversations/models/{modelId}
- "Delete a model?" -> DELETE /conversations/models/{modelId}
- "List all keys?" -> GET /keys
- "Create a key?" -> POST /keys
- "Get key details?" -> GET /keys/{keyId}
- "Delete a key?" -> DELETE /keys/{keyId}
- "List all aliases?" -> GET /aliases
- "Update a aliase?" -> PUT /aliases/{aliasName}
- "Get aliase details?" -> GET /aliases/{aliasName}
- "Delete a aliase?" -> DELETE /aliases/{aliasName}
- "List all debug?" -> GET /debug
- "List all health?" -> GET /health
- "List all schema_changes?" -> GET /operations/schema_changes
- "Create a snapshot?" -> POST /operations/snapshot
- "Create a vote?" -> POST /operations/vote
- "Create a clear?" -> POST /operations/cache/clear
- "Create a compact?" -> POST /operations/db/compact
- "Create a config?" -> POST /config
- "Create a multi_search?" -> POST /multi_search
- "Create a event?" -> POST /analytics/events
- "List all events?" -> GET /analytics/events
- "Create a flush?" -> POST /analytics/flush
- "List all status?" -> GET /analytics/status
- "Create a rule?" -> POST /analytics/rules
- "List all rules?" -> GET /analytics/rules
- "Update a rule?" -> PUT /analytics/rules/{ruleName}
- "Get rule details?" -> GET /analytics/rules/{ruleName}
- "Delete a rule?" -> DELETE /analytics/rules/{ruleName}
- "List all metrics.json?" -> GET /metrics.json
- "List all stats.json?" -> GET /stats.json
- "List all stopwords?" -> GET /stopwords
- "Update a stopword?" -> PUT /stopwords/{setId}
- "Get stopword details?" -> GET /stopwords/{setId}
- "Delete a stopword?" -> DELETE /stopwords/{setId}
- "List all presets?" -> GET /presets
- "Get preset details?" -> GET /presets/{presetId}
- "Update a preset?" -> PUT /presets/{presetId}
- "Delete a preset?" -> DELETE /presets/{presetId}
- "List all dictionaries?" -> GET /stemming/dictionaries
- "Get dictionary details?" -> GET /stemming/dictionaries/{dictionaryId}
- "Create a import?" -> POST /stemming/dictionaries/import
- "List all nl_search_models?" -> GET /nl_search_models
- "Create a nl_search_model?" -> POST /nl_search_models
- "Get nl_search_model details?" -> GET /nl_search_models/{modelId}
- "Update a nl_search_model?" -> PUT /nl_search_models/{modelId}
- "Delete a nl_search_model?" -> DELETE /nl_search_models/{modelId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
