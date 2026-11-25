---
name: local-market-scout
description: Discover and compare local businesses in a city or region using multiple Outscraper MCP tools. Use when an agent needs to find places, rank them by ratings or review volume, inspect reviews, and summarize local market patterns for sales, partnerships, market research, or competitive scouting.
---

# Local Market Scout

Use this skill to evaluate a local market in a practical, business-first way.

## Workflow

1. Start with `google_maps_search` to find businesses in the target city or category.
2. Keep only the most relevant places by rating, review count, and business fit.
3. If the user needs deeper insight, call `google_maps_reviews` for the shortlisted places.
4. Summarize:
   - strongest businesses
   - common customer expectations
   - obvious market gaps

## Recommended Inputs

- location
- category
- ideal review threshold
- whether the user wants just discovery or review analysis too

## Preferred Tool Pattern

### Step 1. Discovery

Use `google_maps_search`.

Good arguments:

```json
{
  "query": ["bars kyiv ukraine"],
  "limit": 20,
  "language": "en",
  "region": "ua",
  "fields": ["name", "full_address", "rating", "reviews", "place_id"],
  "execution_mode": "sync"
}
```

### Step 2. Review Analysis

Use `google_maps_reviews` on the shortlisted `place_id` values.

```json
{
  "query": ["PLACE_ID_1", "PLACE_ID_2"],
  "reviews_limit": 40,
  "sort": "newest",
  "language": "en",
  "execution_mode": "sync"
}
```

## Output Style

Return:

- top candidates
- one-paragraph market summary
- review-driven insights if review analysis was requested

Do not dump raw records unless the user explicitly asks for them.
