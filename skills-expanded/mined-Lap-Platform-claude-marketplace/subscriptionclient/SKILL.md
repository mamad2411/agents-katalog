---
name: subscriptionclient
description: "SubscriptionClient API skill. Use when working with SubscriptionClient for subscriptions. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# SubscriptionClient
API version: 2019-03-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.Subscription/cancel -- create first cancel

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Subscription/cancel | The operation to cancel a subscription |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Subscription/rename | The operation to rename a subscription |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Subscription/enable | The operation to enable a subscription |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a cancel?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Subscription/cancel
- "Create a rename?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Subscription/rename
- "Create a enable?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Subscription/enable
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
