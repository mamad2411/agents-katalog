---
name: most-popular-api
description: "Most Popular API skill. Use when working with Most Popular for mostshared, mostemailed, mostviewed. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Most Popular API
API version: 2.0.0

## Auth
ApiKey api-key in query

## Base URL
http://api.nytimes.com/svc/mostpopular/v2

## Setup
1. Set your API key in the appropriate header
2. GET /mostshared/{section}/{time-period}.json -- verify access

## Endpoints

3 endpoints across 3 groups. See references/api-spec.lap for full details.

### mostshared
| Method | Path | Description |
|--------|------|-------------|
| GET | /mostshared/{section}/{time-period}.json | Most Shared by Section & Time Period |

### mostemailed
| Method | Path | Description |
|--------|------|-------------|
| GET | /mostemailed/{section}/{time-period}.json | Most Emailed by Section & Time Period |

### mostviewed
| Method | Path | Description |
|--------|------|-------------|
| GET | /mostviewed/{section}/{time-period}.json | Most Viewed by Section & Time Period |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get mostshared details?" -> GET /mostshared/{section}/{time-period}.json
- "Get mostemailed details?" -> GET /mostemailed/{section}/{time-period}.json
- "Get mostviewed details?" -> GET /mostviewed/{section}/{time-period}.json
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
