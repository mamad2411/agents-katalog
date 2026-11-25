---
name: weaviate-rest-api
description: "Weaviate REST API skill. Use when working with Weaviate REST for root, .well-known, replication. Covers 101 endpoints."
version: 1.0.0
generator: lapsh
---

# Weaviate REST API
API version: 1.37.0-dev

## Auth
OAuth2

## Base URL
Not specified.

## Setup
1. Configure auth: OAuth2
2. GET / -- verify access
3. POST /replication/replicate -- create first replicate

## Endpoints

101 endpoints across 17 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | List available endpoints |

### .well-known
| Method | Path | Description |
|--------|------|-------------|
| GET | /.well-known/live | Check application liveness |
| GET | /.well-known/ready | Check application readiness |
| GET | /.well-known/openid-configuration | Get OIDC configuration |

### replication
| Method | Path | Description |
|--------|------|-------------|
| POST | /replication/replicate | Initiate a replica movement |
| DELETE | /replication/replicate | Delete all replication operations |
| POST | /replication/replicate/force-delete | Force delete replication operations |
| GET | /replication/replicate/{id} | Retrieve a replication operation |
| DELETE | /replication/replicate/{id} | Delete a replication operation |
| GET | /replication/replicate/list | List replication operations |
| POST | /replication/replicate/{id}/cancel | Cancel a replication operation |
| GET | /replication/sharding-state | Get sharding state |
| GET | /replication/scale | Get replication scale plan |
| POST | /replication/scale | Apply replication scaling plan |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/own-info | Get current user info |
| GET | /users/db | List all users |
| GET | /users/db/{user_id} | Get user info |
| POST | /users/db/{user_id} | Create a new user |
| DELETE | /users/db/{user_id} | Delete a user |
| POST | /users/db/{user_id}/rotate-key | Rotate API key of a user |
| POST | /users/db/{user_id}/activate | Activate a user |
| POST | /users/db/{user_id}/deactivate | Deactivate a user |

### authz
| Method | Path | Description |
|--------|------|-------------|
| GET | /authz/roles | Get all roles |
| POST | /authz/roles | Create new role |
| POST | /authz/roles/{id}/add-permissions | Add permissions to a role |
| POST | /authz/roles/{id}/remove-permissions | Remove permissions from a role |
| GET | /authz/roles/{id} | Get a role |
| DELETE | /authz/roles/{id} | Delete a role |
| POST | /authz/roles/{id}/has-permission | Check whether a role possesses a permission |
| GET | /authz/roles/{id}/users | Get users assigned to a role |
| GET | /authz/roles/{id}/user-assignments | Get users assigned to a role |
| GET | /authz/roles/{id}/group-assignments | Get groups that have a specific role assigned |
| GET | /authz/users/{id}/roles | Get roles assigned to a user |
| GET | /authz/users/{id}/roles/{userType} | Get roles assigned to a user |
| POST | /authz/users/{id}/assign | Assign a role to a user |
| POST | /authz/users/{id}/revoke | Revoke a role from a user |
| POST | /authz/groups/{id}/assign | Assign a role to a group |
| POST | /authz/groups/{id}/revoke | Revoke a role from a group |
| GET | /authz/groups/{id}/roles/{groupType} | Get roles assigned to a specific group |
| GET | /authz/groups/{groupType} | List all groups of a specific type |

### objects
| Method | Path | Description |
|--------|------|-------------|
| GET | /objects | List objects |
| POST | /objects | Create an object |
| DELETE | /objects/{id} | Delete an object |
| GET | /objects/{id} | Get an object |
| PATCH | /objects/{id} | Patch an object |
| PUT | /objects/{id} | Update an object |
| HEAD | /objects/{id} | Check if an object exists |
| GET | /objects/{className}/{id} | Get an object |
| DELETE | /objects/{className}/{id} | Delete an object |
| PUT | /objects/{className}/{id} | Replace an object |
| PATCH | /objects/{className}/{id} | Patch an object |
| HEAD | /objects/{className}/{id} | Check if an object exists |
| POST | /objects/{id}/references/{propertyName} | Add an object reference |
| PUT | /objects/{id}/references/{propertyName} | Replace object references |
| DELETE | /objects/{id}/references/{propertyName} | Delete an object reference |
| POST | /objects/{className}/{id}/references/{propertyName} | Add an object reference |
| PUT | /objects/{className}/{id}/references/{propertyName} | Replace object references |
| DELETE | /objects/{className}/{id}/references/{propertyName} | Delete an object reference |
| POST | /objects/validate | Validate an object |

### batch
| Method | Path | Description |
|--------|------|-------------|
| POST | /batch/objects | Create objects in batch |
| DELETE | /batch/objects | Delete objects in batch |
| POST | /batch/references | Create cross-references in bulk |

### graphql
| Method | Path | Description |
|--------|------|-------------|
| POST | /graphql | Perform a GraphQL query |
| POST | /graphql/batch | Perform batched GraphQL queries |

### meta
| Method | Path | Description |
|--------|------|-------------|
| GET | /meta | Get instance metadata |

### schema
| Method | Path | Description |
|--------|------|-------------|
| GET | /schema | Get all collection definitions |
| POST | /schema | Create a new collection |
| GET | /schema/{className} | Get a single collection |
| DELETE | /schema/{className} | Delete a collection (and all associated data) |
| PUT | /schema/{className} | Update collection definition |
| POST | /schema/{className}/properties | Add a property to a collection |
| DELETE | /schema/{className}/properties/{propertyName}/index/{indexName} | Delete a property's inverted index |
| GET | /schema/{className}/shards | Get the shards status of a collection |
| PUT | /schema/{className}/shards/{shardName} | Update a shard status |
| POST | /schema/{className}/tenants | Create a new tenant |
| PUT | /schema/{className}/tenants | Update a tenant |
| DELETE | /schema/{className}/tenants | Delete tenants |
| GET | /schema/{className}/tenants | Get the list of tenants |
| HEAD | /schema/{className}/tenants/{tenantName} | Check if a tenant exists |
| GET | /schema/{className}/tenants/{tenantName} | Get a specific tenant |

### aliases
| Method | Path | Description |
|--------|------|-------------|
| GET | /aliases | List aliases |
| POST | /aliases | Create a new alias |
| GET | /aliases/{aliasName} | Get an alias |
| PUT | /aliases/{aliasName} | Update an alias |
| DELETE | /aliases/{aliasName} | Delete an alias |

### backups
| Method | Path | Description |
|--------|------|-------------|
| POST | /backups/{backend} | Create a backup |
| GET | /backups/{backend} | List all created backups |
| GET | /backups/{backend}/{id} | Get backup creation status |
| DELETE | /backups/{backend}/{id} | Cancel a backup |
| POST | /backups/{backend}/{id}/restore | Restore from a backup |
| GET | /backups/{backend}/{id}/restore | Get backup restoration status |
| DELETE | /backups/{backend}/{id}/restore | Cancel a backup restoration |

### export
| Method | Path | Description |
|--------|------|-------------|
| POST | /export/{backend} | Start a new export |
| GET | /export/{backend}/{id} | Get export status |
| DELETE | /export/{backend}/{id} | Cancel an export |

### cluster
| Method | Path | Description |
|--------|------|-------------|
| GET | /cluster/statistics | Get cluster statistics |

### nodes
| Method | Path | Description |
|--------|------|-------------|
| GET | /nodes | Get node status |
| GET | /nodes/{className} | Get node status by collection |

### tasks
| Method | Path | Description |
|--------|------|-------------|
| GET | /tasks | Lists all distributed tasks in the cluster |

### classifications
| Method | Path | Description |
|--------|------|-------------|
| POST | /classifications/ | Start a classification |
| GET | /classifications/{id} | Get classification status |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all live?" -> GET /.well-known/live
- "List all ready?" -> GET /.well-known/ready
- "List all openid-configuration?" -> GET /.well-known/openid-configuration
- "Create a replicate?" -> POST /replication/replicate
- "Create a force-delete?" -> POST /replication/replicate/force-delete
- "Get replicate details?" -> GET /replication/replicate/{id}
- "Delete a replicate?" -> DELETE /replication/replicate/{id}
- "List all list?" -> GET /replication/replicate/list
- "Create a cancel?" -> POST /replication/replicate/{id}/cancel
- "List all sharding-state?" -> GET /replication/sharding-state
- "List all scale?" -> GET /replication/scale
- "Create a scale?" -> POST /replication/scale
- "List all own-info?" -> GET /users/own-info
- "List all db?" -> GET /users/db
- "Get db details?" -> GET /users/db/{user_id}
- "Delete a db?" -> DELETE /users/db/{user_id}
- "Create a rotate-key?" -> POST /users/db/{user_id}/rotate-key
- "Create a activate?" -> POST /users/db/{user_id}/activate
- "Create a deactivate?" -> POST /users/db/{user_id}/deactivate
- "List all roles?" -> GET /authz/roles
- "Create a role?" -> POST /authz/roles
- "Create a add-permission?" -> POST /authz/roles/{id}/add-permissions
- "Create a remove-permission?" -> POST /authz/roles/{id}/remove-permissions
- "Get role details?" -> GET /authz/roles/{id}
- "Delete a role?" -> DELETE /authz/roles/{id}
- "Create a has-permission?" -> POST /authz/roles/{id}/has-permission
- "List all users?" -> GET /authz/roles/{id}/users
- "List all user-assignments?" -> GET /authz/roles/{id}/user-assignments
- "List all group-assignments?" -> GET /authz/roles/{id}/group-assignments
- "List all roles?" -> GET /authz/users/{id}/roles
- "Get role details?" -> GET /authz/users/{id}/roles/{userType}
- "Create a assign?" -> POST /authz/users/{id}/assign
- "Create a revoke?" -> POST /authz/users/{id}/revoke
- "Create a assign?" -> POST /authz/groups/{id}/assign
- "Create a revoke?" -> POST /authz/groups/{id}/revoke
- "Get role details?" -> GET /authz/groups/{id}/roles/{groupType}
- "Get group details?" -> GET /authz/groups/{groupType}
- "List all objects?" -> GET /objects
- "Create a object?" -> POST /objects
- "Delete a object?" -> DELETE /objects/{id}
- "Get object details?" -> GET /objects/{id}
- "Partially update a object?" -> PATCH /objects/{id}
- "Update a object?" -> PUT /objects/{id}
- "Get object details?" -> GET /objects/{className}/{id}
- "Delete a object?" -> DELETE /objects/{className}/{id}
- "Update a object?" -> PUT /objects/{className}/{id}
- "Partially update a object?" -> PATCH /objects/{className}/{id}
- "Update a reference?" -> PUT /objects/{id}/references/{propertyName}
- "Delete a reference?" -> DELETE /objects/{id}/references/{propertyName}
- "Update a reference?" -> PUT /objects/{className}/{id}/references/{propertyName}
- "Delete a reference?" -> DELETE /objects/{className}/{id}/references/{propertyName}
- "Create a validate?" -> POST /objects/validate
- "Create a object?" -> POST /batch/objects
- "Create a reference?" -> POST /batch/references
- "Create a graphql?" -> POST /graphql
- "Create a batch?" -> POST /graphql/batch
- "List all meta?" -> GET /meta
- "List all schema?" -> GET /schema
- "Create a schema?" -> POST /schema
- "Get schema details?" -> GET /schema/{className}
- "Delete a schema?" -> DELETE /schema/{className}
- "Update a schema?" -> PUT /schema/{className}
- "Create a property?" -> POST /schema/{className}/properties
- "Delete a index?" -> DELETE /schema/{className}/properties/{propertyName}/index/{indexName}
- "List all shards?" -> GET /schema/{className}/shards
- "Update a shard?" -> PUT /schema/{className}/shards/{shardName}
- "Create a tenant?" -> POST /schema/{className}/tenants
- "List all tenants?" -> GET /schema/{className}/tenants
- "Get tenant details?" -> GET /schema/{className}/tenants/{tenantName}
- "List all aliases?" -> GET /aliases
- "Create a aliase?" -> POST /aliases
- "Get aliase details?" -> GET /aliases/{aliasName}
- "Update a aliase?" -> PUT /aliases/{aliasName}
- "Delete a aliase?" -> DELETE /aliases/{aliasName}
- "Get backup details?" -> GET /backups/{backend}
- "Get backup details?" -> GET /backups/{backend}/{id}
- "Delete a backup?" -> DELETE /backups/{backend}/{id}
- "Create a restore?" -> POST /backups/{backend}/{id}/restore
- "List all restore?" -> GET /backups/{backend}/{id}/restore
- "Get export details?" -> GET /export/{backend}/{id}
- "Delete a export?" -> DELETE /export/{backend}/{id}
- "List all statistics?" -> GET /cluster/statistics
- "List all nodes?" -> GET /nodes
- "Get node details?" -> GET /nodes/{className}
- "List all tasks?" -> GET /tasks
- "Create a classification?" -> POST /classifications/
- "Get classification details?" -> GET /classifications/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
