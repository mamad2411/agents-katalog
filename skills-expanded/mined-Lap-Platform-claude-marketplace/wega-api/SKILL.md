---
name: wega-api
description: "WeGA API skill. Use when working with WeGA for documents, search, code. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# WeGA API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
http://localhost:8080/exist/apps/WeGA-WebApp/api/v1

## Setup
1. No auth setup needed
2. GET /documents -- verify access

## Endpoints

10 endpoints across 5 groups. See references/api-spec.lap for full details.

### documents
| Method | Path | Description |
|--------|------|-------------|
| GET | /documents | Lists all documents |
| GET | /documents/{docID} | Returns documents by ID |
| GET | /documents/findByDate | Finds documents by date |
| GET | /documents/findByMention/{docID} | Finds documents by reference |
| GET | /documents/findByAuthor/{authorID} | Finds documents by author |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search/entity | Search for a WeGA entity |

### code
| Method | Path | Description |
|--------|------|-------------|
| GET | /code/findByElement/{element} | Finds code samples by XML element |

### application
| Method | Path | Description |
|--------|------|-------------|
| GET | /application/status | Get status information about the running WeGA-WebApp |
| GET | /application/newID | Create a new WeGA ID |

### facets
| Method | Path | Description |
|--------|------|-------------|
| GET | /facets/{facet} | Returns facets |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all documents?" -> GET /documents
- "Search entity?" -> GET /search/entity
- "Get document details?" -> GET /documents/{docID}
- "List all findByDate?" -> GET /documents/findByDate
- "Get findByMention details?" -> GET /documents/findByMention/{docID}
- "Get findByAuthor details?" -> GET /documents/findByAuthor/{authorID}
- "Get findByElement details?" -> GET /code/findByElement/{element}
- "List all status?" -> GET /application/status
- "List all newID?" -> GET /application/newID
- "Get facet details?" -> GET /facets/{facet}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
