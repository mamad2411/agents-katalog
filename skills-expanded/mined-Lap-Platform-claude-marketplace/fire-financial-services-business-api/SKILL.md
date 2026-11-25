---
name: fire-financial-services-business-api
description: "Fire Financial Services Business API skill. Use when working with Fire Financial Services Business for apps, accounts, activities. Covers 63 endpoints."
version: 1.0.0
generator: lapsh
---

# Fire Financial Services Business API
API version: 1.0

## Auth
Bearer bearer

## Base URL
https://api.fire.com/business

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/accounts -- verify access
3. POST /v1/apps/accesstokens -- create first accesstokens

## Endpoints

63 endpoints across 17 groups. See references/api-spec.lap for full details.

### apps
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/apps/accesstokens | Authenticate with the API. |
| GET | /v1/apps | List all API applications |
| POST | /v1/apps | Create an API Application |
| GET | /v1/apps/{applicationId}/permissions | List all permissions for an API application |
| GET | /v1/apps/permissions | List all permissions for API applications |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/accounts | List accounts |
| POST | /v1/accounts | Create a new Fire Account. |
| GET | /v2/accounts | List accounts (V2) |
| GET | /v2/accounts/{ican} | Get details of an account (V2) |
| PUT | /v2/accounts/{ican} | Update account configuration |
| PUT | /v2/accounts/{ican}/internationaldetails | Request international account details |
| GET | /v1/accounts/{ican} | Get details of an account |
| GET | /v3/accounts/{ican}/transactions | List transactions for an account |

### activities
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/activities | Get activity |

### cards
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/cards | List debit cards |
| POST | /v1/cards | Create a new Fire debit card |

### me
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/me/cards/{cardId}/transactions | Get a list of debit card transactions |
| POST | /v1/me/cards/{cardId}/block | Block a Fire debit card |
| POST | /v1/me/cards/{cardId}/unblock | Unblock a Fire debit card |

### paymentrequests
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/paymentrequests | Create a payment request |
| GET | /v1/paymentrequests/{paymentRequestCode} | Get payment request details |
| GET | /v2/paymentrequests/{paymentRequestCode}/payments | Get list of all payment attempts related to a payment request |
| GET | /v2/paymentrequests/{paymentRequestCode}/reports | Get a report from a payment request |
| GET | /v2/paymentrequests/sent | Get a list of payment request transactions |
| GET | /v2/paymentrequests/{paymentRequestCode}/public | List details of a public payment request |
| PUT | /v2/paymentrequests/{paymentRequestCode}/status | Update the status of a payment request |

### fx
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/fx/rate | Get FX rates |

### limits
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/limits | List all limits |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/webhooks/{webhookId}/events/{event}/test | Send test webhooks |
| GET | /v2/webhooks | List all webhooks |

### batches
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/batches/{batchUuid}/newpayees | List new payees in a batch |
| POST | /v1/batches | Create a new batch |
| GET | /v1/batches | List all batches |
| POST | /v1/batches/{batchUuid}/internaltransfers | Add an internal transfer to a Batch |
| GET | /v1/batches/{batchUuid}/internaltransfers | List items for an internal transfer batch |
| POST | /v1/batches/{batchUuid}/banktransfers | Add a bank transfer to a batch. |
| GET | /v1/batches/{batchUuid}/banktransfers | List items for a bank transfer batch |
| POST | /v2/batches/{batchUuid}/internationaltransfers | Add an international transfer to a Batch |
| GET | /v2/batches/{batchUuid}/internationaltransfers | List items for an international transfer batch |
| DELETE | /v1/batches/{batchUuid}/internaltransfers/{itemUuid} | Remove an internal transfer from a batch |
| DELETE | /v1/batches/{batchUuid}/banktransfers/{itemUuid} | Remove a bank transfer from a batch. |
| DELETE | /v2/batches/{batchUuid}/internationaltransfers/{itemUuid} | Remove an international transfer from a batch |
| DELETE | /v1/batches/{batchUuid} | Cancel a batch |
| GET | /v1/batches/{batchUuid} | Get the details of a batch |
| PUT | /v1/batches/{batchUuid} | Submit a batch |
| GET | /v1/batches/{batchUuid}/approvals | List approvals for a batch. |

### payments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/payments/{paymentUuid} | Get payment details |

### aspsps
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/aspsps | Get list of ASPSPs / Banks |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/users | List all users |
| GET | /v1/users/{userId} | Get the details of a user |
| GET | /v2/users/{userId}/address | Get the address of a user |

### payees
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/payees | List payees |
| GET | /v1/payees/{payeeId} | Get details of a payee |
| GET | /v1/payees/{payeeId}/transactions | List transaction for a payee account |

### directdebits
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/directdebits | List all direct debits |
| GET | /v1/directdebits/{directDebitUuid} | Get the details of a direct debit |
| POST | /v1/directdebits/{directDebitUuid}/reject | Reject a direct debit |

### mandates
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/mandates | List all direct debit mandates |
| GET | /v1/mandates/{mandateUuid} | Get the details of a direct debit mandate |
| PUT | /v1/mandates/{mandateUuid} | Update direct debit mandate alias |
| POST | /v1/mandates/{mandateUuid}/cancel | Cancel a direct debit mandate |
| POST | /v1/mandates/{mandateUuid}/activate | Activate a direct debit mandate |

### services
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/services | Get service Fees and info |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a accesstoken?" -> POST /v1/apps/accesstokens
- "List all accounts?" -> GET /v1/accounts
- "Create a account?" -> POST /v1/accounts
- "List all accounts?" -> GET /v2/accounts
- "Get account details?" -> GET /v2/accounts/{ican}
- "Update a account?" -> PUT /v2/accounts/{ican}
- "List all activities?" -> GET /v2/activities
- "Get account details?" -> GET /v1/accounts/{ican}
- "List all transactions?" -> GET /v3/accounts/{ican}/transactions
- "List all cards?" -> GET /v1/cards
- "Create a card?" -> POST /v1/cards
- "List all transactions?" -> GET /v1/me/cards/{cardId}/transactions
- "Create a block?" -> POST /v1/me/cards/{cardId}/block
- "Create a unblock?" -> POST /v1/me/cards/{cardId}/unblock
- "Create a paymentrequest?" -> POST /v1/paymentrequests
- "Get paymentrequest details?" -> GET /v1/paymentrequests/{paymentRequestCode}
- "List all payments?" -> GET /v2/paymentrequests/{paymentRequestCode}/payments
- "List all reports?" -> GET /v2/paymentrequests/{paymentRequestCode}/reports
- "List all sent?" -> GET /v2/paymentrequests/sent
- "List all public?" -> GET /v2/paymentrequests/{paymentRequestCode}/public
- "List all rate?" -> GET /v2/fx/rate
- "List all limits?" -> GET /v2/limits
- "List all test?" -> GET /v2/webhooks/{webhookId}/events/{event}/test
- "List all webhooks?" -> GET /v2/webhooks
- "List all newpayees?" -> GET /v2/batches/{batchUuid}/newpayees
- "Get payment details?" -> GET /v2/payments/{paymentUuid}
- "List all aspsps?" -> GET /v1/aspsps
- "List all users?" -> GET /v1/users
- "Get user details?" -> GET /v1/users/{userId}
- "List all apps?" -> GET /v1/apps
- "Create a app?" -> POST /v1/apps
- "List all permissions?" -> GET /v1/apps/{applicationId}/permissions
- "List all permissions?" -> GET /v1/apps/permissions
- "List all payees?" -> GET /v1/payees
- "Get payee details?" -> GET /v1/payees/{payeeId}
- "List all transactions?" -> GET /v1/payees/{payeeId}/transactions
- "List all directdebits?" -> GET /v1/directdebits
- "Get directdebit details?" -> GET /v1/directdebits/{directDebitUuid}
- "Create a reject?" -> POST /v1/directdebits/{directDebitUuid}/reject
- "List all mandates?" -> GET /v1/mandates
- "Get mandate details?" -> GET /v1/mandates/{mandateUuid}
- "Update a mandate?" -> PUT /v1/mandates/{mandateUuid}
- "Create a cancel?" -> POST /v1/mandates/{mandateUuid}/cancel
- "Create a activate?" -> POST /v1/mandates/{mandateUuid}/activate
- "Create a batche?" -> POST /v1/batches
- "List all batches?" -> GET /v1/batches
- "Create a internaltransfer?" -> POST /v1/batches/{batchUuid}/internaltransfers
- "List all internaltransfers?" -> GET /v1/batches/{batchUuid}/internaltransfers
- "Create a banktransfer?" -> POST /v1/batches/{batchUuid}/banktransfers
- "List all banktransfers?" -> GET /v1/batches/{batchUuid}/banktransfers
- "Create a internationaltransfer?" -> POST /v2/batches/{batchUuid}/internationaltransfers
- "List all internationaltransfers?" -> GET /v2/batches/{batchUuid}/internationaltransfers
- "Delete a internaltransfer?" -> DELETE /v1/batches/{batchUuid}/internaltransfers/{itemUuid}
- "Delete a banktransfer?" -> DELETE /v1/batches/{batchUuid}/banktransfers/{itemUuid}
- "Delete a internationaltransfer?" -> DELETE /v2/batches/{batchUuid}/internationaltransfers/{itemUuid}
- "Delete a batche?" -> DELETE /v1/batches/{batchUuid}
- "Get batche details?" -> GET /v1/batches/{batchUuid}
- "Update a batche?" -> PUT /v1/batches/{batchUuid}
- "List all approvals?" -> GET /v1/batches/{batchUuid}/approvals
- "List all address?" -> GET /v2/users/{userId}/address
- "List all services?" -> GET /v2/services
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
