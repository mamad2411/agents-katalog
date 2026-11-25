---
name: adyen-binlookup-api
description: "Adyen BinLookup API skill. Use when working with Adyen BinLookup for get3dsAvailability, getCostEstimate. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Adyen BinLookup API
API version: 54

## Auth
ApiKey X-API-Key in header | Bearer basic

## Base URL
https://pal-test.adyen.com/pal/servlet/BinLookup/v54

## Setup
1. Set Authorization header with your Bearer token
3. POST /get3dsAvailability -- create first get3dsAvailability

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### get3dsAvailability
| Method | Path | Description |
|--------|------|-------------|
| POST | /get3dsAvailability | Check if 3D Secure is available |

### getCostEstimate
| Method | Path | Description |
|--------|------|-------------|
| POST | /getCostEstimate | Get a fees cost estimate |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a get3dsAvailability?" -> POST /get3dsAvailability
- "Create a getCostEstimate?" -> POST /getCostEstimate
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
