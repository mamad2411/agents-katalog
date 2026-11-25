---
name: recoveryservicesclient
description: "RecoveryServicesClient API skill. Use when working with RecoveryServicesClient for Subscriptions. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# RecoveryServicesClient
API version: 2016-06-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /Subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.RecoveryServices/vaults/{vaultName}/usages -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### Subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /Subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.RecoveryServices/vaults/{vaultName}/usages | Fetches the usages of the vault. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all usages?" -> GET /Subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.RecoveryServices/vaults/{vaultName}/usages
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
