---
name: poemist-api
description: "Poemist API skill. Use when working with Poemist for randompoems. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Poemist API
API version: 1.0

## Auth
No authentication required.

## Base URL
https://www.poemist.com/api/v1/

## Setup
1. No auth setup needed
2. GET /randompoems -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### randompoems
| Method | Path | Description |
|--------|------|-------------|
| GET | /randompoems |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all randompoems?" -> GET /randompoems

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
