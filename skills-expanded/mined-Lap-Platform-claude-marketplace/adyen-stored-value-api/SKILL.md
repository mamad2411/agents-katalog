---
name: adyen-stored-value-api
description: "Adyen Stored Value API skill. Use when working with Adyen Stored Value for changeStatus, checkBalance, issue. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Adyen Stored Value API
API version: 46

## Auth
ApiKey X-API-Key in header | Bearer basic

## Base URL
https://pal-test.adyen.com/pal/servlet/StoredValue/v46

## Setup
1. Set Authorization header with your Bearer token
3. POST /changeStatus -- create first changeStatus

## Endpoints

6 endpoints across 6 groups. See references/api-spec.lap for full details.

### changeStatus
| Method | Path | Description |
|--------|------|-------------|
| POST | /changeStatus | Changes the status of the payment method. |

### checkBalance
| Method | Path | Description |
|--------|------|-------------|
| POST | /checkBalance | Checks the balance. |

### issue
| Method | Path | Description |
|--------|------|-------------|
| POST | /issue | Issues a new card. |

### load
| Method | Path | Description |
|--------|------|-------------|
| POST | /load | Loads the payment method. |

### mergeBalance
| Method | Path | Description |
|--------|------|-------------|
| POST | /mergeBalance | Merge the balance of two cards. |

### voidTransaction
| Method | Path | Description |
|--------|------|-------------|
| POST | /voidTransaction | Voids a transaction. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a changeStatus?" -> POST /changeStatus
- "Create a checkBalance?" -> POST /checkBalance
- "Create a issue?" -> POST /issue
- "Create a load?" -> POST /load
- "Create a mergeBalance?" -> POST /mergeBalance
- "Create a voidTransaction?" -> POST /voidTransaction
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
