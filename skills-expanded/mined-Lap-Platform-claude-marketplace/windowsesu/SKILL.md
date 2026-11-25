---
name: windowsesu
description: "windowsesu API skill. Use when working with windowsesu for providers, subscriptions. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# windowsesu
API version: 2019-09-16-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.WindowsESU/operations -- verify access

## Endpoints

7 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.WindowsESU/operations | List all available Windows.ESU provider operations. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.WindowsESU/multipleActivationKeys | List all Multiple Activation Keys (MAK) created for a subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.WindowsESU/multipleActivationKeys | List all Multiple Activation Keys (MAK) in a resource group. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.WindowsESU/multipleActivationKeys/{multipleActivationKeyName} | Get a MAK key. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.WindowsESU/multipleActivationKeys/{multipleActivationKeyName} | Create a MAK key. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.WindowsESU/multipleActivationKeys/{multipleActivationKeyName} | Update a MAK key. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.WindowsESU/multipleActivationKeys/{multipleActivationKeyName} | Delete a MAK key. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.WindowsESU/operations
- "List all multipleActivationKeys?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.WindowsESU/multipleActivationKeys
- "List all multipleActivationKeys?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.WindowsESU/multipleActivationKeys
- "Get multipleActivationKey details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.WindowsESU/multipleActivationKeys/{multipleActivationKeyName}
- "Update a multipleActivationKey?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.WindowsESU/multipleActivationKeys/{multipleActivationKeyName}
- "Partially update a multipleActivationKey?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.WindowsESU/multipleActivationKeys/{multipleActivationKeyName}
- "Delete a multipleActivationKey?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.WindowsESU/multipleActivationKeys/{multipleActivationKeyName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
