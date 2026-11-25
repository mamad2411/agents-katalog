---
name: microsoftserialconsoleclient
description: "MicrosoftSerialConsoleClient API skill. Use when working with MicrosoftSerialConsoleClient for providers, subscriptions. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# MicrosoftSerialConsoleClient
API version: 2018-05-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.SerialConsole/operations -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.SerialConsole/consoleServices/{default}/disableConsole -- create first disableConsole

## Endpoints

4 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.SerialConsole/operations | Gets a list of Serial Console API operations. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.SerialConsole/consoleServices/{default} | Get the disabled status for a subscription |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.SerialConsole/consoleServices/{default}/disableConsole | Disable Serial Console for a subscription |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.SerialConsole/consoleServices/{default}/enableConsole | Enable Serial Console for a subscription |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.SerialConsole/operations
- "Get consoleService details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.SerialConsole/consoleServices/{default}
- "Create a disableConsole?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.SerialConsole/consoleServices/{default}/disableConsole
- "Create a enableConsole?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.SerialConsole/consoleServices/{default}/enableConsole
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
