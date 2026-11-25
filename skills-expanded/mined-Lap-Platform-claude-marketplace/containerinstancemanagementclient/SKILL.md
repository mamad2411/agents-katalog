---
name: containerinstancemanagementclient
description: "ContainerInstanceManagementClient API skill. Use when working with ContainerInstanceManagementClient for subscriptions, providers. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# ContainerInstanceManagementClient
API version: 2018-10-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.ContainerInstance/operations -- verify access
3. POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}/restart -- create first restart

## Endpoints

16 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.ContainerInstance/containerGroups | Get a list of container groups in the specified subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups | Get a list of container groups in the specified subscription and resource group. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName} | Get the properties of the specified container group. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName} | Create or update container groups. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName} | Update container groups. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName} | Delete the specified container group. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}/restart | Restarts all containers in a container group. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}/stop | Stops all containers in a container group. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}/start | Starts all containers in a container group. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.ContainerInstance/locations/{location}/usages | Get the usage for a subscription |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}/containers/{containerName}/logs | Get the logs for a specified container instance. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}/containers/{containerName}/exec | Executes a command in a specific container instance. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}/providers/Microsoft.ContainerInstance/serviceAssociationLinks/default | Delete the container instance service association link for the subnet. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.ContainerInstance/locations/{location}/cachedImages | Get the list of cached images. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.ContainerInstance/locations/{location}/capabilities | Get the list of capabilities of the location. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.ContainerInstance/operations | List the operations for Azure Container Instance service. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all containerGroups?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.ContainerInstance/containerGroups
- "List all containerGroups?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups
- "Get containerGroup details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}
- "Update a containerGroup?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}
- "Partially update a containerGroup?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}
- "Delete a containerGroup?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}
- "Create a restart?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}/restart
- "Create a stop?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}/stop
- "Create a start?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}/start
- "List all operations?" -> GET /providers/Microsoft.ContainerInstance/operations
- "List all usages?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.ContainerInstance/locations/{location}/usages
- "List all logs?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}/containers/{containerName}/logs
- "Create a exec?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerInstance/containerGroups/{containerGroupName}/containers/{containerName}/exec
- "List all cachedImages?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.ContainerInstance/locations/{location}/cachedImages
- "List all capabilities?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.ContainerInstance/locations/{location}/capabilities
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
