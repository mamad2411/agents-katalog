---
name: pinecone-data-plane-api
description: "Pinecone Data Plane API skill. Use when working with Pinecone Data Plane for bulk, describe_index_stats, query. Covers 18 endpoints."
version: 1.0.0
generator: lapsh
---

# Pinecone Data Plane API
API version: 2025-10

## Auth
ApiKey Api-Key in header

## Base URL
https://{index_host}

## Setup
1. Set your API key in the appropriate header
2. GET /bulk/imports -- verify access
3. POST /bulk/imports -- create first imports

## Endpoints

18 endpoints across 6 groups. See references/api-spec.lap for full details.

### bulk
| Method | Path | Description |
|--------|------|-------------|
| GET | /bulk/imports | List imports |
| POST | /bulk/imports | Start import |
| GET | /bulk/imports/{id} | Describe an import |
| DELETE | /bulk/imports/{id} | Cancel an import |

### describe_index_stats
| Method | Path | Description |
|--------|------|-------------|
| POST | /describe_index_stats | Get index stats |

### query
| Method | Path | Description |
|--------|------|-------------|
| POST | /query | Search with a vector |

### vectors
| Method | Path | Description |
|--------|------|-------------|
| POST | /vectors/delete | Delete vectors |
| GET | /vectors/fetch | Fetch vectors |
| POST | /vectors/fetch_by_metadata | Fetch vectors by metadata |
| GET | /vectors/list | List vector IDs |
| POST | /vectors/update | Update a vector |
| POST | /vectors/upsert | Upsert vectors |

### namespaces
| Method | Path | Description |
|--------|------|-------------|
| GET | /namespaces | List namespaces |
| POST | /namespaces | Create a namespace |
| GET | /namespaces/{namespace} | Describe a namespace |
| DELETE | /namespaces/{namespace} | Delete a namespace |

### records
| Method | Path | Description |
|--------|------|-------------|
| POST | /records/namespaces/{namespace}/upsert | Upsert text |
| POST | /records/namespaces/{namespace}/search | Search with text |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all imports?" -> GET /bulk/imports
- "Create a import?" -> POST /bulk/imports
- "Get import details?" -> GET /bulk/imports/{id}
- "Delete a import?" -> DELETE /bulk/imports/{id}
- "Create a describe_index_stat?" -> POST /describe_index_stats
- "Create a query?" -> POST /query
- "Create a delete?" -> POST /vectors/delete
- "List all fetch?" -> GET /vectors/fetch
- "Create a fetch_by_metadata?" -> POST /vectors/fetch_by_metadata
- "List all list?" -> GET /vectors/list
- "Create a update?" -> POST /vectors/update
- "Create a upsert?" -> POST /vectors/upsert
- "List all namespaces?" -> GET /namespaces
- "Create a namespace?" -> POST /namespaces
- "Get namespace details?" -> GET /namespaces/{namespace}
- "Delete a namespace?" -> DELETE /namespaces/{namespace}
- "Create a upsert?" -> POST /records/namespaces/{namespace}/upsert
- "Create a search?" -> POST /records/namespaces/{namespace}/search
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
