---
name: bc-laws
description: "BC Laws API skill. Use when working with BC Laws for content, document, search. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# BC Laws
API version: 1.0.0

## Auth
No authentication required.

## Base URL
http://www.bclaws.ca/civix

## Setup
1. No auth setup needed
2. GET /document/id/{aspectId}/{civixIndexId}/{civixDocumentId}/xml -- verify access

## Endpoints

7 endpoints across 3 groups. See references/api-spec.lap for full details.

### content
| Method | Path | Description |
|--------|------|-------------|
| GET | /content/{aspectId} | Describes the documents and directories available within a specific 'aspect' (content group) of the BCLaws library |
| GET | /content/{aspectId}/{civixDocumentId} | Lists the metadata available for the specified index or directory from the BCLaws legislative respository |

### document
| Method | Path | Description |
|--------|------|-------------|
| GET | /document/id/{aspectId}/{civixIndexId}/{civixDocumentId} | Retrieves a specific document from the BCLaws legislative repository (HTML format) |
| GET | /document/id/{aspectId}/{civixIndexId}/{civixDocumentId}/xml | Retrieves a specific document from the BCLaws legislative repository (XML format) |
| GET | /document/id/{aspectId}/{civixIndexId}/{civixDocumentId}/search/{searchString} | Retrieves a specific document from the BCLaws legislative repository with search text highlighted (HTML format) |
| GET | /document/id/{aspectId}/{civixIndexId}/{civixDocumentId}/xml/search/{searchString} | Retrieves a specific document from the BCLaws legislative repository with search text highlighted (XML format) |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search/{aspectId}/fullsearch | A listing of metadata available for the specified aspect and search term from the BCLaws legislative repository |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get content details?" -> GET /content/{aspectId}
- "Get content details?" -> GET /content/{aspectId}/{civixDocumentId}
- "Get id details?" -> GET /document/id/{aspectId}/{civixIndexId}/{civixDocumentId}
- "List all xml?" -> GET /document/id/{aspectId}/{civixIndexId}/{civixDocumentId}/xml
- "Get search details?" -> GET /document/id/{aspectId}/{civixIndexId}/{civixDocumentId}/search/{searchString}
- "Get search details?" -> GET /document/id/{aspectId}/{civixIndexId}/{civixDocumentId}/xml/search/{searchString}
- "Search fullsearch?" -> GET /search/{aspectId}/fullsearch

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
