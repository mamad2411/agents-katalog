---
name: linqr
description: "LinQR API skill. Use when working with LinQR for qrcode, batch, images. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# LinQR
API version: 2.0

## Auth
OAuth2 | ApiKey X-RapidAPI-Key in header

## Base URL
https://api.linqr.app

## Setup
1. Set your API key in the appropriate header
2. GET /images -- verify access
3. POST /qrcode/text -- create first text

## Endpoints

14 endpoints across 3 groups. See references/api-spec.lap for full details.

### qrcode
| Method | Path | Description |
|--------|------|-------------|
| POST | /qrcode/text | Text QR Code |
| POST | /qrcode/email | Email QR Code |
| POST | /qrcode/wifi | WiFi QR Code |
| POST | /qrcode/contact | Contact QR Code |
| POST | /qrcode/crypto | Cryptocurrency payment QR Code |
| POST | /qrcode/phone | Telephone QR Code |
| POST | /qrcode/sms | SMS QR Code |
| POST | /qrcode/geo | Geolocation QR Code |
| POST | /qrcode | Arbitrary data type QR Code |

### batch
| Method | Path | Description |
|--------|------|-------------|
| POST | /batch/qrcode | QR Code Batch |

### images
| Method | Path | Description |
|--------|------|-------------|
| GET | /images | List all images |
| POST | /images | Upload image |
| DELETE | /images/{id} | Delete image |
| GET | /images/{id} | List image |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a text?" -> POST /qrcode/text
- "Create a email?" -> POST /qrcode/email
- "Create a wifi?" -> POST /qrcode/wifi
- "Create a contact?" -> POST /qrcode/contact
- "Create a crypto?" -> POST /qrcode/crypto
- "Create a phone?" -> POST /qrcode/phone
- "Create a sm?" -> POST /qrcode/sms
- "Create a geo?" -> POST /qrcode/geo
- "Create a qrcode?" -> POST /qrcode
- "Create a qrcode?" -> POST /batch/qrcode
- "List all images?" -> GET /images
- "Create a image?" -> POST /images
- "Delete a image?" -> DELETE /images/{id}
- "Get image details?" -> GET /images/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
