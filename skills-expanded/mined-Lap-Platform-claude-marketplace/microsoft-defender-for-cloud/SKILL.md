---
name: microsoft-defender-for-cloud
description: "Microsoft Defender for Cloud API skill. Use when working with Microsoft Defender for Cloud for subscriptions. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Microsoft Defender for Cloud
API version: 2015-06-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/Microsoft.Security/topologies -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Security/topologies | Gets a list that allows to build a topology view of a subscription. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Security/locations/{ascLocation}/topologies | Gets a list that allows to build a topology view of a subscription and location. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Security/locations/{ascLocation}/topologies/{topologyResourceName} | Gets a specific topology component. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all topologies?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Security/topologies
- "List all topologies?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Security/locations/{ascLocation}/topologies
- "Get topology details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Security/locations/{ascLocation}/topologies/{topologyResourceName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
