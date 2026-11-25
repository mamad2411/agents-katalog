---
name: provider-api-client
description: "Provider API Client API skill. Use when working with Provider API Client for providers, subscriptions. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Provider API Client
API version: 2018-02-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Web/availableStacks -- verify access

## Endpoints

3 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Web/availableStacks | Get available application frameworks and their versions |
| GET | /providers/Microsoft.Web/operations | Gets all available operations for the Microsoft.Web resource provider. Also exposes resource metric definitions |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/availableStacks | Get available application frameworks and their versions |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all availableStacks?" -> GET /providers/Microsoft.Web/availableStacks
- "List all operations?" -> GET /providers/Microsoft.Web/operations
- "List all availableStacks?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/availableStacks
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
