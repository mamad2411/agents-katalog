---
name: enanomapper-federated-search
description: "eNanoMapper federated search API skill. Use when working with eNanoMapper federated search for select, enm. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# eNanoMapper federated search
API version: 1.0

## Auth
No authentication required.

## Base URL
https://api.ideaconsult.net/nanoreg1

## Setup
1. No auth setup needed
2. GET /select -- verify access
3. POST /select -- create first select

## Endpoints

13 endpoints across 2 groups. See references/api-spec.lap for full details.

### select
| Method | Path | Description |
|--------|------|-------------|
| GET | /select | Apache Solr powered search |
| POST | /select | Apache Solr powered search |

### enm
| Method | Path | Description |
|--------|------|-------------|
| GET | /enm/{db}/investigation | Details of multiple studies |
| GET | /enm/{db}/substance | List substances |
| GET | /enm/{db}/substance/{uuid} | Get a substance |
| GET | /enm/{db}/substance/{uuid}/study | get substance study |
| GET | /enm/{db}/substance/{uuid}/composition | Substance composition |
| GET | /enm/{db}/substance/{uuid}/structures | Get substance composition as a dataset |
| GET | /enm/{db}/substance/{uuid}/studySummary | Get study summary for the substance |
| GET | /enm/{db}/query/study | Search endpoint summary |
| GET | /enm/{db}/query/compound/{term}/{representation} | Exact chemical structure search |
| GET | /enm/{db}/query/smarts | Substructure search |
| GET | /enm/{db}/query/similarity | Exact similarity search |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search select?" -> GET /select
- "Create a select?" -> POST /select
- "Search investigation?" -> GET /enm/{db}/investigation
- "Search substance?" -> GET /enm/{db}/substance
- "Get substance details?" -> GET /enm/{db}/substance/{uuid}
- "List all study?" -> GET /enm/{db}/substance/{uuid}/study
- "List all composition?" -> GET /enm/{db}/substance/{uuid}/composition
- "List all structures?" -> GET /enm/{db}/substance/{uuid}/structures
- "List all studySummary?" -> GET /enm/{db}/substance/{uuid}/studySummary
- "List all study?" -> GET /enm/{db}/query/study
- "Search compound?" -> GET /enm/{db}/query/compound/{term}/{representation}
- "Search smarts?" -> GET /enm/{db}/query/smarts
- "Search similarity?" -> GET /enm/{db}/query/similarity

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
