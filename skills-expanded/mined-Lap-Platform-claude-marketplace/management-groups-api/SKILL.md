---
name: management-groups-api
description: "Management Groups API skill. Use when working with Management Groups for providers. Covers 11 endpoints."
version: 1.0.0
generator: lapsh
---

# Management Groups API
API version: 2018-03-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Management/managementGroups -- verify access
3. POST /providers/Microsoft.Management/checkNameAvailability -- create first checkNameAvailability

## Endpoints

11 endpoints across 1 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Management/managementGroups | List management groups for the authenticated user. |
| GET | /providers/Microsoft.Management/managementGroups/{groupId} | Get the details of the management group. |
| PUT | /providers/Microsoft.Management/managementGroups/{groupId} | Create or update a management group. If a management group is already created and a subsequent create request is issued with different properties, the management group properties will be updated. |
| PATCH | /providers/Microsoft.Management/managementGroups/{groupId} | Update a management group. |
| DELETE | /providers/Microsoft.Management/managementGroups/{groupId} | Delete management group. If a management group contains child resources, the request will fail. |
| GET | /providers/Microsoft.Management/managementGroups/{groupId}/descendants | List all entities that descend from a management group. |
| PUT | /providers/Microsoft.Management/managementGroups/{groupId}/subscriptions/{subscriptionId} | Associates existing subscription with the management group. |
| DELETE | /providers/Microsoft.Management/managementGroups/{groupId}/subscriptions/{subscriptionId} | De-associates subscription from the management group. |
| GET | /providers/Microsoft.Management/operations | Lists all of the available Management REST API operations. |
| POST | /providers/Microsoft.Management/checkNameAvailability | Checks if the specified management group name is valid and unique |
| POST | /providers/Microsoft.Management/getEntities | List all entities (Management Groups, Subscriptions, etc.) for the authenticated user. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all managementGroups?" -> GET /providers/Microsoft.Management/managementGroups
- "Get managementGroup details?" -> GET /providers/Microsoft.Management/managementGroups/{groupId}
- "Update a managementGroup?" -> PUT /providers/Microsoft.Management/managementGroups/{groupId}
- "Partially update a managementGroup?" -> PATCH /providers/Microsoft.Management/managementGroups/{groupId}
- "Delete a managementGroup?" -> DELETE /providers/Microsoft.Management/managementGroups/{groupId}
- "List all descendants?" -> GET /providers/Microsoft.Management/managementGroups/{groupId}/descendants
- "Update a subscription?" -> PUT /providers/Microsoft.Management/managementGroups/{groupId}/subscriptions/{subscriptionId}
- "Delete a subscription?" -> DELETE /providers/Microsoft.Management/managementGroups/{groupId}/subscriptions/{subscriptionId}
- "List all operations?" -> GET /providers/Microsoft.Management/operations
- "Create a checkNameAvailability?" -> POST /providers/Microsoft.Management/checkNameAvailability
- "Create a getEntity?" -> POST /providers/Microsoft.Management/getEntities
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
