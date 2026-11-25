---
name: text-analytics-client
description: "Text Analytics Client API skill. Use when working with Text Analytics Client for keyPhrases, languages, sentiment. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Text Analytics Client
API version: v2.1-preview

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
3. POST /keyPhrases -- create first keyPhrases

## Endpoints

4 endpoints across 4 groups. See references/api-spec.lap for full details.

### keyPhrases
| Method | Path | Description |
|--------|------|-------------|
| POST | /keyPhrases | The API returns a list of strings denoting the key talking points in the input text. |

### languages
| Method | Path | Description |
|--------|------|-------------|
| POST | /languages | The API returns the detected language and a numeric score between 0 and 1. |

### sentiment
| Method | Path | Description |
|--------|------|-------------|
| POST | /sentiment | The API returns a numeric score between 0 and 1. |

### entities
| Method | Path | Description |
|--------|------|-------------|
| POST | /entities | The API returns a list of recognized entities in a given document. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a keyPhrase?" -> POST /keyPhrases
- "Create a language?" -> POST /languages
- "Create a sentiment?" -> POST /sentiment
- "Create a entity?" -> POST /entities
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
