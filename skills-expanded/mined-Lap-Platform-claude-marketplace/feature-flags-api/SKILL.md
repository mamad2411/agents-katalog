---
name: feature-flags-api
description: "Feature Flags API skill. Use when working with Feature Flags for flags. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Feature Flags API
API version: 1.0.0

## Auth
Requires API key (token parameter)

## Base URL
Not specified.

## Setup
1. Include your API key via the token parameter
2. GET /flags -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### flags
| Method | Path | Description |
|--------|------|-------------|
| GET | /flags | Evaluate Feature Flags (GET) |
| GET | /flags/definitions | Get Feature Flag Definitions |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all flags?" -> GET /flags
- "List all definitions?" -> GET /flags/definitions

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
