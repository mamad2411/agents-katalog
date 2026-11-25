---
name: costmanagementclient
description: "CostManagementClient API skill. Use when working with CostManagementClient for providers, {scope}. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# CostManagementClient
API version: 2019-04-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.CostManagement/views -- verify access

## Endpoints

13 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.CostManagement/views | Lists all views by tenant and object. |
| GET | /providers/Microsoft.CostManagement/views/{viewName} | Gets the view by view name. |
| PUT | /providers/Microsoft.CostManagement/views/{viewName} | The operation to create or update a view. Update operation requires latest eTag to be set in the request. You may obtain the latest eTag by performing a get operation. Create operation does not require eTag. |
| DELETE | /providers/Microsoft.CostManagement/views/{viewName} | The operation to delete a view. |
| GET | /providers/Microsoft.CostManagement/operations | Lists all of the available consumption REST API operations. |

### {scope}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{scope}/providers/Microsoft.CostManagement/views | Lists all views at the given scope. |
| GET | /{scope}/providers/Microsoft.CostManagement/views/{viewName} | Gets the view for the defined scope by view name. |
| PUT | /{scope}/providers/Microsoft.CostManagement/views/{viewName} | The operation to create or update a view. Update operation requires latest eTag to be set in the request. You may obtain the latest eTag by performing a get operation. Create operation does not require eTag. |
| DELETE | /{scope}/providers/Microsoft.CostManagement/views/{viewName} | The operation to delete a view. |
| GET | /{scope}/providers/Microsoft.CostManagement/budgets | Lists all budgets for the defined scope. |
| GET | /{scope}/providers/Microsoft.CostManagement/budgets/{budgetName} | Gets the budget for the scope by budget name. |
| PUT | /{scope}/providers/Microsoft.CostManagement/budgets/{budgetName} | The operation to create or update a budget. Update operation requires latest eTag to be set in the request mandatorily. You may obtain the latest eTag by performing a get operation. Create operation does not require eTag. |
| DELETE | /{scope}/providers/Microsoft.CostManagement/budgets/{budgetName} | The operation to delete a budget. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all views?" -> GET /providers/Microsoft.CostManagement/views
- "List all views?" -> GET /{scope}/providers/Microsoft.CostManagement/views
- "Get view details?" -> GET /providers/Microsoft.CostManagement/views/{viewName}
- "Update a view?" -> PUT /providers/Microsoft.CostManagement/views/{viewName}
- "Delete a view?" -> DELETE /providers/Microsoft.CostManagement/views/{viewName}
- "Get view details?" -> GET /{scope}/providers/Microsoft.CostManagement/views/{viewName}
- "Update a view?" -> PUT /{scope}/providers/Microsoft.CostManagement/views/{viewName}
- "Delete a view?" -> DELETE /{scope}/providers/Microsoft.CostManagement/views/{viewName}
- "List all budgets?" -> GET /{scope}/providers/Microsoft.CostManagement/budgets
- "Get budget details?" -> GET /{scope}/providers/Microsoft.CostManagement/budgets/{budgetName}
- "Update a budget?" -> PUT /{scope}/providers/Microsoft.CostManagement/budgets/{budgetName}
- "Delete a budget?" -> DELETE /{scope}/providers/Microsoft.CostManagement/budgets/{budgetName}
- "List all operations?" -> GET /providers/Microsoft.CostManagement/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
