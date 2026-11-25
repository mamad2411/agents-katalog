---
name: credas-api
description: "Credas API skill. Use when working with Credas for api. Covers 37 endpoints."
version: 1.0.0
generator: lapsh
---

# Credas API
API version: v1

## Auth
ApiKey apikey in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /api/registrations/search -- verify access
3. POST /api/bank-accounts/verify -- create first verify

## Endpoints

37 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/bank-accounts/verify | Verifies bank account details. |
| POST | /api/companies | Searches for a company based on its Company Number and returns its details. |
| GET | /api/companies/{companyId} |  |
| POST | /api/credit-status/perform | Check includes identifying bankruptcy, insolvency, CCJ's or Company Directorship. |
| POST | /api/datachecks | Creates new data check against a specified registration. |
| GET | /api/images/selfie/{registrationId} | Retrieve the selfie image associated with a registration. |
| POST | /api/images/selfie | Add a selfie image to the registration. |
| GET | /api/images/liveness/{registrationId} | Retrieve the liveness action image (UAP) associated with a registration. |
| POST | /api/images/liveness | Add a liveness image (UAP) to the specified registration. |
| GET | /api/images/liveness-performed/{registrationId} | Retrieve the liveness performed image associated with a registration. |
| GET | /api/images/id-document/{registrationId} | Get all id document images associated with a registration. |
| POST | /api/images/id-document | Add an id document image to the specified registration. |
| GET | /api/images/scan-report-pdf/{scanId} | Returns a detailed report on the analysis that has taken place of a scanned document |
| POST | /api/property-register | Creates new property registry check against the registration. |
| GET | /api/property-register/{id} | Retrieves property registry check associated with the registration. |
| POST | /api/registrations/instant | Creates new registration record, adds an ID document and optional selfie image in one go. |
| POST | /api/registrations | Creates new registration. |
| GET | /api/registrations/{id}/check-submitted-id-documents | Checks if submitted documents are sufficient to complete registration. |
| GET | /api/registrations/referenceid/{referenceId}/summary | Finds registrations by the ReferenceId. |
| GET | /api/registrations/{id}/summary | Finds a registration by the Id. |
| GET | /api/registrations/regcode/{regCode}/summary | Finds a registration by the RegCode. |
| GET | /api/registrations/{id}/supported-id-documents | Get a list of supported id document for the specified registration id. |
| PUT | /api/registrations/{id}/status | Updates the status of the registration to one specified in the request. |
| GET | /api/registrations/{id}/pdf-export | Returns PDF export for a given registration. |
| GET | /api/registrations/{id}/pdf-export-sections | Returns a PDF report for a given registration containing specified sections |
| PUT | /api/registrations/{id}/override-check-status | Sets an override for a specific check on the registration. |
| POST | /api/registrations/{id}/resend-invitation | Resends any invitation for the specified registration. |
| GET | /api/registrations/{id}/settings | Gets registration settings or nothing if there are no settings associated with the registration. |
| PUT | /api/registrations/{id}/settings | Updates registration settings. |
| PUT | /api/registrations/{id}/contact-details | Updates a registration's contact details. |
| GET | /api/registrations/search | Gets paged registration list by search criteria or nothing if there are no matching fields. |
| GET | /api/registrations/{id}/pdf-settlement-status | Returns settlement status PDF (Share Code) for a given registration. |
| GET | /api/reg-types | Gets all available RegTypes. |
| POST | /api/report-view/by-referenceid | Retrieves secure links to registration details pages searching by the Reference Id. |
| POST | /api/report-view/by-registrationid | Retrieves secure link to registration details page searching by the Registration Id. |
| POST | /api/web-verifications/by-referenceid | Retrieves secure links to web verification pages searching by the Reference Id. |
| POST | /api/web-verifications/by-registrationid | Retrieves secure link to web verification page searching by the Registration Id. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a verify?" -> POST /api/bank-accounts/verify
- "Create a company?" -> POST /api/companies
- "Get company details?" -> GET /api/companies/{companyId}
- "Create a perform?" -> POST /api/credit-status/perform
- "Create a datacheck?" -> POST /api/datachecks
- "Get selfie details?" -> GET /api/images/selfie/{registrationId}
- "Create a selfie?" -> POST /api/images/selfie
- "Get liveness details?" -> GET /api/images/liveness/{registrationId}
- "Create a liveness?" -> POST /api/images/liveness
- "Get liveness-performed details?" -> GET /api/images/liveness-performed/{registrationId}
- "Get id-document details?" -> GET /api/images/id-document/{registrationId}
- "Create a id-document?" -> POST /api/images/id-document
- "Get scan-report-pdf details?" -> GET /api/images/scan-report-pdf/{scanId}
- "Create a property-register?" -> POST /api/property-register
- "Get property-register details?" -> GET /api/property-register/{id}
- "Create a instant?" -> POST /api/registrations/instant
- "Create a registration?" -> POST /api/registrations
- "List all check-submitted-id-documents?" -> GET /api/registrations/{id}/check-submitted-id-documents
- "List all summary?" -> GET /api/registrations/referenceid/{referenceId}/summary
- "List all summary?" -> GET /api/registrations/{id}/summary
- "List all summary?" -> GET /api/registrations/regcode/{regCode}/summary
- "List all supported-id-documents?" -> GET /api/registrations/{id}/supported-id-documents
- "List all pdf-export?" -> GET /api/registrations/{id}/pdf-export
- "List all pdf-export-sections?" -> GET /api/registrations/{id}/pdf-export-sections
- "Create a resend-invitation?" -> POST /api/registrations/{id}/resend-invitation
- "List all settings?" -> GET /api/registrations/{id}/settings
- "List all search?" -> GET /api/registrations/search
- "List all pdf-settlement-status?" -> GET /api/registrations/{id}/pdf-settlement-status
- "List all reg-types?" -> GET /api/reg-types
- "Create a by-referenceid?" -> POST /api/report-view/by-referenceid
- "Create a by-registrationid?" -> POST /api/report-view/by-registrationid
- "Create a by-referenceid?" -> POST /api/web-verifications/by-referenceid
- "Create a by-registrationid?" -> POST /api/web-verifications/by-registrationid
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
