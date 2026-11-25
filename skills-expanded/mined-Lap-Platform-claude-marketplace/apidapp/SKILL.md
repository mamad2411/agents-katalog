---
name: apidapp
description: "ApiDapp API skill. Use when working with ApiDapp for root, account, block. Covers 54 endpoints."
version: 1.0.0
generator: lapsh
---

# ApiDapp
API version: 2019-02-14T16:47:01Z

## Auth
ApiKey X-Api-Key in header

## Base URL
https://ethereum.apidapp.com/1

## Setup
1. Set your API key in the appropriate header
2. GET /block -- verify access
3. POST /account -- create first account

## Endpoints

54 endpoints across 11 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| OPTIONS | / |  |

### account
| Method | Path | Description |
|--------|------|-------------|
| POST | /account | Create new account |
| OPTIONS | /account |  |
| GET | /account/{id} | Get account balance |
| OPTIONS | /account/{id} |  |

### block
| Method | Path | Description |
|--------|------|-------------|
| GET | /block | Access detailed block information |
| OPTIONS | /block |  |
| GET | /block/{id} | Get information about particular block |
| OPTIONS | /block/{id} |  |
| GET | /block/{id}/transaction | Get transaction count within block |
| OPTIONS | /block/{id}/transaction |  |
| GET | /block/{id}/transaction/{index} | Get information about particular transaction within block |
| OPTIONS | /block/{id}/transaction/{index} |  |

### blockchain
| Method | Path | Description |
|--------|------|-------------|
| GET | /blockchain | Get a list of supported blockchains |
| OPTIONS | /blockchain |  |
| GET | /blockchain/{id} | Get information about blockchain woth given id |
| OPTIONS | /blockchain/{id} |  |

### contract
| Method | Path | Description |
|--------|------|-------------|
| POST | /contract | Create a new smart contract |
| OPTIONS | /contract |  |
| GET | /contract/{id} | Get contract balance |
| POST | /contract/{id} | Call the contract |
| OPTIONS | /contract/{id} |  |

### echo
| Method | Path | Description |
|--------|------|-------------|
| OPTIONS | /echo |  |

### erc20
| Method | Path | Description |
|--------|------|-------------|
| GET | /erc20 | Get token information such as name, total amount in circulation, etc |
| POST | /erc20 |  |
| OPTIONS | /erc20 |  |
| GET | /erc20/{address} | Get information amout token balance in the account |
| POST | /erc20/{address} | Transfer tokens to another account |
| OPTIONS | /erc20/{address} |  |

### key
| Method | Path | Description |
|--------|------|-------------|
| GET | /key |  |
| POST | /key |  |
| OPTIONS | /key |  |
| DELETE | /key/{key} |  |
| OPTIONS | /key/{key} |  |

### transaction
| Method | Path | Description |
|--------|------|-------------|
| POST | /transaction | Create a new transaction. Transfer Ether between accounts |
| OPTIONS | /transaction |  |
| GET | /transaction/{hash} | Get information about transaction by the transaction hash value |
| OPTIONS | /transaction/{hash} |  |
| GET | /transaction/{hash}/receipt | Get receipt detail information |
| OPTIONS | /transaction/{hash}/receipt |  |

### version
| Method | Path | Description |
|--------|------|-------------|
| GET | /version | Get API version info |
| OPTIONS | /version |  |

### wallet
| Method | Path | Description |
|--------|------|-------------|
| GET | /wallet | Get current account balance |
| POST | /wallet | Create personal wallet |
| OPTIONS | /wallet |  |
| GET | /wallet/account |  |
| POST | /wallet/account |  |
| OPTIONS | /wallet/account |  |
| GET | /wallet/account/{id} | Get account balance |
| OPTIONS | /wallet/account/{id} |  |
| POST | /wallet/account/{id}/contract |  |
| POST | /wallet/account/{id}/erc20 |  |
| POST | /wallet/account/{id}/pay | Send payment from the account held within the wallet |
| OPTIONS | /wallet/account/{id}/pay |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a account?" -> POST /account
- "Get account details?" -> GET /account/{id}
- "List all block?" -> GET /block
- "Get block details?" -> GET /block/{id}
- "List all transaction?" -> GET /block/{id}/transaction
- "Get transaction details?" -> GET /block/{id}/transaction/{index}
- "List all blockchain?" -> GET /blockchain
- "Get blockchain details?" -> GET /blockchain/{id}
- "Create a contract?" -> POST /contract
- "Get contract details?" -> GET /contract/{id}
- "List all erc20?" -> GET /erc20
- "Create a erc20?" -> POST /erc20
- "Get erc20 details?" -> GET /erc20/{address}
- "List all key?" -> GET /key
- "Create a key?" -> POST /key
- "Delete a key?" -> DELETE /key/{key}
- "Create a transaction?" -> POST /transaction
- "Get transaction details?" -> GET /transaction/{hash}
- "List all receipt?" -> GET /transaction/{hash}/receipt
- "List all version?" -> GET /version
- "List all wallet?" -> GET /wallet
- "Create a wallet?" -> POST /wallet
- "List all account?" -> GET /wallet/account
- "Create a account?" -> POST /wallet/account
- "Get account details?" -> GET /wallet/account/{id}
- "Create a contract?" -> POST /wallet/account/{id}/contract
- "Create a erc20?" -> POST /wallet/account/{id}/erc20
- "Create a pay?" -> POST /wallet/account/{id}/pay
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
