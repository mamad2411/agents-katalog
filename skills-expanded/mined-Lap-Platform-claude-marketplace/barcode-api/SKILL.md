---
name: barcode-api
description: "Barcode API skill. Use when working with Barcode for barcode. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Barcode API
API version: 1.5

## Auth
Bearer bearer

## Base URL
http://api.fungenerators.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /barcode/encode/types -- verify access
3. POST /barcode/decode -- create first decode

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### barcode
| Method | Path | Description |
|--------|------|-------------|
| GET | /barcode/encode/types | Get the supported barcode types for encoding / image generation. |
| GET | /barcode/encode | Get a Bar Code image for the given barcode number |
| GET | /barcode/decode/types | Get the supported barcode types for the decoding process. |
| POST | /barcode/decode | Decode a Barcode image and return the cotents if successful |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all types?" -> GET /barcode/encode/types
- "List all encode?" -> GET /barcode/encode
- "List all types?" -> GET /barcode/decode/types
- "Create a decode?" -> POST /barcode/decode
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
