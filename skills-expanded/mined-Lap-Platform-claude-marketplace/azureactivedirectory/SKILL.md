---
name: azureactivedirectory
description: "azureactivedirectory API skill. Use when working with azureactivedirectory for providers. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# azureactivedirectory
API version: 2017-04-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/microsoft.aadiam/operations -- verify access

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/microsoft.aadiam/operations | Operation to return the list of available operations. |
| GET | /providers/microsoft.aadiam/diagnosticSettings | Gets the active diagnostic settings list for AadIam. |
| GET | /providers/microsoft.aadiam/diagnosticSettings/{name} | Gets the active diagnostic setting for AadIam. |
| PUT | /providers/microsoft.aadiam/diagnosticSettings/{name} | Creates or updates diagnostic settings for AadIam. |
| DELETE | /providers/microsoft.aadiam/diagnosticSettings/{name} | Deletes existing diagnostic setting for AadIam. |
| GET | /providers/microsoft.aadiam/diagnosticSettingsCategories | Lists the diagnostic settings categories for AadIam. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/microsoft.aadiam/operations
- "List all diagnosticSettings?" -> GET /providers/microsoft.aadiam/diagnosticSettings
- "Get diagnosticSetting details?" -> GET /providers/microsoft.aadiam/diagnosticSettings/{name}
- "Update a diagnosticSetting?" -> PUT /providers/microsoft.aadiam/diagnosticSettings/{name}
- "Delete a diagnosticSetting?" -> DELETE /providers/microsoft.aadiam/diagnosticSettings/{name}
- "List all diagnosticSettingsCategories?" -> GET /providers/microsoft.aadiam/diagnosticSettingsCategories
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
