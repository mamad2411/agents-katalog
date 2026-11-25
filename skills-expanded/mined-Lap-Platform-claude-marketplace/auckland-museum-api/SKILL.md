---
name: auckland-museum-api
description: "Auckland Museum API skill. Use when working with Auckland Museum for search, id, sparql. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Auckland Museum API
API version: 2.0.0

## Auth
No authentication required.

## Base URL
https://api.aucklandmuseum.com

## Setup
1. No auth setup needed
2. GET /sparql -- verify access
3. POST /search/{index}/{operation} -- create first search

## Endpoints

6 endpoints across 3 groups. See references/api-spec.lap for full details.

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search/{index}/{operation} | Perform simple search queries over Auckland Museum Collections and Cenotaph data |
| POST | /search/{index}/{operation} | Perform complex search queries over Auckland Museum Collections and Cenotaph data |

### id
| Method | Path | Description |
|--------|------|-------------|
| GET | /id/{identifier} | Explore details about a given subject node |
| GET | /id/media/{path} | Retrieve media associated with Collections and Cenotaph subjects in Auckland Museum |

### sparql
| Method | Path | Description |
|--------|------|-------------|
| GET | /sparql | Auckland Museum SPARQL endpoint |
| POST | /sparql | Auckland Museum SPARQL endpoint |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search search?" -> GET /search/{index}/{operation}
- "Get id details?" -> GET /id/{identifier}
- "Get media details?" -> GET /id/media/{path}
- "Search sparql?" -> GET /sparql
- "Create a sparql?" -> POST /sparql

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
