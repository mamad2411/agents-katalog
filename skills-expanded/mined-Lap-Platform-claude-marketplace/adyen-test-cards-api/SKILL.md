---
name: adyen-test-cards-api
description: "Adyen Test Cards API skill. Use when working with Adyen Test Cards for createTestCardRanges. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Adyen Test Cards API
API version: 1

## Auth
ApiKey X-API-Key in header | Bearer basic

## Base URL
https://pal-test.adyen.com/pal/services/TestCard/v1

## Setup
1. Set Authorization header with your Bearer token
3. POST /createTestCardRanges -- create first createTestCardRanges

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### createTestCardRanges
| Method | Path | Description |
|--------|------|-------------|
| POST | /createTestCardRanges | Creates one or more test card ranges. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a createTestCardRange?" -> POST /createTestCardRanges
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
