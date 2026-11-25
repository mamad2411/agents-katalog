---
name: mailboxvalidator-free-email-checker
description: "MailboxValidator Free Email Checker API skill. Use when working with MailboxValidator Free Email Checker for email. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# MailboxValidator Free Email Checker
API version: 1.0.0

## Auth
ApiKey key in query

## Base URL
https://api.mailboxvalidator.com/

## Setup
1. Set your API key in the appropriate header
2. GET /v1/email/free -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### email
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/email/free | The Free Email Checker API does validation on a single email address and returns if it is from a free email provider in either JSON or XML format. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all free?" -> GET /v1/email/free
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
