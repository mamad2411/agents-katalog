---
name: emailverify
description: "EmailVerify API skill. Use when working with EmailVerify for sendCode, checkCode. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# EmailVerify
API version: 1.0.0

## Auth
Bearer bearer

## Base URL
https://ev.apis.paypi.dev

## Setup
1. Set Authorization header with your Bearer token
3. POST /sendCode -- create first sendCode

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### sendCode
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendCode | Send verification code |

### checkCode
| Method | Path | Description |
|--------|------|-------------|
| POST | /checkCode | Check verification code |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a sendCode?" -> POST /sendCode
- "Create a checkCode?" -> POST /checkCode
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
