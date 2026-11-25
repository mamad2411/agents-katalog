---
name: velo-payments-apis
description: "Velo Payments APIs API skill. Use when working with Velo Payments APIs for authenticate, logout, password. Covers 109 endpoints."
version: 1.0.0
generator: lapsh
---

# Velo Payments APIs
API version: 2.38.183

## Auth
OAuth2 | Bearer basic | OAuth2

## Base URL
https://api.sandbox.velopayments.com/

## Setup
1. Set Authorization header with your Bearer token
2. GET /v2/users -- verify access
3. POST /v1/authenticate -- create first authenticate

## Endpoints

109 endpoints across 20 groups. See references/api-spec.lap for full details.

### authenticate
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/authenticate | Authentication endpoint |

### logout
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/logout | Logout |

### password
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/password/reset | Reset password |

### validate
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/validate | validate |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/users | List Users |
| DELETE | /v2/users/{userId} | Delete a User |
| GET | /v2/users/{userId} | Get User |
| POST | /v2/users/{userId}/disable | Disable a User |
| POST | /v2/users/{userId}/enable | Enable a User |
| POST | /v2/users/invite | Invite a User |
| POST | /v2/users/{userId}/roleUpdate | Update User Role |
| POST | /v2/users/{userId}/mfa/unregister | Unregister MFA for the user |
| POST | /v2/users/{userId}/tokens | Resend a token |
| POST | /v2/users/{userId}/unlock | Unlock a User |
| POST | /v2/users/{userId}/userDetailsUpdate | Update User Details |
| POST | /v2/users/registration/sms | Register SMS Number |
| GET | /v2/users/self | Get Self |
| POST | /v2/users/self/userDetailsUpdate | Update User Details for self |
| POST | /v2/users/self/mfa/unregister | Unregister MFA for Self |
| POST | /v2/users/self/password | Update Password for self |
| POST | /v2/users/self/password/validate | Validate the proposed password |

### payors
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/payors/{payorId} | Get Payor |
| POST | /v1/payors/{payorId}/applications | Create Application |
| POST | /v1/payors/{payorId}/applications/{applicationId}/keys | Create API Key |
| POST | /v1/payors/{payorId}/reminderEmailsUpdate | Reminder Email Opt-Out |
| POST | /v1/payors/{payorId}/branding/logos | Add Logo |
| GET | /v1/payors/{payorId}/branding | Get Branding |

### payorLinks
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/payorLinks | List Payor Links |
| POST | /v1/payorLinks | Create a Payor Link |

### payees
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /v3/payees/{payeeId} | Delete Payee by Id |
| GET | /v3/payees/{payeeId} | Get Payee by Id |
| GET | /v3/payees | List Payees |
| POST | /v3/payees | Initiate Payee Creation |
| GET | /v3/payees/batch/{batchId} | Query Batch Status |
| POST | /v3/payees/{payeeId}/invite | Resend Payee Invite |
| GET | /v3/payees/payors/{payorId}/invitationStatus | Get Payee Invitation Status |
| GET | /v3/payees/deltas | List Payee Changes |
| POST | /v3/payees/{payeeId}/remoteIdUpdate | Update Payee Remote Id |
| POST | /v3/payees/{payeeId}/payeeDetailsUpdate | Update Payee Details |
| DELETE | /v4/payees/{payeeId} | Delete Payee by Id |
| GET | /v4/payees/{payeeId} | Get Payee by Id |
| POST | /v4/payees/{payeeId}/payeeDetailsUpdate | Update Payee Details |
| POST | /v4/payees/{payeeId}/remoteIdUpdate | Update Payee Remote Id |
| GET | /v4/payees | List Payees |
| POST | /v4/payees | Initiate Payee Creation |
| GET | /v4/payees/batch/{batchId} | Query Batch Status |
| POST | /v4/payees/{payeeId}/invite | Resend Payee Invite |
| GET | /v4/payees/payors/{payorId}/invitationStatus | Get Payee Invitation Status |
| GET | /v4/payees/deltas | List Payee Changes |
| GET | /v4/payees/{payeeId}/paymentChannels/ | Get All Payment Channels Details |
| POST | /v4/payees/{payeeId}/paymentChannels/ | Create Payment Channel |
| DELETE | /v4/payees/{payeeId}/paymentChannels/{paymentChannelId} | Delete Payment Channel |
| GET | /v4/payees/{payeeId}/paymentChannels/{paymentChannelId} | Get Payment Channel Details |
| POST | /v4/payees/{payeeId}/paymentChannels/{paymentChannelId} | Update Payment Channel |
| POST | /v4/payees/{payeeId}/paymentChannels/{paymentChannelId}/enable | Enable Payment Channel |
| PUT | /v4/payees/{payeeId}/paymentChannels/order | Update Payees preferred Payment Channel order |

### sourceAccounts
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/sourceAccounts/{sourceAccountId}/notifications | Set notifications |
| POST | /v2/sourceAccounts/{sourceAccountId}/fundingRequest | Create Funding Request |
| GET | /v2/sourceAccounts | Get list of source accounts |
| GET | /v2/sourceAccounts/{sourceAccountId} | Get Source Account |
| POST | /v2/sourceAccounts/{sourceAccountId}/transfers | Transfer Funds between source accounts |
| POST | /v3/sourceAccounts/{sourceAccountId}/fundingRequest | Create Funding Request |
| GET | /v3/sourceAccounts | Get list of source accounts |
| DELETE | /v3/sourceAccounts/{sourceAccountId} | Delete a source account by ID |
| GET | /v3/sourceAccounts/{sourceAccountId} | Get details about given source account. |
| POST | /v3/sourceAccounts/{sourceAccountId}/transfers | Transfer Funds between source accounts |
| POST | /v3/sourceAccounts/{sourceAccountId}/notifications | Set notifications |

### fundingAccounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/fundingAccounts | Get Funding Accounts |
| POST | /v2/fundingAccounts | Create Funding Account |
| GET | /v2/fundingAccounts/{fundingAccountId} | Get Funding Account |

### deltas
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/deltas/fundings | Get Funding Audit Delta |
| GET | /v1/deltas/payments | V1 List Payment Changes |

### fundings
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/fundings/{fundingId} | Get Funding |

### transactions
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/transactions | Get Transactions |
| POST | /v1/transactions | Create a Transaction |
| GET | /v1/transactions/{transactionId} | Get Transaction |

### paymentaudit
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/paymentaudit/fundings | V1 Get Fundings for Payor |
| GET | /v1/paymentaudit/payoutStatistics | V1 Get Payout Statistics |
| GET | /v3/paymentaudit/payouts | V3 Get Payouts for Payor |
| GET | /v3/paymentaudit/payouts/{payoutId} | V3 Get Payments for Payout |
| GET | /v3/paymentaudit/payments | V3 Get List of Payments |
| GET | /v3/paymentaudit/payments/{paymentId} | V3 Get Payment |
| GET | /v3/paymentaudit/transactions | V3 Export Transactions |
| GET | /v4/paymentaudit/payouts | Get Payouts for Payor |
| GET | /v4/paymentaudit/payouts/{payoutId} | Get Payments for Payout |
| GET | /v4/paymentaudit/payments | Get List of Payments |
| GET | /v4/paymentaudit/payments/{paymentId} | Get Payment |
| GET | /v4/paymentaudit/fundings | Get Fundings for Payor |
| GET | /v4/paymentaudit/payoutStatistics | Get Payout Statistics |
| GET | /v4/paymentaudit/transactions | Export Transactions |

### payments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/payments/deltas | List Payment Changes |
| POST | /v1/payments/{paymentId}/withdraw | Withdraw a Payment |

### payouts
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/payouts | Submit Payout |
| DELETE | /v3/payouts/{payoutId} | Withdraw Payout |
| GET | /v3/payouts/{payoutId} | Get Payout Summary |
| POST | /v3/payouts/{payoutId} | Instruct Payout |
| POST | /v3/payouts/{payoutId}/quote | Create a quote for the payout |
| GET | /v3/payouts/{payoutId}/payments | Retrieve payments for a payout |
| DELETE | /v3/payouts/{payoutId}/schedule | Deschedule a payout |
| POST | /v3/payouts/{payoutId}/schedule | Schedule a payout |

### paymentChannelRules
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/paymentChannelRules | List Payment Channel Country Rules |

### supportedCountries
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/supportedCountries | List Supported Countries |
| GET | /v2/supportedCountries | List Supported Countries |

### currencies
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/currencies | List Supported Currencies |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/webhooks | List the details about the webhooks for the given payor. |
| POST | /v1/webhooks | Create Webhook |
| GET | /v1/webhooks/{webhookId} | Get details about the given webhook. |
| POST | /v1/webhooks/{webhookId} | Update Webhook |
| POST | /v1/webhooks/{webhookId}/ping |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a authenticate?" -> POST /v1/authenticate
- "Create a logout?" -> POST /v1/logout
- "Create a reset?" -> POST /v1/password/reset
- "Create a validate?" -> POST /v1/validate
- "List all users?" -> GET /v2/users
- "Delete a user?" -> DELETE /v2/users/{userId}
- "Get user details?" -> GET /v2/users/{userId}
- "Create a disable?" -> POST /v2/users/{userId}/disable
- "Create a enable?" -> POST /v2/users/{userId}/enable
- "Create a invite?" -> POST /v2/users/invite
- "Create a roleUpdate?" -> POST /v2/users/{userId}/roleUpdate
- "Create a unregister?" -> POST /v2/users/{userId}/mfa/unregister
- "Create a token?" -> POST /v2/users/{userId}/tokens
- "Create a unlock?" -> POST /v2/users/{userId}/unlock
- "Create a userDetailsUpdate?" -> POST /v2/users/{userId}/userDetailsUpdate
- "Create a sm?" -> POST /v2/users/registration/sms
- "List all self?" -> GET /v2/users/self
- "Create a userDetailsUpdate?" -> POST /v2/users/self/userDetailsUpdate
- "Create a unregister?" -> POST /v2/users/self/mfa/unregister
- "Create a password?" -> POST /v2/users/self/password
- "Create a validate?" -> POST /v2/users/self/password/validate
- "Get payor details?" -> GET /v2/payors/{payorId}
- "Create a application?" -> POST /v1/payors/{payorId}/applications
- "Create a key?" -> POST /v1/payors/{payorId}/applications/{applicationId}/keys
- "Create a reminderEmailsUpdate?" -> POST /v1/payors/{payorId}/reminderEmailsUpdate
- "Create a logo?" -> POST /v1/payors/{payorId}/branding/logos
- "List all branding?" -> GET /v1/payors/{payorId}/branding
- "List all payorLinks?" -> GET /v1/payorLinks
- "Create a payorLink?" -> POST /v1/payorLinks
- "Delete a payee?" -> DELETE /v3/payees/{payeeId}
- "Get payee details?" -> GET /v3/payees/{payeeId}
- "List all payees?" -> GET /v3/payees
- "Create a payee?" -> POST /v3/payees
- "Get batch details?" -> GET /v3/payees/batch/{batchId}
- "Create a invite?" -> POST /v3/payees/{payeeId}/invite
- "List all invitationStatus?" -> GET /v3/payees/payors/{payorId}/invitationStatus
- "List all deltas?" -> GET /v3/payees/deltas
- "Create a remoteIdUpdate?" -> POST /v3/payees/{payeeId}/remoteIdUpdate
- "Create a payeeDetailsUpdate?" -> POST /v3/payees/{payeeId}/payeeDetailsUpdate
- "Delete a payee?" -> DELETE /v4/payees/{payeeId}
- "Get payee details?" -> GET /v4/payees/{payeeId}
- "Create a payeeDetailsUpdate?" -> POST /v4/payees/{payeeId}/payeeDetailsUpdate
- "Create a remoteIdUpdate?" -> POST /v4/payees/{payeeId}/remoteIdUpdate
- "List all payees?" -> GET /v4/payees
- "Create a payee?" -> POST /v4/payees
- "Get batch details?" -> GET /v4/payees/batch/{batchId}
- "Create a invite?" -> POST /v4/payees/{payeeId}/invite
- "List all invitationStatus?" -> GET /v4/payees/payors/{payorId}/invitationStatus
- "List all deltas?" -> GET /v4/payees/deltas
- "List all paymentChannels?" -> GET /v4/payees/{payeeId}/paymentChannels/
- "Create a paymentChannel?" -> POST /v4/payees/{payeeId}/paymentChannels/
- "Delete a paymentChannel?" -> DELETE /v4/payees/{payeeId}/paymentChannels/{paymentChannelId}
- "Get paymentChannel details?" -> GET /v4/payees/{payeeId}/paymentChannels/{paymentChannelId}
- "Create a enable?" -> POST /v4/payees/{payeeId}/paymentChannels/{paymentChannelId}/enable
- "Create a notification?" -> POST /v1/sourceAccounts/{sourceAccountId}/notifications
- "Create a fundingRequest?" -> POST /v2/sourceAccounts/{sourceAccountId}/fundingRequest
- "List all sourceAccounts?" -> GET /v2/sourceAccounts
- "Get sourceAccount details?" -> GET /v2/sourceAccounts/{sourceAccountId}
- "Create a transfer?" -> POST /v2/sourceAccounts/{sourceAccountId}/transfers
- "Create a fundingRequest?" -> POST /v3/sourceAccounts/{sourceAccountId}/fundingRequest
- "List all sourceAccounts?" -> GET /v3/sourceAccounts
- "Delete a sourceAccount?" -> DELETE /v3/sourceAccounts/{sourceAccountId}
- "Get sourceAccount details?" -> GET /v3/sourceAccounts/{sourceAccountId}
- "Create a transfer?" -> POST /v3/sourceAccounts/{sourceAccountId}/transfers
- "Create a notification?" -> POST /v3/sourceAccounts/{sourceAccountId}/notifications
- "List all fundingAccounts?" -> GET /v2/fundingAccounts
- "Create a fundingAccount?" -> POST /v2/fundingAccounts
- "Get fundingAccount details?" -> GET /v2/fundingAccounts/{fundingAccountId}
- "List all fundings?" -> GET /v1/deltas/fundings
- "Get funding details?" -> GET /v1/fundings/{fundingId}
- "List all transactions?" -> GET /v1/transactions
- "Create a transaction?" -> POST /v1/transactions
- "Get transaction details?" -> GET /v1/transactions/{transactionId}
- "List all fundings?" -> GET /v1/paymentaudit/fundings
- "List all payoutStatistics?" -> GET /v1/paymentaudit/payoutStatistics
- "List all payments?" -> GET /v1/deltas/payments
- "List all payouts?" -> GET /v3/paymentaudit/payouts
- "Get payout details?" -> GET /v3/paymentaudit/payouts/{payoutId}
- "List all payments?" -> GET /v3/paymentaudit/payments
- "Get payment details?" -> GET /v3/paymentaudit/payments/{paymentId}
- "List all transactions?" -> GET /v3/paymentaudit/transactions
- "List all payouts?" -> GET /v4/paymentaudit/payouts
- "Get payout details?" -> GET /v4/paymentaudit/payouts/{payoutId}
- "List all payments?" -> GET /v4/paymentaudit/payments
- "Get payment details?" -> GET /v4/paymentaudit/payments/{paymentId}
- "List all fundings?" -> GET /v4/paymentaudit/fundings
- "List all payoutStatistics?" -> GET /v4/paymentaudit/payoutStatistics
- "List all deltas?" -> GET /v4/payments/deltas
- "List all transactions?" -> GET /v4/paymentaudit/transactions
- "Create a payout?" -> POST /v3/payouts
- "Delete a payout?" -> DELETE /v3/payouts/{payoutId}
- "Get payout details?" -> GET /v3/payouts/{payoutId}
- "Create a quote?" -> POST /v3/payouts/{payoutId}/quote
- "List all payments?" -> GET /v3/payouts/{payoutId}/payments
- "Create a schedule?" -> POST /v3/payouts/{payoutId}/schedule
- "List all paymentChannelRules?" -> GET /v1/paymentChannelRules
- "Create a withdraw?" -> POST /v1/payments/{paymentId}/withdraw
- "List all supportedCountries?" -> GET /v1/supportedCountries
- "List all supportedCountries?" -> GET /v2/supportedCountries
- "List all currencies?" -> GET /v2/currencies
- "List all webhooks?" -> GET /v1/webhooks
- "Create a webhook?" -> POST /v1/webhooks
- "Get webhook details?" -> GET /v1/webhooks/{webhookId}
- "Create a ping?" -> POST /v1/webhooks/{webhookId}/ping
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
