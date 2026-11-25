---
name: policyclient
description: "PolicyClient API skill. Use when working with PolicyClient for subscriptions, providers. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# PolicyClient
API version: 2019-06-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Authorization/policySetDefinitions -- verify access

## Endpoints

10 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PUT | /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName} | Creates or updates a policy set definition. |
| DELETE | /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName} | Deletes a policy set definition. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName} | Retrieves a policy set definition. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policySetDefinitions | Retrieves the policy set definitions for a subscription. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName} | Retrieves a built in policy set definition. |
| GET | /providers/Microsoft.Authorization/policySetDefinitions | Retrieves built-in policy set definitions. |
| PUT | /providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName} | Creates or updates a policy set definition. |
| DELETE | /providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName} | Deletes a policy set definition. |
| GET | /providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName} | Retrieves a policy set definition. |
| GET | /providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policySetDefinitions | Retrieves all policy set definitions in management group. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a policySetDefinition?" -> PUT /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}
- "Delete a policySetDefinition?" -> DELETE /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}
- "Get policySetDefinition details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}
- "Get policySetDefinition details?" -> GET /providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}
- "List all policySetDefinitions?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policySetDefinitions
- "List all policySetDefinitions?" -> GET /providers/Microsoft.Authorization/policySetDefinitions
- "Update a policySetDefinition?" -> PUT /providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}
- "Delete a policySetDefinition?" -> DELETE /providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}
- "Get policySetDefinition details?" -> GET /providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}
- "List all policySetDefinitions?" -> GET /providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policySetDefinitions
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
