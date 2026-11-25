---
name: managedserviceidentityclient
description: "ManagedServiceIdentityClient API skill. Use when working with ManagedServiceIdentityClient for {scope}, providers, subscriptions. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# ManagedServiceIdentityClient
API version: 2018-11-30

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.ManagedIdentity/operations -- verify access

## Endpoints

8 endpoints across 3 groups. See references/api-spec.lap for full details.

### {scope}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{scope}/providers/Microsoft.ManagedIdentity/identities/default | Gets the systemAssignedIdentity available under the specified RP scope. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.ManagedIdentity/operations | Lists available operations for the Microsoft.ManagedIdentity provider |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.ManagedIdentity/userAssignedIdentities | Lists all the userAssignedIdentities available under the specified subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities | Lists all the userAssignedIdentities available under the specified ResourceGroup. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{resourceName} | Create or update an identity in the specified subscription and resource group. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{resourceName} | Update an identity in the specified subscription and resource group. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{resourceName} | Gets the identity. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{resourceName} | Deletes the identity. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all default?" -> GET /{scope}/providers/Microsoft.ManagedIdentity/identities/default
- "List all operations?" -> GET /providers/Microsoft.ManagedIdentity/operations
- "List all userAssignedIdentities?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.ManagedIdentity/userAssignedIdentities
- "List all userAssignedIdentities?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities
- "Update a userAssignedIdentity?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{resourceName}
- "Partially update a userAssignedIdentity?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{resourceName}
- "Get userAssignedIdentity details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{resourceName}
- "Delete a userAssignedIdentity?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{resourceName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
