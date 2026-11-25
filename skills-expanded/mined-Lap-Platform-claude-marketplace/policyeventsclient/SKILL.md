---
name: policyeventsclient
description: "PolicyEventsClient API skill. Use when working with PolicyEventsClient for providers, subscriptions, {resourceId}. Covers 9 endpoints."
version: 1.0.0
generator: lapsh
---

# PolicyEventsClient
API version: 2018-04-04

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /{scope}/providers/Microsoft.PolicyInsights/policyEvents/$metadata -- verify access
3. POST /providers/{managementGroupsNamespace}/managementGroups/{managementGroupName}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults -- create first queryResults

## Endpoints

9 endpoints across 4 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| POST | /providers/{managementGroupsNamespace}/managementGroups/{managementGroupName}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults | Queries policy events for the resources under the management group. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults | Queries policy events for the resources under the subscription. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults | Queries policy events for the resources under the resource group. |
| POST | /subscriptions/{subscriptionId}/providers/{authorizationNamespace}/policySetDefinitions/{policySetDefinitionName}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults | Queries policy events for the subscription level policy set definition. |
| POST | /subscriptions/{subscriptionId}/providers/{authorizationNamespace}/policyDefinitions/{policyDefinitionName}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults | Queries policy events for the subscription level policy definition. |
| POST | /subscriptions/{subscriptionId}/providers/{authorizationNamespace}/policyAssignments/{policyAssignmentName}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults | Queries policy events for the subscription level policy assignment. |
| POST | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{authorizationNamespace}/policyAssignments/{policyAssignmentName}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults | Queries policy events for the resource group level policy assignment. |

### {resourceId}
| Method | Path | Description |
|--------|------|-------------|
| POST | /{resourceId}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults | Queries policy events for the resource. |

### {scope}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{scope}/providers/Microsoft.PolicyInsights/policyEvents/$metadata | Gets OData metadata XML document. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a queryResult?" -> POST /providers/{managementGroupsNamespace}/managementGroups/{managementGroupName}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults
- "Create a queryResult?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults
- "Create a queryResult?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults
- "Create a queryResult?" -> POST /{resourceId}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults
- "Create a queryResult?" -> POST /subscriptions/{subscriptionId}/providers/{authorizationNamespace}/policySetDefinitions/{policySetDefinitionName}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults
- "Create a queryResult?" -> POST /subscriptions/{subscriptionId}/providers/{authorizationNamespace}/policyDefinitions/{policyDefinitionName}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults
- "Create a queryResult?" -> POST /subscriptions/{subscriptionId}/providers/{authorizationNamespace}/policyAssignments/{policyAssignmentName}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults
- "Create a queryResult?" -> POST /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{authorizationNamespace}/policyAssignments/{policyAssignmentName}/providers/Microsoft.PolicyInsights/policyEvents/{policyEventsResource}/queryResults
- "List all $metadata?" -> GET /{scope}/providers/Microsoft.PolicyInsights/policyEvents/$metadata
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
