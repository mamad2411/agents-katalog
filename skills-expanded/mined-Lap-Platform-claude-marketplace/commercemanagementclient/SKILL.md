---
name: commercemanagementclient
description: "CommerceManagementClient API skill. Use when working with CommerceManagementClient for providers, subscriptions. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# CommerceManagementClient
API version: 2015-06-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Commerce.Admin/operations -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.Commerce.Admin/updateEncryption -- create first updateEncryption

## Endpoints

3 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Commerce.Admin/operations | Returns the list of supported REST operations. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Commerce.Admin/subscriberUsageAggregates | Gets a collection of SubscriberUsageAggregates, which are UsageAggregates from users. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Commerce.Admin/updateEncryption | Update the encryption. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.Commerce.Admin/operations
- "List all subscriberUsageAggregates?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Commerce.Admin/subscriberUsageAggregates
- "Create a updateEncryption?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Commerce.Admin/updateEncryption
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
