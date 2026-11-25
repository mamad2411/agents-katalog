---
name: apiwordnikcom
description: "api.wordnik.com API skill. Use when working with api.wordnik.com for word.json, words.json. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# api.wordnik.com
API version: 4.0

## Auth
ApiKey api_key in query

## Base URL
https://api.wordnik.com/v4

## Setup
1. Set your API key in the appropriate header
2. GET /words.json/randomWord -- verify access

## Endpoints

16 endpoints across 2 groups. See references/api-spec.lap for full details.

### word.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /word.json/{word}/audio | Fetches audio metadata for a word. |
| GET | /word.json/{word}/definitions | Return definitions for a word |
| GET | /word.json/{word}/etymologies | Fetches etymology data |
| GET | /word.json/{word}/examples | Returns examples for a word |
| GET | /word.json/{word}/frequency | Returns word usage over time |
| GET | /word.json/{word}/hyphenation | Returns syllable information for a word |
| GET | /word.json/{word}/phrases | Fetches bi-gram phrases for a word |
| GET | /word.json/{word}/pronunciations | Returns text pronunciations for a given word |
| GET | /word.json/{word}/relatedWords | Given a word as a string, returns relationships from the Word Graph |
| GET | /word.json/{word}/scrabbleScore | Returns the Scrabble score for a word |
| GET | /word.json/{word}/topExample | Returns a top example for a word |

### words.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /words.json/randomWord | Returns a single random WordObject |
| GET | /words.json/randomWords | Returns an array of random WordObjects |
| GET | /words.json/reverseDictionary | Reverse dictionary search |
| GET | /words.json/search/{query} | Searches words |
| GET | /words.json/wordOfTheDay | Returns a specific WordOfTheDay |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all audio?" -> GET /word.json/{word}/audio
- "List all definitions?" -> GET /word.json/{word}/definitions
- "List all etymologies?" -> GET /word.json/{word}/etymologies
- "List all examples?" -> GET /word.json/{word}/examples
- "List all frequency?" -> GET /word.json/{word}/frequency
- "List all hyphenation?" -> GET /word.json/{word}/hyphenation
- "List all phrases?" -> GET /word.json/{word}/phrases
- "List all pronunciations?" -> GET /word.json/{word}/pronunciations
- "List all relatedWords?" -> GET /word.json/{word}/relatedWords
- "List all scrabbleScore?" -> GET /word.json/{word}/scrabbleScore
- "List all topExample?" -> GET /word.json/{word}/topExample
- "List all randomWord?" -> GET /words.json/randomWord
- "List all randomWords?" -> GET /words.json/randomWords
- "Search reverseDictionary?" -> GET /words.json/reverseDictionary
- "Search search?" -> GET /words.json/search/{query}
- "List all wordOfTheDay?" -> GET /words.json/wordOfTheDay
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
