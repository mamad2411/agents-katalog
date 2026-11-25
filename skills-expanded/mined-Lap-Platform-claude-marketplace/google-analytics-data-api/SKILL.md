---
name: google-analytics-data-api
description: "Google Analytics Data API skill. Use when working with Google Analytics Data for v1beta. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Google Analytics Data API
API version: v1beta

## Auth
OAuth2 | OAuth2

## Base URL
https://analyticsdata.googleapis.com/

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /v1beta/{name} -- verify access
3. POST /v1beta/{property}:batchRunPivotReports -- create first v1beta

## Endpoints

7 endpoints across 1 groups. See references/api-spec.lap for full details.

### v1beta
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1beta/{name} | Returns metadata for dimensions and metrics available in reporting methods. Used to explore the dimensions and metrics. In this method, a Google Analytics GA4 Property Identifier is specified in the request, and the metadata response includes Custom dimensions and metrics as well as Universal metadata. For example if a custom metric with parameter name `levels_unlocked` is registered to a property, the Metadata response will contain `customEvent:levels_unlocked`. Universal metadata are dimensions and metrics applicable to any property such as `country` and `totalUsers`. |
| POST | /v1beta/{property}:batchRunPivotReports | Returns multiple pivot reports in a batch. All reports must be for the same GA4 Property. |
| POST | /v1beta/{property}:batchRunReports | Returns multiple reports in a batch. All reports must be for the same GA4 Property. |
| POST | /v1beta/{property}:checkCompatibility | This compatibility method lists dimensions and metrics that can be added to a report request and maintain compatibility. This method fails if the request's dimensions and metrics are incompatible. In Google Analytics, reports fail if they request incompatible dimensions and/or metrics; in that case, you will need to remove dimensions and/or metrics from the incompatible report until the report is compatible. The Realtime and Core reports have different compatibility rules. This method checks compatibility for Core reports. |
| POST | /v1beta/{property}:runPivotReport | Returns a customized pivot report of your Google Analytics event data. Pivot reports are more advanced and expressive formats than regular reports. In a pivot report, dimensions are only visible if they are included in a pivot. Multiple pivots can be specified to further dissect your data. |
| POST | /v1beta/{property}:runRealtimeReport | Returns a customized report of realtime event data for your property. Events appear in realtime reports seconds after they have been sent to the Google Analytics. Realtime reports show events and usage data for the periods of time ranging from the present moment to 30 minutes ago (up to 60 minutes for Google Analytics 360 properties). For a guide to constructing realtime requests & understanding responses, see [Creating a Realtime Report](https://developers.google.com/analytics/devguides/reporting/data/v1/realtime-basics). |
| POST | /v1beta/{property}:runReport | Returns a customized report of your Google Analytics event data. Reports contain statistics derived from data collected by the Google Analytics tracking code. The data returned from the API is as a table with columns for the requested dimensions and metrics. Metrics are individual measurements of user activity on your property, such as active users or event count. Dimensions break down metrics across some common criteria, such as country or event name. For a guide to constructing requests & understanding responses, see [Creating a Report](https://developers.google.com/analytics/devguides/reporting/data/v1/basics). |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get v1beta details?" -> GET /v1beta/{name}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
