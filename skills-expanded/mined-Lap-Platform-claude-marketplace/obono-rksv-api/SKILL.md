---
name: obono-rksv-api
description: "obono RKSV API skill. Use when working with obono RKSV for auth, registrierkassen, belege. Covers 18 endpoints."
version: 1.0.0
generator: lapsh
---

# obono RKSV API
API version: 1.4.0.0

## Auth
ApiKey Authorization in header | basic

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /auth -- verify access
3. POST /registrierkassen/{registrierkasseUuid}/abschluss -- create first abschluss

## Endpoints

18 endpoints across 4 groups. See references/api-spec.lap for full details.

### auth
| Method | Path | Description |
|--------|------|-------------|
| GET | /auth | Request a JWT access token using your obono username and password. |

### registrierkassen
| Method | Path | Description |
|--------|------|-------------|
| GET | /registrierkassen/{registrierkasseUuid} | Returns information about a particular `Registrierkasse`. |
| GET | /registrierkassen/{registrierkasseUuid}/dep | Generates a DEP file. |
| POST | /registrierkassen/{registrierkasseUuid}/abschluss | Generates an `Abschlussbeleg`. |
| GET | /registrierkassen/{registrierkasseUuid}/belege | Retrieves the `Beleg` collection from the "Datenerfassungsprotokoll". |
| PUT | /registrierkassen/{registrierkasseUuid}/belege/{belegUuid} | Signs a receipt and stores it in the "Datenerfassungsprotokoll". |
| GET | /registrierkassen/{registrierkasseUuid}/belege/{belegUuid} | Retrieves a particular `Beleg` from the "Datenerfassungsprotokoll". |
| GET | /registrierkassen/{registrierkasseUuid}/monatsbelege | Returns a list of `Monatsbelege`. |

### belege
| Method | Path | Description |
|--------|------|-------------|
| GET | /belege/{belegUuid} | Retrieves a particular `Beleg` from the "Datenerfassungsprotokoll". |

### export
| Method | Path | Description |
|--------|------|-------------|
| GET | /export/pdf/belege/{belegUuid} |  |
| GET | /export/qr/belege/{belegUuid} |  |
| GET | /export/html/belege/{belegUuid} |  |
| GET | /export/thermal-print/belege/{belegUuid} |  |
| GET | /export/gobd/registrierkassen/{registrierkasseUuid} |  |
| GET | /export/xls/registrierkassen/{registrierkasseUuid}/belege |  |
| GET | /export/csv/registrierkassen/{registrierkasseUuid}/belege |  |
| GET | /export/dep7/registrierkassen/{registrierkasseUuid}/belege |  |
| GET | /export/dep131/registrierkassen/{registrierkasseUuid}/belege |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all auth?" -> GET /auth
- "Get registrierkassen details?" -> GET /registrierkassen/{registrierkasseUuid}
- "List all dep?" -> GET /registrierkassen/{registrierkasseUuid}/dep
- "Create a abschluss?" -> POST /registrierkassen/{registrierkasseUuid}/abschluss
- "List all belege?" -> GET /registrierkassen/{registrierkasseUuid}/belege
- "Update a belege?" -> PUT /registrierkassen/{registrierkasseUuid}/belege/{belegUuid}
- "Get belege details?" -> GET /registrierkassen/{registrierkasseUuid}/belege/{belegUuid}
- "List all monatsbelege?" -> GET /registrierkassen/{registrierkasseUuid}/monatsbelege
- "Get belege details?" -> GET /belege/{belegUuid}
- "Get belege details?" -> GET /export/pdf/belege/{belegUuid}
- "Get belege details?" -> GET /export/qr/belege/{belegUuid}
- "Get belege details?" -> GET /export/html/belege/{belegUuid}
- "Get belege details?" -> GET /export/thermal-print/belege/{belegUuid}
- "Get registrierkassen details?" -> GET /export/gobd/registrierkassen/{registrierkasseUuid}
- "List all belege?" -> GET /export/xls/registrierkassen/{registrierkasseUuid}/belege
- "List all belege?" -> GET /export/csv/registrierkassen/{registrierkasseUuid}/belege
- "List all belege?" -> GET /export/dep7/registrierkassen/{registrierkasseUuid}/belege
- "List all belege?" -> GET /export/dep131/registrierkassen/{registrierkasseUuid}/belege
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
