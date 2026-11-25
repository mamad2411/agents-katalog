---
name: isbndb-api
description: "ISBNdb API skill. Use when working with ISBNdb for author, authors, book. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# ISBNdb API
API version: 1.0.1

## Auth
ApiKey x-api-key in header

## Base URL
https://api.isbndb.com

## Setup
1. Set your API key in the appropriate header
2. GET /search -- verify access

## Endpoints

10 endpoints across 10 groups. See references/api-spec.lap for full details.

### author
| Method | Path | Description |
|--------|------|-------------|
| GET | /author/{name} | Gets author details |

### authors
| Method | Path | Description |
|--------|------|-------------|
| GET | /authors/{query} | Search authors |

### book
| Method | Path | Description |
|--------|------|-------------|
| GET | /book/{isbn} | Gets book details |

### books
| Method | Path | Description |
|--------|------|-------------|
| GET | /books/{query} | Search books |

### publisher
| Method | Path | Description |
|--------|------|-------------|
| GET | /publisher/{name} | Gets publisher details |

### publishers
| Method | Path | Description |
|--------|------|-------------|
| GET | /publishers/{query} | Search publishers |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search | Search all ISBNDB databases |

### stats
| Method | Path | Description |
|--------|------|-------------|
| GET | /stats | Gets status on the ISBNDB Database |

### subject
| Method | Path | Description |
|--------|------|-------------|
| GET | /subject/{name} | Gets subject details |

### subjects
| Method | Path | Description |
|--------|------|-------------|
| GET | /subjects/{query} | Search subjects |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get author details?" -> GET /author/{name}
- "Search authors?" -> GET /authors/{query}
- "Get book details?" -> GET /book/{isbn}
- "Search books?" -> GET /books/{query}
- "Get publisher details?" -> GET /publisher/{name}
- "Search publishers?" -> GET /publishers/{query}
- "Search search?" -> GET /search
- "List all stats?" -> GET /stats
- "Get subject details?" -> GET /subject/{name}
- "Search subjects?" -> GET /subjects/{query}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
