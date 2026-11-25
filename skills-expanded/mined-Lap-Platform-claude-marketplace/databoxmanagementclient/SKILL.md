---
name: databoxmanagementclient
description: "DataBoxManagementClient API skill. Use when working with DataBoxManagementClient for providers, subscriptions. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# DataBoxManagementClient
API version: 2019-09-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.DataBox/operations -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.DataBox/locations/{location}/availableSkus -- create first availableSkus

## Endpoints

16 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.DataBox/operations | This method gets all the operations. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.DataBox/jobs | Lists all the jobs available under the subscription. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.DataBox/locations/{location}/availableSkus | This method provides the list of available skus for the given subscription and location. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/locations/{location}/availableSkus | This method provides the list of available skus for the given subscription, resource group and location. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.DataBox/locations/{location}/validateAddress | [DEPRECATED NOTICE: This operation will soon be removed] This method validates the customer shipping address and provide alternate addresses if any. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/locations/{location}/validateInputs | This method does all necessary pre-job creation validation under resource group. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.DataBox/locations/{location}/validateInputs | This method does all necessary pre-job creation validation under subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs | Lists all the jobs available under the given resource group. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs/{jobName} | Gets information about the specified job. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs/{jobName} | Creates a new job with the specified parameters. Existing job cannot be updated with this API and should instead be updated with the Update job API. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs/{jobName} | Deletes a job. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs/{jobName} | Updates the properties of an existing job. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs/{jobName}/bookShipmentPickUp | Book shipment pick up. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs/{jobName}/cancel | CancelJob. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs/{jobName}/listCredentials | This method gets the unencrypted secrets related to the job. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.DataBox/locations/{location}/regionConfiguration | This API provides configuration details specific to given region/location. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.DataBox/operations
- "List all jobs?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.DataBox/jobs
- "Create a availableSkus?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.DataBox/locations/{location}/availableSkus
- "Create a availableSkus?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/locations/{location}/availableSkus
- "Create a validateAddress?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.DataBox/locations/{location}/validateAddress
- "Create a validateInput?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/locations/{location}/validateInputs
- "Create a validateInput?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.DataBox/locations/{location}/validateInputs
- "List all jobs?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs
- "Get job details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs/{jobName}
- "Update a job?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs/{jobName}
- "Delete a job?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs/{jobName}
- "Partially update a job?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs/{jobName}
- "Create a bookShipmentPickUp?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs/{jobName}/bookShipmentPickUp
- "Create a cancel?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs/{jobName}/cancel
- "Create a listCredential?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataBox/jobs/{jobName}/listCredentials
- "Create a regionConfiguration?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.DataBox/locations/{location}/regionConfiguration
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
