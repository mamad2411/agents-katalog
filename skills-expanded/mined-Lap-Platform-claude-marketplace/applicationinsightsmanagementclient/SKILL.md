---
name: applicationinsightsmanagementclient
description: "ApplicationInsightsManagementClient API skill. Use when working with ApplicationInsightsManagementClient for subscriptions. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# ApplicationInsightsManagementClient
API version: 2019-10-17-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/workbooktemplates -- verify access

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/workbooktemplates | Get all Workbook templates defined within a specified resource group. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/workbooktemplates/{resourceName} | Get a single workbook template by its resourceName. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/workbooktemplates/{resourceName} | Delete a workbook template. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/workbooktemplates/{resourceName} | Create a new workbook template. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/workbooktemplates/{resourceName} | Updates a workbook template that has already been added. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all workbooktemplates?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/workbooktemplates
- "Get workbooktemplate details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/workbooktemplates/{resourceName}
- "Delete a workbooktemplate?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/workbooktemplates/{resourceName}
- "Update a workbooktemplate?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/workbooktemplates/{resourceName}
- "Partially update a workbooktemplate?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/workbooktemplates/{resourceName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
