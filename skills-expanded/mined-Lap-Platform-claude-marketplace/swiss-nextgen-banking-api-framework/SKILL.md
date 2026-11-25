---
name: swiss-nextgen-banking-api-framework
description: "Swiss NextGen Banking API-Framework API skill. Use when working with Swiss NextGen Banking API-Framework for {payment-service}, accounts, consents. Covers 34 endpoints."
version: 1.0.0
generator: lapsh
---

# Swiss NextGen Banking API-Framework
API version: 1.3.8_2020-12-14 - Swiss edition 1.3.8.1-CH

## Auth
Bearer bearer

## Base URL
https://api.dev.openbankingproject.ch

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/accounts -- verify access
3. POST /v1/{payment-service}/{payment-product} -- create first resource

## Endpoints

34 endpoints across 5 groups. See references/api-spec.lap for full details.

### {payment-service}
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/{payment-service}/{payment-product} | Payment initiation request |
| GET | /v1/{payment-service}/{payment-product}/{paymentId} | Get payment information |
| DELETE | /v1/{payment-service}/{payment-product}/{paymentId} | Payment cancellation request |
| GET | /v1/{payment-service}/{payment-product}/{paymentId}/status | Payment initiation status request |
| POST | /v1/{payment-service}/{payment-product}/{paymentId}/authorisations | Start the authorisation process for a payment initiation |
| GET | /v1/{payment-service}/{payment-product}/{paymentId}/authorisations | Get payment initiation authorisation sub-resources request |
| GET | /v1/{payment-service}/{payment-product}/{paymentId}/authorisations/{authorisationId} | Read the SCA status of the payment authorisation |
| PUT | /v1/{payment-service}/{payment-product}/{paymentId}/authorisations/{authorisationId} | Update PSU data for payment initiation |
| POST | /v1/{payment-service}/{payment-product}/{paymentId}/cancellation-authorisations | Start the authorisation process for the cancellation of the addressed payment |
| GET | /v1/{payment-service}/{payment-product}/{paymentId}/cancellation-authorisations | Will deliver an array of resource identifications to all generated cancellation authorisation sub-resources |
| GET | /v1/{payment-service}/{payment-product}/{paymentId}/cancellation-authorisations/{authorisationId} | Read the SCA status of the payment cancellation's authorisation |
| PUT | /v1/{payment-service}/{payment-product}/{paymentId}/cancellation-authorisations/{authorisationId} | Update PSU data for payment initiation cancellation |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/accounts | Read account list |
| GET | /v1/accounts/{account-id} | Read account details |
| GET | /v1/accounts/{account-id}/balances | Read balance |
| GET | /v1/accounts/{account-id}/transactions | Read transaction list of an account |
| GET | /v1/accounts/{account-id}/transactions/{transactionId} | Read transaction details |

### consents
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/consents | Create consent |
| GET | /v1/consents/{consentId} | Get consent request |
| DELETE | /v1/consents/{consentId} | Delete Consent |
| GET | /v1/consents/{consentId}/status | Consent status request |
| POST | /v1/consents/{consentId}/authorisations | Start the authorisation process for a consent |
| GET | /v1/consents/{consentId}/authorisations | Get consent authorisation sub-resources request |
| GET | /v1/consents/{consentId}/authorisations/{authorisationId} | Read the SCA status of the consent authorisation |
| PUT | /v1/consents/{consentId}/authorisations/{authorisationId} | Update PSU Data for consents |

### funds-confirmations
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/funds-confirmations | Confirmation of funds request |

### signing-baskets
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/signing-baskets | Create a signing basket resource |
| GET | /v1/signing-baskets/{basketId} | Returns the content of an signing basket object |
| DELETE | /v1/signing-baskets/{basketId} | Delete the signing basket |
| GET | /v1/signing-baskets/{basketId}/status | Read the status of the signing basket |
| POST | /v1/signing-baskets/{basketId}/authorisations | Start the authorisation process for a signing basket |
| GET | /v1/signing-baskets/{basketId}/authorisations | Get signing basket authorisation sub-resources request |
| PUT | /v1/signing-baskets/{basketId}/authorisations/{authorisationId} | Update PSU data for signing basket |
| GET | /v1/signing-baskets/{basketId}/authorisations/{authorisationId} | Read the SCA status of the signing basket authorisation |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all status?" -> GET /v1/{payment-service}/{payment-product}/{paymentId}/status
- "Create a authorisation?" -> POST /v1/{payment-service}/{payment-product}/{paymentId}/authorisations
- "List all authorisations?" -> GET /v1/{payment-service}/{payment-product}/{paymentId}/authorisations
- "Get authorisation details?" -> GET /v1/{payment-service}/{payment-product}/{paymentId}/authorisations/{authorisationId}
- "Update a authorisation?" -> PUT /v1/{payment-service}/{payment-product}/{paymentId}/authorisations/{authorisationId}
- "Create a cancellation-authorisation?" -> POST /v1/{payment-service}/{payment-product}/{paymentId}/cancellation-authorisations
- "List all cancellation-authorisations?" -> GET /v1/{payment-service}/{payment-product}/{paymentId}/cancellation-authorisations
- "Get cancellation-authorisation details?" -> GET /v1/{payment-service}/{payment-product}/{paymentId}/cancellation-authorisations/{authorisationId}
- "Update a cancellation-authorisation?" -> PUT /v1/{payment-service}/{payment-product}/{paymentId}/cancellation-authorisations/{authorisationId}
- "List all accounts?" -> GET /v1/accounts
- "Get account details?" -> GET /v1/accounts/{account-id}
- "List all balances?" -> GET /v1/accounts/{account-id}/balances
- "List all transactions?" -> GET /v1/accounts/{account-id}/transactions
- "Get transaction details?" -> GET /v1/accounts/{account-id}/transactions/{transactionId}
- "Create a consent?" -> POST /v1/consents
- "Get consent details?" -> GET /v1/consents/{consentId}
- "Delete a consent?" -> DELETE /v1/consents/{consentId}
- "List all status?" -> GET /v1/consents/{consentId}/status
- "Create a authorisation?" -> POST /v1/consents/{consentId}/authorisations
- "List all authorisations?" -> GET /v1/consents/{consentId}/authorisations
- "Get authorisation details?" -> GET /v1/consents/{consentId}/authorisations/{authorisationId}
- "Update a authorisation?" -> PUT /v1/consents/{consentId}/authorisations/{authorisationId}
- "Create a funds-confirmation?" -> POST /v1/funds-confirmations
- "Create a signing-basket?" -> POST /v1/signing-baskets
- "Get signing-basket details?" -> GET /v1/signing-baskets/{basketId}
- "Delete a signing-basket?" -> DELETE /v1/signing-baskets/{basketId}
- "List all status?" -> GET /v1/signing-baskets/{basketId}/status
- "Create a authorisation?" -> POST /v1/signing-baskets/{basketId}/authorisations
- "List all authorisations?" -> GET /v1/signing-baskets/{basketId}/authorisations
- "Update a authorisation?" -> PUT /v1/signing-baskets/{basketId}/authorisations/{authorisationId}
- "Get authorisation details?" -> GET /v1/signing-baskets/{basketId}/authorisations/{authorisationId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
