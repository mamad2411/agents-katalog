---
name: azure-maps-resource-provider
description: "Azure Maps Resource Provider API skill. Use when working with Azure Maps Resource Provider for subscriptions, providers. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# Azure Maps Resource Provider
API version: 2018-05-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Maps/operations -- verify access
3. POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/moveResources -- create first moveResources

## Endpoints

10 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Maps/accounts/{accountName} | Create or update a Maps Account. A Maps Account holds the keys which allow access to the Maps REST APIs. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Maps/accounts/{accountName} | Updates a Maps Account. Only a subset of the parameters may be updated after creation, such as Sku and Tags. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Maps/accounts/{accountName} | Delete a Maps Account. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Maps/accounts/{accountName} | Get a Maps Account. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Maps/accounts | Get all Maps Accounts in a Resource Group |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Maps/accounts | Get all Maps Accounts in a Subscription |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/moveResources | Moves Maps Accounts from one ResourceGroup (or Subscription) to another |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Maps/accounts/{accountName}/listKeys | Get the keys to use with the Maps APIs. A key is used to authenticate and authorize access to the Maps REST APIs. Only one key is needed at a time; two are given to provide seamless key regeneration. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Maps/accounts/{accountName}/regenerateKey | Regenerate either the primary or secondary key for use with the Maps APIs. The old key will stop working immediately. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Maps/operations | List operations available for the Maps Resource Provider |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a account?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Maps/accounts/{accountName}
- "Partially update a account?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Maps/accounts/{accountName}
- "Delete a account?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Maps/accounts/{accountName}
- "Get account details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Maps/accounts/{accountName}
- "List all accounts?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Maps/accounts
- "List all accounts?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Maps/accounts
- "Create a moveResource?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/moveResources
- "Create a listKey?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Maps/accounts/{accountName}/listKeys
- "Create a regenerateKey?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Maps/accounts/{accountName}/regenerateKey
- "List all operations?" -> GET /providers/Microsoft.Maps/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
