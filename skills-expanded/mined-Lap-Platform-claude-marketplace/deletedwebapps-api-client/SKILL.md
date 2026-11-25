---
name: deletedwebapps-api-client
description: "DeletedWebApps API Client API skill. Use when working with DeletedWebApps API Client for subscriptions. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# DeletedWebApps API Client
API version: 2018-02-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/deletedSites -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/deletedSites | Get all deleted apps for a subscription. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/deletedSites | Get all deleted apps for a subscription at location |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/deletedSites/{deletedSiteId} | Get deleted app for a subscription at location. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all deletedSites?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/deletedSites
- "List all deletedSites?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/deletedSites
- "Get deletedSite details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Web/locations/{location}/deletedSites/{deletedSiteId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
