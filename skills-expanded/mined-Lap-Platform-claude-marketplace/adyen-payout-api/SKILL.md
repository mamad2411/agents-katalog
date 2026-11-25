---
name: adyen-payout-api
description: "Adyen Payout API skill. Use when working with Adyen Payout for confirmThirdParty, declineThirdParty, payout. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Adyen Payout API
API version: 68

## Auth
ApiKey X-API-Key in header | Bearer basic

## Base URL
https://pal-test.adyen.com/pal/servlet/Payout/v68

## Setup
1. Set Authorization header with your Bearer token
3. POST /confirmThirdParty -- create first confirmThirdParty

## Endpoints

6 endpoints across 6 groups. See references/api-spec.lap for full details.

### confirmThirdParty
| Method | Path | Description |
|--------|------|-------------|
| POST | /confirmThirdParty | Confirm a payout |

### declineThirdParty
| Method | Path | Description |
|--------|------|-------------|
| POST | /declineThirdParty | Cancel a payout |

### payout
| Method | Path | Description |
|--------|------|-------------|
| POST | /payout | Make an instant card payout |

### storeDetail
| Method | Path | Description |
|--------|------|-------------|
| POST | /storeDetail | Store payout details |

### storeDetailAndSubmitThirdParty
| Method | Path | Description |
|--------|------|-------------|
| POST | /storeDetailAndSubmitThirdParty | Store details and submit a payout |

### submitThirdParty
| Method | Path | Description |
|--------|------|-------------|
| POST | /submitThirdParty | Submit a payout |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a confirmThirdParty?" -> POST /confirmThirdParty
- "Create a declineThirdParty?" -> POST /declineThirdParty
- "Create a payout?" -> POST /payout
- "Create a storeDetail?" -> POST /storeDetail
- "Create a storeDetailAndSubmitThirdParty?" -> POST /storeDetailAndSubmitThirdParty
- "Create a submitThirdParty?" -> POST /submitThirdParty
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
