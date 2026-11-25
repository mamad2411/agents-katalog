---
name: frontdoormanagementclient
description: "FrontDoorManagementClient API skill. Use when working with FrontDoorManagementClient for providers, subscriptions. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# FrontDoorManagementClient
API version: 2019-05-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/Microsoft.Network/frontDoors -- verify access
3. POST /providers/Microsoft.Network/checkFrontDoorNameAvailability -- create first checkFrontDoorNameAvailability

## Endpoints

13 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| POST | /providers/Microsoft.Network/checkFrontDoorNameAvailability | Check the availability of a Front Door resource name. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Network/checkFrontDoorNameAvailability | Check the availability of a Front Door subdomain. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Network/frontDoors | Lists all of the Front Doors within an Azure subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors | Lists all of the Front Doors within a resource group under a subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName} | Gets a Front Door with the specified Front Door name under the specified subscription and resource group. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName} | Creates a new Front Door with a Front Door name under the specified subscription and resource group. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName} | Deletes an existing Front Door with the specified parameters. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}/frontendEndpoints | Lists all of the frontend endpoints within a Front Door. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}/frontendEndpoints/{frontendEndpointName} | Gets a Frontend endpoint with the specified name within the specified Front Door. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}/purge | Removes a content from Front Door. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}/frontendEndpoints/{frontendEndpointName}/enableHttps | Enables a frontendEndpoint for HTTPS traffic |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}/frontendEndpoints/{frontendEndpointName}/disableHttps | Disables a frontendEndpoint for HTTPS traffic |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}/validateCustomDomain | Validates the custom domain mapping to ensure it maps to the correct Front Door endpoint in DNS. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a checkFrontDoorNameAvailability?" -> POST /providers/Microsoft.Network/checkFrontDoorNameAvailability
- "Create a checkFrontDoorNameAvailability?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Network/checkFrontDoorNameAvailability
- "List all frontDoors?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Network/frontDoors
- "List all frontDoors?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors
- "Get frontDoor details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}
- "Update a frontDoor?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}
- "Delete a frontDoor?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}
- "List all frontendEndpoints?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}/frontendEndpoints
- "Get frontendEndpoint details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}/frontendEndpoints/{frontendEndpointName}
- "Create a purge?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}/purge
- "Create a enableHttp?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}/frontendEndpoints/{frontendEndpointName}/enableHttps
- "Create a disableHttp?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}/frontendEndpoints/{frontendEndpointName}/disableHttps
- "Create a validateCustomDomain?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/frontDoors/{frontDoorName}/validateCustomDomain
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
