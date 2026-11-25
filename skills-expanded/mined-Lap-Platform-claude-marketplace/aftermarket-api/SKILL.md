---
name: aftermarket-api
description: "Aftermarket API skill. Use when working with Aftermarket for customers, aftermarket. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Aftermarket API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /v1/customers/{customerId}/auctions/listings -- verify access
3. POST /v1/aftermarket/listings/expiry -- create first expiry

## Endpoints

3 endpoints across 2 groups. See references/api-spec.lap for full details.

### customers
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/customers/{customerId}/auctions/listings | Get listings from GoDaddy Auctions |

### aftermarket
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /v1/aftermarket/listings | Remove listings from GoDaddy Auction |
| POST | /v1/aftermarket/listings/expiry | Add expiry listings into GoDaddy Auction |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all listings?" -> GET /v1/customers/{customerId}/auctions/listings
- "Create a expiry?" -> POST /v1/aftermarket/listings/expiry

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
