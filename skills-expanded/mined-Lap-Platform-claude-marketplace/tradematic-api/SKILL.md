---
name: tradematic-api
description: "Tradematic API skill. Use when working with Tradematic for ping, time, client. Covers 90 endpoints."
version: 1.0.0
generator: lapsh
---

# Tradematic API
API version: 1.0.6

## Auth
ApiKey X-API-Key in header

## Base URL
https://api.tradematic.com

## Setup
1. Set your API key in the appropriate header
2. GET /ping -- verify access
3. POST /client/users/login -- create first login

## Endpoints

90 endpoints across 9 groups. See references/api-spec.lap for full details.

### ping
| Method | Path | Description |
|--------|------|-------------|
| GET | /ping | Ping |

### time
| Method | Path | Description |
|--------|------|-------------|
| GET | /time | Get current server time |

### client
| Method | Path | Description |
|--------|------|-------------|
| GET | /client/users | Get users list |
| GET | /client/users/{userid} | Get user by ID |
| POST | /client/users/login | Logs user into the system |
| POST | /client/users/register | Register a new user |
| GET | /client/users/roles | Get user roles list |
| PUT | /client/users/{userid}/role | Get user roles list |
| POST | /client/users/check | Checks for a user |
| GET | /client/apikeys | Get API keys |
| POST | /client/apikeys | Create new API key |
| DELETE | /client/apikeys/{keyid} | Delete API key |

### autofollow
| Method | Path | Description |
|--------|------|-------------|
| GET | /autofollow/strategies | Get autofollow strategies list |
| POST | /autofollow/strategies | Create new autofollow strategy |
| GET | /autofollow/strategies/{strategyid} | Get autofollow strategy by ID |
| PUT | /autofollow/strategies/{strategyid} | Update autofollow strategy |
| PUT | /autofollow/strategies/{strategyid}/content | Update rules for strategy that was created with strategy builder, or just content field |
| PUT | /autofollow/strategies/{strategyid}/state | Update autofollow strategy state |
| PUT | /autofollow/strategies/{strategyid}/status | Update autofollow strategy status |
| GET | /autofollow/strategies/{strategyid}/positions | Get positions for strategy |
| POST | /autofollow/strategies/{strategyid}/positions | Send a new position for autofollow strategy |
| PUT | /autofollow/strategies/{strategyid}/positions | Update an existing position for autofollow strategy |
| DELETE | /autofollow/strategies/{strategyid}/positions | Delete an existing position for autofollow strategy |
| GET | /autofollow/strategies/{strategyid}/signals | Get trading signals for strategy |
| POST | /autofollow/strategies/{strategyid}/signals | Send a new signal for autofollow strategy |
| GET | /autofollow/strategies/risklevels | Get risk levels |
| GET | /autofollow/strategies/rates | Get strategies rates |
| GET | /autofollow/strategies/statuses | Get strategies statuses |
| GET | /autofollow/authors | Get authors |

### taskmanager
| Method | Path | Description |
|--------|------|-------------|
| GET | /taskmanager/tasks | Get tasks list |
| POST | /taskmanager/tasks | Create a new task |
| GET | /taskmanager/tasks/{taskid} | Get task by ID |
| GET | /taskmanager/tasks/{taskid}/status | Get task status |
| GET | /taskmanager/tasks/{taskid}/folder | Get task result folder name |
| GET | /taskmanager/tasks/{taskid}/result | Get task result |
| GET | /taskmanager/tasks/{taskid}/result2 | Get task result (version 2) |
| GET | /taskmanager/tasks/{taskid}/equity | Get data for equity chart |
| GET | /taskmanager/tasks/{taskid}/equitypct | Get data for equity chart (%) |
| GET | /taskmanager/tasks/{taskid}/equitypctsm | Get spared data for equity chart (%) |
| GET | /taskmanager/tasks/{taskid}/drawdown | Get data for drawdown chart |
| GET | /taskmanager/tasks/{taskid}/performance | Get backtest statistics |
| GET | /taskmanager/tasks/{taskid}/trades | Get backtest trades list |
| GET | /taskmanager/tasks/{taskid}/contribution | Get backtest symbol contribution data |
| GET | /taskmanager/tasks/{taskid}/bymonths | Get backtest data for equity chart, grouped by months |
| GET | /taskmanager/tasks/{taskid}/byquarters | Get backtest data for equity chart, grouped by quarters |
| GET | /taskmanager/tasks/{taskid}/byyears | Get backtest data for equity chart, grouped by years |

### builder
| Method | Path | Description |
|--------|------|-------------|
| GET | /builder/rules | Get strategy builder rules list |
| GET | /builder/rules/{ruleid} | Get strategy builder rules by ID |

### marketdata
| Method | Path | Description |
|--------|------|-------------|
| GET | /marketdata/markets | Get markets list |
| GET | /marketdata/markets/{name} | Get market by name |
| GET | /marketdata/indicators | Get technical indicators list |
| GET | /marketdata/indicators/{name} | Get technical indicator by name |
| GET | /marketdata/indicators/{name}/histdata | Get technical indicator historical data by name |
| GET | /marketdata/symbols | Get symbols list |
| GET | /marketdata/symbols/{name} | Get symbol by name |
| GET | /marketdata/symbols/{name}/histdata | Get historical data for instrument |
| GET | /marketdata/symbols/{name}/snapshot | Get snapshot for a symbol by name |
| GET | /marketdata/symbols/snapshots | Get snapshots for symbols |

### cloud
| Method | Path | Description |
|--------|------|-------------|
| GET | /cloud/accounts | Get trading accounts list |
| GET | /cloud/accounts/{accountid} | Get trading account by ID |
| GET | /cloud/accounts/{accountid}/orders | Get orders list by account |
| POST | /cloud/accounts/{accountid}/orders | Place a new order |
| DELETE | /cloud/accounts/{accountid}/orders/{orderid} | Cancel an order by ID |
| GET | /cloud/accounts/{accountid}/trades | Get trades list by account |
| GET | /cloud/accounts/{accountid}/snapshots | Get account equity and cash snapshots |
| POST | /cloud/accounts/{accountid}/closeall | Close all positions by account |
| POST | /cloud/accounts/{accountid}/close | Close symbol position by account |
| POST | /cloud/accounts/{accountid}/sync | Syhchronize an account with account active strategies |
| GET | /cloud/accounts/{accountid}/sync | Get synchronization status of account with account active strategies |
| GET | /cloud/accounts/{accountid}/commands | Get commands list by account |
| GET | /cloud/commands | Get commands list |
| GET | /cloud/commands/{commandid} | Get command by ID |
| GET | /cloud/sessions | Get sessions list |
| GET | /cloud/sessions/{sessionid} | Get session by ID |
| GET | /cloud/strategies | Get list of active (executing) strategies |
| GET | /cloud/strategies/{strategyid} | Get active (executing) strategy by ID |
| POST | /cloud/strategies/start | Start a strategy execution for account |
| POST | /cloud/strategies/{strategyid}/stop | Stop a strategy execution by ID |
| GET | /cloud/connectors | Get available connectors list |
| GET | /cloud/connectors/{connectorid} | Get connector by ID |
| GET | /cloud/connections | Get connections list |
| POST | /cloud/connections | Create a new connection |
| GET | /cloud/connections/{connectionid} | Get connection by ID |
| PUT | /cloud/connections/{connectionid} | Update existing connection |
| DELETE | /cloud/connections/{connectionid} | Delete connection by ID |

### marketplace
| Method | Path | Description |
|--------|------|-------------|
| GET | /marketplace/balance | Get user balance |
| GET | /marketplace/products | Get products list |
| GET | /marketplace/products/{productid} | Get product by ID |
| GET | /marketplace/products/{productid}/rates | Get product rates by product ID |
| GET | /marketplace/groups | Get product groups list |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all ping?" -> GET /ping
- "List all time?" -> GET /time
- "List all users?" -> GET /client/users
- "Get user details?" -> GET /client/users/{userid}
- "Create a login?" -> POST /client/users/login
- "Create a register?" -> POST /client/users/register
- "List all roles?" -> GET /client/users/roles
- "Create a check?" -> POST /client/users/check
- "List all apikeys?" -> GET /client/apikeys
- "Create a apikey?" -> POST /client/apikeys
- "Delete a apikey?" -> DELETE /client/apikeys/{keyid}
- "List all strategies?" -> GET /autofollow/strategies
- "Create a strategy?" -> POST /autofollow/strategies
- "Get strategy details?" -> GET /autofollow/strategies/{strategyid}
- "Update a strategy?" -> PUT /autofollow/strategies/{strategyid}
- "List all positions?" -> GET /autofollow/strategies/{strategyid}/positions
- "Create a position?" -> POST /autofollow/strategies/{strategyid}/positions
- "List all signals?" -> GET /autofollow/strategies/{strategyid}/signals
- "Create a signal?" -> POST /autofollow/strategies/{strategyid}/signals
- "List all risklevels?" -> GET /autofollow/strategies/risklevels
- "List all rates?" -> GET /autofollow/strategies/rates
- "List all statuses?" -> GET /autofollow/strategies/statuses
- "List all authors?" -> GET /autofollow/authors
- "List all tasks?" -> GET /taskmanager/tasks
- "Create a task?" -> POST /taskmanager/tasks
- "Get task details?" -> GET /taskmanager/tasks/{taskid}
- "List all status?" -> GET /taskmanager/tasks/{taskid}/status
- "List all folder?" -> GET /taskmanager/tasks/{taskid}/folder
- "List all result?" -> GET /taskmanager/tasks/{taskid}/result
- "List all result2?" -> GET /taskmanager/tasks/{taskid}/result2
- "List all equity?" -> GET /taskmanager/tasks/{taskid}/equity
- "List all equitypct?" -> GET /taskmanager/tasks/{taskid}/equitypct
- "List all equitypctsm?" -> GET /taskmanager/tasks/{taskid}/equitypctsm
- "List all drawdown?" -> GET /taskmanager/tasks/{taskid}/drawdown
- "List all performance?" -> GET /taskmanager/tasks/{taskid}/performance
- "List all trades?" -> GET /taskmanager/tasks/{taskid}/trades
- "List all contribution?" -> GET /taskmanager/tasks/{taskid}/contribution
- "List all bymonths?" -> GET /taskmanager/tasks/{taskid}/bymonths
- "List all byquarters?" -> GET /taskmanager/tasks/{taskid}/byquarters
- "List all byyears?" -> GET /taskmanager/tasks/{taskid}/byyears
- "List all rules?" -> GET /builder/rules
- "Get rule details?" -> GET /builder/rules/{ruleid}
- "List all markets?" -> GET /marketdata/markets
- "Get market details?" -> GET /marketdata/markets/{name}
- "List all indicators?" -> GET /marketdata/indicators
- "Get indicator details?" -> GET /marketdata/indicators/{name}
- "List all histdata?" -> GET /marketdata/indicators/{name}/histdata
- "List all symbols?" -> GET /marketdata/symbols
- "Get symbol details?" -> GET /marketdata/symbols/{name}
- "List all histdata?" -> GET /marketdata/symbols/{name}/histdata
- "List all snapshot?" -> GET /marketdata/symbols/{name}/snapshot
- "List all snapshots?" -> GET /marketdata/symbols/snapshots
- "List all accounts?" -> GET /cloud/accounts
- "Get account details?" -> GET /cloud/accounts/{accountid}
- "List all orders?" -> GET /cloud/accounts/{accountid}/orders
- "Create a order?" -> POST /cloud/accounts/{accountid}/orders
- "Delete a order?" -> DELETE /cloud/accounts/{accountid}/orders/{orderid}
- "List all trades?" -> GET /cloud/accounts/{accountid}/trades
- "List all snapshots?" -> GET /cloud/accounts/{accountid}/snapshots
- "Create a closeall?" -> POST /cloud/accounts/{accountid}/closeall
- "Create a close?" -> POST /cloud/accounts/{accountid}/close
- "Create a sync?" -> POST /cloud/accounts/{accountid}/sync
- "List all sync?" -> GET /cloud/accounts/{accountid}/sync
- "List all commands?" -> GET /cloud/accounts/{accountid}/commands
- "List all commands?" -> GET /cloud/commands
- "Get command details?" -> GET /cloud/commands/{commandid}
- "List all sessions?" -> GET /cloud/sessions
- "Get session details?" -> GET /cloud/sessions/{sessionid}
- "List all strategies?" -> GET /cloud/strategies
- "Get strategy details?" -> GET /cloud/strategies/{strategyid}
- "Create a start?" -> POST /cloud/strategies/start
- "Create a stop?" -> POST /cloud/strategies/{strategyid}/stop
- "List all connectors?" -> GET /cloud/connectors
- "Get connector details?" -> GET /cloud/connectors/{connectorid}
- "List all connections?" -> GET /cloud/connections
- "Create a connection?" -> POST /cloud/connections
- "Get connection details?" -> GET /cloud/connections/{connectionid}
- "Update a connection?" -> PUT /cloud/connections/{connectionid}
- "Delete a connection?" -> DELETE /cloud/connections/{connectionid}
- "List all balance?" -> GET /marketplace/balance
- "List all products?" -> GET /marketplace/products
- "Get product details?" -> GET /marketplace/products/{productid}
- "List all rates?" -> GET /marketplace/products/{productid}/rates
- "List all groups?" -> GET /marketplace/groups
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
