---
name: dynamics-telemetry
description: "Dynamics Telemetry API skill. Use when working with Dynamics Telemetry for providers. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Dynamics Telemetry
API version: 2019-01-24

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.DynamicsTelemetry/operations -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.DynamicsTelemetry/operations |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.DynamicsTelemetry/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
