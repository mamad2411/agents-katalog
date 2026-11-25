---
name: nlpcloud
description: "NLPCloud API skill. Use when working with NLPCloud for en_core_web_sm. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# NLPCloud
API version: 1.0.0

## Auth
Bearer bearer

## Base URL
Not specified.

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/en_core_web_sm/version -- verify access
3. POST /v1/en_core_web_sm/entities -- create first entities

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### en_core_web_sm
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/en_core_web_sm/entities | Read Entities |
| POST | /v1/en_core_web_sm/dependencies | Read Dependencies |
| POST | /v1/en_core_web_sm/sentence-dependencies | Read Sentence Dependencies |
| GET | /v1/en_core_web_sm/version | Read Version |
| GET | /v1/en_core_web_sm/ | Read Root |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a entity?" -> POST /v1/en_core_web_sm/entities
- "Create a dependency?" -> POST /v1/en_core_web_sm/dependencies
- "Create a sentence-dependency?" -> POST /v1/en_core_web_sm/sentence-dependencies
- "List all version?" -> GET /v1/en_core_web_sm/version
- "List all en_core_web_sm?" -> GET /v1/en_core_web_sm/
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
