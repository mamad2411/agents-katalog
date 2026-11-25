---
name: open-data-api
description: "Open Data API skill. Use when working with Open Data for branches, atms, personal-current-accounts. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# Open Data API
API version: v1.3

## Auth
No authentication required.

## Base URL
https://developer.openbanking.org.uk/reference-implementation/open-banking/v1.3

## Setup
1. No auth setup needed
2. GET /branches -- verify access

## Endpoints

12 endpoints across 6 groups. See references/api-spec.lap for full details.

### branches
| Method | Path | Description |
|--------|------|-------------|
| GET | /branches | Gets a list of all `Branch` objects. |
| HEAD | /branches | Gets header information on the current set of `Branch` data |

### atms
| Method | Path | Description |
|--------|------|-------------|
| GET | /atms | Gets a list of all `ATM` objects. |
| HEAD | /atms | Gets header information on the current set of `ATM` data |

### personal-current-accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /personal-current-accounts | Gets a list of all `Personal Current Account` objects. |
| HEAD | /personal-current-accounts | Gets header information on the current set of `Personal Current Account` data |

### business-current-accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /business-current-accounts | Gets a list of all `Branch Current Account` objects. |
| HEAD | /business-current-accounts | Gets header information on the current set of `Business Current Account` data |

### unsecured-sme-loans
| Method | Path | Description |
|--------|------|-------------|
| GET | /unsecured-sme-loans | Gets a list of all `Unsercured SME Lending` objects. |
| HEAD | /unsecured-sme-loans | Gets header information on the current set of `Unsercured SME Lending` data |

### commercial-credit-cards
| Method | Path | Description |
|--------|------|-------------|
| GET | /commercial-credit-cards | Gets a list of all `Commerical Credit Card` objects. |
| HEAD | /commercial-credit-cards | Gets header information on the current set of `Commerical Credit Card` data |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all branches?" -> GET /branches
- "List all atms?" -> GET /atms
- "List all personal-current-accounts?" -> GET /personal-current-accounts
- "List all business-current-accounts?" -> GET /business-current-accounts
- "List all unsecured-sme-loans?" -> GET /unsecured-sme-loans
- "List all commercial-credit-cards?" -> GET /commercial-credit-cards

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
