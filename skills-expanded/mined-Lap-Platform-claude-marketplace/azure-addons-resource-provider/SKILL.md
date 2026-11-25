---
name: azure-addons-resource-provider
description: "Azure Addons Resource Provider API skill. Use when working with Azure Addons Resource Provider for providers, subscriptions. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Azure Addons Resource Provider
API version: 2017-05-15

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Addons/operations -- verify access

## Endpoints

5 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Addons/operations | Lists all of the available Addons RP operations. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Addons/supportProviders/{providerName}/supportPlanTypes/{planTypeName} | Returns whether or not the canonical support plan of type {type} is enabled for the subscription. |
| PUT | /subscriptions/{subscriptionId}/providers/Microsoft.Addons/supportProviders/{providerName}/supportPlanTypes/{planTypeName} | Creates or updates the Canonical support plan of type {type} for the subscription. |
| DELETE | /subscriptions/{subscriptionId}/providers/Microsoft.Addons/supportProviders/{providerName}/supportPlanTypes/{planTypeName} | Cancels the Canonical support plan of type {type} for the subscription. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Addons/supportProviders/{providerName}/supportPlanTypes | Returns the Canonical Support Plans. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.Addons/operations
- "Get supportPlanType details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Addons/supportProviders/{providerName}/supportPlanTypes/{planTypeName}
- "Update a supportPlanType?" -> PUT /subscriptions/{subscriptionId}/providers/Microsoft.Addons/supportProviders/{providerName}/supportPlanTypes/{planTypeName}
- "Delete a supportPlanType?" -> DELETE /subscriptions/{subscriptionId}/providers/Microsoft.Addons/supportProviders/{providerName}/supportPlanTypes/{planTypeName}
- "List all supportPlanTypes?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Addons/supportProviders/{providerName}/supportPlanTypes
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
