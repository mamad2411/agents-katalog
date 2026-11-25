---
name: xero-bank-feeds-api
description: "Xero Bank Feeds API skill. Use when working with Xero Bank Feeds for FeedConnections, Statements. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Xero Bank Feeds API
API version: 11.1.0

## Auth
OAuth2

## Base URL
https://api.xero.com/bankfeeds.xro/1.0

## Setup
1. Configure auth: OAuth2
2. GET /FeedConnections -- verify access
3. POST /FeedConnections -- create first FeedConnections

## Endpoints

7 endpoints across 2 groups. See references/api-spec.lap for full details.

### FeedConnections
| Method | Path | Description |
|--------|------|-------------|
| GET | /FeedConnections | Searches for feed connections |
| POST | /FeedConnections | Create one or more new feed connection |
| GET | /FeedConnections/{id} | Retrieve single feed connection based on a unique id provided |
| POST | /FeedConnections/DeleteRequests | Delete an existing feed connection |

### Statements
| Method | Path | Description |
|--------|------|-------------|
| GET | /Statements | Retrieve all statements |
| POST | /Statements | Creates one or more new statements |
| GET | /Statements/{statementId} | Retrieve single statement based on unique id provided |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all FeedConnections?" -> GET /FeedConnections
- "Create a FeedConnection?" -> POST /FeedConnections
- "Get FeedConnection details?" -> GET /FeedConnections/{id}
- "Create a DeleteRequest?" -> POST /FeedConnections/DeleteRequests
- "List all Statements?" -> GET /Statements
- "Create a Statement?" -> POST /Statements
- "Get Statement details?" -> GET /Statements/{statementId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
