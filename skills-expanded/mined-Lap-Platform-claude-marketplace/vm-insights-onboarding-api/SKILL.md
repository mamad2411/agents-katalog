---
name: vm-insights-onboarding-api
description: "VM Insights Onboarding API skill. Use when working with VM Insights Onboarding for {resourceUri}. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# VM Insights Onboarding API
API version: 2018-11-27-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /{resourceUri}/providers/Microsoft.Insights/vmInsightsOnboardingStatuses/default -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### {resourceUri}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{resourceUri}/providers/Microsoft.Insights/vmInsightsOnboardingStatuses/default | Retrieves the VM Insights onboarding status for the specified resource or resource scope. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all default?" -> GET /{resourceUri}/providers/Microsoft.Insights/vmInsightsOnboardingStatuses/default
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
