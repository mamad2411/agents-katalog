---
name: facts-api
description: "Facts API skill. Use when working with Facts for fact. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# Facts API
API version: 1.5

## Auth
Bearer bearer

## Base URL
https://api.fungenerators.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /fact -- verify access

## Endpoints

12 endpoints across 1 groups. See references/api-spec.lap for full details.

### fact
| Method | Path | Description |
|--------|------|-------------|
| GET | /fact | Get a Fact belonging to the id. |
| PUT | /fact | Add a Fact entry to the database (private collection). |
| DELETE | /fact | Delete a Fact entry identified by the id. |
| GET | /fact/fod/categories | Get the list of supported fact of the day categories. |
| GET | /fact/fod | Get fact of the day for the given category. |
| GET | /fact/random | Get a random Fact for a given category(optional) and subcategory(optional). |
| GET | /fact/search | Search for random Fact which has the text in the query, for a given category(optional) and subcategory(optional). |
| GET | /fact/categories | Get a random Fact. |
| GET | /fact/numbers | Get a random fact about a number |
| GET | /fact/onthisday/born | Returns a random ( famous/ relatively famous ) person born on a given day and month |
| GET | /fact/onthisday/died | Returns a random ( famous/ relatively famous ) person died on a given day and month |
| GET | /fact/onthisday/event | Returns a random ( famous/ relatively famous ) historic event on a given day and month |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all fact?" -> GET /fact
- "List all categories?" -> GET /fact/fod/categories
- "List all fod?" -> GET /fact/fod
- "List all random?" -> GET /fact/random
- "Search search?" -> GET /fact/search
- "List all categories?" -> GET /fact/categories
- "List all numbers?" -> GET /fact/numbers
- "List all born?" -> GET /fact/onthisday/born
- "List all died?" -> GET /fact/onthisday/died
- "List all event?" -> GET /fact/onthisday/event
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
