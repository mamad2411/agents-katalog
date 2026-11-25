---
name: who-hosts-this-api
description: "Who Hosts This API skill. Use when working with Who Hosts This for Detect, Status. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Who Hosts This API
API version: 0.0.1

## Auth
ApiKey key in query

## Base URL
https://www.who-hosts-this.com/APIEndpoint

## Setup
1. Set your API key in the appropriate header
2. GET /Detect -- verify access

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### Detect
| Method | Path | Description |
|--------|------|-------------|
| GET | /Detect | Discover the hosting provider for a web site |

### Status
| Method | Path | Description |
|--------|------|-------------|
| GET | /Status | View usage details for the current billing period |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all Detect?" -> GET /Detect
- "List all Status?" -> GET /Status
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
