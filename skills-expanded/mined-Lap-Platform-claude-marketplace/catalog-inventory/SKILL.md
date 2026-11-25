---
name: catalog-inventory
description: "Catalog Inventory API skill. Use when working with Catalog Inventory for graphql, openapi.json, service_credential_types. Covers 38 endpoints."
version: 1.0.0
generator: lapsh
---

# Catalog Inventory
API version: 1.0.0

## Auth
Bearer basic

## Base URL
https://cloud.redhat.com//api/catalog-inventory/v1.0

## Setup
1. Set Authorization header with your Bearer token
2. GET /openapi.json -- verify access
3. POST /graphql -- create first graphql

## Endpoints

38 endpoints across 12 groups. See references/api-spec.lap for full details.

### graphql
| Method | Path | Description |
|--------|------|-------------|
| POST | /graphql | Perform a GraphQL Query |

### openapi.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /openapi.json | Return this API document in JSON format |

### service_credential_types
| Method | Path | Description |
|--------|------|-------------|
| GET | /service_credential_types | List ServiceCredentialTypes |
| GET | /service_credential_types/{id} | Show an existing ServiceCredentialType |

### service_credentials
| Method | Path | Description |
|--------|------|-------------|
| GET | /service_credentials | List ServiceCredentials |
| GET | /service_credentials/{id} | Show an existing ServiceCredential |

### service_instances
| Method | Path | Description |
|--------|------|-------------|
| GET | /service_instances | List ServiceInstances |
| GET | /service_instances/{id} | Show an existing ServiceInstance |

### service_inventories
| Method | Path | Description |
|--------|------|-------------|
| GET | /service_inventories | List ServiceInventories |
| GET | /service_inventories/{id} | Show an existing ServiceInventory |
| POST | /service_inventories/{id}/tag | Tag a ServiceInventory |
| GET | /service_inventories/{id}/tags | List Tags for ServiceInventory |
| POST | /service_inventories/{id}/untag | Untag a ServiceInventory |

### service_offering_nodes
| Method | Path | Description |
|--------|------|-------------|
| GET | /service_offering_nodes | List ServiceOfferingNodes |
| GET | /service_offering_nodes/{id} | Show an existing ServiceOfferingNode |

### service_offerings
| Method | Path | Description |
|--------|------|-------------|
| GET | /service_offerings | List ServiceOfferings |
| GET | /service_offerings/{id} | Show an existing ServiceOffering |
| POST | /service_offerings/{id}/applied_inventories_tags | Invokes computing of ServiceInventories tags for given ServiceOffering |
| POST | /service_offerings/{id}/order | Order an existing ServiceOffering |
| GET | /service_offerings/{id}/service_instances | List ServiceInstances for ServiceOffering |
| GET | /service_offerings/{id}/service_offering_nodes | List ServiceOfferingNodes for ServiceOffering |
| GET | /service_offerings/{id}/service_plans | List ServicePlans for ServiceOffering |

### service_plans
| Method | Path | Description |
|--------|------|-------------|
| GET | /service_plans | List ServicePlans |
| GET | /service_plans/{id} | Show an existing ServicePlan |

### sources
| Method | Path | Description |
|--------|------|-------------|
| GET | /sources | List Sources |
| GET | /sources/{id} | Show an existing Source |
| PATCH | /sources/{id}/refresh | Refresh an existing Source |
| PATCH | /sources/{id}/incremental_refresh | Incremental Refresh an existing Source |
| GET | /sources/{id}/service_instances | List ServiceInstances for Source |
| GET | /sources/{id}/service_inventories | List ServiceInventories for Source |
| GET | /sources/{id}/service_offering_nodes | List ServiceOfferingNodes for Source |
| GET | /sources/{id}/service_offerings | List ServiceOfferings for Source |
| GET | /sources/{id}/service_plans | List ServicePlans for Source |
| GET | /sources/{id}/tasks | List Tasks for Source |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags | List Tags |

### tasks
| Method | Path | Description |
|--------|------|-------------|
| GET | /tasks | List Tasks |
| GET | /tasks/{id} | Show an existing Task |
| PATCH | /tasks/{id} | Update an existing Task |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a graphql?" -> POST /graphql
- "List all openapi.json?" -> GET /openapi.json
- "List all service_credential_types?" -> GET /service_credential_types
- "Get service_credential_type details?" -> GET /service_credential_types/{id}
- "List all service_credentials?" -> GET /service_credentials
- "Get service_credential details?" -> GET /service_credentials/{id}
- "List all service_instances?" -> GET /service_instances
- "Get service_instance details?" -> GET /service_instances/{id}
- "List all service_inventories?" -> GET /service_inventories
- "Get service_inventory details?" -> GET /service_inventories/{id}
- "Create a tag?" -> POST /service_inventories/{id}/tag
- "List all tags?" -> GET /service_inventories/{id}/tags
- "Create a untag?" -> POST /service_inventories/{id}/untag
- "List all service_offering_nodes?" -> GET /service_offering_nodes
- "Get service_offering_node details?" -> GET /service_offering_nodes/{id}
- "List all service_offerings?" -> GET /service_offerings
- "Get service_offering details?" -> GET /service_offerings/{id}
- "Create a applied_inventories_tag?" -> POST /service_offerings/{id}/applied_inventories_tags
- "Create a order?" -> POST /service_offerings/{id}/order
- "List all service_instances?" -> GET /service_offerings/{id}/service_instances
- "List all service_offering_nodes?" -> GET /service_offerings/{id}/service_offering_nodes
- "List all service_plans?" -> GET /service_offerings/{id}/service_plans
- "List all service_plans?" -> GET /service_plans
- "Get service_plan details?" -> GET /service_plans/{id}
- "List all sources?" -> GET /sources
- "Get source details?" -> GET /sources/{id}
- "List all service_instances?" -> GET /sources/{id}/service_instances
- "List all service_inventories?" -> GET /sources/{id}/service_inventories
- "List all service_offering_nodes?" -> GET /sources/{id}/service_offering_nodes
- "List all service_offerings?" -> GET /sources/{id}/service_offerings
- "List all service_plans?" -> GET /sources/{id}/service_plans
- "List all tasks?" -> GET /sources/{id}/tasks
- "List all tags?" -> GET /tags
- "List all tasks?" -> GET /tasks
- "Get task details?" -> GET /tasks/{id}
- "Partially update a task?" -> PATCH /tasks/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
