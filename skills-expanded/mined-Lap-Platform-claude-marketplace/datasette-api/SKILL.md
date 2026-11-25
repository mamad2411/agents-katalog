---
name: datasette-api
description: "Datasette API skill. Use when working with Datasette for content.json. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Datasette API
API version: v1

## Auth
No authentication required.

## Base URL
https://datasette.io

## Setup
1. No auth setup needed
2. GET /content.json -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### content.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /content.json | Execute a SQLite SQL query against the content database |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all content.json?" -> GET /content.json

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
