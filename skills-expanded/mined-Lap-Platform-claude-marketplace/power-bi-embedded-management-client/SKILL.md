---
name: power-bi-embedded-management-client
description: "Power BI Embedded Management Client API skill. Use when working with Power BI Embedded Management Client for subscriptions, providers. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# Power BI Embedded Management Client
API version: 2016-01-29

## Auth
No authentication required.

## Base URL
https://management.azure.com

## Setup
1. No auth setup needed
2. GET /providers/Microsoft.PowerBI/operations -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.PowerBI/locations/{location}/checkNameAvailability -- create first checkNameAvailability

## Endpoints

12 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections/{workspaceCollectionName} | Retrieves an existing Power BI Workspace Collection. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections/{workspaceCollectionName} | Creates a new Power BI Workspace Collection with the specified properties. A Power BI Workspace Collection contains one or more workspaces, and can be used to provision keys that provide API access to those workspaces. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections/{workspaceCollectionName} | Update an existing Power BI Workspace Collection with the specified properties. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections/{workspaceCollectionName} | Delete a Power BI Workspace Collection. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.PowerBI/locations/{location}/checkNameAvailability | Verify the specified Power BI Workspace Collection name is valid and not already in use. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections | Retrieves all existing Power BI workspace collections in the specified resource group. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.PowerBI/workspaceCollections | Retrieves all existing Power BI workspace collections in the specified subscription. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections/{workspaceCollectionName}/listKeys | Retrieves the primary and secondary access keys for the specified Power BI Workspace Collection. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections/{workspaceCollectionName}/regenerateKey | Regenerates the primary or secondary access key for the specified Power BI Workspace Collection. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections/{workspaceCollectionName}/workspaces | Retrieves all existing Power BI workspaces in the specified workspace collection. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/moveResources | Migrates an existing Power BI Workspace Collection to a different resource group and/or subscription. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.PowerBI/operations | Indicates which operations can be performed by the Power BI Resource Provider. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get workspaceCollection details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections/{workspaceCollectionName}
- "Update a workspaceCollection?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections/{workspaceCollectionName}
- "Partially update a workspaceCollection?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections/{workspaceCollectionName}
- "Delete a workspaceCollection?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections/{workspaceCollectionName}
- "Create a checkNameAvailability?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.PowerBI/locations/{location}/checkNameAvailability
- "List all workspaceCollections?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections
- "List all workspaceCollections?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.PowerBI/workspaceCollections
- "Create a listKey?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections/{workspaceCollectionName}/listKeys
- "Create a regenerateKey?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections/{workspaceCollectionName}/regenerateKey
- "List all operations?" -> GET /providers/Microsoft.PowerBI/operations
- "List all workspaces?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBI/workspaceCollections/{workspaceCollectionName}/workspaces
- "Create a moveResource?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/moveResources

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
