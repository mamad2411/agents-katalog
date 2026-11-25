---
name: tokenjay-api-services
description: "TokenJay API services API skill. Use when working with TokenJay API services for payment, mosaik, tokens. Covers 27 endpoints."
version: 1.0.0
generator: lapsh
---

# TokenJay API services

## Auth
No authentication required.

## Base URL
https://api.tokenjay.app/

## Setup
1. No auth setup needed
2. GET /tokens/prices/all -- verify access
3. POST /payment/addrequest -- create first addrequest

## Endpoints

27 endpoints across 9 groups. See references/api-spec.lap for full details.

### payment
| Method | Path | Description |
|--------|------|-------------|
| POST | /payment/addrequest | Creates a new payment request. Will return request id to check for transaction state and ergopay url to show the user as QR code |
| GET | /payment/state/{requestId} | Returns the state of a payment request. Please note that payment requests are purged after some time, so persist the state at your side when needed |

### mosaik
| Method | Path | Description |
|--------|------|-------------|
| POST | /mosaik/tokenburn/prepare |  |
| POST | /mosaik/babelfee/newoffer/new-input |  |
| POST | /mosaik/babelfee/newoffer/doit |  |
| GET | /mosaik/tokenburn |  |
| GET | /mosaik/tokenburn/get/{uuid} |  |
| GET | /mosaik/boxconsolidation/consolidate/{p2pkaddress} |  |
| GET | /mosaik/boxconsolidation/ |  |
| GET | /mosaik/babelfee/notificationcheck |  |
| GET | /mosaik/babelfee/newoffer |  |
| GET | /mosaik/babelfee/ |  |

### tokens
| Method | Path | Description |
|--------|------|-------------|
| GET | /tokens/prices/{tokenId} | Lists price and available volume for a certain token |
| GET | /tokens/prices/all | Lists all token prices and available volume |
| GET | /tokens/listGenuine | Lists all genuine tokens known |
| GET | /tokens/listBlocked | Lists all blocked tokens |
| GET | /tokens/check/{tokenId}/{tokenName} | Check a token verification |

### sigusd
| Method | Path | Description |
|--------|------|-------------|
| GET | /sigusd/price | Lists price and available volume for SigmaUSD |
| GET | /sigusd/exchange/{amount}/info | Calculates SigUSD exchange |
| GET | /sigusd/exchange/ | Builds ErgoPayRequest for SigUSD exchange |

### sigrsv
| Method | Path | Description |
|--------|------|-------------|
| GET | /sigrsv/price | Lists price and available volume for SigmaRSV |
| GET | /sigrsv/exchange/{amount}/info | Calculates SigRSV exchange |
| GET | /sigrsv/exchange/ | Builds ErgoPayRequest for SigRSV exchange |

### peers
| Method | Path | Description |
|--------|------|-------------|
| GET | /peers/list | Lists known peers sorted by block height |

### createbabel
| Method | Path | Description |
|--------|------|-------------|
| GET | /createbabel/{address} |  |

### cancelbabel
| Method | Path | Description |
|--------|------|-------------|
| GET | /cancelbabel/{boxId} |  |

### ageusd
| Method | Path | Description |
|--------|------|-------------|
| GET | /ageusd/info | Returns state of AgeUSD at this moment |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a addrequest?" -> POST /payment/addrequest
- "Create a prepare?" -> POST /mosaik/tokenburn/prepare
- "Create a new-input?" -> POST /mosaik/babelfee/newoffer/new-input
- "Create a doit?" -> POST /mosaik/babelfee/newoffer/doit
- "Get price details?" -> GET /tokens/prices/{tokenId}
- "List all all?" -> GET /tokens/prices/all
- "List all listGenuine?" -> GET /tokens/listGenuine
- "List all listBlocked?" -> GET /tokens/listBlocked
- "Get check details?" -> GET /tokens/check/{tokenId}/{tokenName}
- "List all price?" -> GET /sigusd/price
- "List all info?" -> GET /sigusd/exchange/{amount}/info
- "List all exchange?" -> GET /sigusd/exchange/
- "List all price?" -> GET /sigrsv/price
- "List all info?" -> GET /sigrsv/exchange/{amount}/info
- "List all exchange?" -> GET /sigrsv/exchange/
- "List all list?" -> GET /peers/list
- "Get state details?" -> GET /payment/state/{requestId}
- "List all tokenburn?" -> GET /mosaik/tokenburn
- "Get get details?" -> GET /mosaik/tokenburn/get/{uuid}
- "Get consolidate details?" -> GET /mosaik/boxconsolidation/consolidate/{p2pkaddress}
- "List all boxconsolidation?" -> GET /mosaik/boxconsolidation/
- "List all notificationcheck?" -> GET /mosaik/babelfee/notificationcheck
- "List all newoffer?" -> GET /mosaik/babelfee/newoffer
- "List all babelfee?" -> GET /mosaik/babelfee/
- "Get createbabel details?" -> GET /createbabel/{address}
- "Get cancelbabel details?" -> GET /cancelbabel/{boxId}
- "List all info?" -> GET /ageusd/info

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
