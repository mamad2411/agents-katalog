---
name: mailboxvalidator-disposable-email-checker
description: "MailboxValidator Disposable Email Checker API skill. Use when working with MailboxValidator Disposable Email Checker for email. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# MailboxValidator Disposable Email Checker
API version: 1.0.0

## Auth
ApiKey key in query

## Base URL
https://virtserver.swaggerhub.com/mailboxvalidator/MailboxValidator-Disposable-Email-Checker/1.0.0

## Setup
1. Set your API key in the appropriate header
2. GET /v1/email/disposable -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### email
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/email/disposable | The Disposable Email Checker API does checking on a single email address and returns if it is from a disposable email provider in either JSON or XML format. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all disposable?" -> GET /v1/email/disposable
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
