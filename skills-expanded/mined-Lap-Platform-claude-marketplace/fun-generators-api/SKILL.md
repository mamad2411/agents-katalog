---
name: fun-generators-api
description: "Fun Generators API skill. Use when working with Fun Generators for qrcode. Covers 9 endpoints."
version: 1.0.0
generator: lapsh
---

# Fun Generators API
API version: 1.5

## Auth
ApiKey X-Fungenerators-Api-Secret in header

## Base URL
https://api.fungenerators.com

## Setup
1. Set your API key in the appropriate header
2. GET /qrcode/text -- verify access
3. POST /qrcode/decode -- create first decode

## Endpoints

9 endpoints across 1 groups. See references/api-spec.lap for full details.

### qrcode
| Method | Path | Description |
|--------|------|-------------|
| GET | /qrcode/text | Get a QR Code image for a block of text |
| GET | /qrcode/raw | Get a QR Code image for a block of raw data |
| GET | /qrcode/url | Get a QR Code image for a url |
| GET | /qrcode/phone | Get a QR Code image for a phone number |
| GET | /qrcode/sms | Get a QR Code image for a Phone number for SMS messaging |
| GET | /qrcode/skype | Get a QR Code image for a skype user |
| GET | /qrcode/email | Get a QR Code image for an email |
| GET | /qrcode/business_card | Get a QR Code image for a business card aka VCARD |
| POST | /qrcode/decode | Decode a QR Code image and return the cotents if successful |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all text?" -> GET /qrcode/text
- "List all raw?" -> GET /qrcode/raw
- "List all url?" -> GET /qrcode/url
- "List all phone?" -> GET /qrcode/phone
- "List all sms?" -> GET /qrcode/sms
- "List all skype?" -> GET /qrcode/skype
- "List all email?" -> GET /qrcode/email
- "List all business_card?" -> GET /qrcode/business_card
- "Create a decode?" -> POST /qrcode/decode
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
