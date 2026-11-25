---
name: schemas
description: "Schemas API skill. Use when working with Schemas for discoverers, registries, policy. Covers 31 endpoints."
version: 1.0.0
generator: lapsh
---

# Schemas
API version: 2019-12-02

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /v1/policy -- verify access
3. POST /v1/discoverers -- create first discoverers

## Endpoints

31 endpoints across 5 groups. See references/api-spec.lap for full details.

### discoverers
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/discoverers | Creates a discoverer. |
| DELETE | /v1/discoverers/id/{discovererId} | Deletes a discoverer. |
| GET | /v1/discoverers/id/{discovererId} | Describes the discoverer. |
| GET | /v1/discoverers | List the discoverers. |
| POST | /v1/discoverers/id/{discovererId}/start | Starts the discoverer |
| POST | /v1/discoverers/id/{discovererId}/stop | Stops the discoverer |
| PUT | /v1/discoverers/id/{discovererId} | Updates the discoverer |

### registries
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/registries/name/{registryName} | Creates a registry. |
| POST | /v1/registries/name/{registryName}/schemas/name/{schemaName} | Creates a schema definition. Inactive schemas will be deleted after two years. |
| DELETE | /v1/registries/name/{registryName} | Deletes a Registry. |
| DELETE | /v1/registries/name/{registryName}/schemas/name/{schemaName} | Delete a schema definition. |
| DELETE | /v1/registries/name/{registryName}/schemas/name/{schemaName}/version/{schemaVersion} | Delete the schema version definition |
| GET | /v1/registries/name/{registryName}/schemas/name/{schemaName}/language/{language} | Describe the code binding URI. |
| GET | /v1/registries/name/{registryName} | Describes the registry. |
| GET | /v1/registries/name/{registryName}/schemas/name/{schemaName} | Retrieve the schema definition. |
| GET | /v1/registries/name/{registryName}/schemas/name/{schemaName}/export |  |
| GET | /v1/registries/name/{registryName}/schemas/name/{schemaName}/language/{language}/source | Get the code binding source URI. |
| GET | /v1/registries | List the registries. |
| GET | /v1/registries/name/{registryName}/schemas/name/{schemaName}/versions | Provides a list of the schema versions and related information. |
| GET | /v1/registries/name/{registryName}/schemas | List the schemas. |
| POST | /v1/registries/name/{registryName}/schemas/name/{schemaName}/language/{language} | Put code binding URI |
| GET | /v1/registries/name/{registryName}/schemas/search | Search the schemas |
| PUT | /v1/registries/name/{registryName} | Updates a registry. |
| PUT | /v1/registries/name/{registryName}/schemas/name/{schemaName} | Updates the schema definition Inactive schemas will be deleted after two years. |

### policy
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /v1/policy | Delete the resource-based policy attached to the specified registry. |
| GET | /v1/policy | Retrieves the resource-based policy attached to a given registry. |
| PUT | /v1/policy | The name of the policy. |

### discover
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/discover | Get the discovered schema that was generated based on sampled events. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resource-arn} | Get tags for resource. |
| POST | /tags/{resource-arn} | Add tags to a resource. |
| DELETE | /tags/{resource-arn} | Removes tags from a resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a discoverer?" -> POST /v1/discoverers
- "Delete a id?" -> DELETE /v1/discoverers/id/{discovererId}
- "Delete a name?" -> DELETE /v1/registries/name/{registryName}
- "Delete a name?" -> DELETE /v1/registries/name/{registryName}/schemas/name/{schemaName}
- "Delete a version?" -> DELETE /v1/registries/name/{registryName}/schemas/name/{schemaName}/version/{schemaVersion}
- "Get language details?" -> GET /v1/registries/name/{registryName}/schemas/name/{schemaName}/language/{language}
- "Get id details?" -> GET /v1/discoverers/id/{discovererId}
- "Get name details?" -> GET /v1/registries/name/{registryName}
- "Get name details?" -> GET /v1/registries/name/{registryName}/schemas/name/{schemaName}
- "List all export?" -> GET /v1/registries/name/{registryName}/schemas/name/{schemaName}/export
- "List all source?" -> GET /v1/registries/name/{registryName}/schemas/name/{schemaName}/language/{language}/source
- "Create a discover?" -> POST /v1/discover
- "List all policy?" -> GET /v1/policy
- "List all discoverers?" -> GET /v1/discoverers
- "List all registries?" -> GET /v1/registries
- "List all versions?" -> GET /v1/registries/name/{registryName}/schemas/name/{schemaName}/versions
- "List all schemas?" -> GET /v1/registries/name/{registryName}/schemas
- "Get tag details?" -> GET /tags/{resource-arn}
- "List all search?" -> GET /v1/registries/name/{registryName}/schemas/search
- "Create a start?" -> POST /v1/discoverers/id/{discovererId}/start
- "Create a stop?" -> POST /v1/discoverers/id/{discovererId}/stop
- "Delete a tag?" -> DELETE /tags/{resource-arn}
- "Update a id?" -> PUT /v1/discoverers/id/{discovererId}
- "Update a name?" -> PUT /v1/registries/name/{registryName}
- "Update a name?" -> PUT /v1/registries/name/{registryName}/schemas/name/{schemaName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
