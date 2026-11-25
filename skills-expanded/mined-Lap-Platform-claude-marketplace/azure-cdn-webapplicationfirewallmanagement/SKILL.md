---
name: azure-cdn-webapplicationfirewallmanagement
description: "Azure CDN WebApplicationFirewallManagement API skill. Use when working with Azure CDN WebApplicationFirewallManagement for subscriptions. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Azure CDN WebApplicationFirewallManagement
API version: 2019-06-15-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/CdnWebApplicationFirewallPolicies -- verify access

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/CdnWebApplicationFirewallPolicies | Lists all of the protection policies within a resource group. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/CdnWebApplicationFirewallPolicies/{policyName} | Retrieve protection policy with specified name within a resource group. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/CdnWebApplicationFirewallPolicies/{policyName} | Create or update policy with specified rule set name within a resource group. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/CdnWebApplicationFirewallPolicies/{policyName} | Update an existing CdnWebApplicationFirewallPolicy with the specified policy name under the specified subscription and resource group |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/CdnWebApplicationFirewallPolicies/{policyName} | Deletes Policy |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Cdn/CdnWebApplicationFirewallManagedRuleSets | Lists all available managed rule sets. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all CdnWebApplicationFirewallPolicies?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/CdnWebApplicationFirewallPolicies
- "Get CdnWebApplicationFirewallPolicy details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/CdnWebApplicationFirewallPolicies/{policyName}
- "Update a CdnWebApplicationFirewallPolicy?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/CdnWebApplicationFirewallPolicies/{policyName}
- "Partially update a CdnWebApplicationFirewallPolicy?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/CdnWebApplicationFirewallPolicies/{policyName}
- "Delete a CdnWebApplicationFirewallPolicy?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/CdnWebApplicationFirewallPolicies/{policyName}
- "List all CdnWebApplicationFirewallManagedRuleSets?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Cdn/CdnWebApplicationFirewallManagedRuleSets
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
