---
name: subscriptionsmanagementclient
description: "SubscriptionsManagementClient API skill. Use when working with SubscriptionsManagementClient for subscriptions. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# SubscriptionsManagementClient
API version: 2015-11-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/Microsoft.Subscriptions.Admin/locations/{location}/quotas -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Subscriptions.Admin/locations/{location}/quotas | Get the list of quotas at a location. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Subscriptions.Admin/locations/{location}/quotas/{quota} | Gets a quota by name. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all quotas?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Subscriptions.Admin/locations/{location}/quotas
- "Get quota details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Subscriptions.Admin/locations/{location}/quotas/{quota}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
