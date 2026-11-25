---
name: mixed-reality
description: "Mixed Reality API skill. Use when working with Mixed Reality for providers, subscriptions. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# Mixed Reality
API version: 2019-02-28-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.MixedReality/operations -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.MixedReality/locations/{location}/checkNameAvailability -- create first checkNameAvailability

## Endpoints

10 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.MixedReality/operations | Exposing Available Operations |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.MixedReality/locations/{location}/checkNameAvailability | Check Name Availability for global uniqueness |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.MixedReality/spatialAnchorsAccounts | List Spatial Anchors Accounts by Subscription |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MixedReality/spatialAnchorsAccounts | List Resources by Resource Group |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MixedReality/spatialAnchorsAccounts/{spatialAnchorsAccountName} | Delete a Spatial Anchors Account. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MixedReality/spatialAnchorsAccounts/{spatialAnchorsAccountName} | Retrieve a Spatial Anchors Account. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MixedReality/spatialAnchorsAccounts/{spatialAnchorsAccountName} | Updating a Spatial Anchors Account |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MixedReality/spatialAnchorsAccounts/{spatialAnchorsAccountName} | Creating or Updating a Spatial Anchors Account. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MixedReality/spatialAnchorsAccounts/{spatialAnchorsAccountName}/keys | Get Both of the 2 Keys of a Spatial Anchors Account |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MixedReality/spatialAnchorsAccounts/{spatialAnchorsAccountName}/keys | Regenerate 1 Key of a Spatial Anchors Account |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.MixedReality/operations
- "Create a checkNameAvailability?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.MixedReality/locations/{location}/checkNameAvailability
- "List all spatialAnchorsAccounts?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.MixedReality/spatialAnchorsAccounts
- "List all spatialAnchorsAccounts?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MixedReality/spatialAnchorsAccounts
- "Delete a spatialAnchorsAccount?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MixedReality/spatialAnchorsAccounts/{spatialAnchorsAccountName}
- "Get spatialAnchorsAccount details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MixedReality/spatialAnchorsAccounts/{spatialAnchorsAccountName}
- "Partially update a spatialAnchorsAccount?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MixedReality/spatialAnchorsAccounts/{spatialAnchorsAccountName}
- "Update a spatialAnchorsAccount?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MixedReality/spatialAnchorsAccounts/{spatialAnchorsAccountName}
- "List all keys?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MixedReality/spatialAnchorsAccounts/{spatialAnchorsAccountName}/keys
- "Create a key?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MixedReality/spatialAnchorsAccounts/{spatialAnchorsAccountName}/keys
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
