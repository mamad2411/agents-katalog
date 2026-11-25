---
name: iotcentralclient
description: "IotCentralClient API skill. Use when working with IotCentralClient for subscriptions, providers. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# IotCentralClient
API version: 2018-09-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.IoTCentral/operations -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.IoTCentral/checkNameAvailability -- create first checkNameAvailability

## Endpoints

10 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.IoTCentral/iotApps/{resourceName} | Get the metadata of an IoT Central application. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.IoTCentral/iotApps/{resourceName} | Create or update the metadata of an IoT Central application. The usual pattern to modify a property is to retrieve the IoT Central application metadata and security metadata, and then combine them with the modified values in a new body to update the IoT Central application. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.IoTCentral/iotApps/{resourceName} | Update the metadata of an IoT Central application. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.IoTCentral/iotApps/{resourceName} | Delete an IoT Central application. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.IoTCentral/iotApps | Get all IoT Central Applications in a subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.IoTCentral/iotApps | Get all the IoT Central Applications in a resource group. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.IoTCentral/checkNameAvailability | Check if an IoT Central application name is available. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.IoTCentral/checkSubdomainAvailability | Check if an IoT Central application subdomain is available. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.IoTCentral/appTemplates | Get all available application templates. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.IoTCentral/operations | Lists all of the available IoT Central application REST API operations. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get iotApp details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.IoTCentral/iotApps/{resourceName}
- "Update a iotApp?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.IoTCentral/iotApps/{resourceName}
- "Partially update a iotApp?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.IoTCentral/iotApps/{resourceName}
- "Delete a iotApp?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.IoTCentral/iotApps/{resourceName}
- "List all iotApps?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.IoTCentral/iotApps
- "List all iotApps?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.IoTCentral/iotApps
- "Create a checkNameAvailability?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.IoTCentral/checkNameAvailability
- "Create a checkSubdomainAvailability?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.IoTCentral/checkSubdomainAvailability
- "Create a appTemplate?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.IoTCentral/appTemplates
- "List all operations?" -> GET /providers/Microsoft.IoTCentral/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
