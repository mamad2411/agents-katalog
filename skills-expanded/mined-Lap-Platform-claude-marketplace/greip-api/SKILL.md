---
name: greip-api
description: "Greip API skill. Use when working with Greip for geoip, lookup, scoring. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# Greip API
API version: 1.2.0

## Auth
Bearer bearer | ApiKey key in query

## Base URL
https://greipapi.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /geoip -- verify access
3. POST /scoring/payment -- create first payment

## Endpoints

14 endpoints across 5 groups. See references/api-spec.lap for full details.

### geoip
| Method | Path | Description |
|--------|------|-------------|
| GET | /geoip | Retrieve detailed geolocation information for a visitor’s or user’s IP address |

### lookup
| Method | Path | Description |
|--------|------|-------------|
| GET | /lookup/ip | Get the full information of a given IP address |
| GET | /lookup/ip/threats | Retrieve threat intelligence information for a given IP address |
| GET | /lookup/ip/bulk | Get the full information of multiple IP Addresses |
| GET | /lookup/asn | Lookup any AS Number and receive it's details |
| GET | /lookup/bin | Get the complete data associated with a debit/credit card |
| GET | /lookup/iban | Validate International IBANs and obtain essential information |
| GET | /lookup/country | Get the full information of a country |

### scoring
| Method | Path | Description |
|--------|------|-------------|
| POST | /scoring/payment | Prevent financial losses by deploying AI-Powered modules |
| GET | /scoring/email | Validate email addresses and retrieve additional information |
| GET | /scoring/phone | Validate phone numbers and retrieve additional information |
| GET | /scoring/profanity | Detect profanity in a given text |

### ip
| Method | Path | Description |
|--------|------|-------------|
| GET | /ip | Retrieve the IP address of your visitors or users without the need for an account or API key in Greip |

### account
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /account/users/delete | Request to delete your user data from Greip |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all geoip?" -> GET /geoip
- "List all ip?" -> GET /lookup/ip
- "List all threats?" -> GET /lookup/ip/threats
- "List all bulk?" -> GET /lookup/ip/bulk
- "List all asn?" -> GET /lookup/asn
- "List all bin?" -> GET /lookup/bin
- "Create a payment?" -> POST /scoring/payment
- "List all iban?" -> GET /lookup/iban
- "List all email?" -> GET /scoring/email
- "List all phone?" -> GET /scoring/phone
- "List all country?" -> GET /lookup/country
- "List all profanity?" -> GET /scoring/profanity
- "List all ip?" -> GET /ip
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
