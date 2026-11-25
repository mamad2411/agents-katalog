---
name: house-of-commons-oral-and-written-questions-api
description: "House of Commons Oral and Written Questions API skill. Use when working with House of Commons Oral and Written Questions for EarlyDayMotion, EarlyDayMotions, oralquestions. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# House of Commons Oral and Written Questions API
API version: v1

## Auth
No authentication required.

## Base URL
http://oralquestionsandmotions-api.parliament.uk

## Setup
1. No auth setup needed
2. GET /EarlyDayMotions/list -- verify access

## Endpoints

4 endpoints across 4 groups. See references/api-spec.lap for full details.

### EarlyDayMotion
| Method | Path | Description |
|--------|------|-------------|
| GET | /EarlyDayMotion/{id} | Returns a single Early Day Motion by ID |

### EarlyDayMotions
| Method | Path | Description |
|--------|------|-------------|
| GET | /EarlyDayMotions/list | Returns a list of Early Day Motions |

### oralquestions
| Method | Path | Description |
|--------|------|-------------|
| GET | /oralquestions/list | Returns a list of oral questions |

### oralquestiontimes
| Method | Path | Description |
|--------|------|-------------|
| GET | /oralquestiontimes/list | Returns a list of oral question times |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get EarlyDayMotion details?" -> GET /EarlyDayMotion/{id}
- "List all list?" -> GET /EarlyDayMotions/list
- "List all list?" -> GET /oralquestions/list
- "List all list?" -> GET /oralquestiontimes/list

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
