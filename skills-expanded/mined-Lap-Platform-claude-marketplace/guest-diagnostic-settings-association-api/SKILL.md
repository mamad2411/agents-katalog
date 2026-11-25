---
name: guest-diagnostic-settings-association-api
description: "Guest Diagnostic Settings Association API skill. Use when working with Guest Diagnostic Settings Association for {resourceUri}, subscriptions. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Guest Diagnostic Settings Association API
API version: 2018-06-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/microsoft.insights/guestDiagnosticSettingsAssociations -- verify access

## Endpoints

6 endpoints across 2 groups. See references/api-spec.lap for full details.

### {resourceUri}
| Method | Path | Description |
|--------|------|-------------|
| PUT | /{resourceUri}/providers/microsoft.insights/guestDiagnosticSettingsAssociation/{associationName} | Creates or updates guest diagnostics settings association. |
| GET | /{resourceUri}/providers/microsoft.insights/guestDiagnosticSettingsAssociation/{associationName} | Gets guest diagnostics association settings. |
| DELETE | /{resourceUri}/providers/microsoft.insights/guestDiagnosticSettingsAssociation/{associationName} | Delete guest diagnostics association settings. |
| PATCH | /{resourceUri}/providers/microsoft.insights/guestDiagnosticSettingsAssociation/{associationName} | Updates an existing guestDiagnosticsSettingsAssociation Resource. To update other fields use the CreateOrUpdate method |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/microsoft.insights/guestDiagnosticSettingsAssociations | Get a list of all guest diagnostic settings association in a subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/guestDiagnosticSettingsAssociations | Get a list of all guest diagnostic settings association in a resource group. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a guestDiagnosticSettingsAssociation?" -> PUT /{resourceUri}/providers/microsoft.insights/guestDiagnosticSettingsAssociation/{associationName}
- "Get guestDiagnosticSettingsAssociation details?" -> GET /{resourceUri}/providers/microsoft.insights/guestDiagnosticSettingsAssociation/{associationName}
- "Delete a guestDiagnosticSettingsAssociation?" -> DELETE /{resourceUri}/providers/microsoft.insights/guestDiagnosticSettingsAssociation/{associationName}
- "Partially update a guestDiagnosticSettingsAssociation?" -> PATCH /{resourceUri}/providers/microsoft.insights/guestDiagnosticSettingsAssociation/{associationName}
- "List all guestDiagnosticSettingsAssociations?" -> GET /subscriptions/{subscriptionId}/providers/microsoft.insights/guestDiagnosticSettingsAssociations
- "List all guestDiagnosticSettingsAssociations?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/guestDiagnosticSettingsAssociations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
