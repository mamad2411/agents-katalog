---
name: funtranslations-braille-api
description: "FunTranslations Braille API skill. Use when working with FunTranslations Braille for translate. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# FunTranslations Braille API
API version: 2.3

## Auth
ApiKey X-Funtranslations-Api-Secret in header

## Base URL
https://api.funtranslations.com

## Setup
1. Set your API key in the appropriate header
2. GET /translate/braille -- verify access

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### translate
| Method | Path | Description |
|--------|------|-------------|
| GET | /translate/braille | Translate from English to Braille. This is what you use if you have a braille display. This API translates the English text into characters that a braille display understands and you can feed the translated text directly to the display. |
| GET | /translate/braille/dots | Use this to see which dots are enabled for each Braille letters. This is highly educational (to see which dots are enabled) and can potentially drive a non braille display which works on individual dots. |
| GET | /translate/braille/unicode | Translate from English to Braille Unicode characters. |
| GET | /translate/braille/image | Translate from English to Braille image characters. This is probably what you want to use if you are displaying braille in a browser. |
| GET | /translate/braille/html | Translate from English to Braille Image characters. This is probably what you want to use if you are displaying braille in a browser. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all braille?" -> GET /translate/braille
- "List all dots?" -> GET /translate/braille/dots
- "List all unicode?" -> GET /translate/braille/unicode
- "List all image?" -> GET /translate/braille/image
- "List all html?" -> GET /translate/braille/html
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
