---
name: logicappsmanagementclient
description: "LogicAppsManagementClient API skill. Use when working with LogicAppsManagementClient for subscriptions. Covers 26 endpoints."
version: 1.0.0
generator: lapsh
---

# LogicAppsManagementClient
API version: 2016-06-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/connectionGateways -- verify access
3. POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/customApis/{apiName}/move -- create first move

## Endpoints

26 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/connectionGateways | Lists all of the connection gateways |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connectionGateways | Lists all of the connection gateways |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connectionGateways/{connectionGatewayName} | Gets a specific gateway |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connectionGateways/{connectionGatewayName} | Replaces a specific gateway |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connectionGateways/{connectionGatewayName} | Updates a specific gateway |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connectionGateways/{connectionGatewayName} | Deletes a specific gateway |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/connectionGatewayInstallations | Gets a list of installed gateways that the user is an admin of |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/connectionGatewayInstallations/{gatewayId} | Gets an installed gateway that the user is an admin of |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/customApis | List of custom APIs |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/customApis | List of custom APIs |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/customApis/{apiName} | Get a custom API |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/customApis/{apiName} | Replaces an existing custom API |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/customApis/{apiName} | Update an existing custom API |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/customApis/{apiName} | Delete a custom API |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/customApis/{apiName}/move | Moves the custom API |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/listWsdlInterfaces | Lists WSDL interfaces |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/extractApiDefinitionFromWsdl | Returns API definition from WSDL |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/managedApis | Lists managed APIs |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/managedApis/{apiName} | Gets managed API |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connections | Get all connections |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connections/{connectionName} | Get a connection |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connections/{connectionName} | Replace an existing connection |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connections/{connectionName} | Update an existing connection |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connections/{connectionName} | Delete an existing connection |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connections/{connectionName}/listConsentLinks | Lists consent links for a connection |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connections/{connectionName}/confirmConsentCode | Confirms the consent code for a connection |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all connectionGateways?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/connectionGateways
- "List all connectionGateways?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connectionGateways
- "Get connectionGateway details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connectionGateways/{connectionGatewayName}
- "Update a connectionGateway?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connectionGateways/{connectionGatewayName}
- "Partially update a connectionGateway?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connectionGateways/{connectionGatewayName}
- "Delete a connectionGateway?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connectionGateways/{connectionGatewayName}
- "List all connectionGatewayInstallations?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/connectionGatewayInstallations
- "Get connectionGatewayInstallation details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/connectionGatewayInstallations/{gatewayId}
- "List all customApis?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/customApis
- "List all customApis?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/customApis
- "Get customApis details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/customApis/{apiName}
- "Update a customApis?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/customApis/{apiName}
- "Partially update a customApis?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/customApis/{apiName}
- "Delete a customApis?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/customApis/{apiName}
- "Create a move?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/customApis/{apiName}/move
- "Create a listWsdlInterface?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/listWsdlInterfaces
- "Create a extractApiDefinitionFromWsdl?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/extractApiDefinitionFromWsdl
- "List all managedApis?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/managedApis
- "Get managedApis details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/managedApis/{apiName}
- "List all connections?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connections
- "Get connection details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connections/{connectionName}
- "Update a connection?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connections/{connectionName}
- "Partially update a connection?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connections/{connectionName}
- "Delete a connection?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connections/{connectionName}
- "Create a listConsentLink?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connections/{connectionName}/listConsentLinks
- "Create a confirmConsentCode?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/connections/{connectionName}/confirmConsentCode
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
