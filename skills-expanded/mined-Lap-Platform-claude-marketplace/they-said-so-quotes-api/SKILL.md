---
name: they-said-so-quotes-api
description: "They Said So Quotes API skill. Use when working with They Said So Quotes for qod, quote, qshow. Covers 45 endpoints."
version: 1.0.0
generator: lapsh
---

# They Said So Quotes API
API version: 5.1

## Auth
Bearer bearer

## Base URL
https://quotes.rest

## Setup
1. Set Authorization header with your Bearer token
2. GET /qod -- verify access
3. POST /quote -- create first quote

## Endpoints

45 endpoints across 3 groups. See references/api-spec.lap for full details.

### qod
| Method | Path | Description |
|--------|------|-------------|
| GET | /qod | Gets `Quote of the Day` (QOD). Optional `category` param determines the category of returned quote of the day |
| PUT | /qod | Create a private `Quote of the Day` service. |
| PATCH | /qod | Update an existing private `Quote of the Day` definition. |
| GET | /qod/categories | Gets a list of `Quote of the Day` Categories. |
| GET | /qod/languages | Gets a list of supported languages for `Quote of the Day`. |

### quote
| Method | Path | Description |
|--------|------|-------------|
| GET | /quote/random | Gets a `Random Quote`. When you are in a hurry this is what you call to get a random famous quote. |
| GET | /quote/search | Search for a `Quote` in They Said So platform. Optional `category` , `author`, `minlength`, `maxlength` params determines the filters applied while searching for the quote. |
| GET | /quote/categories/popular | Gets a list of popular `Quote` Categories. |
| GET | /quote/categories/search | Gets a list of `Quote` Categories matching the query string. |
| GET | /quote/authors/popular | Gets a list of popular author names in the system. |
| GET | /quote/authors/search | Gets a list of author names in the system. |
| PUT | /quote | Add a new quote to your private collection. |
| POST | /quote | Add a new quote to your private collection. Same as 'PUT' but added since some clients don't handle PUT well. |
| PATCH | /quote | Update a quote |
| GET | /quote | Gets a `Quote` with a given `id`. |
| DELETE | /quote | Delete a quote. The user needs to be the owner of the quote to be able to delete it. |
| GET | /quote/list | Get the list of quotes in your private collection. |
| POST | /quote/tags/add | Add a tag to a given Quote. |
| POST | /quote/tags/remove | Remove a tag from a given quote. |
| GET | /quote/like/toggle | Toggle the user like of the given Quote as a user of the API Key. |
| GET | /quote/bookmark/toggle | Toggle the user bookmark of the given Quote as a user of the API Key. |
| PUT | /quote/image | Create a new quote image for a given quote. Choose background colors/images , choose different font styles and generate a beautiful quote image. Did you just had a feeling of being a god or what?! |
| GET | /quote/image | Gets a Quote image for a given id. Response can be an image file as a binary or a base64 encoded contents wrapped in json. `TODO` |
| DELETE | /quote/image | Delete a quote image. The user needs to be the owner of the quote image to be able to delete it. |
| GET | /quote/image/search | Gets a Random Quote image. Optional `category` param determines the category of quote used in the image. Optional `author` param gets the quote image of a given author. |
| POST | /quote/image/background | Add an image for use later as a quote background image. |
| DELETE | /quote/image/background | Delete a background image file. The user needs to be the owner of the background image to be able to delete it. |
| GET | /quote/image/background/search | Searches for a background image with a given tag. |
| GET | /quote/image/background/list | Lists background images in your private collection. |
| POST | /quote/image/background/tags/add | Add a tag to a given Image. |
| POST | /quote/image/background/tags/remove | Remove a tag from a given Image. |
| POST | /quote/image/font | Add a font file for use later in creating a quote image. This is essentially a `PUT` but not many clients handle PUT with binary stream i.e. a file, gracefully. |
| DELETE | /quote/image/font | Delete a font file. The user needs to be the owner of the font to be able to delete it. |
| GET | /quote/image/font/search | Searches for a font with a given tag. |
| GET | /quote/image/font/list | Lists background images in your private collection. |
| POST | /quote/image/font/tags/add | Add a tag to a given font. |
| POST | /quote/image/font/tags/remove | Remove a tag from a given Font. |

### qshow
| Method | Path | Description |
|--------|------|-------------|
| PUT | /qshow | Create and add a new qshow to your private collection. |
| GET | /qshow | Gets a details about a qshow. |
| PATCH | /qshow | Update an existing qshow. |
| DELETE | /qshow | Delete a qshow. |
| POST | /qshow/quotes/add | Add a quote to a given Qshow. |
| POST | /qshow/quotes/remove | Remove a quote to a given Qshow. |
| GET | /qshow/quotes | Get the quotes in a given Qshow. |
| GET | /qshow/list | Get the list of Qshows in They Said So platform. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all qod?" -> GET /qod
- "List all categories?" -> GET /qod/categories
- "List all languages?" -> GET /qod/languages
- "List all random?" -> GET /quote/random
- "Search search?" -> GET /quote/search
- "List all popular?" -> GET /quote/categories/popular
- "Search search?" -> GET /quote/categories/search
- "List all popular?" -> GET /quote/authors/popular
- "Search search?" -> GET /quote/authors/search
- "Create a quote?" -> POST /quote
- "List all quote?" -> GET /quote
- "List all list?" -> GET /quote/list
- "Create a add?" -> POST /quote/tags/add
- "Create a remove?" -> POST /quote/tags/remove
- "List all toggle?" -> GET /quote/like/toggle
- "List all toggle?" -> GET /quote/bookmark/toggle
- "List all qshow?" -> GET /qshow
- "Create a add?" -> POST /qshow/quotes/add
- "Create a remove?" -> POST /qshow/quotes/remove
- "List all quotes?" -> GET /qshow/quotes
- "List all list?" -> GET /qshow/list
- "List all image?" -> GET /quote/image
- "List all search?" -> GET /quote/image/search
- "Create a background?" -> POST /quote/image/background
- "Search search?" -> GET /quote/image/background/search
- "List all list?" -> GET /quote/image/background/list
- "Create a add?" -> POST /quote/image/background/tags/add
- "Create a remove?" -> POST /quote/image/background/tags/remove
- "Create a font?" -> POST /quote/image/font
- "Search search?" -> GET /quote/image/font/search
- "List all list?" -> GET /quote/image/font/list
- "Create a add?" -> POST /quote/image/font/tags/add
- "Create a remove?" -> POST /quote/image/font/tags/remove
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
