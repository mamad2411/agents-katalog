---
name: starwars-translations-api
description: "Starwars Translations API skill. Use when working with Starwars Translations for translate. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Starwars Translations API
API version: 2.3

## Auth
ApiKey X-Funtranslations-Api-Secret in header

## Base URL
https://api.funtranslations.com

## Setup
1. Set your API key in the appropriate header
2. GET /translate/yoda -- verify access

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### translate
| Method | Path | Description |
|--------|------|-------------|
| GET | /translate/yoda | Translate from English to Yoda Speak. |
| GET | /translate/sith | Translate from English to Sith Speak. |
| GET | /translate/cheunh | Translate from English to Starwars cheunh. |
| GET | /translate/gungan | Translate from English to Starwars Gungan Language. |
| GET | /translate/mandalorian | Translate from English to Starwars Mandalorian Language. |
| GET | /translate/huttese | Translate from English to Starwars Huttese Language. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all yoda?" -> GET /translate/yoda
- "List all sith?" -> GET /translate/sith
- "List all cheunh?" -> GET /translate/cheunh
- "List all gungan?" -> GET /translate/gungan
- "List all mandalorian?" -> GET /translate/mandalorian
- "List all huttese?" -> GET /translate/huttese
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
