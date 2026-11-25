---
name: hybridcomputemanagementclient
description: "HybridComputeManagementClient API skill. Use when working with HybridComputeManagementClient for subscriptions, providers. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# HybridComputeManagementClient
API version: 2019-12-12

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.HybridCompute/operations -- verify access
3. POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}/reconnect -- create first reconnect

## Endpoints

13 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name} | The operation to create or update a hybrid machine resource identity in Azure. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name} | The operation to update a hybrid machine. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name} | The operation to remove a hybrid machine identity in Azure. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name} | Retrieves information about the model view or the instance view of a hybrid machine. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}/reconnect | The operation to reconnect a hybrid machine resource to its identity in Azure. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines | Lists all the hybrid machines in the specified resource group. Use the nextLink property in the response to get the next page of hybrid machines. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.HybridCompute/machines | Lists all the hybrid machines in the specified subscription. Use the nextLink property in the response to get the next page of hybrid machines. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}/extensions/{extensionName} | The operation to create or update the extension. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}/extensions/{extensionName} | The operation to create or update the extension. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}/extensions/{extensionName} | The operation to delete the extension. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}/extensions/{extensionName} | The operation to get the extension. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}/extensions | The operation to get all extensions of a non-Azure machine |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.HybridCompute/operations | Gets a list of hybrid compute operations. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a machine?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}
- "Partially update a machine?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}
- "Delete a machine?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}
- "Get machine details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}
- "Create a reconnect?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}/reconnect
- "List all machines?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines
- "List all machines?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.HybridCompute/machines
- "Update a extension?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}/extensions/{extensionName}
- "Partially update a extension?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}/extensions/{extensionName}
- "Delete a extension?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}/extensions/{extensionName}
- "Get extension details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}/extensions/{extensionName}
- "List all extensions?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/machines/{name}/extensions
- "List all operations?" -> GET /providers/Microsoft.HybridCompute/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
