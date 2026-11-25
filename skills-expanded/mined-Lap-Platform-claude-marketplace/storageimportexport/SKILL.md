---
name: storageimportexport
description: "StorageImportExport API skill. Use when working with StorageImportExport for providers, subscriptions. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# StorageImportExport
API version: 2016-11-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.ImportExport/locations -- verify access
3. POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ImportExport/jobs/{jobName}/listBitLockerKeys -- create first listBitLockerKeys

## Endpoints

10 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.ImportExport/locations | Returns a list of locations to which you can ship the disks associated with an import or export job. A location is a Microsoft data center region. |
| GET | /providers/Microsoft.ImportExport/locations/{locationName} | Returns the details about a location to which you can ship the disks associated with an import or export job. A location is an Azure region. |
| GET | /providers/Microsoft.ImportExport/operations | Returns the list of operations supported by the import/export resource provider. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.ImportExport/jobs | Returns all active and completed jobs in a subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ImportExport/jobs | Returns all active and completed jobs in a resource group. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ImportExport/jobs/{jobName} | Gets information about an existing job. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ImportExport/jobs/{jobName} | Updates specific properties of a job. You can call this operation to notify the Import/Export service that the hard drives comprising the import or export job have been shipped to the Microsoft data center. It can also be used to cancel an existing job. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ImportExport/jobs/{jobName} | Creates a new job or updates an existing job in the specified subscription. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ImportExport/jobs/{jobName} | Deletes an existing job. Only jobs in the Creating or Completed states can be deleted. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ImportExport/jobs/{jobName}/listBitLockerKeys | Returns the BitLocker Keys for all drives in the specified job. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all locations?" -> GET /providers/Microsoft.ImportExport/locations
- "Get location details?" -> GET /providers/Microsoft.ImportExport/locations/{locationName}
- "List all jobs?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.ImportExport/jobs
- "List all jobs?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ImportExport/jobs
- "Get job details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ImportExport/jobs/{jobName}
- "Partially update a job?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ImportExport/jobs/{jobName}
- "Update a job?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ImportExport/jobs/{jobName}
- "Delete a job?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ImportExport/jobs/{jobName}
- "Create a listBitLockerKey?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ImportExport/jobs/{jobName}/listBitLockerKeys
- "List all operations?" -> GET /providers/Microsoft.ImportExport/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
