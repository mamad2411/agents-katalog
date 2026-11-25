---
name: remediationsclient
description: "RemediationsClient API skill. Use when working with RemediationsClient for providers, subscriptions, {resourceId}. Covers 24 endpoints."
version: 1.0.0
generator: lapsh
---

# RemediationsClient
API version: 2019-07-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/{managementGroupsNamespace}/managementGroups/{managementGroupId}/providers/Microsoft.PolicyInsights/remediations -- verify access
3. POST /providers/{managementGroupsNamespace}/managementGroups/{managementGroupId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/listDeployments -- create first listDeployments

## Endpoints

24 endpoints across 3 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| POST | /providers/{managementGroupsNamespace}/managementGroups/{managementGroupId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/listDeployments | Gets all deployments for a remediation at management group scope. |
| POST | /providers/{managementGroupsNamespace}/managementGroups/{managementGroupId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/cancel | Cancels a remediation at management group scope. |
| GET | /providers/{managementGroupsNamespace}/managementGroups/{managementGroupId}/providers/Microsoft.PolicyInsights/remediations | Gets all remediations for the management group. |
| PUT | /providers/{managementGroupsNamespace}/managementGroups/{managementGroupId}/providers/Microsoft.PolicyInsights/remediations/{remediationName} | Creates or updates a remediation at management group scope. |
| GET | /providers/{managementGroupsNamespace}/managementGroups/{managementGroupId}/providers/Microsoft.PolicyInsights/remediations/{remediationName} | Gets an existing remediation at management group scope. |
| DELETE | /providers/{managementGroupsNamespace}/managementGroups/{managementGroupId}/providers/Microsoft.PolicyInsights/remediations/{remediationName} | Deletes an existing remediation at management group scope. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/listDeployments | Gets all deployments for a remediation at subscription scope. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/cancel | Cancels a remediation at subscription scope. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/remediations | Gets all remediations for the subscription. |
| PUT | /subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/remediations/{remediationName} | Creates or updates a remediation at subscription scope. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/remediations/{remediationName} | Gets an existing remediation at subscription scope. |
| DELETE | /subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/remediations/{remediationName} | Deletes an existing remediation at subscription scope. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/listDeployments | Gets all deployments for a remediation at resource group scope. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/cancel | Cancels a remediation at resource group scope. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/remediations | Gets all remediations for the subscription. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/remediations/{remediationName} | Creates or updates a remediation at resource group scope. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/remediations/{remediationName} | Gets an existing remediation at resource group scope. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/remediations/{remediationName} | Deletes an existing remediation at resource group scope. |

### {resourceId}
| Method | Path | Description |
|--------|------|-------------|
| POST | /{resourceId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/listDeployments | Gets all deployments for a remediation at resource scope. |
| POST | /{resourceId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/cancel | Cancel a remediation at resource scope. |
| GET | /{resourceId}/providers/Microsoft.PolicyInsights/remediations | Gets all remediations for a resource. |
| PUT | /{resourceId}/providers/Microsoft.PolicyInsights/remediations/{remediationName} | Creates or updates a remediation at resource scope. |
| GET | /{resourceId}/providers/Microsoft.PolicyInsights/remediations/{remediationName} | Gets an existing remediation at resource scope. |
| DELETE | /{resourceId}/providers/Microsoft.PolicyInsights/remediations/{remediationName} | Deletes an existing remediation at individual resource scope. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a listDeployment?" -> POST /providers/{managementGroupsNamespace}/managementGroups/{managementGroupId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/listDeployments
- "Create a cancel?" -> POST /providers/{managementGroupsNamespace}/managementGroups/{managementGroupId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/cancel
- "List all remediations?" -> GET /providers/{managementGroupsNamespace}/managementGroups/{managementGroupId}/providers/Microsoft.PolicyInsights/remediations
- "Update a remediation?" -> PUT /providers/{managementGroupsNamespace}/managementGroups/{managementGroupId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}
- "Get remediation details?" -> GET /providers/{managementGroupsNamespace}/managementGroups/{managementGroupId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}
- "Delete a remediation?" -> DELETE /providers/{managementGroupsNamespace}/managementGroups/{managementGroupId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}
- "Create a listDeployment?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/listDeployments
- "Create a cancel?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/cancel
- "List all remediations?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/remediations
- "Update a remediation?" -> PUT /subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}
- "Get remediation details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}
- "Delete a remediation?" -> DELETE /subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}
- "Create a listDeployment?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/listDeployments
- "Create a cancel?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/cancel
- "List all remediations?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/remediations
- "Update a remediation?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/remediations/{remediationName}
- "Get remediation details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/remediations/{remediationName}
- "Delete a remediation?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/remediations/{remediationName}
- "Create a listDeployment?" -> POST /{resourceId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/listDeployments
- "Create a cancel?" -> POST /{resourceId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}/cancel
- "List all remediations?" -> GET /{resourceId}/providers/Microsoft.PolicyInsights/remediations
- "Update a remediation?" -> PUT /{resourceId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}
- "Get remediation details?" -> GET /{resourceId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}
- "Delete a remediation?" -> DELETE /{resourceId}/providers/Microsoft.PolicyInsights/remediations/{remediationName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
