---
name: api-client
description: "API Client API skill. Use when working with API Client for providers, subscriptions. Covers 17 endpoints."
version: 1.0.0
generator: lapsh
---

# API Client
API version: 2018-02-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Web/publishingUsers/web -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.Web/checknameavailability -- create first checknameavailability

## Endpoints

17 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Web/publishingUsers/web | Gets publishing user |
| PUT | /providers/Microsoft.Web/publishingUsers/web | Updates publishing user |
| GET | /providers/Microsoft.Web/sourcecontrols | Gets the source controls available for Azure websites. |
| GET | /providers/Microsoft.Web/sourcecontrols/{sourceControlType} | Gets source control token |
| PUT | /providers/Microsoft.Web/sourcecontrols/{sourceControlType} | Updates source control token |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/billingMeters | Gets a list of meters for a given location. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Web/checknameavailability | Check if a resource name is available. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/deploymentLocations | Gets list of available geo regions plus ministamps |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/geoRegions | Get a list of available geographical regions. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Web/listSitesAssignedToHostName | List all apps that are assigned to a hostname. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/premieraddonoffers | List all premier add-on offers. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/skus | List all SKUs. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Web/verifyHostingEnvironmentVnet | Verifies if this VNET is compatible with an App Service Environment by analyzing the Network Security Group rules. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/moveResources | Move resources between resource groups. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/validate | Validate if a resource can be created. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/validateContainerSettings | Validate if the container settings are correct. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/validateMoveResources | Validate whether a resource can be moved. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all web?" -> GET /providers/Microsoft.Web/publishingUsers/web
- "List all sourcecontrols?" -> GET /providers/Microsoft.Web/sourcecontrols
- "Get sourcecontrol details?" -> GET /providers/Microsoft.Web/sourcecontrols/{sourceControlType}
- "Update a sourcecontrol?" -> PUT /providers/Microsoft.Web/sourcecontrols/{sourceControlType}
- "List all billingMeters?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/billingMeters
- "Create a checknameavailability?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Web/checknameavailability
- "List all deploymentLocations?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/deploymentLocations
- "List all geoRegions?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/geoRegions
- "Create a listSitesAssignedToHostName?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Web/listSitesAssignedToHostName
- "List all premieraddonoffers?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/premieraddonoffers
- "List all skus?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/skus
- "Create a verifyHostingEnvironmentVnet?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Web/verifyHostingEnvironmentVnet
- "Create a moveResource?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/moveResources
- "Create a validate?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/validate
- "Create a validateContainerSetting?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/validateContainerSettings
- "Create a validateMoveResource?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/validateMoveResources
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
