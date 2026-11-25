---
name: security-center
description: "Security Center API skill. Use when working with Security Center for subscriptions. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Security Center
API version: 2017-08-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/Microsoft.Security/workspaceSettings -- verify access

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Security/workspaceSettings | Settings about where we should store your security data and logs. If the result is empty, it means that no custom-workspace configuration was set |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Security/workspaceSettings/{workspaceSettingName} | Settings about where we should store your security data and logs. If the result is empty, it means that no custom-workspace configuration was set |
| PUT | /subscriptions/{subscriptionId}/providers/Microsoft.Security/workspaceSettings/{workspaceSettingName} | creating settings about where we should store your security data and logs |
| PATCH | /subscriptions/{subscriptionId}/providers/Microsoft.Security/workspaceSettings/{workspaceSettingName} | Settings about where we should store your security data and logs |
| DELETE | /subscriptions/{subscriptionId}/providers/Microsoft.Security/workspaceSettings/{workspaceSettingName} | Deletes the custom workspace settings for this subscription. new VMs will report to the default workspace |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all workspaceSettings?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Security/workspaceSettings
- "Get workspaceSetting details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Security/workspaceSettings/{workspaceSettingName}
- "Update a workspaceSetting?" -> PUT /subscriptions/{subscriptionId}/providers/Microsoft.Security/workspaceSettings/{workspaceSettingName}
- "Partially update a workspaceSetting?" -> PATCH /subscriptions/{subscriptionId}/providers/Microsoft.Security/workspaceSettings/{workspaceSettingName}
- "Delete a workspaceSetting?" -> DELETE /subscriptions/{subscriptionId}/providers/Microsoft.Security/workspaceSettings/{workspaceSettingName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
