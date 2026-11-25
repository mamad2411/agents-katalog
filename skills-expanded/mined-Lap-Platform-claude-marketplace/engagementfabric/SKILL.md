---
name: engagementfabric
description: "EngagementFabric API skill. Use when working with EngagementFabric for subscriptions, providers. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# EngagementFabric
API version: 2018-09-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.EngagementFabric/operations -- verify access
3. POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/listKeys -- create first listKeys

## Endpoints

16 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName} | Get the EngagementFabric account |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName} | Create or Update the EngagementFabric account |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName} | Delete the EngagementFabric account |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName} | Update EngagementFabric account |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.EngagementFabric/Accounts | List the EngagementFabric accounts in given subscription |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts | List EngagementFabric accounts in given resource group |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/listKeys | List keys of the EngagementFabric account |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/regenerateKey | Regenerate key of the EngagementFabric account |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/listChannelTypes | List available EngagementFabric channel types and functions |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/Channels/{channelName} | Get the EngagementFabric channel |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/Channels/{channelName} | Create or Update the EngagementFabric channel |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/Channels/{channelName} | Delete the EngagementFabric channel |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/Channels | List the EngagementFabric channels |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/checkNameAvailability | Check availability of EngagementFabric resource |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.EngagementFabric/skus | List available SKUs of EngagementFabric resource |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.EngagementFabric/operations | List operation of EngagementFabric resources |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get Account details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}
- "Update a Account?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}
- "Delete a Account?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}
- "Partially update a Account?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}
- "List all Accounts?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.EngagementFabric/Accounts
- "List all Accounts?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts
- "Create a listKey?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/listKeys
- "Create a regenerateKey?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/regenerateKey
- "Create a listChannelType?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/listChannelTypes
- "Get Channel details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/Channels/{channelName}
- "Update a Channel?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/Channels/{channelName}
- "Delete a Channel?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/Channels/{channelName}
- "List all Channels?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/Accounts/{accountName}/Channels
- "Create a checkNameAvailability?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EngagementFabric/checkNameAvailability
- "List all operations?" -> GET /providers/Microsoft.EngagementFabric/operations
- "List all skus?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.EngagementFabric/skus
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
