---
name: google-analytics-admin-api
description: "Google Analytics Admin API skill. Use when working with Google Analytics Admin for v1beta. Covers 26 endpoints."
version: 1.0.0
generator: lapsh
---

# Google Analytics Admin API
API version: v1beta

## Auth
OAuth2 | OAuth2

## Base URL
https://analyticsadmin.googleapis.com/

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /v1beta/accountSummaries -- verify access
3. POST /v1beta/accounts:provisionAccountTicket -- create first accounts:provisionAccountTicket

## Endpoints

26 endpoints across 1 groups. See references/api-spec.lap for full details.

### v1beta
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1beta/accountSummaries | Returns summaries of all accounts accessible by the caller. |
| GET | /v1beta/accounts | Returns all accounts accessible by the caller. Note that these accounts might not currently have GA4 properties. Soft-deleted (ie: "trashed") accounts are excluded by default. Returns an empty list if no relevant accounts are found. |
| POST | /v1beta/accounts:provisionAccountTicket | Requests a ticket for creating an account. |
| GET | /v1beta/properties | Returns child Properties under the specified parent Account. Only "GA4" properties will be returned. Properties will be excluded if the caller does not have access. Soft-deleted (ie: "trashed") properties are excluded by default. Returns an empty list if no relevant properties are found. |
| POST | /v1beta/properties | Creates an "GA4" property with the specified location and attributes. |
| POST | /v1beta/{account}:searchChangeHistoryEvents | Searches through all changes to an account or its children given the specified set of filters. |
| POST | /v1beta/{entity}:runAccessReport | Returns a customized report of data access records. The report provides records of each time a user reads Google Analytics reporting data. Access records are retained for up to 2 years. Data Access Reports can be requested for a property. The property must be in Google Analytics 360. This method is only available to Administrators. These data access records include GA4 UI Reporting, GA4 UI Explorations, GA4 Data API, and other products like Firebase & Admob that can retrieve data from Google Analytics through a linkage. These records don't include property configuration changes like adding a stream or changing a property's time zone. For configuration change history, see [searchChangeHistoryEvents](https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/accounts/searchChangeHistoryEvents). |
| DELETE | /v1beta/{name} | Deletes a GoogleAdsLink on a property |
| GET | /v1beta/{name} | Lookup for a single "GA4" MeasurementProtocolSecret. |
| PATCH | /v1beta/{name} | Updates a GoogleAdsLink on a property |
| POST | /v1beta/{name}:archive | Archives a CustomMetric on a property. |
| GET | /v1beta/{parent}/conversionEvents | Returns a list of conversion events in the specified parent property. Returns an empty list if no conversion events are found. |
| POST | /v1beta/{parent}/conversionEvents | Creates a conversion event with the specified attributes. |
| GET | /v1beta/{parent}/customDimensions | Lists CustomDimensions on a property. |
| POST | /v1beta/{parent}/customDimensions | Creates a CustomDimension. |
| GET | /v1beta/{parent}/customMetrics | Lists CustomMetrics on a property. |
| POST | /v1beta/{parent}/customMetrics | Creates a CustomMetric. |
| GET | /v1beta/{parent}/dataStreams | Lists DataStreams on a property. |
| POST | /v1beta/{parent}/dataStreams | Creates a DataStream. |
| GET | /v1beta/{parent}/firebaseLinks | Lists FirebaseLinks on a property. Properties can have at most one FirebaseLink. |
| POST | /v1beta/{parent}/firebaseLinks | Creates a FirebaseLink. Properties can have at most one FirebaseLink. |
| GET | /v1beta/{parent}/googleAdsLinks | Lists GoogleAdsLinks on a property. |
| POST | /v1beta/{parent}/googleAdsLinks | Creates a GoogleAdsLink. |
| GET | /v1beta/{parent}/measurementProtocolSecrets | Returns child MeasurementProtocolSecrets under the specified parent Property. |
| POST | /v1beta/{parent}/measurementProtocolSecrets | Creates a measurement protocol secret. |
| POST | /v1beta/{property}:acknowledgeUserDataCollection | Acknowledges the terms of user data collection for the specified property. This acknowledgement must be completed (either in the Google Analytics UI or through this API) before MeasurementProtocolSecret resources may be created. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all accountSummaries?" -> GET /v1beta/accountSummaries
- "List all accounts?" -> GET /v1beta/accounts
- "Create a accounts:provisionAccountTicket?" -> POST /v1beta/accounts:provisionAccountTicket
- "List all properties?" -> GET /v1beta/properties
- "Create a property?" -> POST /v1beta/properties
- "Delete a v1beta?" -> DELETE /v1beta/{name}
- "Get v1beta details?" -> GET /v1beta/{name}
- "Partially update a v1beta?" -> PATCH /v1beta/{name}
- "List all conversionEvents?" -> GET /v1beta/{parent}/conversionEvents
- "Create a conversionEvent?" -> POST /v1beta/{parent}/conversionEvents
- "List all customDimensions?" -> GET /v1beta/{parent}/customDimensions
- "Create a customDimension?" -> POST /v1beta/{parent}/customDimensions
- "List all customMetrics?" -> GET /v1beta/{parent}/customMetrics
- "Create a customMetric?" -> POST /v1beta/{parent}/customMetrics
- "List all dataStreams?" -> GET /v1beta/{parent}/dataStreams
- "Create a dataStream?" -> POST /v1beta/{parent}/dataStreams
- "List all firebaseLinks?" -> GET /v1beta/{parent}/firebaseLinks
- "Create a firebaseLink?" -> POST /v1beta/{parent}/firebaseLinks
- "List all googleAdsLinks?" -> GET /v1beta/{parent}/googleAdsLinks
- "Create a googleAdsLink?" -> POST /v1beta/{parent}/googleAdsLinks
- "List all measurementProtocolSecrets?" -> GET /v1beta/{parent}/measurementProtocolSecrets
- "Create a measurementProtocolSecret?" -> POST /v1beta/{parent}/measurementProtocolSecrets
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
