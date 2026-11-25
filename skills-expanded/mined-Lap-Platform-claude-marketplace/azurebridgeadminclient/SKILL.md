---
name: azurebridgeadminclient
description: "AzureBridgeAdminClient API skill. Use when working with AzureBridgeAdminClient for subscriptions. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# AzureBridgeAdminClient
API version: 2016-01-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.AzureBridge.Admin/activations/{activationName}/products -- verify access
3. POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.AzureBridge.Admin/activations/{activationName}/products/{productName}/download -- create first download

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.AzureBridge.Admin/activations/{activationName}/products | Return product name. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.AzureBridge.Admin/activations/{activationName}/products/{productName} | Return product name. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.AzureBridge.Admin/activations/{activationName}/products/{productName}/download | Downloads a product from azure marketplace. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all products?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.AzureBridge.Admin/activations/{activationName}/products
- "Get product details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.AzureBridge.Admin/activations/{activationName}/products/{productName}
- "Create a download?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.AzureBridge.Admin/activations/{activationName}/products/{productName}/download
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
