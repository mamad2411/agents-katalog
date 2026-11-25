---
name: written-questions-service-api
description: "Written Questions Service API skill. Use when working with Written Questions Service for api. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Written Questions Service API
API version: v1

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /api/dailyreports/dailyreports -- verify access

## Endpoints

7 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/dailyreports/dailyreports | Returns a list of daily reports |
| GET | /api/writtenquestions/questions | Returns a list of written questions |
| GET | /api/writtenquestions/questions/{id} | Returns a written question |
| GET | /api/writtenquestions/questions/{date}/{uin} | Returns a written question |
| GET | /api/writtenstatements/statements | Returns a list of written statements |
| GET | /api/writtenstatements/statements/{id} | Returns a written statement |
| GET | /api/writtenstatements/statements/{date}/{uin} | Returns a written statemnet |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all dailyreports?" -> GET /api/dailyreports/dailyreports
- "List all questions?" -> GET /api/writtenquestions/questions
- "Get question details?" -> GET /api/writtenquestions/questions/{id}
- "Get question details?" -> GET /api/writtenquestions/questions/{date}/{uin}
- "List all statements?" -> GET /api/writtenstatements/statements
- "Get statement details?" -> GET /api/writtenstatements/statements/{id}
- "Get statement details?" -> GET /api/writtenstatements/statements/{date}/{uin}

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
