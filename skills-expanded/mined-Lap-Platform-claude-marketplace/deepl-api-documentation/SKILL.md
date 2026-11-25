---
name: deepl-api-documentation
description: "DeepL API Documentation API skill. Use when working with DeepL API Documentation for translate, document, glossary-language-pairs. Covers 30 endpoints."
version: 1.0.0
generator: lapsh
---

# DeepL API Documentation
API version: 3.9.0

## Auth
ApiKey Authorization in header

## Base URL
https://api.deepl.com

## Setup
1. Set your API key in the appropriate header
2. GET /v2/glossary-language-pairs -- verify access
3. POST /v2/translate -- create first translate

## Endpoints

30 endpoints across 10 groups. See references/api-spec.lap for full details.

### translate
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/translate | Request Translation |

### document
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/document | Upload and Translate a Document |
| POST | /v2/document/{document_id} | Check Document Status |
| POST | /v2/document/{document_id}/result | Download Translated Document |

### glossary-language-pairs
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/glossary-language-pairs | List Language Pairs Supported by Glossaries |

### glossaries
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/glossaries | Create a Glossary |
| GET | /v3/glossaries | List all Glossaries |
| GET | /v3/glossaries/{glossary_id} | Retrieve Glossary Details |
| PATCH | /v3/glossaries/{glossary_id} | Edit glossary details |
| DELETE | /v3/glossaries/{glossary_id} | Delete a Glossary |
| GET | /v3/glossaries/{glossary_id}/entries | Retrieve Glossary Entries |
| DELETE | /v3/glossaries/{glossary_id}/dictionaries | Deletes the dictionary associated with the given language pair with the given glossary ID. |
| PUT | /v3/glossaries/{glossary_id}/dictionaries | Replaces or creates a dictionary in the glossary with the specified entries. |
| POST | /v2/glossaries | Create a Glossary |
| GET | /v2/glossaries | List all Glossaries |
| GET | /v2/glossaries/{glossary_id} | Retrieve Glossary Details |
| DELETE | /v2/glossaries/{glossary_id} | Delete a Glossary |
| GET | /v2/glossaries/{glossary_id}/entries | Retrieve Glossary Entries |

### write
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/write/rephrase | Request text improvement |

### usage
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/usage | Check Usage and Limits |

### languages
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/languages | Retrieve Supported Languages |

### admin
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/admin/developer-keys | Create a developer key as an admin |
| GET | /v2/admin/developer-keys | Get all developer keys as an admin |
| PUT | /v2/admin/developer-keys/deactivate | Deactivate a developer key as an admin |
| PUT | /v2/admin/developer-keys/label | Rename a developer key as an admin |
| PUT | /v2/admin/developer-keys/limits | Set developer key usage limits as an admin |
| GET | /v2/admin/analytics | Get usage statistics as an admin |

### style_rules
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/style_rules | Retrieve style rule lists |

### voice
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/voice/realtime | Get Streaming URL |
| GET | /v3/voice/realtime | Request Reconnection |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a translate?" -> POST /v2/translate
- "Create a document?" -> POST /v2/document
- "Create a result?" -> POST /v2/document/{document_id}/result
- "List all glossary-language-pairs?" -> GET /v2/glossary-language-pairs
- "Create a glossary?" -> POST /v3/glossaries
- "List all glossaries?" -> GET /v3/glossaries
- "Get glossary details?" -> GET /v3/glossaries/{glossary_id}
- "Partially update a glossary?" -> PATCH /v3/glossaries/{glossary_id}
- "Delete a glossary?" -> DELETE /v3/glossaries/{glossary_id}
- "List all entries?" -> GET /v3/glossaries/{glossary_id}/entries
- "Create a glossary?" -> POST /v2/glossaries
- "List all glossaries?" -> GET /v2/glossaries
- "Get glossary details?" -> GET /v2/glossaries/{glossary_id}
- "Delete a glossary?" -> DELETE /v2/glossaries/{glossary_id}
- "List all entries?" -> GET /v2/glossaries/{glossary_id}/entries
- "Create a rephrase?" -> POST /v2/write/rephrase
- "List all usage?" -> GET /v2/usage
- "List all languages?" -> GET /v2/languages
- "Create a developer-key?" -> POST /v2/admin/developer-keys
- "List all developer-keys?" -> GET /v2/admin/developer-keys
- "List all analytics?" -> GET /v2/admin/analytics
- "List all style_rules?" -> GET /v3/style_rules
- "Create a realtime?" -> POST /v3/voice/realtime
- "List all realtime?" -> GET /v3/voice/realtime
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
