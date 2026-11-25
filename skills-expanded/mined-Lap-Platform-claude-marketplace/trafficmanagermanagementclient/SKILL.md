---
name: trafficmanagermanagementclient
description: "TrafficManagerManagementClient API skill. Use when working with TrafficManagerManagementClient for subscriptions, providers. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# TrafficManagerManagementClient
API version: 2018-04-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Network/trafficManagerGeographicHierarchies/default -- verify access
3. POST /providers/Microsoft.Network/checkTrafficManagerNameAvailability -- create first checkTrafficManagerNameAvailability

## Endpoints

16 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName}/{endpointType}/{endpointName} | Update a Traffic Manager endpoint. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName}/{endpointType}/{endpointName} | Gets a Traffic Manager endpoint. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName}/{endpointType}/{endpointName} | Create or update a Traffic Manager endpoint. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName}/{endpointType}/{endpointName} | Deletes a Traffic Manager endpoint. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles | Lists all Traffic Manager profiles within a resource group. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Network/trafficmanagerprofiles | Lists all Traffic Manager profiles within a subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName} | Gets a Traffic Manager profile. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName} | Create or update a Traffic Manager profile. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName} | Deletes a Traffic Manager profile. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName} | Update a Traffic Manager profile. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName}/heatMaps/{heatMapType} | Gets latest heatmap for Traffic Manager profile. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Network/trafficManagerUserMetricsKeys/default | Get the subscription-level key used for Real User Metrics collection. |
| PUT | /subscriptions/{subscriptionId}/providers/Microsoft.Network/trafficManagerUserMetricsKeys/default | Create or update a subscription-level key used for Real User Metrics collection. |
| DELETE | /subscriptions/{subscriptionId}/providers/Microsoft.Network/trafficManagerUserMetricsKeys/default | Delete a subscription-level key used for Real User Metrics collection. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| POST | /providers/Microsoft.Network/checkTrafficManagerNameAvailability | Checks the availability of a Traffic Manager Relative DNS name. |
| GET | /providers/Microsoft.Network/trafficManagerGeographicHierarchies/default | Gets the default Geographic Hierarchy used by the Geographic traffic routing method. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Partially update a trafficmanagerprofile?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName}/{endpointType}/{endpointName}
- "Get trafficmanagerprofile details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName}/{endpointType}/{endpointName}
- "Update a trafficmanagerprofile?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName}/{endpointType}/{endpointName}
- "Delete a trafficmanagerprofile?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName}/{endpointType}/{endpointName}
- "Create a checkTrafficManagerNameAvailability?" -> POST /providers/Microsoft.Network/checkTrafficManagerNameAvailability
- "List all trafficmanagerprofiles?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles
- "List all trafficmanagerprofiles?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Network/trafficmanagerprofiles
- "Get trafficmanagerprofile details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName}
- "Update a trafficmanagerprofile?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName}
- "Delete a trafficmanagerprofile?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName}
- "Partially update a trafficmanagerprofile?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName}
- "List all default?" -> GET /providers/Microsoft.Network/trafficManagerGeographicHierarchies/default
- "Get heatMap details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficmanagerprofiles/{profileName}/heatMaps/{heatMapType}
- "List all default?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Network/trafficManagerUserMetricsKeys/default
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
