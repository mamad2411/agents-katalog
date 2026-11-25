---
name: random-riddles-api
description: "Random Riddles API skill. Use when working with Random Riddles for riddle. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Random Riddles API
API version: 1.5

## Auth
ApiKey X-Fungenerators-Api-Secret in header

## Base URL
https://api.fungenerators.com

## Setup
1. Set your API key in the appropriate header
2. GET /riddle -- verify access
3. POST /riddle -- create first riddle

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### riddle
| Method | Path | Description |
|--------|------|-------------|
| GET | /riddle | Get a Riddle entry for a given id. Retrieves a riddle question and answer based on the id. |
| POST | /riddle | Create a random Riddle entry. Same as 'PUT' but can be used when some of the client libraries don't support 'PUT'. |
| PUT | /riddle | Create a random Riddle entry. |
| DELETE | /riddle | Create a random Riddle entry. |
| GET | /riddle/random | Get a random riddle for a given category(optional) |
| GET | /riddle/search | Search for random riddle which has the text in the query, for a given category(optional). |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all riddle?" -> GET /riddle
- "Create a riddle?" -> POST /riddle
- "List all random?" -> GET /riddle/random
- "Search search?" -> GET /riddle/search
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
