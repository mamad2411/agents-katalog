---
name: spoonacular-api
description: "spoonacular API skill. Use when working with spoonacular for recipes, food, mealplanner. Covers 99 endpoints."
version: 1.0.0
generator: lapsh
---

# spoonacular API
API version: 1.1

## Auth
ApiKey x-api-key in header

## Base URL
https://api.spoonacular.com

## Setup
1. Set your API key in the appropriate header
2. GET /recipes/complexSearch -- verify access
3. POST /recipes/visualizeTaste -- create first visualizeTaste

## Endpoints

99 endpoints across 4 groups. See references/api-spec.lap for full details.

### recipes
| Method | Path | Description |
|--------|------|-------------|
| GET | /recipes/complexSearch | Search Recipes |
| GET | /recipes/findByIngredients | Search Recipes by Ingredients |
| GET | /recipes/findByNutrients | Search Recipes by Nutrients |
| GET | /recipes/{id}/information | Get Recipe Information |
| GET | /recipes/informationBulk | Get Recipe Information Bulk |
| GET | /recipes/{id}/similar | Get Similar Recipes |
| GET | /recipes/random | Get Random Recipes |
| GET | /recipes/autocomplete | Autocomplete Recipe Search |
| GET | /recipes/{id}/tasteWidget.json | Taste by ID |
| GET | /recipes/{id}/tasteWidget.png | Recipe Taste by ID Image |
| GET | /recipes/{id}/equipmentWidget.json | Equipment by ID |
| GET | /recipes/{id}/equipmentWidget.png | Equipment by ID Image |
| GET | /recipes/{id}/priceBreakdownWidget.json | Price Breakdown by ID |
| GET | /recipes/{id}/priceBreakdownWidget.png | Price Breakdown by ID Image |
| GET | /recipes/{id}/ingredientWidget.json | Ingredients by ID |
| GET | /recipes/{id}/ingredientWidget.png | Ingredients by ID Image |
| GET | /recipes/{id}/nutritionWidget.json | Nutrition by ID |
| GET | /recipes/{id}/nutritionWidget.png | Recipe Nutrition by ID Image |
| GET | /recipes/{id}/nutritionLabel | Recipe Nutrition Label Widget |
| GET | /recipes/{id}/nutritionLabel.png | Recipe Nutrition Label Image |
| GET | /recipes/{id}/analyzedInstructions | Get Analyzed Recipe Instructions |
| GET | /recipes/extract | Extract Recipe from Website |
| GET | /recipes/{id}/ingredientWidget | Ingredients by ID Widget |
| GET | /recipes/{id}/tasteWidget | Recipe Taste by ID Widget |
| GET | /recipes/{id}/equipmentWidget | Equipment by ID Widget |
| GET | /recipes/{id}/priceBreakdownWidget | Price Breakdown by ID Widget |
| POST | /recipes/visualizeTaste | Recipe Taste Widget |
| POST | /recipes/visualizeNutrition | Recipe Nutrition Widget |
| POST | /recipes/visualizePriceEstimator | Price Breakdown Widget |
| POST | /recipes/visualizeEquipment | Equipment Widget |
| POST | /recipes/analyze | Analyze Recipe |
| GET | /recipes/{id}/summary | Summarize Recipe |
| GET | /recipes/{id}/card | Create Recipe Card |
| POST | /recipes/visualizeRecipe | Create Recipe Card |
| POST | /recipes/analyzeInstructions | Analyze Recipe Instructions |
| POST | /recipes/cuisine | Classify Cuisine |
| GET | /recipes/queries/analyze | Analyze a Recipe Search Query |
| GET | /recipes/convert | Convert Amounts |
| POST | /recipes/parseIngredients | Parse Ingredients |
| GET | /recipes/{id}/nutritionWidget | Recipe Nutrition by ID Widget |
| POST | /recipes/visualizeIngredients | Ingredients Widget |
| GET | /recipes/guessNutrition | Guess Nutrition by Dish Name |
| GET | /recipes/quickAnswer | Quick Answer |

### food
| Method | Path | Description |
|--------|------|-------------|
| GET | /food/ingredients/{id}/information | Get Ingredient Information |
| GET | /food/ingredients/{id}/amount | Compute Ingredient Amount |
| POST | /food/ingredients/glycemicLoad | Compute Glycemic Load |
| GET | /food/ingredients/autocomplete | Autocomplete Ingredient Search |
| GET | /food/ingredients/search | Ingredient Search |
| GET | /food/ingredients/substitutes | Get Ingredient Substitutes |
| GET | /food/ingredients/{id}/substitutes | Get Ingredient Substitutes by ID |
| GET | /food/products/search | Search Grocery Products |
| GET | /food/products/upc/{upc} | Search Grocery Products by UPC |
| GET | /food/customFoods/search | Search Custom Foods |
| GET | /food/products/{id} | Get Product Information |
| GET | /food/products/upc/{upc}/comparable | Get Comparable Products |
| GET | /food/products/suggest | Autocomplete Product Search |
| GET | /food/products/{id}/nutritionWidget | Product Nutrition by ID Widget |
| GET | /food/products/{id}/nutritionWidget.png | Product Nutrition by ID Image |
| GET | /food/products/{id}/nutritionLabel | Product Nutrition Label Widget |
| GET | /food/products/{id}/nutritionLabel.png | Product Nutrition Label Image |
| POST | /food/products/classify | Classify Grocery Product |
| POST | /food/products/classifyBatch | Classify Grocery Product Bulk |
| POST | /food/ingredients/map | Map Ingredients to Grocery Products |
| GET | /food/menuItems/suggest | Autocomplete Menu Item Search |
| GET | /food/menuItems/search | Search Menu Items |
| GET | /food/menuItems/{id} | Get Menu Item Information |
| GET | /food/menuItems/{id}/nutritionWidget | Menu Item Nutrition by ID Widget |
| GET | /food/menuItems/{id}/nutritionWidget.png | Menu Item Nutrition by ID Image |
| GET | /food/menuItems/{id}/nutritionLabel | Menu Item Nutrition Label Widget |
| GET | /food/menuItems/{id}/nutritionLabel.png | Menu Item Nutrition Label Image |
| GET | /food/restaurants/search | Search Restaurants |
| GET | /food/wine/dishes | Dish Pairing for Wine |
| GET | /food/wine/pairing | Wine Pairing |
| GET | /food/wine/description | Wine Description |
| GET | /food/wine/recommendation | Wine Recommendation |
| GET | /food/images/classify | Image Classification by URL |
| GET | /food/images/analyze | Image Analysis by URL |
| POST | /food/detect | Detect Food in Text |
| GET | /food/site/search | Search Site Content |
| GET | /food/search | Search All Food |
| GET | /food/videos/search | Search Food Videos |
| GET | /food/jokes/random | Random Food Joke |
| GET | /food/trivia/random | Random Food Trivia |
| GET | /food/converse | Talk to Chatbot |
| GET | /food/converse/suggest | Conversation Suggests |

### mealplanner
| Method | Path | Description |
|--------|------|-------------|
| GET | /mealplanner/generate | Generate Meal Plan |
| GET | /mealplanner/{username}/week/{start-date} | Get Meal Plan Week |
| DELETE | /mealplanner/{username}/day/{date} | Clear Meal Plan Day |
| POST | /mealplanner/{username}/items | Add to Meal Plan |
| DELETE | /mealplanner/{username}/items/{id} | Delete from Meal Plan |
| GET | /mealplanner/{username}/templates | Get Meal Plan Templates |
| POST | /mealplanner/{username}/templates | Add Meal Plan Template |
| GET | /mealplanner/{username}/templates/{id} | Get Meal Plan Template |
| DELETE | /mealplanner/{username}/templates/{id} | Delete Meal Plan Template |
| GET | /mealplanner/{username}/shopping-list | Get Shopping List |
| POST | /mealplanner/{username}/shopping-list/{start-date}/{end-date} | Generate Shopping List |
| POST | /mealplanner/{username}/shopping-list/items | Add to Shopping List |
| DELETE | /mealplanner/{username}/shopping-list/items/{id} | Delete from Shopping List |

### users
| Method | Path | Description |
|--------|------|-------------|
| POST | /users/connect | Connect User |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search complexSearch?" -> GET /recipes/complexSearch
- "List all findByIngredients?" -> GET /recipes/findByIngredients
- "List all findByNutrients?" -> GET /recipes/findByNutrients
- "List all information?" -> GET /recipes/{id}/information
- "List all informationBulk?" -> GET /recipes/informationBulk
- "List all similar?" -> GET /recipes/{id}/similar
- "List all random?" -> GET /recipes/random
- "Search autocomplete?" -> GET /recipes/autocomplete
- "List all tasteWidget.json?" -> GET /recipes/{id}/tasteWidget.json
- "List all tasteWidget.png?" -> GET /recipes/{id}/tasteWidget.png
- "List all equipmentWidget.json?" -> GET /recipes/{id}/equipmentWidget.json
- "List all equipmentWidget.png?" -> GET /recipes/{id}/equipmentWidget.png
- "List all priceBreakdownWidget.json?" -> GET /recipes/{id}/priceBreakdownWidget.json
- "List all priceBreakdownWidget.png?" -> GET /recipes/{id}/priceBreakdownWidget.png
- "List all ingredientWidget.json?" -> GET /recipes/{id}/ingredientWidget.json
- "List all ingredientWidget.png?" -> GET /recipes/{id}/ingredientWidget.png
- "List all nutritionWidget.json?" -> GET /recipes/{id}/nutritionWidget.json
- "List all nutritionWidget.png?" -> GET /recipes/{id}/nutritionWidget.png
- "List all nutritionLabel?" -> GET /recipes/{id}/nutritionLabel
- "List all nutritionLabel.png?" -> GET /recipes/{id}/nutritionLabel.png
- "List all analyzedInstructions?" -> GET /recipes/{id}/analyzedInstructions
- "List all extract?" -> GET /recipes/extract
- "List all ingredientWidget?" -> GET /recipes/{id}/ingredientWidget
- "List all tasteWidget?" -> GET /recipes/{id}/tasteWidget
- "List all equipmentWidget?" -> GET /recipes/{id}/equipmentWidget
- "List all priceBreakdownWidget?" -> GET /recipes/{id}/priceBreakdownWidget
- "Create a visualizeTaste?" -> POST /recipes/visualizeTaste
- "Create a visualizeNutrition?" -> POST /recipes/visualizeNutrition
- "Create a visualizePriceEstimator?" -> POST /recipes/visualizePriceEstimator
- "Create a visualizeEquipment?" -> POST /recipes/visualizeEquipment
- "Create a analyze?" -> POST /recipes/analyze
- "List all summary?" -> GET /recipes/{id}/summary
- "List all card?" -> GET /recipes/{id}/card
- "Create a visualizeRecipe?" -> POST /recipes/visualizeRecipe
- "Create a analyzeInstruction?" -> POST /recipes/analyzeInstructions
- "Create a cuisine?" -> POST /recipes/cuisine
- "Search analyze?" -> GET /recipes/queries/analyze
- "List all convert?" -> GET /recipes/convert
- "Create a parseIngredient?" -> POST /recipes/parseIngredients
- "List all nutritionWidget?" -> GET /recipes/{id}/nutritionWidget
- "Create a visualizeIngredient?" -> POST /recipes/visualizeIngredients
- "List all guessNutrition?" -> GET /recipes/guessNutrition
- "List all information?" -> GET /food/ingredients/{id}/information
- "List all amount?" -> GET /food/ingredients/{id}/amount
- "Create a glycemicLoad?" -> POST /food/ingredients/glycemicLoad
- "Search autocomplete?" -> GET /food/ingredients/autocomplete
- "Search search?" -> GET /food/ingredients/search
- "List all substitutes?" -> GET /food/ingredients/substitutes
- "List all substitutes?" -> GET /food/ingredients/{id}/substitutes
- "Search search?" -> GET /food/products/search
- "Get upc details?" -> GET /food/products/upc/{upc}
- "Search search?" -> GET /food/customFoods/search
- "Get product details?" -> GET /food/products/{id}
- "List all comparable?" -> GET /food/products/upc/{upc}/comparable
- "Search suggest?" -> GET /food/products/suggest
- "List all nutritionWidget?" -> GET /food/products/{id}/nutritionWidget
- "List all nutritionWidget.png?" -> GET /food/products/{id}/nutritionWidget.png
- "List all nutritionLabel?" -> GET /food/products/{id}/nutritionLabel
- "List all nutritionLabel.png?" -> GET /food/products/{id}/nutritionLabel.png
- "Create a classify?" -> POST /food/products/classify
- "Create a classifyBatch?" -> POST /food/products/classifyBatch
- "Create a map?" -> POST /food/ingredients/map
- "Search suggest?" -> GET /food/menuItems/suggest
- "Search search?" -> GET /food/menuItems/search
- "Get menuItem details?" -> GET /food/menuItems/{id}
- "List all nutritionWidget?" -> GET /food/menuItems/{id}/nutritionWidget
- "List all nutritionWidget.png?" -> GET /food/menuItems/{id}/nutritionWidget.png
- "List all nutritionLabel?" -> GET /food/menuItems/{id}/nutritionLabel
- "List all nutritionLabel.png?" -> GET /food/menuItems/{id}/nutritionLabel.png
- "List all generate?" -> GET /mealplanner/generate
- "Get week details?" -> GET /mealplanner/{username}/week/{start-date}
- "Delete a day?" -> DELETE /mealplanner/{username}/day/{date}
- "Create a item?" -> POST /mealplanner/{username}/items
- "Delete a item?" -> DELETE /mealplanner/{username}/items/{id}
- "List all templates?" -> GET /mealplanner/{username}/templates
- "Create a template?" -> POST /mealplanner/{username}/templates
- "Get template details?" -> GET /mealplanner/{username}/templates/{id}
- "Delete a template?" -> DELETE /mealplanner/{username}/templates/{id}
- "List all shopping-list?" -> GET /mealplanner/{username}/shopping-list
- "Create a connect?" -> POST /users/connect
- "Create a item?" -> POST /mealplanner/{username}/shopping-list/items
- "Delete a item?" -> DELETE /mealplanner/{username}/shopping-list/items/{id}
- "Search search?" -> GET /food/restaurants/search
- "List all dishes?" -> GET /food/wine/dishes
- "List all pairing?" -> GET /food/wine/pairing
- "List all description?" -> GET /food/wine/description
- "List all recommendation?" -> GET /food/wine/recommendation
- "List all classify?" -> GET /food/images/classify
- "List all analyze?" -> GET /food/images/analyze
- "Search quickAnswer?" -> GET /recipes/quickAnswer
- "Create a detect?" -> POST /food/detect
- "Search search?" -> GET /food/site/search
- "Search search?" -> GET /food/search
- "Search search?" -> GET /food/videos/search
- "List all random?" -> GET /food/jokes/random
- "List all random?" -> GET /food/trivia/random
- "List all converse?" -> GET /food/converse
- "Search suggest?" -> GET /food/converse/suggest
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
