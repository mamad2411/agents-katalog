---
name: randommer-api
description: "Randommer API skill. Use when working with Randommer for api. Covers 25 endpoints."
version: 1.0.0
generator: lapsh
---

# Randommer API
API version: v1

## Auth
ApiKey X-Api-Key in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /api/Card -- verify access
3. POST /api/Finance/Vat/Validator -- create first Validator

## Endpoints

25 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/Card | Get Card |
| GET | /api/Card/Types | Get available card types |
| GET | /api/Finance/CryptoAddress/Types | Get available crypto types |
| GET | /api/Finance/CryptoAddress | Get crypto address |
| GET | /api/Finance/Iban/{countryCode} | Get IBAN by countryCode |
| GET | /api/Finance/Countries | Get available countries |
| POST | /api/Finance/Vat/Validator |  |
| GET | /api/Misc/Cultures |  |
| GET | /api/Misc/Random-Address |  |
| GET | /api/Name | Get name |
| GET | /api/Name/Suggestions | Get business name suggestions |
| GET | /api/Name/Cultures | Get available cultures |
| POST | /api/Name/BusinessName | Get business names for a specific culture |
| POST | /api/Name/BrandName | Generate brand name suggestions |
| GET | /api/Phone/Generate | Get bulk telephone numbers for a country |
| GET | /api/Phone/IMEI | Get bulk imeis |
| GET | /api/Phone/Validate | Validate a phone number |
| GET | /api/Phone/Countries | Get available countries |
| GET | /api/SocialNumber | Generate a social security number |
| POST | /api/SocialNumber | Validate VAT/identity numbers |
| GET | /api/Text/LoremIpsum | Generate lorem ipsum |
| GET | /api/Text/Password | Generate password |
| POST | /api/Text/Humanize | Humanize text |
| POST | /api/Text/Transform | Transform text |
| POST | /api/Text/Review | Get reviews (max quantity=500) |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all Card?" -> GET /api/Card
- "List all Types?" -> GET /api/Card/Types
- "List all Types?" -> GET /api/Finance/CryptoAddress/Types
- "List all CryptoAddress?" -> GET /api/Finance/CryptoAddress
- "Get Iban details?" -> GET /api/Finance/Iban/{countryCode}
- "List all Countries?" -> GET /api/Finance/Countries
- "Create a Validator?" -> POST /api/Finance/Vat/Validator
- "List all Cultures?" -> GET /api/Misc/Cultures
- "List all Random-Address?" -> GET /api/Misc/Random-Address
- "List all Name?" -> GET /api/Name
- "List all Suggestions?" -> GET /api/Name/Suggestions
- "List all Cultures?" -> GET /api/Name/Cultures
- "Create a BusinessName?" -> POST /api/Name/BusinessName
- "Create a BrandName?" -> POST /api/Name/BrandName
- "List all Generate?" -> GET /api/Phone/Generate
- "List all IMEI?" -> GET /api/Phone/IMEI
- "List all Validate?" -> GET /api/Phone/Validate
- "List all Countries?" -> GET /api/Phone/Countries
- "List all SocialNumber?" -> GET /api/SocialNumber
- "Create a SocialNumber?" -> POST /api/SocialNumber
- "List all LoremIpsum?" -> GET /api/Text/LoremIpsum
- "List all Password?" -> GET /api/Text/Password
- "Create a Humanize?" -> POST /api/Text/Humanize
- "Create a Transform?" -> POST /api/Text/Transform
- "Create a Review?" -> POST /api/Text/Review
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
