---
name: 1000000-recipe-and-grocery-list-api-v2
description: "1,000,000+ Recipe and Grocery List API (v2) API skill. Use when working with 1,000,000+ Recipe and Grocery List API (v2) for collection, collections, grocerylist. Covers 66 endpoints."
version: 1.0.0
generator: lapsh
---

# 1,000,000+ Recipe and Grocery List API (v2)
API version: partner

## Auth
basic | ApiKey X-BigOven-API-Key in header

## Base URL
https://api2.bigoven.com

## Setup
1. Set your API key in the appropriate header
2. GET /collections -- verify access
3. POST /grocerylist/department -- create first department

## Endpoints

66 endpoints across 7 groups. See references/api-spec.lap for full details.

### collection
| Method | Path | Description |
|--------|------|-------------|
| GET | /collection/{id} | Gets a recipe collection. A recipe collection is a curated set of recipes. |
| GET | /collection/{id}/meta | Gets a recipe collection metadata. A recipe collection is a curated set of recipes. |

### collections
| Method | Path | Description |
|--------|------|-------------|
| GET | /collections | Get the list of current, seasonal recipe collections. From here, you can use the /collection/{id} endpoint to retrieve the recipes in those collections. |

### grocerylist
| Method | Path | Description |
|--------|------|-------------|
| POST | /grocerylist/department | Departmentalize a list of strings -- used for ad-hoc grocery list item addition |
| GET | /grocerylist | Get the user's grocery list.  User is determined by Basic Authentication. |
| DELETE | /grocerylist | Delete all the items on a grocery list; faster operation than a sync with deleted items. |
| POST | /grocerylist/recipe | Add a Recipe to the grocery list.  In the request data, pass in recipeId, scale (scale=1.0 says to keep the recipe the same size as originally posted), markAsPending (true/false) to indicate that |
| POST | /grocerylist/line | Add a single line item to the grocery list |
| POST | /grocerylist/item | Add a single line item to the grocery list |
| POST | /grocerylist/sync | Synchronize the grocery list.  Call this with a POST to /grocerylist/sync |
| PUT | /grocerylist/item/{guid} | Update a grocery item by GUID |
| DELETE | /grocerylist/item/{guid} | /grocerylist/item/{guid}  DELETE will delete this item assuming you own it. |
| POST | /grocerylist/clearcheckedlines | Clears the checked lines. |

### recipe
| Method | Path | Description |
|--------|------|-------------|
| GET | /recipe/{recipeId}/images | Get all the images for a recipe. DEPRECATED. Please use /recipe/{recipeId}/photos. |
| GET | /recipe/photos/pending | Gets the pending by user. |
| GET | /recipe/{recipeId}/photos | Get all the photos for a recipe |
| GET | /recipe/{recipeId}/scans | Gets a list of RecipeScan images for the recipe. There will be at most 3 per recipe. |
| POST | /recipe/{recipeId}/image | POST: /recipe/{recipeId}/image?lat=42&amp;lng=21&amp;caption=this%20is%20my%20caption |
| GET | /recipe/{recipeId}/note/{noteId} | Get a given note. Make sure you're passing authentication information in the header for the user who owns the note. |
| PUT | /recipe/{recipeId}/note/{noteId} | HTTP PUT (update) a Recipe note (RecipeNote). |
| DELETE | /recipe/{recipeId}/note/{noteId} | Delete a review |
| GET | /recipe/{recipeId}/notes | recipe/100/notes |
| POST | /recipe/{recipeId}/note | HTTP POST a new note into the system. |
| GET | /recipe/{id}/zap | Zaps the recipe. |
| GET | /recipe/{id} | Return full Recipe detail. Returns 403 if the recipe is owned by someone else. |
| DELETE | /recipe/{id} | Deletes specified recipe (you must be authenticated as the owner of the recipe) |
| GET | /recipe/steps/{id} | Return full Recipe detail with steps. Returns 403 if the recipe is owned by someone else. |
| POST | /recipe/post/step | Stores recipe step number and returns saved step data |
| POST | /recipe/get/step/number | Returns stored step number and number of steps in recipe |
| GET | /recipe/get/active/recipe | Returns last active recipe for the user |
| POST | /recipe/get/saved/step | Gets recipe single step as text |
| GET | /recipe/{recipeId}/related | Get recipes related to the given recipeId |
| POST | /recipe/{recipeId}/feedback | Feedback on a Recipe -- for internal BigOven editors |
| GET | /recipe/categories | Get a list of recipe categories (the ID field can be used for include_cat in search parameters) |
| GET | /recipe/autocomplete | Given a query, return recipe titles starting with query. Query must be at least 3 chars in length. |
| GET | /recipe/autocomplete/mine | Automatics the complete my recipes. |
| GET | /recipe/autocomplete/all | Automatics the complete all recipes. |
| POST | /recipe/scan | POST an image as a new RecipeScan request |
| PUT | /recipe | Update a recipe |
| POST | /recipe | Add a new recipe |
| GET | /recipe/{recipeId}/review/{reviewId} | Get a given review - DEPRECATED. See recipe/review/{reviewId} for the current usage. |
| PUT | /recipe/{recipeId}/review/{reviewId} | HTTP PUT (update) a recipe review. DEPRECATED. Please see recipe/review/{reviewId} PUT for the new endpoint. |
| DELETE | /recipe/{recipeId}/review/{reviewId} | DEPRECATED! - Deletes a review by recipeId and reviewId. Please use recipe/review/{reviewId} instead. |
| GET | /recipe/review/{reviewId} | Get a given review by string-style ID. This will return a payload with FeaturedReply, ReplyCount. |
| PUT | /recipe/review/{reviewId} | Update a given top-level review. |
| GET | /recipe/{recipeId}/review | Get *my* review for the recipe {recipeId}, where "me" is determined by standard authentication headers |
| POST | /recipe/{recipeId}/review | Add a new review. Only one review can be provided per {userId, recipeId} pair. Otherwise your review will be updated. |
| GET | /recipe/{recipeId}/reviews | Get paged list of reviews for a recipe. Each review will have at most one FeaturedReply, as well as a ReplyCount. |
| GET | /recipe/review/{reviewId}/replies | Get a paged list of replies for a given review. |
| POST | /recipe/review/{reviewId}/replies | POST a reply to a given review. The date will be set by server. Note that replies no longer have star ratings, only top-level reviews do. |
| PUT | /recipe/review/replies/{replyId} | Update (PUT) a reply to a given review. Authenticated user must be the original one that posted the reply. |
| DELETE | /recipe/review/replies/{replyId} | DELETE a reply to a given review. Authenticated user must be the one who originally posted the reply. |

### image
| Method | Path | Description |
|--------|------|-------------|
| POST | /image/avatar | POST: /image/avatar |

### me
| Method | Path | Description |
|--------|------|-------------|
| GET | /me | Indexes this instance. |
| PUT | /me | Puts me. |
| GET | /me/skinny | Skinnies this instance. |
| GET | /me/preferences/options | Gets the options. |
| PUT | /me/profile | Puts me. |
| PUT | /me/personal | Puts me personal. |
| PUT | /me/preferences | Puts me preferences. |

### recipes
| Method | Path | Description |
|--------|------|-------------|
| GET | /recipes/raves | Get the recipe/comment tuples for those recipes with 4 or 5 star ratings |
| GET | /recipes/{id} | Same as GET recipe but also includes the recipe videos (if any) |
| GET | /recipes/random | Get a random, home-page-quality Recipe. |
| GET | /recipes/top25random | Search for recipes. There are many parameters that you can apply. Starting with the most common, use title_kw to search within a title. |
| GET | /recipes | Search for recipes. There are many parameters that you can apply. Starting with the most common, use title_kw to search within a title. |
| GET | /recipes/recentviews | Get a list of recipes that the authenticated user has most recently viewed |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get collection details?" -> GET /collection/{id}
- "List all meta?" -> GET /collection/{id}/meta
- "List all collections?" -> GET /collections
- "Create a department?" -> POST /grocerylist/department
- "List all grocerylist?" -> GET /grocerylist
- "Create a recipe?" -> POST /grocerylist/recipe
- "Create a line?" -> POST /grocerylist/line
- "Create a item?" -> POST /grocerylist/item
- "Create a sync?" -> POST /grocerylist/sync
- "Update a item?" -> PUT /grocerylist/item/{guid}
- "Delete a item?" -> DELETE /grocerylist/item/{guid}
- "Create a clearcheckedline?" -> POST /grocerylist/clearcheckedlines
- "List all images?" -> GET /recipe/{recipeId}/images
- "List all pending?" -> GET /recipe/photos/pending
- "List all photos?" -> GET /recipe/{recipeId}/photos
- "List all scans?" -> GET /recipe/{recipeId}/scans
- "Create a image?" -> POST /recipe/{recipeId}/image
- "Create a avatar?" -> POST /image/avatar
- "List all me?" -> GET /me
- "List all skinny?" -> GET /me/skinny
- "List all options?" -> GET /me/preferences/options
- "Get note details?" -> GET /recipe/{recipeId}/note/{noteId}
- "Update a note?" -> PUT /recipe/{recipeId}/note/{noteId}
- "Delete a note?" -> DELETE /recipe/{recipeId}/note/{noteId}
- "List all notes?" -> GET /recipe/{recipeId}/notes
- "Create a note?" -> POST /recipe/{recipeId}/note
- "List all raves?" -> GET /recipes/raves
- "List all zap?" -> GET /recipe/{id}/zap
- "Get recipe details?" -> GET /recipe/{id}
- "Delete a recipe?" -> DELETE /recipe/{id}
- "Get recipe details?" -> GET /recipes/{id}
- "Get step details?" -> GET /recipe/steps/{id}
- "Create a step?" -> POST /recipe/post/step
- "Create a number?" -> POST /recipe/get/step/number
- "List all recipe?" -> GET /recipe/get/active/recipe
- "Create a step?" -> POST /recipe/get/saved/step
- "List all related?" -> GET /recipe/{recipeId}/related
- "Create a feedback?" -> POST /recipe/{recipeId}/feedback
- "List all random?" -> GET /recipes/random
- "List all top25random?" -> GET /recipes/top25random
- "List all recipes?" -> GET /recipes
- "List all categories?" -> GET /recipe/categories
- "Search autocomplete?" -> GET /recipe/autocomplete
- "Search mine?" -> GET /recipe/autocomplete/mine
- "Search all?" -> GET /recipe/autocomplete/all
- "Create a scan?" -> POST /recipe/scan
- "Create a recipe?" -> POST /recipe
- "List all recentviews?" -> GET /recipes/recentviews
- "Get review details?" -> GET /recipe/{recipeId}/review/{reviewId}
- "Update a review?" -> PUT /recipe/{recipeId}/review/{reviewId}
- "Delete a review?" -> DELETE /recipe/{recipeId}/review/{reviewId}
- "Get review details?" -> GET /recipe/review/{reviewId}
- "Update a review?" -> PUT /recipe/review/{reviewId}
- "List all review?" -> GET /recipe/{recipeId}/review
- "Create a review?" -> POST /recipe/{recipeId}/review
- "List all reviews?" -> GET /recipe/{recipeId}/reviews
- "List all replies?" -> GET /recipe/review/{reviewId}/replies
- "Create a reply?" -> POST /recipe/review/{reviewId}/replies
- "Update a reply?" -> PUT /recipe/review/replies/{replyId}
- "Delete a reply?" -> DELETE /recipe/review/replies/{replyId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
