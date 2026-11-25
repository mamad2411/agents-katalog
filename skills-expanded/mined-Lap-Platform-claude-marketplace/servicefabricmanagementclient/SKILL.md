---
name: servicefabricmanagementclient
description: "ServiceFabricManagementClient API skill. Use when working with ServiceFabricManagementClient for subscriptions, providers. Covers 11 endpoints."
version: 1.0.0
generator: lapsh
---

# ServiceFabricManagementClient
API version: 2019-03-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.ServiceFabric/operations -- verify access

## Endpoints

11 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ServiceFabric/clusters/{clusterName} | Gets a Service Fabric cluster resource. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ServiceFabric/clusters/{clusterName} | Creates or updates a Service Fabric cluster resource. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ServiceFabric/clusters/{clusterName} | Updates the configuration of a Service Fabric cluster resource. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ServiceFabric/clusters/{clusterName} | Deletes a Service Fabric cluster resource. |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.ServiceFabric/clusters | Gets the list of Service Fabric cluster resources created in the specified resource group. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.ServiceFabric/clusters | Gets the list of Service Fabric cluster resources created in the specified subscription. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.ServiceFabric/locations/{location}/clusterVersions/{clusterVersion} | Gets information about a Service Fabric cluster code version available in the specified location. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.ServiceFabric/locations/{location}/environments/{environment}/clusterVersions/{clusterVersion} | Gets information about a Service Fabric cluster code version available for the specified environment. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.ServiceFabric/locations/{location}/clusterVersions | Gets the list of Service Fabric cluster code versions available for the specified location. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.ServiceFabric/locations/{location}/environments/{environment}/clusterVersions | Gets the list of Service Fabric cluster code versions available for the specified environment. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.ServiceFabric/operations | Lists all of the available Service Fabric resource provider API operations. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get cluster details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ServiceFabric/clusters/{clusterName}
- "Update a cluster?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ServiceFabric/clusters/{clusterName}
- "Partially update a cluster?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ServiceFabric/clusters/{clusterName}
- "Delete a cluster?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ServiceFabric/clusters/{clusterName}
- "List all clusters?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.ServiceFabric/clusters
- "List all clusters?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.ServiceFabric/clusters
- "Get clusterVersion details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.ServiceFabric/locations/{location}/clusterVersions/{clusterVersion}
- "Get clusterVersion details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.ServiceFabric/locations/{location}/environments/{environment}/clusterVersions/{clusterVersion}
- "List all clusterVersions?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.ServiceFabric/locations/{location}/clusterVersions
- "List all clusterVersions?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.ServiceFabric/locations/{location}/environments/{environment}/clusterVersions
- "List all operations?" -> GET /providers/Microsoft.ServiceFabric/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
