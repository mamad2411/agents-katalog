---
name: authorizationmanagementclient
description: "AuthorizationManagementClient API skill. Use when working with AuthorizationManagementClient for subscriptions, {scope}. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# AuthorizationManagementClient
API version: 2018-01-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Authorization/permissions -- verify access

## Endpoints

6 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Authorization/permissions | Gets all permissions the caller has for a resource group. |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}/providers/Microsoft.Authorization/permissions | Gets all permissions the caller has for a resource. |

### {scope}
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /{scope}/providers/Microsoft.Authorization/roleDefinitions/{roleDefinitionId} | Deletes a role definition. |
| GET | /{scope}/providers/Microsoft.Authorization/roleDefinitions/{roleDefinitionId} | Get role definition by name (GUID). |
| PUT | /{scope}/providers/Microsoft.Authorization/roleDefinitions/{roleDefinitionId} | Creates or updates a role definition. |
| GET | /{scope}/providers/Microsoft.Authorization/roleDefinitions | Get all role definitions that are applicable at scope and above. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all permissions?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Authorization/permissions
- "List all permissions?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}/providers/Microsoft.Authorization/permissions
- "Delete a roleDefinition?" -> DELETE /{scope}/providers/Microsoft.Authorization/roleDefinitions/{roleDefinitionId}
- "Get roleDefinition details?" -> GET /{scope}/providers/Microsoft.Authorization/roleDefinitions/{roleDefinitionId}
- "Update a roleDefinition?" -> PUT /{scope}/providers/Microsoft.Authorization/roleDefinitions/{roleDefinitionId}
- "List all roleDefinitions?" -> GET /{scope}/providers/Microsoft.Authorization/roleDefinitions
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
