---
name: confirmation-of-funds-api-specification
description: "Confirmation of Funds API Specification API skill. Use when working with Confirmation of Funds API Specification for funds-confirmation-consents, funds-confirmations. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Confirmation of Funds API Specification
API version: 4.0.0

## Auth
OAuth2 | OAuth2

## Base URL
/open-banking/v4.0/cbpii

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /funds-confirmation-consents/{ConsentId} -- verify access
3. POST /funds-confirmation-consents -- create first funds-confirmation-consents

## Endpoints

4 endpoints across 2 groups. See references/api-spec.lap for full details.

### funds-confirmation-consents
| Method | Path | Description |
|--------|------|-------------|
| POST | /funds-confirmation-consents | Create Funds Confirmation Consent |
| GET | /funds-confirmation-consents/{ConsentId} | Get Funds Confirmation Consent |
| DELETE | /funds-confirmation-consents/{ConsentId} | Delete Funds Confirmation Consent |

### funds-confirmations
| Method | Path | Description |
|--------|------|-------------|
| POST | /funds-confirmations | Create Funds Confirmation |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a funds-confirmation-consent?" -> POST /funds-confirmation-consents
- "Get funds-confirmation-consent details?" -> GET /funds-confirmation-consents/{ConsentId}
- "Delete a funds-confirmation-consent?" -> DELETE /funds-confirmation-consents/{ConsentId}
- "Create a funds-confirmation?" -> POST /funds-confirmations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
