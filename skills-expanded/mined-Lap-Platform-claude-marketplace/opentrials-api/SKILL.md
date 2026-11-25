---
name: opentrials-api
description: "OpenTrials API skill. Use when working with OpenTrials for search, trials, publications. Covers 17 endpoints."
version: 1.0.0
generator: lapsh
---

# OpenTrials API
API version: 0.0.1

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /search -- verify access

## Endpoints

17 endpoints across 11 groups. See references/api-spec.lap for full details.

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search | Returns trials based on a search query. By default, it'll search in all of a trial's attributes. |
| GET | /search/autocomplete/{in} | Autocomplete search feature for supported database entities (`location`). It has the same options as a regular `search` operation, with an extra **required** `in` parameter indicating the entity type to search. |
| GET | /search/fda_documents | Search the FDA documents |

### trials
| Method | Path | Description |
|--------|------|-------------|
| GET | /trials/{id} | Returns a trial's details and related entities (e.g. `conditions`). |
| GET | /trials/{id}/records | Returns a trial's raw records from its sources |
| GET | /trials/{trialId}/records/{id} | Returns a trial's raw record from its sources |

### publications
| Method | Path | Description |
|--------|------|-------------|
| GET | /publications/{id} | Returns publication details |

### conditions
| Method | Path | Description |
|--------|------|-------------|
| GET | /conditions/{id} | Returns condition details |

### organisations
| Method | Path | Description |
|--------|------|-------------|
| GET | /organisations/{id} | Returns organisation details |

### persons
| Method | Path | Description |
|--------|------|-------------|
| GET | /persons/{id} | Returns person details |

### interventions
| Method | Path | Description |
|--------|------|-------------|
| GET | /interventions/{id} | Returns intervention details |

### sources
| Method | Path | Description |
|--------|------|-------------|
| GET | /sources | Returns list of sources |

### fda_applications
| Method | Path | Description |
|--------|------|-------------|
| GET | /fda_applications | Returns FDA applications |
| GET | /fda_applications/{id} | Returns an FDA application details |

### documents
| Method | Path | Description |
|--------|------|-------------|
| GET | /documents | Returns documents |
| GET | /documents/{id} | Returns details of a document |

### document_categories
| Method | Path | Description |
|--------|------|-------------|
| GET | /document_categories | Returns document categories |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search search?" -> GET /search
- "Search autocomplete?" -> GET /search/autocomplete/{in}
- "Search fda_documents?" -> GET /search/fda_documents
- "Get trial details?" -> GET /trials/{id}
- "Get publication details?" -> GET /publications/{id}
- "Get condition details?" -> GET /conditions/{id}
- "Get organisation details?" -> GET /organisations/{id}
- "List all records?" -> GET /trials/{id}/records
- "Get record details?" -> GET /trials/{trialId}/records/{id}
- "Get person details?" -> GET /persons/{id}
- "Get intervention details?" -> GET /interventions/{id}
- "List all sources?" -> GET /sources
- "List all fda_applications?" -> GET /fda_applications
- "Get fda_application details?" -> GET /fda_applications/{id}
- "List all documents?" -> GET /documents
- "Get document details?" -> GET /documents/{id}
- "List all document_categories?" -> GET /document_categories

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
