---
name: analytics-api
description: "Analytics API skill. Use when working with Analytics for rate_limit, user_rate_limit. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Analytics API
API version: v1_beta.0.1

## Auth
OAuth2

## Base URL
https://api.ebay.com/developer/analytics/v1_beta

## Setup
1. Configure auth: OAuth2
2. GET /rate_limit/ -- verify access

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### rate_limit
| Method | Path | Description |
|--------|------|-------------|
| GET | /rate_limit/ | This method retrieves the call limit and utilization data for an application. The data is retrieved for all RESTful APIs and the legacy Trading API.  <br><br>The response from <b>getRateLimits</b> includes a list of the applicable resources and the "call limit", or quota, that is set for each resource. In addition to quota information, the response also includes the number of remaining calls available before the limit is reached, the time remaining before the quota resets, the number of calls made to the specific resource, and the length of the "time window" to which the quota applies.  <br><br>By default, this method returns utilization data for all RESTful API and the legacy Trading API resources. Use the <b>api_name</b> and <b>api_context</b> query parameters to filter the response to only the desired APIs.  <br><br>For more on call limits, see <a href="https://developer.ebay.com/support/app-check " target="_blank">Application Growth Check</a>. |

### user_rate_limit
| Method | Path | Description |
|--------|------|-------------|
| GET | /user_rate_limit/ | This method retrieves the call limit and utilization data for an application user. The call-limit data is returned for all RESTful APIs and the legacy Trading API that limit calls on a per-user basis.  <br><br>The response from <b>getUserRateLimits</b> includes a list of the applicable resources and the "call limit", or quota, that is set for each resource. In addition to quota information, the response also includes the number of remaining calls available before the limit is reached, the time remaining before the quota resets, the number of calls made to the specific resource, and the length of the "time window" to which the quota applies.  <br><br>By default, this method returns utilization data for all RESTful APIs resources and the legacy Trading API calls that limit request access by user. Use the <b>api_name</b> and <b>api_context</b> query parameters to filter the response to only the desired APIs.  <br><br>For more on call limits, see <a href="https://developer.ebay.com/support/app-check " target="_blank">Application Growth Check</a>. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all rate_limit?" -> GET /rate_limit/
- "List all user_rate_limit?" -> GET /user_rate_limit/
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
