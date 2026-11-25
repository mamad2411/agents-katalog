---
name: neblio-rest-api-suite
description: "Neblio REST API Suite API skill. Use when working with Neblio REST API Suite for ntp1, ins, testnet. Covers 50 endpoints."
version: 1.0.0
generator: lapsh
---

# Neblio REST API Suite
API version: 1.3.0

## Auth
Bearer basic

## Base URL
https://ntp1node.nebl.io/

## Setup
1. Set Authorization header with your Bearer token
2. GET /ins/txs -- verify access
3. POST /ntp1/broadcast -- create first broadcast

## Endpoints

50 endpoints across 4 groups. See references/api-spec.lap for full details.

### ntp1
| Method | Path | Description |
|--------|------|-------------|
| GET | /ntp1/tokenid/{tokensymbol} | Returns the tokenId representing a token |
| POST | /ntp1/broadcast | Broadcasts a signed raw transaction to the network |
| GET | /ntp1/addressinfo/{address} | Information On a Neblio Address |
| GET | /ntp1/transactioninfo/{txid} | Information On an NTP1 Transaction |
| GET | /ntp1/tokenmetadata/{tokenid} | Get Metadata of Token |
| GET | /ntp1/tokenmetadata/{tokenid}/{utxo} | Get UTXO Metadata of Token |
| GET | /ntp1/stakeholders/{tokenid} | Get Addresses Holding a Token |
| POST | /ntp1/issue | Builds a transaction that issues a new NTP1 Token |
| POST | /ntp1/sendtoken | Builds a transaction that sends an NTP1 Token |
| POST | /ntp1/burntoken | Builds a transaction that burns an NTP1 Token |

### ins
| Method | Path | Description |
|--------|------|-------------|
| POST | /ins/tx/send | Broadcasts a signed raw transaction to the network (not NTP1 specific) |
| GET | /ins/block/{blockhash} | Returns information regarding a Neblio block |
| GET | /ins/block-index/{blockindex} | Returns block hash of block |
| GET | /ins/tx/{txid} | Returns transaction object |
| GET | /ins/rawtx/{txid} | Returns raw transaction hex |
| GET | /ins/addr/{address} | Returns address object |
| GET | /ins/addr/{address}/balance | Returns address balance in sats |
| GET | /ins/addr/{address}/unconfirmedBalance | Returns address unconfirmed balance in sats |
| GET | /ins/addr/{address}/totalReceived | Returns total received by address in sats |
| GET | /ins/addr/{address}/utxo | Returns all UTXOs at a given address |
| GET | /ins/addr/{address}/totalSent | Returns total sent by address in sats |
| GET | /ins/txs | Get transactions by block or address |
| GET | /ins/sync | Get node sync status |
| GET | /ins/status | Utility API for calling several blockchain node functions |

### testnet
| Method | Path | Description |
|--------|------|-------------|
| POST | /testnet/ins/tx/send | Broadcasts a signed raw transaction to the network (not NTP1 specific) |
| GET | /testnet/ins/block/{blockhash} | Returns information regarding a Neblio block |
| GET | /testnet/ins/block-index/{blockindex} | Returns block hash of block |
| GET | /testnet/ins/tx/{txid} | Returns transaction object |
| GET | /testnet/ins/rawtx/{txid} | Returns raw transaction hex |
| GET | /testnet/ins/addr/{address} | Returns address object |
| GET | /testnet/ins/addr/{address}/balance | Returns address balance in sats |
| GET | /testnet/ins/addr/{address}/unconfirmedBalance | Returns address unconfirmed balance in sats |
| GET | /testnet/ins/addr/{address}/totalReceived | Returns total received by address in sats |
| GET | /testnet/ins/addr/{address}/utxo | Returns all UTXOs at a given address |
| GET | /testnet/ins/addr/{address}/totalSent | Returns total sent by address in sats |
| GET | /testnet/ins/txs | Get transactions by block or address |
| GET | /testnet/ins/sync | Get node sync status |
| GET | /testnet/ins/status | Utility API for calling several blockchain node functions |
| GET | /testnet/ntp1/tokenid/{tokensymbol} | Returns the tokenId representing a token |
| POST | /testnet/ntp1/broadcast | Broadcasts a signed raw transaction to the network |
| GET | /testnet/ntp1/addressinfo/{address} | Information On a Neblio Address |
| GET | /testnet/ntp1/transactioninfo/{txid} | Information On an NTP1 Transaction |
| GET | /testnet/ntp1/tokenmetadata/{tokenid} | Get Metadata of Token |
| GET | /testnet/ntp1/tokenmetadata/{tokenid}/{utxo} | Get UTXO Metadata of Token |
| GET | /testnet/ntp1/stakeholders/{tokenid} | Get Addresses Holding a Token |
| POST | /testnet/ntp1/issue | Builds a transaction that issues a new NTP1 Token |
| POST | /testnet/ntp1/sendtoken | Builds a transaction that sends an NTP1 Token |
| POST | /testnet/ntp1/burntoken | Builds a transaction that burns an NTP1 Token |
| GET | /testnet/faucet | Withdraws testnet NEBL to the specified address |

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Send a JSON-RPC call to a localhost neblio-Qt or nebliod node |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get tokenid details?" -> GET /ntp1/tokenid/{tokensymbol}
- "Create a broadcast?" -> POST /ntp1/broadcast
- "Get addressinfo details?" -> GET /ntp1/addressinfo/{address}
- "Get transactioninfo details?" -> GET /ntp1/transactioninfo/{txid}
- "Get tokenmetadata details?" -> GET /ntp1/tokenmetadata/{tokenid}
- "Get tokenmetadata details?" -> GET /ntp1/tokenmetadata/{tokenid}/{utxo}
- "Get stakeholder details?" -> GET /ntp1/stakeholders/{tokenid}
- "Create a issue?" -> POST /ntp1/issue
- "Create a sendtoken?" -> POST /ntp1/sendtoken
- "Create a burntoken?" -> POST /ntp1/burntoken
- "Create a send?" -> POST /ins/tx/send
- "Get block details?" -> GET /ins/block/{blockhash}
- "Get block-index details?" -> GET /ins/block-index/{blockindex}
- "Get tx details?" -> GET /ins/tx/{txid}
- "Get rawtx details?" -> GET /ins/rawtx/{txid}
- "Get addr details?" -> GET /ins/addr/{address}
- "List all balance?" -> GET /ins/addr/{address}/balance
- "List all unconfirmedBalance?" -> GET /ins/addr/{address}/unconfirmedBalance
- "List all totalReceived?" -> GET /ins/addr/{address}/totalReceived
- "List all utxo?" -> GET /ins/addr/{address}/utxo
- "List all totalSent?" -> GET /ins/addr/{address}/totalSent
- "List all txs?" -> GET /ins/txs
- "List all sync?" -> GET /ins/sync
- "Search status?" -> GET /ins/status
- "Create a send?" -> POST /testnet/ins/tx/send
- "Get block details?" -> GET /testnet/ins/block/{blockhash}
- "Get block-index details?" -> GET /testnet/ins/block-index/{blockindex}
- "Get tx details?" -> GET /testnet/ins/tx/{txid}
- "Get rawtx details?" -> GET /testnet/ins/rawtx/{txid}
- "Get addr details?" -> GET /testnet/ins/addr/{address}
- "List all balance?" -> GET /testnet/ins/addr/{address}/balance
- "List all unconfirmedBalance?" -> GET /testnet/ins/addr/{address}/unconfirmedBalance
- "List all totalReceived?" -> GET /testnet/ins/addr/{address}/totalReceived
- "List all utxo?" -> GET /testnet/ins/addr/{address}/utxo
- "List all totalSent?" -> GET /testnet/ins/addr/{address}/totalSent
- "List all txs?" -> GET /testnet/ins/txs
- "List all sync?" -> GET /testnet/ins/sync
- "Search status?" -> GET /testnet/ins/status
- "Get tokenid details?" -> GET /testnet/ntp1/tokenid/{tokensymbol}
- "Create a broadcast?" -> POST /testnet/ntp1/broadcast
- "Get addressinfo details?" -> GET /testnet/ntp1/addressinfo/{address}
- "Get transactioninfo details?" -> GET /testnet/ntp1/transactioninfo/{txid}
- "Get tokenmetadata details?" -> GET /testnet/ntp1/tokenmetadata/{tokenid}
- "Get tokenmetadata details?" -> GET /testnet/ntp1/tokenmetadata/{tokenid}/{utxo}
- "Get stakeholder details?" -> GET /testnet/ntp1/stakeholders/{tokenid}
- "Create a issue?" -> POST /testnet/ntp1/issue
- "Create a sendtoken?" -> POST /testnet/ntp1/sendtoken
- "Create a burntoken?" -> POST /testnet/ntp1/burntoken
- "List all faucet?" -> GET /testnet/faucet
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
