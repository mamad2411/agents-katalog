---
name: adyen-balance-control-api
description: "Adyen Balance Control API skill. Use when working with Adyen Balance Control for balanceTransfer. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Adyen Balance Control API
API version: 1

## Auth
ApiKey X-API-Key in header | Bearer basic

## Base URL
https://pal-test.adyen.com/pal/servlet/BalanceControl/v1

## Setup
1. Set Authorization header with your Bearer token
3. POST /balanceTransfer -- create first balanceTransfer

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### balanceTransfer
| Method | Path | Description |
|--------|------|-------------|
| POST | /balanceTransfer | Start a balance transfer |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a balanceTransfer?" -> POST /balanceTransfer
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
