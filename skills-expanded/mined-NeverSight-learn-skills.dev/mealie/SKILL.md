---
name: mealie
description: "Mealie recipe manager API: recipes, shopping lists, meal plans. Requires MEALIE_BASE_URL and MEALIE_API_KEY."
---

# Mealie API Skill

## Setup

```bash
# Environment variables required
export MEALIE_BASE_URL="https://mealie.example.com"  # with or without trailing slash
export MEALIE_API_KEY="your-api-key"

# Common patterns (set these for shorter commands)
AUTH="Authorization: Bearer $MEALIE_API_KEY"
API="${MEALIE_BASE_URL%/}/api"  # strips trailing slash, adds /api
```

## Authentication

```bash
# All requests require Bearer token
curl -H "Authorization: Bearer $MEALIE_API_KEY" "${API}/recipes"

# Using pre-set variables:
curl -H "$AUTH" "${API}/recipes"
```

---

# Recipes

| Action | Method | Endpoint | Body/Params |
|--------|--------|----------|-------------|
| List | GET | `/api/recipes` | `?page=1&perPage=50&search=term&categories=uuid1,uuid2&tags=uuid1,uuid2&orderBy=name&orderDirection=asc` |
| Get | GET | `/api/recipes/{slug}` | - |
| Create | POST | `/api/recipes` | `{"name": "Recipe Name"}` |
| Update | PUT | `/api/recipes/{slug}` | `{...fields}` |
| Patch | PATCH | `/api/recipes/{slug}` | `{...fields}` |
| Delete | DELETE | `/api/recipes/{slug}` | - |
| Duplicate | POST | `/api/recipes/{slug}/duplicate` | - |
| Import URL | POST | `/api/recipes/create/url` | `{"url": "https://..."}` |
| Import bulk | POST | `/api/recipes/create/url/bulk` | `{"urls": ["https://...", ...]}` |
| Import HTML/JSON | POST | `/api/recipes/create/html-or-json` | `{name, recipeIngredient[], recipeInstructions[]}` |
| Import ZIP | POST | `/api/recipes/create/zip` | `-F archive=@file.zip` |
| Import image | POST | `/api/recipes/create/image` | `-F images=@image.jpg` |
| Bulk delete | POST | `/api/recipes/bulk-actions/delete` | `["slug1", "slug2"]` |
| Bulk categorize | POST | `/api/recipes/bulk-actions/categorize` | `{recipes[], categories[]}` |
| Bulk tag | POST | `/api/recipes/bulk-actions/tag` | `{recipes[], tags[]}` |
| Test scrape | POST | `/api/recipes/test-scrape-url` | `{"url": "https://..."}` |

### Recipe Query Parameters

| Param | Type | Description |
|-------|------|-------------|
| `page`, `perPage` | int | Pagination (default: 1, 50) |
| `search` | string | Search term |
| `categories`, `tags`, `tools`, `foods` | UUID[] | Filter by IDs |
| `cookbook` | UUID | Filter by cookbook |
| `requireAllCategories`, `requireAllTags`, `requireAllTools`, `requireAllFoods` | bool | AND logic (default: false) |
| `orderBy`, `orderDirection` | string | Sort field and `asc`/`desc` |

### Examples

```bash
# List recipes
curl -sH "$AUTH" "${API}/recipes?perPage=10&search=pasta" | jq '.items[].name'

# Get recipe
curl -sH "$AUTH" "${API}/recipes/chicken-stir-fry" | jq '{name, recipeServings, recipeIngredient}'

# Create from URL
curl -sX POST -H "$AUTH" -H "Content-Type: application/json" \
  "${API}/recipes/create/url" \
  -d '{"url":"https://example.com/recipe"}' | jq '.slug'

# Update recipe
curl -sX PUT -H "$AUTH" -H "Content-Type: application/json" \
  "${API}/recipes/my-recipe" \
  -d '{"recipeServings": 6, "description": "Updated"}' | jq '.'
```

---

# Meal Plans

| Action | Method | Endpoint | Body/Params |
|--------|--------|----------|-------------|
| List | GET | `/api/households/mealplans` | `?start_date=2025-01-01&end_date=2025-01-07&page=1&perPage=30` |
| Today | GET | `/api/households/mealplans/today` | - |
| Random | GET | `/api/households/mealplans/random` | - |
| Create | POST | `/api/households/mealplans` | `{date, entryType, title?, text?, recipeId?}` |
| Update | PUT | `/api/households/mealplans/{id}` | `{...fields}` |
| Delete | DELETE | `/api/households/mealplans/{id}` | - |
| Rules list | GET | `/api/households/mealplans/rules` | - |
| Rules create | POST | `/api/households/mealplans/rules` | `{day, entryType, tags[]}` |
| Rules delete | DELETE | `/api/households/mealplans/rules/{id}` | - |

### Meal Entry Types
`breakfast` | `lunch` | `dinner` | `side` | `snack` | `drink` | `dessert`

### Examples

```bash
# Create meal plan entry
curl -sX POST -H "$AUTH" -H "Content-Type: application/json" \
  "${API}/households/mealplans" \
  -d '{"date":"2025-01-20","entryType":"dinner","recipeId":"uuid-here"}' | jq '.'

# Get week's meal plans
curl -sH "$AUTH" "${API}/households/mealplans?start_date=2025-01-20&end_date=2025-01-27" | jq '.items[]'
```

---

# Shopping Lists

| Action | Method | Endpoint | Body |
|--------|--------|----------|------|
| List | GET | `/api/households/shopping/lists` | - |
| Get | GET | `/api/households/shopping/lists/{id}` | - |
| Create | POST | `/api/households/shopping/lists` | `{name?}` |
| Update | PUT | `/api/households/shopping/lists/{id}` | `{name?}` |
| Delete | DELETE | `/api/households/shopping/lists/{id}` | - |
| Add recipe | POST | `/api/households/shopping/lists/{id}/recipe/{recipeId}` | - |
| Remove recipe | DELETE | `/api/households/shopping/lists/{id}/recipe/{recipeId}` | - |

---

# Shopping Items

| Action | Method | Endpoint | Body |
|--------|--------|----------|------|
| List | GET | `/api/households/shopping/items` | - |
| Create | POST | `/api/households/shopping/items` | `{shoppingListId, note?, quantity?, checked?, position?, foodId?, unitId?, labelId?}` |
| Update | PUT | `/api/households/shopping/items/{id}` | `{...fields}` |
| Delete | DELETE | `/api/households/shopping/items/{id}` | - |
| Bulk create | POST | `/api/households/shopping/items/create-bulk` | `{shoppingListId, items[]}` |
| Bulk delete | DELETE | `/api/households/shopping/items?ids=uuid1,uuid2` | - |

### Examples

```bash
# Create shopping item
curl -sX POST -H "$AUTH" -H "Content-Type: application/json" \
  "${API}/households/shopping/items" \
  -d '{"shoppingListId":"uuid","note":"2 cups flour","quantity":2}' | jq '.'

# Check item
curl -sX PUT -H "$AUTH" -H "Content-Type: application/json" \
  "${API}/households/shopping/items/{id}" \
  -d '{"checked":true}' | jq '.'
```

---

# Cookbooks

| Action | Method | Endpoint | Body |
|--------|--------|----------|------|
| List | GET | `/api/households/cookbooks` | - |
| Get | GET | `/api/households/cookbooks/{id}` | - |
| Create | POST | `/api/households/cookbooks` | `{name, description?, categories[]?, tags[]?}` |
| Update | PUT | `/api/households/cookbooks/{id}` | `{...fields}` |
| Delete | DELETE | `/api/households/cookbooks/{id}` | - |

---

# Organizers (Categories, Tags, Tools)

| Resource | List (GET) | Create (POST) | Get by Slug (GET) |
|----------|------------|---------------|-------------------|
| Categories | `/api/organizers/categories` | `{name}` | `/api/organizers/categories/slug/{slug}` |
| Tags | `/api/organizers/tags` | `{name}` | `/api/organizers/tags/slug/{slug}` |
| Tools | `/api/organizers/tools` | `{name}` | `/api/organizers/tools/slug/{slug}` |

---

# Foods & Units

| Action | Food Endpoint | Unit Endpoint | Body |
|--------|---------------|----------------|------|
| List | GET `/api/foods` | GET `/api/units` | - |
| Create | POST `/api/foods` | POST `/api/units` | `{name}` |
| Get | GET `/api/foods/{id}` | GET `/api/units/{id}` | - |
| Update | PUT `/api/foods/{id}` | PUT `/api/units/{id}` | `{name}` |
| Delete | DELETE `/api/foods/{id}` | DELETE `/api/units/{id}` | - |

---

# Labels (Shopping Categories)

```bash
# List labels
curl -sH "$AUTH" "${API}/groups/labels" | jq '.items[].name'

# Create label
curl -sX POST -H "$AUTH" -H "Content-Type: application/json" \
  "${API}/groups/labels" \
  -d '{"name":"Produce","color":"#4CAF50"}' | jq '.'
```

---

# Ingredient Parser

```bash
# Parse single ingredient
curl -sX POST -H "$AUTH" -H "Content-Type: application/json" \
  "${API}/parser/ingredient" \
  -d '{"ingredient":"2 cups all-purpose flour"}' | jq '.'

# Parse multiple
curl -sX POST -H "$AUTH" -H "Content-Type: application/json" \
  "${API}/parser/ingredients" \
  -d '["2 cups flour","1 tsp salt","3 eggs"]' | jq '.'
```

---

# Users & Households

| Action | Endpoint |
|--------|----------|
| Current user | GET `/api/users/self` |
| Current household | GET `/api/households/self` |
| Group info | GET `/api/groups/self` |
| Favorites | GET `/api/users/self/favorites` |
| Add favorite | POST `/api/users/{id}/favorites/{slug}` |
| Remove favorite | DELETE `/api/users/{id}/favorites/{slug}` |

---

# Recipe Timeline

```bash
# List events
curl -sH "$AUTH" "${API}/recipes/timeline/events" | jq '.'

# Create event
curl -sX POST -H "$AUTH" -H "Content-Type: application/json" \
  "${API}/recipes/timeline/events" \
  -d '{"recipeId":"uuid","subject":"Made this","eventType":"made"}' | jq '.'
```

---

# Bulk Operations

```bash
# Export recipes
curl -sX POST -H "$AUTH" -H "Content-Type: application/json" \
  "${API}/recipes/bulk-actions/export" \
  -d '["slug1","slug2"]' | jq '.exportId'

# Download export
curl -sH "$AUTH" "${API}/recipes/bulk-actions/export/{exportId}/download" -o export.zip
```

---

# Shared Recipes

```bash
# List shared
curl -sH "$AUTH" "${API}/shared/recipes" | jq '.'

# Access by token
curl -sH "$AUTH" "${API}/recipes/shared/{tokenId}" | jq '.'
```

---

# Common Workflows

## Add Recipe to Meal Plan + Shopping List

```bash
RECIPE_ID="your-recipe-uuid"
DATE="2025-01-20"

# Get shopping list ID
LIST_ID=$(curl -sH "$AUTH" "${API}/households/shopping/lists?perPage=1" | jq -r '.items[0].id')

# Add to meal plan
curl -sX POST -H "$AUTH" -H "Content-Type: application/json" \
  "${API}/households/mealplans" \
  -d "{\"date\":\"$DATE\",\"entryType\":\"dinner\",\"recipeId\":\"$RECIPE_ID\"}" | jq '.'

# Add ingredients to shopping list
curl -sX POST -H "$AUTH" "${API}/households/shopping/lists/$LIST_ID/recipe/$RECIPE_ID" | jq '.'
```

## Search & Filter

```bash
# Search recipes
curl -sH "$AUTH" "${API}/recipes?search=pasta&perPage=10" | jq '.items[].slug'

# Filter by tag
curl -sH "$AUTH" "${API}/recipes?tags=tag-uuid&requireAllTags=true" | jq '.total'
```

---

# Error Handling

```bash
response=$(curl -s -w "\n%{http_code}" -H "$AUTH" "${API}/recipes/invalid")
code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

[ "$code" != "200" ] && { echo "Error $code"; echo "$body" | jq '.detail'; }
```

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 422 | Validation Error |

---

# API Reference

```bash
# OpenAPI spec
curl -s "${MEALIE_BASE_URL%/}/openapi.json" | jq '.info'

# Swagger UI (browser)
# ${MEALIE_BASE_URL%/}/docs
```

**Total Endpoints:** 170 | **API Version:** v3.17.0