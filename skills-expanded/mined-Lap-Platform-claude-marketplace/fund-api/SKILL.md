---
name: fund-api
description: "Fund API skill. Use when working with Fund for accountHolderBalance, accountHolderTransactionList, debitAccountHolder. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# Fund API
API version: 6

## Auth
ApiKey X-API-Key in header | Bearer basic

## Base URL
https://cal-test.adyen.com/cal/services/Fund/v6

## Setup
1. Set Authorization header with your Bearer token
3. POST /accountHolderBalance -- create first accountHolderBalance

## Endpoints

8 endpoints across 8 groups. See references/api-spec.lap for full details.

### accountHolderBalance
| Method | Path | Description |
|--------|------|-------------|
| POST | /accountHolderBalance | Get the balances of an account holder |

### accountHolderTransactionList
| Method | Path | Description |
|--------|------|-------------|
| POST | /accountHolderTransactionList | Get a list of transactions |

### debitAccountHolder
| Method | Path | Description |
|--------|------|-------------|
| POST | /debitAccountHolder | Send a direct debit request |

### payoutAccountHolder
| Method | Path | Description |
|--------|------|-------------|
| POST | /payoutAccountHolder | Pay out from an account to the account holder |

### refundFundsTransfer
| Method | Path | Description |
|--------|------|-------------|
| POST | /refundFundsTransfer | Refund a funds transfer |

### refundNotPaidOutTransfers
| Method | Path | Description |
|--------|------|-------------|
| POST | /refundNotPaidOutTransfers | Refund all transactions of an account since the most recent payout |

### setupBeneficiary
| Method | Path | Description |
|--------|------|-------------|
| POST | /setupBeneficiary | Designate a beneficiary account and transfer the benefactor's current balance |

### transferFunds
| Method | Path | Description |
|--------|------|-------------|
| POST | /transferFunds | Transfer funds between platform accounts |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a accountHolderBalance?" -> POST /accountHolderBalance
- "Create a accountHolderTransactionList?" -> POST /accountHolderTransactionList
- "Create a debitAccountHolder?" -> POST /debitAccountHolder
- "Create a payoutAccountHolder?" -> POST /payoutAccountHolder
- "Create a refundFundsTransfer?" -> POST /refundFundsTransfer
- "Create a refundNotPaidOutTransfer?" -> POST /refundNotPaidOutTransfers
- "Create a setupBeneficiary?" -> POST /setupBeneficiary
- "Create a transferFund?" -> POST /transferFunds
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
