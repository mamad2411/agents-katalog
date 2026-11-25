---
name: apicurio-registry-api-v2
description: "Apicurio Registry API [v2] API skill. Use when working with Apicurio Registry API [v2] for ids, admin, system. Covers 65 endpoints."
version: 1.0.0
generator: lapsh
---

# Apicurio Registry API [v2]
API version: 2.6.x

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /admin/artifactTypes -- verify access
3. POST /admin/rules -- create first rules

## Endpoints

65 endpoints across 6 groups. See references/api-spec.lap for full details.

### ids
| Method | Path | Description |
|--------|------|-------------|
| GET | /ids/globalIds/{globalId} | Get artifact by global ID |
| GET | /ids/contentHashes/{contentHash}/references | List artifact references by hash |
| GET | /ids/contentIds/{contentId}/references | List artifact references by content ID |
| GET | /ids/globalIds/{globalId}/references | List artifact references by global ID |
| GET | /ids/contentIds/{contentId} | Get artifact content by ID |
| GET | /ids/contentHashes/{contentHash} | Get artifact content by SHA-256 hash |

### admin
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin/artifactTypes | List artifact types |
| GET | /admin/rules | List global rules |
| POST | /admin/rules | Create global rule |
| DELETE | /admin/rules | Delete all global rules |
| GET | /admin/rules/{rule} | Get global rule configuration |
| PUT | /admin/rules/{rule} | Update global rule configuration |
| DELETE | /admin/rules/{rule} | Delete global rule |
| GET | /admin/export | Export registry data |
| POST | /admin/import | Import registry data |
| GET | /admin/roleMappings/{principalId} | Return a single role mapping |
| PUT | /admin/roleMappings/{principalId} | Update a role mapping |
| DELETE | /admin/roleMappings/{principalId} | Delete a role mapping |
| GET | /admin/roleMappings | List all role mappings |
| POST | /admin/roleMappings | Create a new role mapping |
| GET | /admin/config/properties | List all configuration properties |
| GET | /admin/config/properties/{propertyName} | Get configuration property value |
| PUT | /admin/config/properties/{propertyName} | Update a configuration property |
| DELETE | /admin/config/properties/{propertyName} | Reset a configuration property |

### system
| Method | Path | Description |
|--------|------|-------------|
| GET | /system/info | Get system information |
| GET | /system/limits | Get resource limits information |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search/artifacts | Search for artifacts |
| POST | /search/artifacts | Search for artifacts by content |

### groups
| Method | Path | Description |
|--------|------|-------------|
| PUT | /groups/{groupId}/artifacts/{artifactId}/state | Update artifact state |
| GET | /groups/{groupId}/artifacts/{artifactId}/versions/{version}/meta | Get artifact version metadata |
| PUT | /groups/{groupId}/artifacts/{artifactId}/versions/{version}/meta | Update artifact version metadata |
| DELETE | /groups/{groupId}/artifacts/{artifactId}/versions/{version}/meta | Delete artifact version metadata |
| GET | /groups/{groupId}/artifacts/{artifactId}/versions/{version} | Get artifact version |
| DELETE | /groups/{groupId}/artifacts/{artifactId}/versions/{version} | Delete artifact version |
| PUT | /groups/{groupId}/artifacts/{artifactId}/versions/{version}/state | Update artifact version state |
| GET | /groups/{groupId}/artifacts/{artifactId}/rules | List artifact rules |
| POST | /groups/{groupId}/artifacts/{artifactId}/rules | Create artifact rule |
| DELETE | /groups/{groupId}/artifacts/{artifactId}/rules | Delete artifact rules |
| GET | /groups/{groupId}/artifacts/{artifactId}/rules/{rule} | Get artifact rule configuration |
| PUT | /groups/{groupId}/artifacts/{artifactId}/rules/{rule} | Update artifact rule configuration |
| DELETE | /groups/{groupId}/artifacts/{artifactId}/rules/{rule} | Delete artifact rule |
| GET | /groups/{groupId}/artifacts/{artifactId}/versions/{version}/references | Get artifact version references |
| GET | /groups/{groupId}/artifacts/{artifactId} | Get latest artifact |
| PUT | /groups/{groupId}/artifacts/{artifactId} | Update artifact |
| DELETE | /groups/{groupId}/artifacts/{artifactId} | Delete artifact |
| GET | /groups/{groupId}/artifacts | List artifacts in group |
| POST | /groups/{groupId}/artifacts | Create artifact |
| DELETE | /groups/{groupId}/artifacts | Delete artifacts in group |
| PUT | /groups/{groupId}/artifacts/{artifactId}/test | Test update artifact |
| GET | /groups/{groupId}/artifacts/{artifactId}/versions | List artifact versions |
| POST | /groups/{groupId}/artifacts/{artifactId}/versions | Create artifact version |
| GET | /groups/{groupId}/artifacts/{artifactId}/owner | Get artifact owner |
| PUT | /groups/{groupId}/artifacts/{artifactId}/owner | Update artifact owner |
| GET | /groups/{groupId} | Get a group by the specified ID. |
| DELETE | /groups/{groupId} | Delete a group by the specified ID. |
| GET | /groups | List groups |
| POST | /groups | Create a new group |
| GET | /groups/{groupId}/artifacts/{artifactId}/meta | Get artifact metadata |
| PUT | /groups/{groupId}/artifacts/{artifactId}/meta | Update artifact metadata |
| POST | /groups/{groupId}/artifacts/{artifactId}/meta | Get artifact version metadata by content |
| GET | /groups/{groupId}/artifacts/{artifactId}/versions/{version}/comments | Get artifact version comments |
| POST | /groups/{groupId}/artifacts/{artifactId}/versions/{version}/comments | Add new comment |
| PUT | /groups/{groupId}/artifacts/{artifactId}/versions/{version}/comments/{commentId} | Update a comment |
| DELETE | /groups/{groupId}/artifacts/{artifactId}/versions/{version}/comments/{commentId} | Delete a single comment |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/me | Get current user |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get globalId details?" -> GET /ids/globalIds/{globalId}
- "List all artifactTypes?" -> GET /admin/artifactTypes
- "List all rules?" -> GET /admin/rules
- "Create a rule?" -> POST /admin/rules
- "Get rule details?" -> GET /admin/rules/{rule}
- "Update a rule?" -> PUT /admin/rules/{rule}
- "Delete a rule?" -> DELETE /admin/rules/{rule}
- "List all info?" -> GET /system/info
- "List all artifacts?" -> GET /search/artifacts
- "Create a artifact?" -> POST /search/artifacts
- "List all export?" -> GET /admin/export
- "Create a import?" -> POST /admin/import
- "List all meta?" -> GET /groups/{groupId}/artifacts/{artifactId}/versions/{version}/meta
- "Get version details?" -> GET /groups/{groupId}/artifacts/{artifactId}/versions/{version}
- "Delete a version?" -> DELETE /groups/{groupId}/artifacts/{artifactId}/versions/{version}
- "List all rules?" -> GET /groups/{groupId}/artifacts/{artifactId}/rules
- "Create a rule?" -> POST /groups/{groupId}/artifacts/{artifactId}/rules
- "Get rule details?" -> GET /groups/{groupId}/artifacts/{artifactId}/rules/{rule}
- "Update a rule?" -> PUT /groups/{groupId}/artifacts/{artifactId}/rules/{rule}
- "Delete a rule?" -> DELETE /groups/{groupId}/artifacts/{artifactId}/rules/{rule}
- "Get roleMapping details?" -> GET /admin/roleMappings/{principalId}
- "Update a roleMapping?" -> PUT /admin/roleMappings/{principalId}
- "Delete a roleMapping?" -> DELETE /admin/roleMappings/{principalId}
- "List all roleMappings?" -> GET /admin/roleMappings
- "Create a roleMapping?" -> POST /admin/roleMappings
- "List all me?" -> GET /users/me
- "List all references?" -> GET /ids/contentHashes/{contentHash}/references
- "List all references?" -> GET /ids/contentIds/{contentId}/references
- "List all references?" -> GET /ids/globalIds/{globalId}/references
- "List all references?" -> GET /groups/{groupId}/artifacts/{artifactId}/versions/{version}/references
- "List all properties?" -> GET /admin/config/properties
- "Get property details?" -> GET /admin/config/properties/{propertyName}
- "Update a property?" -> PUT /admin/config/properties/{propertyName}
- "Delete a property?" -> DELETE /admin/config/properties/{propertyName}
- "List all limits?" -> GET /system/limits
- "Get artifact details?" -> GET /groups/{groupId}/artifacts/{artifactId}
- "Update a artifact?" -> PUT /groups/{groupId}/artifacts/{artifactId}
- "Delete a artifact?" -> DELETE /groups/{groupId}/artifacts/{artifactId}
- "List all artifacts?" -> GET /groups/{groupId}/artifacts
- "Create a artifact?" -> POST /groups/{groupId}/artifacts
- "List all versions?" -> GET /groups/{groupId}/artifacts/{artifactId}/versions
- "Create a version?" -> POST /groups/{groupId}/artifacts/{artifactId}/versions
- "List all owner?" -> GET /groups/{groupId}/artifacts/{artifactId}/owner
- "Get group details?" -> GET /groups/{groupId}
- "Delete a group?" -> DELETE /groups/{groupId}
- "List all groups?" -> GET /groups
- "Create a group?" -> POST /groups
- "List all meta?" -> GET /groups/{groupId}/artifacts/{artifactId}/meta
- "Create a meta?" -> POST /groups/{groupId}/artifacts/{artifactId}/meta
- "List all comments?" -> GET /groups/{groupId}/artifacts/{artifactId}/versions/{version}/comments
- "Create a comment?" -> POST /groups/{groupId}/artifacts/{artifactId}/versions/{version}/comments
- "Update a comment?" -> PUT /groups/{groupId}/artifacts/{artifactId}/versions/{version}/comments/{commentId}
- "Delete a comment?" -> DELETE /groups/{groupId}/artifacts/{artifactId}/versions/{version}/comments/{commentId}
- "Get contentId details?" -> GET /ids/contentIds/{contentId}
- "Get contentHashe details?" -> GET /ids/contentHashes/{contentHash}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
