---
name: powerbidedicated
description: "PowerBIDedicated API skill. Use when working with PowerBIDedicated for subscriptions, providers. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# PowerBIDedicated
API version: 2017-10-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.PowerBIDedicated/operations -- verify access
3. POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName}/suspend -- create first suspend

## Endpoints

12 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName} | Gets details about the specified dedicated capacity. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName} | Provisions the specified dedicated capacity based on the configuration specified in the request. You can’t create a capacity with a name that’s used by another capacity in another tenant in the target location. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName} | Deletes the specified Dedicated capacity. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName} | Updates the current state of the specified Dedicated capacity. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName}/suspend | Suspends operation of the specified dedicated capacity instance. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName}/resume | Resumes operation of the specified Dedicated capacity instance. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities | Gets all the Dedicated capacities for the given resource group. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.PowerBIDedicated/capacities | Lists all the Dedicated capacities for the given subscription. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.PowerBIDedicated/skus | Lists eligible SKUs for PowerBI Dedicated resource provider. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName}/skus | Lists eligible SKUs for a PowerBI Dedicated resource. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.PowerBIDedicated/locations/{location}/checkNameAvailability | Check the name availability in the target location. The name isn’t available if it’s used by another capacity in another tenant in the target location. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.PowerBIDedicated/operations | Lists all of the available PowerBIDedicated REST API operations. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get capacity details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName}
- "Update a capacity?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName}
- "Delete a capacity?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName}
- "Partially update a capacity?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName}
- "Create a suspend?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName}/suspend
- "Create a resume?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName}/resume
- "List all capacities?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities
- "List all capacities?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.PowerBIDedicated/capacities
- "List all skus?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.PowerBIDedicated/skus
- "List all skus?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PowerBIDedicated/capacities/{dedicatedCapacityName}/skus
- "List all operations?" -> GET /providers/Microsoft.PowerBIDedicated/operations
- "Create a checkNameAvailability?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.PowerBIDedicated/locations/{location}/checkNameAvailability
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
