---
name: databricksclient
description: "DatabricksClient API skill. Use when working with DatabricksClient for subscriptions, providers. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# DatabricksClient
API version: 2018-04-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Databricks/operations -- verify access

## Endpoints

7 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces/{workspaceName} | Gets the workspace. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces/{workspaceName} | Deletes the workspace. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces/{workspaceName} | Creates a new workspace. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces/{workspaceName} | Updates a workspace. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces | Gets all the workspaces within a resource group. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Databricks/workspaces | Gets all the workspaces within a subscription. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Databricks/operations | Lists all of the available RP operations. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get workspace details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces/{workspaceName}
- "Delete a workspace?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces/{workspaceName}
- "Update a workspace?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces/{workspaceName}
- "Partially update a workspace?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces/{workspaceName}
- "List all workspaces?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces
- "List all workspaces?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Databricks/workspaces
- "List all operations?" -> GET /providers/Microsoft.Databricks/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
