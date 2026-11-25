---
name: twilio-sendgrid-mail-api
description: "Twilio SendGrid Mail API skill. Use when working with Twilio SendGrid Mail for mail. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio SendGrid Mail API
API version: 1.0.0

## Auth
Bearer bearer

## Base URL
https://api.sendgrid.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v3/mail/batch/{batch_id} -- verify access
3. POST /v3/mail/batch -- create first batch

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### mail
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/mail/batch | Create a batch ID. |
| GET | /v3/mail/batch/{batch_id} | Validate a batch ID. |
| POST | /v3/mail/send | Send Email with Twilio SendGrid. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a batch?" -> POST /v3/mail/batch
- "Get batch details?" -> GET /v3/mail/batch/{batch_id}
- "Create a send?" -> POST /v3/mail/send
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
