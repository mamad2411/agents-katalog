---
name: azure-log-analytics-operations-management
description: "Azure Log Analytics - Operations Management API skill. Use when working with Azure Log Analytics - Operations Management for subscriptions, providers. Covers 15 endpoints."
version: 1.0.0
generator: lapsh
---

# Azure Log Analytics - Operations Management
API version: 2015-11-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.OperationsManagement/operations -- verify access

## Endpoints

15 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PUT | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/solutions/{solutionName} | Create/Update Solution. |
| PATCH | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/solutions/{solutionName} | Patch a Solution. |
| DELETE | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/solutions/{solutionName} | Deletes the solution |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/solutions/{solutionName} | Retrieve solution. |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/solutions | Retrieves the solution list for the subscription |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.OperationsManagement/solutions | Retrieves the solution list for the subscription |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.OperationsManagement/ManagementAssociations | Retrieves the ManagementAssociations list for the subscription |
| PUT | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{providerName}/{resourceType}/{resourceName}/providers/Microsoft.OperationsManagement/ManagementAssociations/{managementAssociationName} | Create/Update ManagementAssociation. |
| DELETE | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{providerName}/{resourceType}/{resourceName}/providers/Microsoft.OperationsManagement/ManagementAssociations/{managementAssociationName} | Deletes the ManagementAssociation |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{providerName}/{resourceType}/{resourceName}/providers/Microsoft.OperationsManagement/ManagementAssociations/{managementAssociationName} | Retrieve ManagementAssociation. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.OperationsManagement/ManagementConfigurations | Retrieves the ManagementConfigurations list for the subscription |
| PUT | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/ManagementConfigurations/{managementConfigurationName} | Create/Update ManagementConfiguration. |
| DELETE | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/ManagementConfigurations/{managementConfigurationName} | Deletes the ManagementConfiguration |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/ManagementConfigurations/{managementConfigurationName} | Retrieve ManagementConfiguration. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.OperationsManagement/operations | Lists all of the available OperationsManagement Rest API operations. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a solution?" -> PUT /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/solutions/{solutionName}
- "Partially update a solution?" -> PATCH /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/solutions/{solutionName}
- "Delete a solution?" -> DELETE /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/solutions/{solutionName}
- "Get solution details?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/solutions/{solutionName}
- "List all solutions?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/solutions
- "List all solutions?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.OperationsManagement/solutions
- "List all ManagementAssociations?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.OperationsManagement/ManagementAssociations
- "Update a ManagementAssociation?" -> PUT /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{providerName}/{resourceType}/{resourceName}/providers/Microsoft.OperationsManagement/ManagementAssociations/{managementAssociationName}
- "Delete a ManagementAssociation?" -> DELETE /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{providerName}/{resourceType}/{resourceName}/providers/Microsoft.OperationsManagement/ManagementAssociations/{managementAssociationName}
- "Get ManagementAssociation details?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{providerName}/{resourceType}/{resourceName}/providers/Microsoft.OperationsManagement/ManagementAssociations/{managementAssociationName}
- "List all ManagementConfigurations?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.OperationsManagement/ManagementConfigurations
- "Update a ManagementConfiguration?" -> PUT /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/ManagementConfigurations/{managementConfigurationName}
- "Delete a ManagementConfiguration?" -> DELETE /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/ManagementConfigurations/{managementConfigurationName}
- "Get ManagementConfiguration details?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationsManagement/ManagementConfigurations/{managementConfigurationName}
- "List all operations?" -> GET /providers/Microsoft.OperationsManagement/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
