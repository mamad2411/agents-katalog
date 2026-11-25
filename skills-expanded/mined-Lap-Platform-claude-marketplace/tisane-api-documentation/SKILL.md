---
name: tisane-api-documentation
description: "Tisane API Documentation API skill. Use when working with Tisane API Documentation for parse, languages, helper. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# Tisane API Documentation

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
https://api.tisane.ai

## Setup
1. Set your API key in the appropriate header
2. GET /languages -- verify access
3. POST /parse -- create first parse

## Endpoints

8 endpoints across 8 groups. See references/api-spec.lap for full details.

### parse
| Method | Path | Description |
|--------|------|-------------|
| POST | /parse | Analyze text |

### languages
| Method | Path | Description |
|--------|------|-------------|
| GET | /languages | List available languages |

### helper
| Method | Path | Description |
|--------|------|-------------|
| POST | /helper/extract_text | Text clean up |

### compare
| Method | Path | Description |
|--------|------|-------------|
| POST | /compare/entities | Named entity comparison |

### similarity
| Method | Path | Description |
|--------|------|-------------|
| POST | /similarity | Semantic similarity |

### detectLanguage
| Method | Path | Description |
|--------|------|-------------|
| POST | /detectLanguage | Detect language |

### transform
| Method | Path | Description |
|--------|------|-------------|
| POST | /transform | Translate text |

### lm
| Method | Path | Description |
|--------|------|-------------|
| GET | /lm/inflections | List inflected forms |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a parse?" -> POST /parse
- "List all languages?" -> GET /languages
- "Create a extract_text?" -> POST /helper/extract_text
- "Create a entity?" -> POST /compare/entities
- "Create a similarity?" -> POST /similarity
- "Create a detectLanguage?" -> POST /detectLanguage
- "Create a transform?" -> POST /transform
- "List all inflections?" -> GET /lm/inflections
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
