---
name: languagetool-api
description: "LanguageTool API skill. Use when working with LanguageTool for check, languages, words. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# LanguageTool API
API version: 1.1.2

## Auth
ApiKey apiKey in formData

## Base URL
https://api.languagetoolplus.com/v2

## Setup
1. Set your API key in the appropriate header
2. GET /languages -- verify access
3. POST /check -- create first check

## Endpoints

5 endpoints across 3 groups. See references/api-spec.lap for full details.

### check
| Method | Path | Description |
|--------|------|-------------|
| POST | /check | Check a text |

### languages
| Method | Path | Description |
|--------|------|-------------|
| GET | /languages | Get a list of supported languages. |

### words
| Method | Path | Description |
|--------|------|-------------|
| GET | /words | List words in dictionaries |
| POST | /words/add | Add word to a dictionary |
| POST | /words/delete | Remove word from a dictionary |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a check?" -> POST /check
- "List all languages?" -> GET /languages
- "List all words?" -> GET /words
- "Create a add?" -> POST /words/add
- "Create a delete?" -> POST /words/delete
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
