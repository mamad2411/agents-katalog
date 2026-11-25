---
name: dlx
description: "DLx API skill. Use when working with DLx for languages, lexemes. Covers 18 endpoints."
version: 1.0.0
generator: lapsh
---

# DLx
API version: 0.3.1

## Auth
ApiKey Authorization in header

## Base URL
https://api.digitallinguistics.io/v0

## Setup
1. Set your API key in the appropriate header
2. GET /languages -- verify access
3. POST /languages -- create first languages

## Endpoints

18 endpoints across 2 groups. See references/api-spec.lap for full details.

### languages
| Method | Path | Description |
|--------|------|-------------|
| GET | /languages | Get all Languages |
| POST | /languages | Add a new Language |
| PUT | /languages | Upsert (create or replace) a Language |
| GET | /languages/{languageID} | Retrieve a Language by ID |
| DELETE | /languages/{languageID} | Delete a Language by ID |
| PATCH | /languages/{languageID} | Perform a partial update on a Language |
| GET | /languages/{languageID}/lexemes | Get all Lexemes for a Language |
| POST | /languages/{languageID}/lexemes | Add a new Lexeme to a Language |
| PUT | /languages/{languageID}/lexemes | Upsert (add or replace) a Lexeme |
| GET | /languages/{languageID}/lexemes/{lexemeID} | Get a Lexeme by ID |
| DELETE | /languages/{languageID}/lexemes/{lexemeID} | Delete a Lexeme by ID |
| PATCH | /languages/{languageID}/lexemes/{lexemeID} | Perform a partial update on a Lexeme |

### lexemes
| Method | Path | Description |
|--------|------|-------------|
| GET | /lexemes | Get all Lexemes |
| POST | /lexemes | Add a new Lexeme |
| PUT | /lexemes | Upsert (add or replace) a Lexeme |
| GET | /lexemes/{lexemeID} | Get a Lexeme by ID |
| DELETE | /lexemes/{lexemeID} | Delete a Lexeme by ID |
| PATCH | /lexemes/{lexemeID} | Perform a partial update on a Lexeme |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all languages?" -> GET /languages
- "Create a language?" -> POST /languages
- "Get language details?" -> GET /languages/{languageID}
- "Delete a language?" -> DELETE /languages/{languageID}
- "Partially update a language?" -> PATCH /languages/{languageID}
- "List all lexemes?" -> GET /languages/{languageID}/lexemes
- "Create a lexeme?" -> POST /languages/{languageID}/lexemes
- "Get lexeme details?" -> GET /languages/{languageID}/lexemes/{lexemeID}
- "Delete a lexeme?" -> DELETE /languages/{languageID}/lexemes/{lexemeID}
- "Partially update a lexeme?" -> PATCH /languages/{languageID}/lexemes/{lexemeID}
- "List all lexemes?" -> GET /lexemes
- "Create a lexeme?" -> POST /lexemes
- "Get lexeme details?" -> GET /lexemes/{lexemeID}
- "Delete a lexeme?" -> DELETE /lexemes/{lexemeID}
- "Partially update a lexeme?" -> PATCH /lexemes/{lexemeID}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object
- Error responses use types: 304

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
