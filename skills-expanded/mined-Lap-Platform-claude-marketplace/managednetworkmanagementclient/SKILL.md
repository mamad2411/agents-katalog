---
name: managednetworkmanagementclient
description: "ManagedNetworkManagementClient API skill. Use when working with ManagedNetworkManagementClient for subscriptions, {scope}, providers. Covers 19 endpoints."
version: 1.0.0
generator: lapsh
---

# ManagedNetworkManagementClient
API version: 2019-06-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.ManagedNetwork/operations -- verify access

## Endpoints

19 endpoints across 3 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName} | The Get ManagedNetworks operation gets a Managed Network Resource, specified by the resource group and Managed Network name |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName} | The Put ManagedNetworks operation creates/updates a Managed Network Resource, specified by resource group and Managed Network name |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName} | The Delete ManagedNetworks operation deletes a Managed Network Resource, specified by the  resource group and Managed Network name |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName} | Updates the specified Managed Network resource tags. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks | The ListByResourceGroup ManagedNetwork operation retrieves all the Managed Network resources in a resource group in a paginated format. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.ManagedNetwork/managedNetworks | The ListBySubscription  ManagedNetwork operation retrieves all the Managed Network Resources in the current subscription in a paginated format. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkGroups/{managedNetworkGroupName} | The Get ManagedNetworkGroups operation gets a Managed Network Group specified by the resource group, Managed Network name, and group name |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkGroups/{managedNetworkGroupName} | The Put ManagedNetworkGroups operation creates or updates a Managed Network Group resource |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkGroups/{managedNetworkGroupName} | The Delete ManagedNetworkGroups operation deletes a Managed Network Group specified by the resource group, Managed Network name, and group name |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkGroups | The ListByManagedNetwork ManagedNetworkGroup operation retrieves all the Managed Network Groups in a specified Managed Networks in a paginated format. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkPeeringPolicies/{managedNetworkPeeringPolicyName} | The Get ManagedNetworkPeeringPolicies operation gets a Managed Network Peering Policy resource, specified by the  resource group, Managed Network name, and peering policy name |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkPeeringPolicies/{managedNetworkPeeringPolicyName} | The Put ManagedNetworkPeeringPolicies operation creates/updates a new Managed Network Peering Policy |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkPeeringPolicies/{managedNetworkPeeringPolicyName} | The Delete ManagedNetworkPeeringPolicies operation deletes a Managed Network Peering Policy, specified by the  resource group, Managed Network name, and peering policy name |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkPeeringPolicies | The ListByManagedNetwork PeeringPolicies operation retrieves all the Managed Network Peering Policies in a specified Managed Network, in a paginated format. |

### {scope}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{scope}/providers/Microsoft.ManagedNetwork/scopeAssignments/{scopeAssignmentName} | Get the specified scope assignment. |
| PUT | /{scope}/providers/Microsoft.ManagedNetwork/scopeAssignments/{scopeAssignmentName} | Creates a scope assignment. |
| DELETE | /{scope}/providers/Microsoft.ManagedNetwork/scopeAssignments/{scopeAssignmentName} | Deletes a scope assignment. |
| GET | /{scope}/providers/Microsoft.ManagedNetwork/scopeAssignments | Get the specified scope assignment. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.ManagedNetwork/operations | Lists all of the available MNC operations. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get managedNetwork details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}
- "Update a managedNetwork?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}
- "Delete a managedNetwork?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}
- "Partially update a managedNetwork?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}
- "List all managedNetworks?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks
- "List all managedNetworks?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.ManagedNetwork/managedNetworks
- "Get scopeAssignment details?" -> GET /{scope}/providers/Microsoft.ManagedNetwork/scopeAssignments/{scopeAssignmentName}
- "Update a scopeAssignment?" -> PUT /{scope}/providers/Microsoft.ManagedNetwork/scopeAssignments/{scopeAssignmentName}
- "Delete a scopeAssignment?" -> DELETE /{scope}/providers/Microsoft.ManagedNetwork/scopeAssignments/{scopeAssignmentName}
- "List all scopeAssignments?" -> GET /{scope}/providers/Microsoft.ManagedNetwork/scopeAssignments
- "Get managedNetworkGroup details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkGroups/{managedNetworkGroupName}
- "Update a managedNetworkGroup?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkGroups/{managedNetworkGroupName}
- "Delete a managedNetworkGroup?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkGroups/{managedNetworkGroupName}
- "List all managedNetworkGroups?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkGroups
- "Get managedNetworkPeeringPolicy details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkPeeringPolicies/{managedNetworkPeeringPolicyName}
- "Update a managedNetworkPeeringPolicy?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkPeeringPolicies/{managedNetworkPeeringPolicyName}
- "Delete a managedNetworkPeeringPolicy?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkPeeringPolicies/{managedNetworkPeeringPolicyName}
- "List all managedNetworkPeeringPolicies?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetwork/managedNetworks/{managedNetworkName}/managedNetworkPeeringPolicies
- "List all operations?" -> GET /providers/Microsoft.ManagedNetwork/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
