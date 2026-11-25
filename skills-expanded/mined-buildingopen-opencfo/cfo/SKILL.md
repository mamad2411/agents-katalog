---
name: cfo
description: Find restaurants and food delivery options near a location. Searches delivery apps for restaurants, cross-references Google Maps ratings, and recommends the best options. Learns food preferences over time.
trigger_keywords: food, restaurant, delivery, order food, dumplings, momos, pizza, biryani, swiggy, zomato, wolt, ubereats, what to eat, hungry, lunch, dinner, cfo
user_invocable: true
---

# Chief Food Officer

You find the best food delivery options by searching delivery apps and cross-referencing Google Maps ratings.

## Prerequisites

- **Browser MCP** must be available (Playwright MCP or similar browser automation)
- Browser can access Google Maps
- Delivery platform accessible without login for browsing

## Workflow

### Step 1: Parse the Request

Extract from the user's query:
- **Dish/cuisine** (e.g., "momos", "pizza", "biryani", "ramen")
- **Location** (from user's preferences or query)
- **Party size** (default: 2)
- **Budget** (optional)
- **Dietary preferences** (default: no preference)

### Step 2: Read Preferences

Read `~/.claude/skills/cfo/references/preferences.md` to check:
- Known favorite restaurants
- Rating thresholds
- Cuisine preferences
- Usual budget range

### Step 3: Search Delivery App

The default platform is Swiggy (swiggy.com). Adapt these steps for your platform.

1. Navigate to the delivery platform
2. Set delivery location:
   - Click the location/address field
   - Type the location
   - Select the first autocomplete suggestion
   - Wait for page to reload with local restaurants
3. Search for the dish/cuisine:
   - Click the search bar
   - Type the dish/cuisine name
   - Press Enter or click search
   - Wait for results to load
4. Switch to "Restaurants" tab if available (not "Dishes")
5. Collect top 8-10 results:
   - Restaurant name
   - Rating (out of 5)
   - Delivery time (minutes)
   - Price for two
   - Cuisine tags
   - Any offers/discounts visible

**Tips for scraping delivery apps:**
- Use `browser_snapshot` to read page content, more reliable than screenshots
- Delivery apps load restaurants dynamically; scroll down if needed using `browser_evaluate` with `window.scrollBy(0, 800)`
- Look for rating in the snapshot text (usually like "4.3" near the restaurant name)
- Price for two is usually shown as "₹300 for two" or similar

### Step 4: Cross-reference Google Maps

For the **top 5 restaurants** (by app rating):

1. Open a new tab: `browser_tabs` with action "new"
2. Navigate to `https://www.google.com/maps/search/<restaurant name> <location>`
3. Take a snapshot to find:
   - Google Maps rating (out of 5)
   - Number of reviews
   - Any notable review highlights
4. Go back to the delivery app tab

### Step 5: Rank & Recommend

Create a comparison table sorted by combined score:
- **Combined score** = (App rating x 0.4) + (Google Maps rating x 0.4) + (review volume score x 0.2)
  - Review volume score: 4.5+ if >1000 reviews, 4.0 if >500, 3.5 if >200, 3.0 otherwise

Present the table:

```
| # | Restaurant | Cuisine | App  | Google (reviews) | Delivery | Price/2 | Score |
|---|-----------|---------|------|-----------------|----------|---------|-------|
| 1 | Name      | Type    | 4.5  | 4.4 (1.2k)      | 30 min   | ₹400    | 4.48  |
```

Highlight the **top pick** with a brief reason (e.g., "Best overall rating + fast delivery").

Apply preference adjustments:
- Boost restaurants matching known favorites
- Boost restaurants above user's rating threshold
- Flag if below user's usual budget or rating preferences

### Step 6: Offer Next Steps

Ask if the user wants to:
1. **Open the menu** on the delivery app (navigate to the restaurant page)
2. **See more options** (scroll for more results)
3. **Try a different cuisine/location**

### Step 7: Update Preferences

After the interaction, run the preferences update:

```bash
python3 ~/.claude/skills/cfo/scripts/update_prefs.py \
  --cuisine "<cuisine searched>" \
  --location "<location>" \
  --chosen "<restaurant chosen, if any>" \
  --party-size <N> \
  --budget "<budget range>"
```

This appends/updates entries in `references/preferences.md`.

## Error Handling

- **App not loading**: Try refreshing. If still broken, fall back to Google Maps search only.
- **Location not setting**: Try typing a more specific address.
- **No results**: Broaden the search (e.g., "Chinese" instead of "Szechuan dumplings").
- **Google Maps rate limit**: Skip cross-referencing, present delivery app results only with a note.

## Output Format

Keep the final recommendation **concise**, a table + 1-2 line recommendation. Example:

```
Top picks for ramen near Shibuya:

| # | Restaurant      | App  | Google (reviews) | Time  | Price/2  |
|---|----------------|------|-----------------|-------|----------|
| 1 | Fuunji         | 4.6  | 4.5 (2.1k)      | 20min | ¥1,800   |
| 2 | Afuri          | 4.4  | 4.3 (1.8k)      | 25min | ¥1,600   |
| 3 | Ichiran        | 4.3  | 4.1 (3.2k)      | 15min | ¥1,400   |

Top pick: Fuunji, highest combined rating, reasonable delivery time.
```

If sending via messaging (cfo.sh), strip markdown formatting and use plain text.
