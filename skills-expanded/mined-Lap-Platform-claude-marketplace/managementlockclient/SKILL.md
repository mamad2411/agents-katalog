---
name: managementlockclient
description: "ManagementLockClient API skill. Use when working with ManagementLockClient for providers, subscriptions, {scope}. Covers 17 endpoints."
version: 1.0.0
generator: lapsh
---

# ManagementLockClient
API version: 2016-09-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Authorization/operations -- verify access

## Endpoints

17 endpoints across 3 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Authorization/operations | Lists all of the available Microsoft.Authorization REST API operations. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Authorization/locks/{lockName} | Creates or updates a management lock at the resource group level. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Authorization/locks/{lockName} | Deletes a management lock at the resource group level. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Authorization/locks/{lockName} | Gets a management lock at the resource group level. |
| PUT | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}/providers/Microsoft.Authorization/locks/{lockName} | Creates or updates a management lock at the resource level or any level below the resource. |
| DELETE | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}/providers/Microsoft.Authorization/locks/{lockName} | Deletes the management lock of a resource or any level below the resource. |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}/providers/Microsoft.Authorization/locks/{lockName} | Get the management lock of a resource or any level below resource. |
| PUT | /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/locks/{lockName} | Creates or updates a management lock at the subscription level. |
| DELETE | /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/locks/{lockName} | Deletes the management lock at the subscription level. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/locks/{lockName} | Gets a management lock at the subscription level. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Authorization/locks | Gets all the management locks for a resource group. |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}/providers/Microsoft.Authorization/locks | Gets all the management locks for a resource or any level below resource. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/locks | Gets all the management locks for a subscription. |

### {scope}
| Method | Path | Description |
|--------|------|-------------|
| PUT | /{scope}/providers/Microsoft.Authorization/locks/{lockName} | Create or update a management lock by scope. |
| DELETE | /{scope}/providers/Microsoft.Authorization/locks/{lockName} | Delete a management lock by scope. |
| GET | /{scope}/providers/Microsoft.Authorization/locks/{lockName} | Get a management lock by scope. |
| GET | /{scope}/providers/Microsoft.Authorization/locks | Gets all the management locks for a scope. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.Authorization/operations
- "Update a lock?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Authorization/locks/{lockName}
- "Delete a lock?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Authorization/locks/{lockName}
- "Get lock details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Authorization/locks/{lockName}
- "Update a lock?" -> PUT /{scope}/providers/Microsoft.Authorization/locks/{lockName}
- "Delete a lock?" -> DELETE /{scope}/providers/Microsoft.Authorization/locks/{lockName}
- "Get lock details?" -> GET /{scope}/providers/Microsoft.Authorization/locks/{lockName}
- "Update a lock?" -> PUT /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}/providers/Microsoft.Authorization/locks/{lockName}
- "Delete a lock?" -> DELETE /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}/providers/Microsoft.Authorization/locks/{lockName}
- "Get lock details?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}/providers/Microsoft.Authorization/locks/{lockName}
- "Update a lock?" -> PUT /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/locks/{lockName}
- "Delete a lock?" -> DELETE /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/locks/{lockName}
- "Get lock details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/locks/{lockName}
- "List all locks?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Authorization/locks
- "List all locks?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}/providers/Microsoft.Authorization/locks
- "List all locks?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/locks
- "List all locks?" -> GET /{scope}/providers/Microsoft.Authorization/locks
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
