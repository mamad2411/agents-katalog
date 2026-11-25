---
name: google-analytics-api
description: "Google Analytics API skill. Use when working with Google Analytics for data, management, metadata. Covers 88 endpoints."
version: 1.0.0
generator: lapsh
---

# Google Analytics API
API version: v3

## Auth
OAuth2 | OAuth2

## Base URL
https://analytics.googleapis.com/analytics/v3

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /data/ga -- verify access
3. POST /management/accounts/{accountId}/entityUserLinks -- create first entityUserLinks

## Endpoints

88 endpoints across 5 groups. See references/api-spec.lap for full details.

### data
| Method | Path | Description |
|--------|------|-------------|
| GET | /data/ga | Returns Analytics data for a view (profile). |
| GET | /data/mcf | Returns Analytics Multi-Channel Funnels data for a view (profile). |
| GET | /data/realtime | Returns real time data for a view (profile). |

### management
| Method | Path | Description |
|--------|------|-------------|
| GET | /management/accountSummaries | Lists account summaries (lightweight tree comprised of accounts/properties/profiles) to which the user has access. |
| GET | /management/accounts | Lists all accounts to which the user has access. |
| GET | /management/accounts/{accountId}/entityUserLinks | Lists account-user links for a given account. |
| POST | /management/accounts/{accountId}/entityUserLinks | Adds a new user to the given account. |
| DELETE | /management/accounts/{accountId}/entityUserLinks/{linkId} | Removes a user from the given account. |
| PUT | /management/accounts/{accountId}/entityUserLinks/{linkId} | Updates permissions for an existing user on the given account. |
| GET | /management/accounts/{accountId}/filters | Lists all filters for an account |
| POST | /management/accounts/{accountId}/filters | Create a new filter. |
| DELETE | /management/accounts/{accountId}/filters/{filterId} | Delete a filter. |
| GET | /management/accounts/{accountId}/filters/{filterId} | Returns filters to which the user has access. |
| PATCH | /management/accounts/{accountId}/filters/{filterId} | Updates an existing filter. This method supports patch semantics. |
| PUT | /management/accounts/{accountId}/filters/{filterId} | Updates an existing filter. |
| GET | /management/accounts/{accountId}/webproperties | Lists web properties to which the user has access. |
| POST | /management/accounts/{accountId}/webproperties | Create a new property if the account has fewer than 20 properties. Web properties are visible in the Google Analytics interface only if they have at least one profile. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId} | Gets a web property to which the user has access. |
| PATCH | /management/accounts/{accountId}/webproperties/{webPropertyId} | Updates an existing web property. This method supports patch semantics. |
| PUT | /management/accounts/{accountId}/webproperties/{webPropertyId} | Updates an existing web property. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/customDataSources | List custom data sources to which the user has access. |
| POST | /management/accounts/{accountId}/webproperties/{webPropertyId}/customDataSources/{customDataSourceId}/deleteUploadData | Delete data associated with a previous upload. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/customDataSources/{customDataSourceId}/uploads | List uploads to which the user has access. |
| POST | /management/accounts/{accountId}/webproperties/{webPropertyId}/customDataSources/{customDataSourceId}/uploads | Upload data for a custom data source. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/customDataSources/{customDataSourceId}/uploads/{uploadId} | List uploads to which the user has access. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/customDimensions | Lists custom dimensions to which the user has access. |
| POST | /management/accounts/{accountId}/webproperties/{webPropertyId}/customDimensions | Create a new custom dimension. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/customDimensions/{customDimensionId} | Get a custom dimension to which the user has access. |
| PATCH | /management/accounts/{accountId}/webproperties/{webPropertyId}/customDimensions/{customDimensionId} | Updates an existing custom dimension. This method supports patch semantics. |
| PUT | /management/accounts/{accountId}/webproperties/{webPropertyId}/customDimensions/{customDimensionId} | Updates an existing custom dimension. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/customMetrics | Lists custom metrics to which the user has access. |
| POST | /management/accounts/{accountId}/webproperties/{webPropertyId}/customMetrics | Create a new custom metric. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/customMetrics/{customMetricId} | Get a custom metric to which the user has access. |
| PATCH | /management/accounts/{accountId}/webproperties/{webPropertyId}/customMetrics/{customMetricId} | Updates an existing custom metric. This method supports patch semantics. |
| PUT | /management/accounts/{accountId}/webproperties/{webPropertyId}/customMetrics/{customMetricId} | Updates an existing custom metric. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/entityAdWordsLinks | Lists webProperty-Google Ads links for a given web property. |
| POST | /management/accounts/{accountId}/webproperties/{webPropertyId}/entityAdWordsLinks | Creates a webProperty-Google Ads link. |
| DELETE | /management/accounts/{accountId}/webproperties/{webPropertyId}/entityAdWordsLinks/{webPropertyAdWordsLinkId} | Deletes a web property-Google Ads link. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/entityAdWordsLinks/{webPropertyAdWordsLinkId} | Returns a web property-Google Ads link to which the user has access. |
| PATCH | /management/accounts/{accountId}/webproperties/{webPropertyId}/entityAdWordsLinks/{webPropertyAdWordsLinkId} | Updates an existing webProperty-Google Ads link. This method supports patch semantics. |
| PUT | /management/accounts/{accountId}/webproperties/{webPropertyId}/entityAdWordsLinks/{webPropertyAdWordsLinkId} | Updates an existing webProperty-Google Ads link. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/entityUserLinks | Lists webProperty-user links for a given web property. |
| POST | /management/accounts/{accountId}/webproperties/{webPropertyId}/entityUserLinks | Adds a new user to the given web property. |
| DELETE | /management/accounts/{accountId}/webproperties/{webPropertyId}/entityUserLinks/{linkId} | Removes a user from the given web property. |
| PUT | /management/accounts/{accountId}/webproperties/{webPropertyId}/entityUserLinks/{linkId} | Updates permissions for an existing user on the given web property. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles | Lists views (profiles) to which the user has access. |
| POST | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles | Create a new view (profile). |
| DELETE | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId} | Deletes a view (profile). |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId} | Gets a view (profile) to which the user has access. |
| PATCH | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId} | Updates an existing view (profile). This method supports patch semantics. |
| PUT | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId} | Updates an existing view (profile). |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/entityUserLinks | Lists profile-user links for a given view (profile). |
| POST | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/entityUserLinks | Adds a new user to the given view (profile). |
| DELETE | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/entityUserLinks/{linkId} | Removes a user from the given view (profile). |
| PUT | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/entityUserLinks/{linkId} | Updates permissions for an existing user on the given view (profile). |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/experiments | Lists experiments to which the user has access. |
| POST | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/experiments | Create a new experiment. |
| DELETE | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/experiments/{experimentId} | Delete an experiment. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/experiments/{experimentId} | Returns an experiment to which the user has access. |
| PATCH | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/experiments/{experimentId} | Update an existing experiment. This method supports patch semantics. |
| PUT | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/experiments/{experimentId} | Update an existing experiment. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/goals | Lists goals to which the user has access. |
| POST | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/goals | Create a new goal. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/goals/{goalId} | Gets a goal to which the user has access. |
| PATCH | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/goals/{goalId} | Updates an existing goal. This method supports patch semantics. |
| PUT | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/goals/{goalId} | Updates an existing goal. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/profileFilterLinks | Lists all profile filter links for a profile. |
| POST | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/profileFilterLinks | Create a new profile filter link. |
| DELETE | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/profileFilterLinks/{linkId} | Delete a profile filter link. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/profileFilterLinks/{linkId} | Returns a single profile filter link. |
| PATCH | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/profileFilterLinks/{linkId} | Update an existing profile filter link. This method supports patch semantics. |
| PUT | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/profileFilterLinks/{linkId} | Update an existing profile filter link. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/unsampledReports | Lists unsampled reports to which the user has access. |
| POST | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/unsampledReports | Create a new unsampled report. |
| DELETE | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/unsampledReports/{unsampledReportId} | Deletes an unsampled report. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/unsampledReports/{unsampledReportId} | Returns a single unsampled report. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/remarketingAudiences | Lists remarketing audiences to which the user has access. |
| POST | /management/accounts/{accountId}/webproperties/{webPropertyId}/remarketingAudiences | Creates a new remarketing audience. |
| DELETE | /management/accounts/{accountId}/webproperties/{webPropertyId}/remarketingAudiences/{remarketingAudienceId} | Delete a remarketing audience. |
| GET | /management/accounts/{accountId}/webproperties/{webPropertyId}/remarketingAudiences/{remarketingAudienceId} | Gets a remarketing audience to which the user has access. |
| PATCH | /management/accounts/{accountId}/webproperties/{webPropertyId}/remarketingAudiences/{remarketingAudienceId} | Updates an existing remarketing audience. This method supports patch semantics. |
| PUT | /management/accounts/{accountId}/webproperties/{webPropertyId}/remarketingAudiences/{remarketingAudienceId} | Updates an existing remarketing audience. |
| POST | /management/clientId:hashClientId | Hashes the given Client ID. |
| GET | /management/segments | Lists segments to which the user has access. |

### metadata
| Method | Path | Description |
|--------|------|-------------|
| GET | /metadata/{reportType}/columns | Lists all columns for a report type |

### provisioning
| Method | Path | Description |
|--------|------|-------------|
| POST | /provisioning/createAccountTicket | Creates an account ticket. |
| POST | /provisioning/createAccountTree | Provision account. |

### userDeletion
| Method | Path | Description |
|--------|------|-------------|
| POST | /userDeletion/userDeletionRequests:upsert | Insert or update a user deletion requests. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all ga?" -> GET /data/ga
- "List all mcf?" -> GET /data/mcf
- "List all realtime?" -> GET /data/realtime
- "List all accountSummaries?" -> GET /management/accountSummaries
- "List all accounts?" -> GET /management/accounts
- "List all entityUserLinks?" -> GET /management/accounts/{accountId}/entityUserLinks
- "Create a entityUserLink?" -> POST /management/accounts/{accountId}/entityUserLinks
- "Delete a entityUserLink?" -> DELETE /management/accounts/{accountId}/entityUserLinks/{linkId}
- "Update a entityUserLink?" -> PUT /management/accounts/{accountId}/entityUserLinks/{linkId}
- "List all filters?" -> GET /management/accounts/{accountId}/filters
- "Create a filter?" -> POST /management/accounts/{accountId}/filters
- "Delete a filter?" -> DELETE /management/accounts/{accountId}/filters/{filterId}
- "Get filter details?" -> GET /management/accounts/{accountId}/filters/{filterId}
- "Partially update a filter?" -> PATCH /management/accounts/{accountId}/filters/{filterId}
- "Update a filter?" -> PUT /management/accounts/{accountId}/filters/{filterId}
- "List all webproperties?" -> GET /management/accounts/{accountId}/webproperties
- "Create a webproperty?" -> POST /management/accounts/{accountId}/webproperties
- "Get webproperty details?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}
- "Partially update a webproperty?" -> PATCH /management/accounts/{accountId}/webproperties/{webPropertyId}
- "Update a webproperty?" -> PUT /management/accounts/{accountId}/webproperties/{webPropertyId}
- "List all customDataSources?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/customDataSources
- "Create a deleteUploadData?" -> POST /management/accounts/{accountId}/webproperties/{webPropertyId}/customDataSources/{customDataSourceId}/deleteUploadData
- "List all uploads?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/customDataSources/{customDataSourceId}/uploads
- "Create a upload?" -> POST /management/accounts/{accountId}/webproperties/{webPropertyId}/customDataSources/{customDataSourceId}/uploads
- "Get upload details?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/customDataSources/{customDataSourceId}/uploads/{uploadId}
- "List all customDimensions?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/customDimensions
- "Create a customDimension?" -> POST /management/accounts/{accountId}/webproperties/{webPropertyId}/customDimensions
- "Get customDimension details?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/customDimensions/{customDimensionId}
- "Partially update a customDimension?" -> PATCH /management/accounts/{accountId}/webproperties/{webPropertyId}/customDimensions/{customDimensionId}
- "Update a customDimension?" -> PUT /management/accounts/{accountId}/webproperties/{webPropertyId}/customDimensions/{customDimensionId}
- "List all customMetrics?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/customMetrics
- "Create a customMetric?" -> POST /management/accounts/{accountId}/webproperties/{webPropertyId}/customMetrics
- "Get customMetric details?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/customMetrics/{customMetricId}
- "Partially update a customMetric?" -> PATCH /management/accounts/{accountId}/webproperties/{webPropertyId}/customMetrics/{customMetricId}
- "Update a customMetric?" -> PUT /management/accounts/{accountId}/webproperties/{webPropertyId}/customMetrics/{customMetricId}
- "List all entityAdWordsLinks?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/entityAdWordsLinks
- "Create a entityAdWordsLink?" -> POST /management/accounts/{accountId}/webproperties/{webPropertyId}/entityAdWordsLinks
- "Delete a entityAdWordsLink?" -> DELETE /management/accounts/{accountId}/webproperties/{webPropertyId}/entityAdWordsLinks/{webPropertyAdWordsLinkId}
- "Get entityAdWordsLink details?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/entityAdWordsLinks/{webPropertyAdWordsLinkId}
- "Partially update a entityAdWordsLink?" -> PATCH /management/accounts/{accountId}/webproperties/{webPropertyId}/entityAdWordsLinks/{webPropertyAdWordsLinkId}
- "Update a entityAdWordsLink?" -> PUT /management/accounts/{accountId}/webproperties/{webPropertyId}/entityAdWordsLinks/{webPropertyAdWordsLinkId}
- "List all entityUserLinks?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/entityUserLinks
- "Create a entityUserLink?" -> POST /management/accounts/{accountId}/webproperties/{webPropertyId}/entityUserLinks
- "Delete a entityUserLink?" -> DELETE /management/accounts/{accountId}/webproperties/{webPropertyId}/entityUserLinks/{linkId}
- "Update a entityUserLink?" -> PUT /management/accounts/{accountId}/webproperties/{webPropertyId}/entityUserLinks/{linkId}
- "List all profiles?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles
- "Create a profile?" -> POST /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles
- "Delete a profile?" -> DELETE /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}
- "Get profile details?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}
- "Partially update a profile?" -> PATCH /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}
- "Update a profile?" -> PUT /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}
- "List all entityUserLinks?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/entityUserLinks
- "Create a entityUserLink?" -> POST /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/entityUserLinks
- "Delete a entityUserLink?" -> DELETE /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/entityUserLinks/{linkId}
- "Update a entityUserLink?" -> PUT /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/entityUserLinks/{linkId}
- "List all experiments?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/experiments
- "Create a experiment?" -> POST /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/experiments
- "Delete a experiment?" -> DELETE /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/experiments/{experimentId}
- "Get experiment details?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/experiments/{experimentId}
- "Partially update a experiment?" -> PATCH /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/experiments/{experimentId}
- "Update a experiment?" -> PUT /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/experiments/{experimentId}
- "List all goals?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/goals
- "Create a goal?" -> POST /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/goals
- "Get goal details?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/goals/{goalId}
- "Partially update a goal?" -> PATCH /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/goals/{goalId}
- "Update a goal?" -> PUT /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/goals/{goalId}
- "List all profileFilterLinks?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/profileFilterLinks
- "Create a profileFilterLink?" -> POST /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/profileFilterLinks
- "Delete a profileFilterLink?" -> DELETE /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/profileFilterLinks/{linkId}
- "Get profileFilterLink details?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/profileFilterLinks/{linkId}
- "Partially update a profileFilterLink?" -> PATCH /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/profileFilterLinks/{linkId}
- "Update a profileFilterLink?" -> PUT /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/profileFilterLinks/{linkId}
- "List all unsampledReports?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/unsampledReports
- "Create a unsampledReport?" -> POST /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/unsampledReports
- "Delete a unsampledReport?" -> DELETE /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/unsampledReports/{unsampledReportId}
- "Get unsampledReport details?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/profiles/{profileId}/unsampledReports/{unsampledReportId}
- "List all remarketingAudiences?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/remarketingAudiences
- "Create a remarketingAudience?" -> POST /management/accounts/{accountId}/webproperties/{webPropertyId}/remarketingAudiences
- "Delete a remarketingAudience?" -> DELETE /management/accounts/{accountId}/webproperties/{webPropertyId}/remarketingAudiences/{remarketingAudienceId}
- "Get remarketingAudience details?" -> GET /management/accounts/{accountId}/webproperties/{webPropertyId}/remarketingAudiences/{remarketingAudienceId}
- "Partially update a remarketingAudience?" -> PATCH /management/accounts/{accountId}/webproperties/{webPropertyId}/remarketingAudiences/{remarketingAudienceId}
- "Update a remarketingAudience?" -> PUT /management/accounts/{accountId}/webproperties/{webPropertyId}/remarketingAudiences/{remarketingAudienceId}
- "Create a clientId:hashClientId?" -> POST /management/clientId:hashClientId
- "List all segments?" -> GET /management/segments
- "List all columns?" -> GET /metadata/{reportType}/columns
- "Create a createAccountTicket?" -> POST /provisioning/createAccountTicket
- "Create a createAccountTree?" -> POST /provisioning/createAccountTree
- "Create a userDeletionRequests:upsert?" -> POST /userDeletion/userDeletionRequests:upsert
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
