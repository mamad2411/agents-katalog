---
name: jokes-one-api
description: "Jokes One API skill. Use when working with Jokes One for jod, joke. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# Jokes One API
API version: 1.1

## Auth
ApiKey X-JokesOne-Api-Secret in header

## Base URL
https://api.jokes.one

## Setup
1. Set your API key in the appropriate header
2. GET /jod -- verify access
3. POST /joke/tags/add -- create first add

## Endpoints

12 endpoints across 2 groups. See references/api-spec.lap for full details.

### jod
| Method | Path | Description |
|--------|------|-------------|
| GET | /jod | Gets `Joke of the Day`. |
| GET | /jod/categories | Gets a list of `Joke of the Day` Categories. |

### joke
| Method | Path | Description |
|--------|------|-------------|
| PUT | /joke | Add a new joke to your private collection. |
| PATCH | /joke | Update a joke |
| GET | /joke | Gets a `Joke` with a given `id`. |
| DELETE | /joke | Delete a joke. The user needs to be the owner of the joke to be able to delete it. |
| GET | /joke/random | Gets a `Random Joke`. When you are in a hurry this is what you call to get a random famous joke. |
| GET | /joke/search | Search for a `Joke` in Jokes One platform. Optional `category` , `author`, `minlength`, `maxlength` params determines the filters applied while searching for the joke. |
| GET | /joke/categories/search | Gets a list of `Joke` Categories, based on a query term. |
| GET | /joke/list | Get the list of jokes in your private collection. |
| POST | /joke/tags/add | Add a tag to a given Joke. |
| POST | /joke/tags/remove | Remove a tag from a given joke. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all jod?" -> GET /jod
- "List all categories?" -> GET /jod/categories
- "List all joke?" -> GET /joke
- "List all random?" -> GET /joke/random
- "Search search?" -> GET /joke/search
- "Search search?" -> GET /joke/categories/search
- "List all list?" -> GET /joke/list
- "Create a add?" -> POST /joke/tags/add
- "Create a remove?" -> POST /joke/tags/remove
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
