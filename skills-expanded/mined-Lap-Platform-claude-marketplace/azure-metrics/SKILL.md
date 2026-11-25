---
name: azure-metrics
description: "Azure Metrics API skill. Use when working with Azure Metrics for subscriptions. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Azure Metrics
API version: 2018-09-01-preview

## Auth
ApiKey Authorization in header

## Base URL
https://monitoring.azure.com

## Setup
1. Set your API key in the appropriate header
3. POST /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProvider}/{resourceTypeName}/{resourceName}/metrics -- create first metrics

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| POST | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProvider}/{resourceTypeName}/{resourceName}/metrics | **Post the metric values for a resource**. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a metric?" -> POST /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProvider}/{resourceTypeName}/{resourceName}/metrics
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
