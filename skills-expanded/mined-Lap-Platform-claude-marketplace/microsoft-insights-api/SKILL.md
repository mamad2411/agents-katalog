---
name: microsoft-insights-api
description: "Microsoft Insights API skill. Use when working with Microsoft Insights for subscriptions. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Microsoft Insights API
API version: 2018-04-16

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/Microsoft.Insights/scheduledQueryRules -- verify access

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PUT | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Insights/scheduledQueryRules/{ruleName} | Creates or updates an log search rule. |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Insights/scheduledQueryRules/{ruleName} | Gets an Log Search rule |
| PATCH | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Insights/scheduledQueryRules/{ruleName} | Update log search Rule. |
| DELETE | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Insights/scheduledQueryRules/{ruleName} | Deletes a Log Search rule |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Insights/scheduledQueryRules | List the Log Search rules within a subscription group. |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Insights/scheduledQueryRules | List the Log Search rules within a resource group. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a scheduledQueryRule?" -> PUT /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Insights/scheduledQueryRules/{ruleName}
- "Get scheduledQueryRule details?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Insights/scheduledQueryRules/{ruleName}
- "Partially update a scheduledQueryRule?" -> PATCH /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Insights/scheduledQueryRules/{ruleName}
- "Delete a scheduledQueryRule?" -> DELETE /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Insights/scheduledQueryRules/{ruleName}
- "List all scheduledQueryRules?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Insights/scheduledQueryRules
- "List all scheduledQueryRules?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Insights/scheduledQueryRules
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
