---
name: ipqualityscore-api
description: "IPQualityScore API skill. Use when working with IPQualityScore for json. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# IPQualityScore API

## Auth
Basic username:password

## Base URL
https://ipqualityscore.com/api

## Setup
1. Configure auth: Basic username:password
2. GET /json/email/{YOUR_API_KEY_HERE}/{USER_EMAIL_HERE} -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### json
| Method | Path | Description |
|--------|------|-------------|
| GET | /json/email/{YOUR_API_KEY_HERE}/{USER_EMAIL_HERE} | Email Validation |
| GET | /json/phone/{YOUR_API_KEY_HERE}/{USER_PHONE_HERE} | Phone Validation |
| GET | /json/url/{YOUR_API_KEY_HERE}/{URL_HERE} | Malicious URL Scanner |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get email details?" -> GET /json/email/{YOUR_API_KEY_HERE}/{USER_EMAIL_HERE}
- "Get phone details?" -> GET /json/phone/{YOUR_API_KEY_HERE}/{USER_PHONE_HERE}
- "Get url details?" -> GET /json/url/{YOUR_API_KEY_HERE}/{URL_HERE}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
