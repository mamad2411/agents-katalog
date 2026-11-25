---
name: libretranslate
description: "LibreTranslate API skill. Use when working with LibreTranslate for detect, frontend, health. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# LibreTranslate
API version: 1.8.4

## Auth
ApiKey api_key in formData

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /frontend/settings -- verify access
3. POST /detect -- create first detect

## Endpoints

7 endpoints across 7 groups. See references/api-spec.lap for full details.

### detect
| Method | Path | Description |
|--------|------|-------------|
| POST | /detect | Detect Language of Text |

### frontend
| Method | Path | Description |
|--------|------|-------------|
| GET | /frontend/settings | Retrieve Frontend Settings |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health Check |

### languages
| Method | Path | Description |
|--------|------|-------------|
| GET | /languages | Get Supported Languages |

### suggest
| Method | Path | Description |
|--------|------|-------------|
| POST | /suggest | Submit a Suggestion to Improve a Translation |

### translate
| Method | Path | Description |
|--------|------|-------------|
| POST | /translate | Translate Text |

### translate_file
| Method | Path | Description |
|--------|------|-------------|
| POST | /translate_file | Translate a File |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a detect?" -> POST /detect
- "List all settings?" -> GET /frontend/settings
- "List all health?" -> GET /health
- "List all languages?" -> GET /languages
- "Create a suggest?" -> POST /suggest
- "Create a translate?" -> POST /translate
- "Create a translate_file?" -> POST /translate_file
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
