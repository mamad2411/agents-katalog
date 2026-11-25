---
name: amazon-workmail-message-flow
description: "Amazon WorkMail Message Flow API skill. Use when working with Amazon WorkMail Message Flow for messages. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon WorkMail Message Flow
API version: 2019-05-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /messages/{messageId} -- verify access
3. POST /messages/{messageId} -- create first messages

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### messages
| Method | Path | Description |
|--------|------|-------------|
| GET | /messages/{messageId} | Retrieves the raw content of an in-transit email message, in MIME format. |
| POST | /messages/{messageId} | Updates the raw content of an in-transit email message, in MIME format. This example describes how to update in-transit email message. For more information and examples for using this API, see  Updating message content with AWS Lambda.  Updates to an in-transit message only appear when you call PutRawMessageContent from an AWS Lambda function configured with a synchronous  Run Lambda rule. If you call PutRawMessageContent on a delivered or sent message, the message remains unchanged, even though GetRawMessageContent returns an updated message. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get message details?" -> GET /messages/{messageId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
