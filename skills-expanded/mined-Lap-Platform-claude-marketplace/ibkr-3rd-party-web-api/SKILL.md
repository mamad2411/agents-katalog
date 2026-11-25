---
name: ibkr-3rd-party-web-api
description: "IBKR 3rd Party Web API skill. Use when working with IBKR 3rd Party Web for oauth, accounts, secdef. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# IBKR 3rd Party Web API
API version: 1.0.0

## Auth
ApiKey portal in header

## Base URL
https://www.interactivebrokers.com/tradingapi/v1

## Setup
1. Set your API key in the appropriate header
2. GET /accounts -- verify access
3. POST /oauth/request_token -- create first request_token

## Endpoints

16 endpoints across 4 groups. See references/api-spec.lap for full details.

### oauth
| Method | Path | Description |
|--------|------|-------------|
| POST | /oauth/request_token | Obtain a request token |
| POST | /oauth/access_token | Obtain a access token |
| POST | /oauth/live_session_token | Obtain a live session token |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts | Brokerage Accounts |
| GET | /accounts/{account}/positions | Account Positions |
| GET | /accounts/{account}/summary | Account Values Summary |
| GET | /accounts/{account}/orders | Open Orders |
| POST | /accounts/{account}/orders | Place Order |
| GET | /accounts/{account}/orders/{CustomerOrderId} | Return specific order info |
| DELETE | /accounts/{account}/orders/{CustomerOrderId} | Cancel Order |
| PUT | /accounts/{account}/orders/{CustomerOrderId} | Modify Order |
| POST | /accounts/{account}/order_impact | Return margin impact info |
| GET | /accounts/{account}/trades | Returns trades in account |

### secdef
| Method | Path | Description |
|--------|------|-------------|
| GET | /secdef | Get security definition |

### marketdata
| Method | Path | Description |
|--------|------|-------------|
| GET | /marketdata/snapshot | Market Data Snapshot |
| GET | /marketdata/exchange_components | Exchange Components |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a request_token?" -> POST /oauth/request_token
- "Create a access_token?" -> POST /oauth/access_token
- "Create a live_session_token?" -> POST /oauth/live_session_token
- "List all accounts?" -> GET /accounts
- "List all positions?" -> GET /accounts/{account}/positions
- "List all summary?" -> GET /accounts/{account}/summary
- "List all orders?" -> GET /accounts/{account}/orders
- "Create a order?" -> POST /accounts/{account}/orders
- "Get order details?" -> GET /accounts/{account}/orders/{CustomerOrderId}
- "Delete a order?" -> DELETE /accounts/{account}/orders/{CustomerOrderId}
- "Update a order?" -> PUT /accounts/{account}/orders/{CustomerOrderId}
- "Create a order_impact?" -> POST /accounts/{account}/order_impact
- "List all trades?" -> GET /accounts/{account}/trades
- "List all secdef?" -> GET /secdef
- "List all snapshot?" -> GET /marketdata/snapshot
- "List all exchange_components?" -> GET /marketdata/exchange_components
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
