---
name: trivia-api
description: "Trivia API skill. Use when working with Trivia for trivia. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Trivia API
API version: 1.5

## Auth
ApiKey X-Fungenerators-Api-Secret in header

## Base URL
https://api.fungenerators.com/

## Setup
1. Set your API key in the appropriate header
2. GET /trivia -- verify access

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### trivia
| Method | Path | Description |
|--------|------|-------------|
| GET | /trivia | Get a Trivia entry for a given id. Retrieves a trivia question and answer based on the id. |
| PUT | /trivia | Create a random Trivia entry. |
| DELETE | /trivia | Create a random Trivia entry. |
| GET | /trivia/random | Get a random trivia for a given category(optional) |
| GET | /trivia/search | Search for random trivia which has the text in the query, for a given category(optional). |
| GET | /trivia/categories | Get a random Trivia. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all trivia?" -> GET /trivia
- "List all random?" -> GET /trivia/random
- "Search search?" -> GET /trivia/search
- "List all categories?" -> GET /trivia/categories
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
