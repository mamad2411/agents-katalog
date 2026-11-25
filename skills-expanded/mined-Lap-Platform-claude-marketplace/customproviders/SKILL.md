---
name: customproviders
description: "customproviders API skill. Use when working with customproviders for providers, subscriptions, {scope}. Covers 11 endpoints."
version: 1.0.0
generator: lapsh
---

# customproviders
API version: 2018-09-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.CustomProviders/operations -- verify access

## Endpoints

11 endpoints across 3 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.CustomProviders/operations | The list of operations provided by Microsoft CustomProviders. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CustomProviders/resourceProviders/{resourceProviderName} | Creates or updates the custom resource provider. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CustomProviders/resourceProviders/{resourceProviderName} | Deletes the custom resource provider. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CustomProviders/resourceProviders/{resourceProviderName} | Gets the custom resource provider manifest. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CustomProviders/resourceProviders/{resourceProviderName} | Updates an existing custom resource provider. The only value that can be updated via PATCH currently is the tags. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CustomProviders/resourceProviders | Gets all the custom resource providers within a resource group. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.CustomProviders/resourceProviders | Gets all the custom resource providers within a subscription. |

### {scope}
| Method | Path | Description |
|--------|------|-------------|
| PUT | /{scope}/providers/Microsoft.CustomProviders/associations/{associationName} | Create or update an association. |
| DELETE | /{scope}/providers/Microsoft.CustomProviders/associations/{associationName} | Delete an association. |
| GET | /{scope}/providers/Microsoft.CustomProviders/associations/{associationName} | Get an association. |
| GET | /{scope}/providers/Microsoft.CustomProviders/associations | Gets all association for the given scope. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.CustomProviders/operations
- "Update a resourceProvider?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CustomProviders/resourceProviders/{resourceProviderName}
- "Delete a resourceProvider?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CustomProviders/resourceProviders/{resourceProviderName}
- "Get resourceProvider details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CustomProviders/resourceProviders/{resourceProviderName}
- "Partially update a resourceProvider?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CustomProviders/resourceProviders/{resourceProviderName}
- "List all resourceProviders?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CustomProviders/resourceProviders
- "List all resourceProviders?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.CustomProviders/resourceProviders
- "Update a association?" -> PUT /{scope}/providers/Microsoft.CustomProviders/associations/{associationName}
- "Delete a association?" -> DELETE /{scope}/providers/Microsoft.CustomProviders/associations/{associationName}
- "Get association details?" -> GET /{scope}/providers/Microsoft.CustomProviders/associations/{associationName}
- "List all associations?" -> GET /{scope}/providers/Microsoft.CustomProviders/associations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
