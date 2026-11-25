---
name: guest-diagnostic-settings-api
description: "Guest Diagnostic Settings API skill. Use when working with Guest Diagnostic Settings for subscriptions. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Guest Diagnostic Settings API
API version: 2018-06-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/microsoft.insights/guestDiagnosticSettings -- verify access

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PUT | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/microsoft.insights/guestDiagnosticSettings/{diagnosticSettingsName} | Creates or updates guest diagnostics settings. |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/microsoft.insights/guestDiagnosticSettings/{diagnosticSettingsName} | Gets guest diagnostics settings. |
| PATCH | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/microsoft.insights/guestDiagnosticSettings/{diagnosticSettingsName} | Updates guest diagnostics settings. |
| DELETE | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/microsoft.insights/guestDiagnosticSettings/{diagnosticSettingsName} | Delete guest diagnostics settings. |
| GET | /subscriptions/{subscriptionId}/providers/microsoft.insights/guestDiagnosticSettings | Get a list of all guest diagnostic settings in a subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/guestDiagnosticSettings | Get a list of all guest diagnostic settings in a resource group. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a guestDiagnosticSetting?" -> PUT /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/microsoft.insights/guestDiagnosticSettings/{diagnosticSettingsName}
- "Get guestDiagnosticSetting details?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/microsoft.insights/guestDiagnosticSettings/{diagnosticSettingsName}
- "Partially update a guestDiagnosticSetting?" -> PATCH /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/microsoft.insights/guestDiagnosticSettings/{diagnosticSettingsName}
- "Delete a guestDiagnosticSetting?" -> DELETE /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/microsoft.insights/guestDiagnosticSettings/{diagnosticSettingsName}
- "List all guestDiagnosticSettings?" -> GET /subscriptions/{subscriptionId}/providers/microsoft.insights/guestDiagnosticSettings
- "List all guestDiagnosticSettings?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/guestDiagnosticSettings
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
