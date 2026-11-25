---
name: pinecone-api
description: "Pinecone API skill. Use when working with Pinecone for collections, databases, describe_index_stats. Covers 15 endpoints."
version: 1.0.0
generator: lapsh
---

# Pinecone API
API version: 20230406.1

## Auth
ApiKey Api-Key in header

## Base URL
https://controller.{environment}.pinecone.io

## Setup
1. Set your API key in the appropriate header
2. GET /collections -- verify access
3. POST /collections -- create first collections

## Endpoints

15 endpoints across 5 groups. See references/api-spec.lap for full details.

### collections
| Method | Path | Description |
|--------|------|-------------|
| GET | /collections | List collections |
| POST | /collections | Create collection |
| GET | /collections/{collectionName} | Describe collection |
| DELETE | /collections/{collectionName} | Delete Collection |

### databases
| Method | Path | Description |
|--------|------|-------------|
| GET | /databases | List indexes |
| POST | /databases | Create index |
| GET | /databases/{indexName} | Describe index |
| DELETE | /databases/{indexName} | Delete Index |
| PATCH | /databases/{indexName} | Configure index |

### describe_index_stats
| Method | Path | Description |
|--------|------|-------------|
| POST | /describe_index_stats | Describe Index Stats |

### query
| Method | Path | Description |
|--------|------|-------------|
| POST | /query | Query |

### vectors
| Method | Path | Description |
|--------|------|-------------|
| POST | /vectors/delete | Delete |
| POST | /vectors/fetch | Fetch |
| POST | /vectors/update | Fetch |
| POST | /vectors/upsert | Upsert |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all collections?" -> GET /collections
- "Create a collection?" -> POST /collections
- "Get collection details?" -> GET /collections/{collectionName}
- "Delete a collection?" -> DELETE /collections/{collectionName}
- "List all databases?" -> GET /databases
- "Create a database?" -> POST /databases
- "Get database details?" -> GET /databases/{indexName}
- "Delete a database?" -> DELETE /databases/{indexName}
- "Partially update a database?" -> PATCH /databases/{indexName}
- "Create a describe_index_stat?" -> POST /describe_index_stats
- "Create a query?" -> POST /query
- "Create a delete?" -> POST /vectors/delete
- "Create a fetch?" -> POST /vectors/fetch
- "Create a update?" -> POST /vectors/update
- "Create a upsert?" -> POST /vectors/upsert
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
