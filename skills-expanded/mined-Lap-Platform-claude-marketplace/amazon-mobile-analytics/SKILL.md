---
name: amazon-mobile-analytics
description: "Amazon Mobile Analytics API skill. Use when working with Amazon Mobile Analytics for 2014-06-05. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Amazon Mobile Analytics
API version: 2014-06-05

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /2014-06-05/events -- create first events

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### 2014-06-05
| Method | Path | Description |
|--------|------|-------------|
| POST | /2014-06-05/events | The PutEvents operation records one or more events. You can have up to 1,500 unique custom events per app, any combination of up to 40 attributes and metrics per custom event, and any number of attribute or metric values. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a event?" -> POST /2014-06-05/events
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object
- Error responses use types: BadRequestException

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
