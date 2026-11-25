---
name: paylocity-api
description: "Paylocity API skill. Use when working with Paylocity for companies, credentials, weblinkstaging. Covers 32 endpoints."
version: 1.0.0
generator: lapsh
---

# Paylocity API
API version: 2

## Auth
OAuth2

## Base URL
https://api.paylocity.com/api

## Setup
1. Configure auth: OAuth2
2. GET /v2/companies/{companyId}/openapi -- verify access
3. POST /v2/credentials/secrets -- create first secrets

## Endpoints

32 endpoints across 3 groups. See references/api-spec.lap for full details.

### companies
| Method | Path | Description |
|--------|------|-------------|
| PUT | /v2/companies/{companyId}/employees/{employeeId}/additionalRates | Add/update additional rates |
| GET | /v2/companies/{companyId}/codes/{codeResource} | Get All Company Codes |
| GET | /v2/companies/{companyId}/openapi | Get Company-Specific Open API Documentation |
| GET | /v2/companies/{companyId}/customfields/{category} | Get All Custom Fields |
| GET | /v2/companies/{companyId}/employees/{employeeId}/directDeposit | Get All Direct Deposit |
| PUT | /v2/companies/{companyId}/employees/{employeeId}/earnings | Add/Update Earning |
| GET | /v2/companies/{companyId}/employees/{employeeId}/earnings | Get All Earnings |
| DELETE | /v2/companies/{companyId}/employees/{employeeId}/earnings/{earningCode}/{startDate} | Delete Earning by Earning Code and Start Date |
| GET | /v2/companies/{companyId}/employees/{employeeId}/earnings/{earningCode}/{startDate} | Get Earning by Earning Code and Start Date |
| GET | /v2/companies/{companyId}/employees/{employeeId}/earnings/{earningCode} | Get Earnings by Earning Code |
| PUT | /v2/companies/{companyId}/employees/{employeeId}/emergencyContacts | Add/update emergency contacts |
| PUT | /v2/companies/{companyId}/employees/{employeeId}/benefitSetup | Add/update employee's benefit setup |
| POST | /v2/companies/{companyId}/employees | Add new employee |
| GET | /v2/companies/{companyId}/employees/ | Get all employees |
| GET | /v2/companies/{companyId}/employees/{employeeId} | Get employee |
| PATCH | /v2/companies/{companyId}/employees/{employeeId} | Update employee |
| POST | /v2/companies/{companyId}/employees/{employeeId}/localTaxes | Add new local tax |
| GET | /v2/companies/{companyId}/employees/{employeeId}/localTaxes | Get all local taxes |
| DELETE | /v2/companies/{companyId}/employees/{employeeId}/localTaxes/{taxCode} | Delete local tax by tax code |
| GET | /v2/companies/{companyId}/employees/{employeeId}/localTaxes/{taxCode} | Get local taxes by tax code |
| PUT | /v2/companies/{companyId}/employees/{employeeId}/nonprimaryStateTax | Add/update non-primary state tax |
| POST | /v2/companies/{companyId}/employeePayRateSearches | Searches for pay rates for the specified company. |
| GET | /v2/companies/{companyId}/employees/{employeeId}/paystatement/details/{year}/{checkDate} | Get employee pay statement details data for the specified year and check date. |
| GET | /v2/companies/{companyId}/employees/{employeeId}/paystatement/details/{year} | Get employee pay statement details data for the specified year. |
| GET | /v2/companies/{companyId}/employees/{employeeId}/paystatement/summary/{year}/{checkDate} | Get employee pay statement summary data for the specified year and check date. |
| GET | /v2/companies/{companyId}/employees/{employeeId}/paystatement/summary/{year} | Get employee pay statement summary data for the specified year. |
| PUT | /v2/companies/{companyId}/employees/{employeeId}/primaryStateTax | Add/update primary state tax |
| PUT | /v2/companies/{companyId}/employees/{employeeId}/sensitivedata | Add/update sensitive data |
| GET | /v2/companies/{companyId}/employees/{employeeId}/sensitivedata | Get sensitive data |
| POST | /v2/companies/{companyId}/employeeStatusSearches | Searches for employee statuses for the specified company. |

### credentials
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/credentials/secrets | Obtain new client secret. |

### weblinkstaging
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/weblinkstaging/companies/{companyId}/employees/newemployees | Add new employee to Web Link |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a secret?" -> POST /v2/credentials/secrets
- "Get code details?" -> GET /v2/companies/{companyId}/codes/{codeResource}
- "List all openapi?" -> GET /v2/companies/{companyId}/openapi
- "Get customfield details?" -> GET /v2/companies/{companyId}/customfields/{category}
- "List all directDeposit?" -> GET /v2/companies/{companyId}/employees/{employeeId}/directDeposit
- "List all earnings?" -> GET /v2/companies/{companyId}/employees/{employeeId}/earnings
- "Delete a earning?" -> DELETE /v2/companies/{companyId}/employees/{employeeId}/earnings/{earningCode}/{startDate}
- "Get earning details?" -> GET /v2/companies/{companyId}/employees/{employeeId}/earnings/{earningCode}/{startDate}
- "Get earning details?" -> GET /v2/companies/{companyId}/employees/{employeeId}/earnings/{earningCode}
- "Create a newemployee?" -> POST /v2/weblinkstaging/companies/{companyId}/employees/newemployees
- "Create a employee?" -> POST /v2/companies/{companyId}/employees
- "List all employees?" -> GET /v2/companies/{companyId}/employees/
- "Get employee details?" -> GET /v2/companies/{companyId}/employees/{employeeId}
- "Partially update a employee?" -> PATCH /v2/companies/{companyId}/employees/{employeeId}
- "Create a localTaxe?" -> POST /v2/companies/{companyId}/employees/{employeeId}/localTaxes
- "List all localTaxes?" -> GET /v2/companies/{companyId}/employees/{employeeId}/localTaxes
- "Delete a localTaxe?" -> DELETE /v2/companies/{companyId}/employees/{employeeId}/localTaxes/{taxCode}
- "Get localTaxe details?" -> GET /v2/companies/{companyId}/employees/{employeeId}/localTaxes/{taxCode}
- "Create a employeePayRateSearche?" -> POST /v2/companies/{companyId}/employeePayRateSearches
- "Get detail details?" -> GET /v2/companies/{companyId}/employees/{employeeId}/paystatement/details/{year}/{checkDate}
- "Get detail details?" -> GET /v2/companies/{companyId}/employees/{employeeId}/paystatement/details/{year}
- "Get summary details?" -> GET /v2/companies/{companyId}/employees/{employeeId}/paystatement/summary/{year}/{checkDate}
- "Get summary details?" -> GET /v2/companies/{companyId}/employees/{employeeId}/paystatement/summary/{year}
- "List all sensitivedata?" -> GET /v2/companies/{companyId}/employees/{employeeId}/sensitivedata
- "Create a employeeStatusSearche?" -> POST /v2/companies/{companyId}/employeeStatusSearches
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
