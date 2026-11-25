---
name: mailboxvalidator-email-validation
description: "MailboxValidator Email Validation API skill. Use when working with MailboxValidator Email Validation for validation. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# MailboxValidator Email Validation
API version: 0.1

## Auth
ApiKey key in query

## Base URL
https://api.mailboxvalidator.com

## Setup
1. Set your API key in the appropriate header
2. GET /v1/validation/single -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### validation
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/validation/single | The Single Validation API does validation on a single email address and returns all the validation results in either JSON or XML format. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all single?" -> GET /v1/validation/single
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
