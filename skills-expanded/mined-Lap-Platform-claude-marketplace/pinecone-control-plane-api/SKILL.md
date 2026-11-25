---
name: pinecone-control-plane-api
description: "Pinecone Control Plane API skill. Use when working with Pinecone Control Plane for indexes, collections, backups. Covers 18 endpoints."
version: 1.0.0
generator: lapsh
---

# Pinecone Control Plane API
API version: 2025-10

## Auth
ApiKey Api-Key in header

## Base URL
https://api.pinecone.io

## Setup
1. Set your API key in the appropriate header
2. GET /indexes -- verify access
3. POST /indexes -- create first indexes

## Endpoints

18 endpoints across 4 groups. See references/api-spec.lap for full details.

### indexes
| Method | Path | Description |
|--------|------|-------------|
| GET | /indexes | List indexes |
| POST | /indexes | Create an index |
| GET | /indexes/{index_name} | Describe an index |
| DELETE | /indexes/{index_name} | Delete an index |
| PATCH | /indexes/{index_name} | Configure an index |
| GET | /indexes/{index_name}/backups | List backups for an index |
| POST | /indexes/{index_name}/backups | Create a backup of an index |
| POST | /indexes/create-for-model | Create an index with integrated embedding |

### collections
| Method | Path | Description |
|--------|------|-------------|
| GET | /collections | List collections |
| POST | /collections | Create a collection |
| GET | /collections/{collection_name} | Describe a collection |
| DELETE | /collections/{collection_name} | Delete a collection |

### backups
| Method | Path | Description |
|--------|------|-------------|
| GET | /backups | List backups for all indexes in a project |
| GET | /backups/{backup_id} | Describe a backup |
| DELETE | /backups/{backup_id} | Delete a backup |
| POST | /backups/{backup_id}/create-index | Create an index from a backup |

### restore-jobs
| Method | Path | Description |
|--------|------|-------------|
| GET | /restore-jobs | List restore jobs |
| GET | /restore-jobs/{job_id} | Describe a restore job |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all indexes?" -> GET /indexes
- "Create a indexe?" -> POST /indexes
- "Get indexe details?" -> GET /indexes/{index_name}
- "Delete a indexe?" -> DELETE /indexes/{index_name}
- "Partially update a indexe?" -> PATCH /indexes/{index_name}
- "List all backups?" -> GET /indexes/{index_name}/backups
- "Create a backup?" -> POST /indexes/{index_name}/backups
- "List all collections?" -> GET /collections
- "Create a collection?" -> POST /collections
- "Create a create-for-model?" -> POST /indexes/create-for-model
- "List all backups?" -> GET /backups
- "Get backup details?" -> GET /backups/{backup_id}
- "Delete a backup?" -> DELETE /backups/{backup_id}
- "Create a create-index?" -> POST /backups/{backup_id}/create-index
- "List all restore-jobs?" -> GET /restore-jobs
- "Get restore-job details?" -> GET /restore-jobs/{job_id}
- "Get collection details?" -> GET /collections/{collection_name}
- "Delete a collection?" -> DELETE /collections/{collection_name}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
