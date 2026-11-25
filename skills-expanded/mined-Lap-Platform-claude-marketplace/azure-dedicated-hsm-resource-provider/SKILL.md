---
name: azure-dedicated-hsm-resource-provider
description: "Azure Dedicated HSM Resource Provider API skill. Use when working with Azure Dedicated HSM Resource Provider for providers, subscriptions. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Azure Dedicated HSM Resource Provider
API version: 2018-10-31-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.HardwareSecurityModules/operations -- verify access

## Endpoints

7 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.HardwareSecurityModules/operations | Get a list of Dedicated HSM operations. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HardwareSecurityModules/dedicatedHSMs/{name} | Create or Update a dedicated HSM in the specified subscription. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HardwareSecurityModules/dedicatedHSMs/{name} | Update a dedicated HSM in the specified subscription. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HardwareSecurityModules/dedicatedHSMs/{name} | Deletes the specified Azure Dedicated HSM. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HardwareSecurityModules/dedicatedHSMs/{name} | Gets the specified Azure dedicated HSM. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HardwareSecurityModules/dedicatedHSMs | The List operation gets information about the dedicated hsms associated with the subscription and within the specified resource group. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.HardwareSecurityModules/dedicatedHSMs | The List operation gets information about the dedicated HSMs associated with the subscription. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.HardwareSecurityModules/operations
- "Update a dedicatedHSM?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HardwareSecurityModules/dedicatedHSMs/{name}
- "Partially update a dedicatedHSM?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HardwareSecurityModules/dedicatedHSMs/{name}
- "Delete a dedicatedHSM?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HardwareSecurityModules/dedicatedHSMs/{name}
- "Get dedicatedHSM details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HardwareSecurityModules/dedicatedHSMs/{name}
- "List all dedicatedHSMs?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HardwareSecurityModules/dedicatedHSMs
- "List all dedicatedHSMs?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.HardwareSecurityModules/dedicatedHSMs
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
