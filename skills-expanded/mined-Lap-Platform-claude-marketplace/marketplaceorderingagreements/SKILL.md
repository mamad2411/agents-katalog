---
name: marketplaceorderingagreements
description: "MarketplaceOrdering.Agreements API skill. Use when working with MarketplaceOrdering.Agreements for subscriptions, providers. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# MarketplaceOrdering.Agreements
API version: 2015-06-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.MarketplaceOrdering/operations -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.MarketplaceOrdering/agreements/{publisherId}/offers/{offerId}/plans/{planId}/sign -- create first sign

## Endpoints

7 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.MarketplaceOrdering/offerTypes/{offerType}/publishers/{publisherId}/offers/{offerId}/plans/{planId}/agreements/current | Get marketplace terms. |
| PUT | /subscriptions/{subscriptionId}/providers/Microsoft.MarketplaceOrdering/offerTypes/{offerType}/publishers/{publisherId}/offers/{offerId}/plans/{planId}/agreements/current | Save marketplace terms. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.MarketplaceOrdering/agreements/{publisherId}/offers/{offerId}/plans/{planId}/sign | Sign marketplace terms. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.MarketplaceOrdering/agreements/{publisherId}/offers/{offerId}/plans/{planId}/cancel | Cancel marketplace terms. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.MarketplaceOrdering/agreements/{publisherId}/offers/{offerId}/plans/{planId} | Get marketplace agreement. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.MarketplaceOrdering/agreements | List marketplace agreements in the subscription. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.MarketplaceOrdering/operations | Lists all of the available Microsoft.MarketplaceOrdering REST API operations. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all current?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.MarketplaceOrdering/offerTypes/{offerType}/publishers/{publisherId}/offers/{offerId}/plans/{planId}/agreements/current
- "List all operations?" -> GET /providers/Microsoft.MarketplaceOrdering/operations
- "Create a sign?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.MarketplaceOrdering/agreements/{publisherId}/offers/{offerId}/plans/{planId}/sign
- "Create a cancel?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.MarketplaceOrdering/agreements/{publisherId}/offers/{offerId}/plans/{planId}/cancel
- "Get plan details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.MarketplaceOrdering/agreements/{publisherId}/offers/{offerId}/plans/{planId}
- "List all agreements?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.MarketplaceOrdering/agreements
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
