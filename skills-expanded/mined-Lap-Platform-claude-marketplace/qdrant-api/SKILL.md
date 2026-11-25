---
name: qdrant-api
description: "Qdrant API skill. Use when working with Qdrant for collections, root, telemetry. Covers 73 endpoints."
version: 1.0.0
generator: lapsh
---

# Qdrant API
API version: master

## Auth
ApiKey api-key in header | Bearer bearer

## Base URL
http://localhost:6333

## Setup
1. Set Authorization header with your Bearer token
2. GET / -- verify access
3. POST /collections/{collection_name}/shards/delete -- create first delete

## Endpoints

73 endpoints across 11 groups. See references/api-spec.lap for full details.

### collections
| Method | Path | Description |
|--------|------|-------------|
| PUT | /collections/{collection_name}/shards | Create shard key |
| GET | /collections/{collection_name}/shards | List shard keys |
| POST | /collections/{collection_name}/shards/delete | Delete shard key |
| GET | /collections | List collections |
| GET | /collections/{collection_name} | Collection info |
| PUT | /collections/{collection_name} | Create collection |
| PATCH | /collections/{collection_name} | Update collection parameters |
| DELETE | /collections/{collection_name} | Delete collection |
| POST | /collections/aliases | Update aliases of the collections |
| PUT | /collections/{collection_name}/index | Create index for field in collection |
| GET | /collections/{collection_name}/exists | Check the existence of a collection |
| DELETE | /collections/{collection_name}/index/{field_name} | Delete index for field in collection |
| GET | /collections/{collection_name}/cluster | Collection cluster info |
| POST | /collections/{collection_name}/cluster | Update collection cluster setup |
| GET | /collections/{collection_name}/optimizations | Get optimization progress |
| GET | /collections/{collection_name}/aliases | List aliases for collection |
| POST | /collections/{collection_name}/snapshots/upload | Recover from an uploaded snapshot |
| PUT | /collections/{collection_name}/snapshots/recover | Recover from a snapshot |
| GET | /collections/{collection_name}/snapshots | List collection snapshots |
| POST | /collections/{collection_name}/snapshots | Create collection snapshot |
| DELETE | /collections/{collection_name}/snapshots/{snapshot_name} | Delete collection snapshot |
| GET | /collections/{collection_name}/snapshots/{snapshot_name} | Download collection snapshot |
| GET | /collections/{collection_name}/shards/{shard_id}/snapshot | Download shard snapshot |
| POST | /collections/{collection_name}/shards/{shard_id}/snapshots/upload | Recover shard from an uploaded snapshot |
| PUT | /collections/{collection_name}/shards/{shard_id}/snapshots/recover | Recover from a snapshot |
| GET | /collections/{collection_name}/shards/{shard_id}/snapshots | List shards snapshots for a collection |
| POST | /collections/{collection_name}/shards/{shard_id}/snapshots | Create shard snapshot |
| DELETE | /collections/{collection_name}/shards/{shard_id}/snapshots/{snapshot_name} | Delete shard snapshot |
| GET | /collections/{collection_name}/shards/{shard_id}/snapshots/{snapshot_name} | Download collection snapshot |
| GET | /collections/{collection_name}/points/{id} | Get point |
| POST | /collections/{collection_name}/points | Get points |
| PUT | /collections/{collection_name}/points | Upsert points |
| POST | /collections/{collection_name}/points/delete | Delete points |
| PUT | /collections/{collection_name}/points/vectors | Update vectors |
| POST | /collections/{collection_name}/points/vectors/delete | Delete vectors |
| POST | /collections/{collection_name}/points/payload | Set payload |
| PUT | /collections/{collection_name}/points/payload | Overwrite payload |
| POST | /collections/{collection_name}/points/payload/delete | Delete payload |
| POST | /collections/{collection_name}/points/payload/clear | Clear payload |
| POST | /collections/{collection_name}/points/batch | Batch update points |
| POST | /collections/{collection_name}/points/scroll | Scroll points |
| POST | /collections/{collection_name}/points/search | Search points |
| POST | /collections/{collection_name}/points/search/batch | Search batch points |
| POST | /collections/{collection_name}/points/search/groups | Search point groups |
| POST | /collections/{collection_name}/points/recommend | Recommend points |
| POST | /collections/{collection_name}/points/recommend/batch | Recommend batch points |
| POST | /collections/{collection_name}/points/recommend/groups | Recommend point groups |
| POST | /collections/{collection_name}/points/discover | Discover points |
| POST | /collections/{collection_name}/points/discover/batch | Discover batch points |
| POST | /collections/{collection_name}/points/count | Count points |
| POST | /collections/{collection_name}/facet | Facet a payload key with a given filter. |
| POST | /collections/{collection_name}/points/query | Query points |
| POST | /collections/{collection_name}/points/query/batch | Query points in batch |
| POST | /collections/{collection_name}/points/query/groups | Query points, grouped by a given payload field |
| POST | /collections/{collection_name}/points/search/matrix/pairs | Search points matrix distance pairs |
| POST | /collections/{collection_name}/points/search/matrix/offsets | Search points matrix distance offsets |

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | Returns information about the running Qdrant instance |

### telemetry
| Method | Path | Description |
|--------|------|-------------|
| GET | /telemetry | Collect telemetry data |

### metrics
| Method | Path | Description |
|--------|------|-------------|
| GET | /metrics | Collect Prometheus metrics data |

### healthz
| Method | Path | Description |
|--------|------|-------------|
| GET | /healthz | Kubernetes healthz endpoint |

### livez
| Method | Path | Description |
|--------|------|-------------|
| GET | /livez | Kubernetes livez endpoint |

### readyz
| Method | Path | Description |
|--------|------|-------------|
| GET | /readyz | Kubernetes readyz endpoint |

### issues
| Method | Path | Description |
|--------|------|-------------|
| GET | /issues | Get issues |
| DELETE | /issues | Clear issues |

### cluster
| Method | Path | Description |
|--------|------|-------------|
| GET | /cluster | Get cluster status info |
| GET | /cluster/telemetry | Collect cluster telemetry data |
| POST | /cluster/recover | Tries to recover current peer Raft state. |
| DELETE | /cluster/peer/{peer_id} | Remove peer from the cluster |

### aliases
| Method | Path | Description |
|--------|------|-------------|
| GET | /aliases | List collections aliases |

### snapshots
| Method | Path | Description |
|--------|------|-------------|
| GET | /snapshots | List of storage snapshots |
| POST | /snapshots | Create storage snapshot |
| DELETE | /snapshots/{snapshot_name} | Delete storage snapshot |
| GET | /snapshots/{snapshot_name} | Download storage snapshot |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all shards?" -> GET /collections/{collection_name}/shards
- "Create a delete?" -> POST /collections/{collection_name}/shards/delete
- "List all telemetry?" -> GET /telemetry
- "List all metrics?" -> GET /metrics
- "List all healthz?" -> GET /healthz
- "List all livez?" -> GET /livez
- "List all readyz?" -> GET /readyz
- "List all issues?" -> GET /issues
- "List all cluster?" -> GET /cluster
- "List all telemetry?" -> GET /cluster/telemetry
- "Create a recover?" -> POST /cluster/recover
- "Delete a peer?" -> DELETE /cluster/peer/{peer_id}
- "List all collections?" -> GET /collections
- "Get collection details?" -> GET /collections/{collection_name}
- "Update a collection?" -> PUT /collections/{collection_name}
- "Partially update a collection?" -> PATCH /collections/{collection_name}
- "Delete a collection?" -> DELETE /collections/{collection_name}
- "Create a aliase?" -> POST /collections/aliases
- "List all exists?" -> GET /collections/{collection_name}/exists
- "Delete a index?" -> DELETE /collections/{collection_name}/index/{field_name}
- "List all cluster?" -> GET /collections/{collection_name}/cluster
- "Create a cluster?" -> POST /collections/{collection_name}/cluster
- "List all optimizations?" -> GET /collections/{collection_name}/optimizations
- "List all aliases?" -> GET /collections/{collection_name}/aliases
- "List all aliases?" -> GET /aliases
- "Create a upload?" -> POST /collections/{collection_name}/snapshots/upload
- "List all snapshots?" -> GET /collections/{collection_name}/snapshots
- "Create a snapshot?" -> POST /collections/{collection_name}/snapshots
- "Delete a snapshot?" -> DELETE /collections/{collection_name}/snapshots/{snapshot_name}
- "Get snapshot details?" -> GET /collections/{collection_name}/snapshots/{snapshot_name}
- "List all snapshots?" -> GET /snapshots
- "Create a snapshot?" -> POST /snapshots
- "Delete a snapshot?" -> DELETE /snapshots/{snapshot_name}
- "Get snapshot details?" -> GET /snapshots/{snapshot_name}
- "List all snapshot?" -> GET /collections/{collection_name}/shards/{shard_id}/snapshot
- "Create a upload?" -> POST /collections/{collection_name}/shards/{shard_id}/snapshots/upload
- "List all snapshots?" -> GET /collections/{collection_name}/shards/{shard_id}/snapshots
- "Create a snapshot?" -> POST /collections/{collection_name}/shards/{shard_id}/snapshots
- "Delete a snapshot?" -> DELETE /collections/{collection_name}/shards/{shard_id}/snapshots/{snapshot_name}
- "Get snapshot details?" -> GET /collections/{collection_name}/shards/{shard_id}/snapshots/{snapshot_name}
- "Get point details?" -> GET /collections/{collection_name}/points/{id}
- "Create a point?" -> POST /collections/{collection_name}/points
- "Create a delete?" -> POST /collections/{collection_name}/points/delete
- "Create a delete?" -> POST /collections/{collection_name}/points/vectors/delete
- "Create a payload?" -> POST /collections/{collection_name}/points/payload
- "Create a delete?" -> POST /collections/{collection_name}/points/payload/delete
- "Create a clear?" -> POST /collections/{collection_name}/points/payload/clear
- "Create a batch?" -> POST /collections/{collection_name}/points/batch
- "Create a scroll?" -> POST /collections/{collection_name}/points/scroll
- "Create a search?" -> POST /collections/{collection_name}/points/search
- "Create a batch?" -> POST /collections/{collection_name}/points/search/batch
- "Create a group?" -> POST /collections/{collection_name}/points/search/groups
- "Create a recommend?" -> POST /collections/{collection_name}/points/recommend
- "Create a batch?" -> POST /collections/{collection_name}/points/recommend/batch
- "Create a group?" -> POST /collections/{collection_name}/points/recommend/groups
- "Create a discover?" -> POST /collections/{collection_name}/points/discover
- "Create a batch?" -> POST /collections/{collection_name}/points/discover/batch
- "Create a count?" -> POST /collections/{collection_name}/points/count
- "Create a facet?" -> POST /collections/{collection_name}/facet
- "Create a query?" -> POST /collections/{collection_name}/points/query
- "Create a batch?" -> POST /collections/{collection_name}/points/query/batch
- "Create a group?" -> POST /collections/{collection_name}/points/query/groups
- "Create a pair?" -> POST /collections/{collection_name}/points/search/matrix/pairs
- "Create a offset?" -> POST /collections/{collection_name}/points/search/matrix/offsets
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
