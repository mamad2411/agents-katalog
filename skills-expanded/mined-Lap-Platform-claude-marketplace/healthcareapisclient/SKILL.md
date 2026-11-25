---
name: healthcareapisclient
description: "HealthcareApisClient API skill. Use when working with HealthcareApisClient for subscriptions, providers. Covers 9 endpoints."
version: 1.0.0
generator: lapsh
---

# HealthcareApisClient
API version: 2019-09-16

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.HealthcareApis/operations -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.HealthcareApis/checkNameAvailability -- create first checkNameAvailability

## Endpoints

9 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HealthcareApis/services/{resourceName} | Get the metadata of a service instance. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HealthcareApis/services/{resourceName} | Create or update the metadata of a service instance. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HealthcareApis/services/{resourceName} | Update the metadata of a service instance. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HealthcareApis/services/{resourceName} | Delete a service instance. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.HealthcareApis/services | Get all the service instances in a subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HealthcareApis/services | Get all the service instances in a resource group. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.HealthcareApis/checkNameAvailability | Check if a service instance name is available. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.HealthcareApis/locations/{locationName}/operationresults/{operationResultId} | Get the operation result for a long running operation. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.HealthcareApis/operations | Lists all of the available Healthcare service REST API operations. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get service details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HealthcareApis/services/{resourceName}
- "Update a service?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HealthcareApis/services/{resourceName}
- "Partially update a service?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HealthcareApis/services/{resourceName}
- "Delete a service?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HealthcareApis/services/{resourceName}
- "List all services?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.HealthcareApis/services
- "List all services?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HealthcareApis/services
- "List all operations?" -> GET /providers/Microsoft.HealthcareApis/operations
- "Create a checkNameAvailability?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.HealthcareApis/checkNameAvailability
- "Get operationresult details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.HealthcareApis/locations/{locationName}/operationresults/{operationResultId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
