---
name: usagemanagementclient
description: "UsageManagementClient API skill. Use when working with UsageManagementClient for subscriptions. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# UsageManagementClient
API version: 2015-06-01-preview

## Auth
No authentication required.

## Base URL
https://management.azure.com

## Setup
1. No auth setup needed
2. GET /subscriptions/{subscriptionId}/providers/Microsoft.Commerce/UsageAggregates -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Commerce/UsageAggregates | Query aggregated Azure subscription consumption data for a date range. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Commerce/RateCard | Enables you to query for the resource/meter metadata and related prices used in a given subscription by Offer ID, Currency, Locale and Region. The metadata associated with the billing meters, including but not limited to service names, types, resources, units of measure, and regions, is subject to change at any time and without notice. If you intend to use this billing data in an automated fashion, please use the billing meter GUID to uniquely identify each billable item. If the billing meter GUID is scheduled to change due to a new billing model, you will be notified in advance of the change. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all UsageAggregates?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Commerce/UsageAggregates
- "List all RateCard?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Commerce/RateCard

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
