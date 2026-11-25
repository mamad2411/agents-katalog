---
name: erskine-may-api
description: "Erskine May API skill. Use when working with Erskine May for api. Covers 11 endpoints."
version: 1.0.0
generator: lapsh
---

# Erskine May API
API version: v1

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /api/IndexTerm/browse -- verify access

## Endpoints

11 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/Chapter/{chapterNumber} | Returns a single chapter overview by chapter number. |
| GET | /api/IndexTerm/browse | Returns a list of index terms by start letter. |
| GET | /api/IndexTerm/{indexTermId} | Returns an index term by id. |
| GET | /api/Part | Returns a list of all parts. |
| GET | /api/Part/{partNumber} | Returns a part by part number. |
| GET | /api/Search/IndexTermSearchResults/{searchTerm} | Returns a list of index terms which contain the search term. |
| GET | /api/Search/Paragraph/{reference} | Returns a section overview by reference. |
| GET | /api/Search/ParagraphSearchResults/{searchTerm} | Returns a list of paragraphs which contain the search term. |
| GET | /api/Search/SectionSearchResults/{searchTerm} | Returns a list of sections which contain the search term. |
| GET | /api/Section/{sectionId} | Returns a section by section id. |
| GET | /api/Section/{sectionId},{step} | Returns a section overview by section id and step. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get Chapter details?" -> GET /api/Chapter/{chapterNumber}
- "List all browse?" -> GET /api/IndexTerm/browse
- "Get IndexTerm details?" -> GET /api/IndexTerm/{indexTermId}
- "List all Part?" -> GET /api/Part
- "Get Part details?" -> GET /api/Part/{partNumber}
- "Get IndexTermSearchResult details?" -> GET /api/Search/IndexTermSearchResults/{searchTerm}
- "Get Paragraph details?" -> GET /api/Search/Paragraph/{reference}
- "Get ParagraphSearchResult details?" -> GET /api/Search/ParagraphSearchResults/{searchTerm}
- "Get SectionSearchResult details?" -> GET /api/Search/SectionSearchResults/{searchTerm}
- "Get Section details?" -> GET /api/Section/{sectionId}
- "Get Section details?" -> GET /api/Section/{sectionId},{step}

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
