---
name: listing-search
description: >-
  Use when the user wants to find for-sale (or sold) homes matching criteria in an
  area — location, price range, beds/baths, home type, status. Searches the right
  portal(s) with filters, paginates, and returns a ranked, de-duplicated listings
  table with source links. Triggers on "find houses in …", "search for 3-bed homes
  under $500k", "what's for sale in …", "show me recently sold homes near …".
allowed-tools: Bash, Read, Write, WebFetch
version: 1.0.0
homepage: https://www.realtyapi.io
repository: https://github.com/realtyapi/realtyapi-skills
license: MIT
metadata:
  openclaw:
    requires:
      env:
        - REALTYAPI_API_KEY
    primaryEnv: REALTYAPI_API_KEY
    homepage: https://www.realtyapi.io
    tags:
      - real-estate
      - search
      - listings
      - realtyapi
---

# Listing Search

## Overview

Find homes for sale (or recently sold) that match the user's criteria in a given
area, and return a clean, ranked shortlist with links — not raw JSON.

Use [`realtyapi-api`](../realtyapi-api/SKILL.md) for auth and endpoint discovery.

## When to Use

- "Find 3-bed houses under $600k in Austin."
- "What condos are for sale near this zip with a pool?"
- "Show recently sold homes on this street."
- Building a buyer's shortlist or a market scan for an area.

## Workflow

1. **Clarify criteria** if missing the essentials: location, buy vs. rent vs. sold,
   price range, beds/baths, home type. Don't over-ask — sensible defaults are fine.
2. **Pick the portal** for the location's market (catalog in `realtyapi-api`).
3. **Resolve the area** — use `autocomplete` / `locations` to turn a place name into
   the id/coordinates/polygon the search endpoint expects.
4. **Search with filters** — call `search/byaddress` | `search/bycoordinates` |
   `search/bypolygon` | `search/bymapbounds`. Read the endpoint's `openapi.json` for
   the exact filter params (price, beds, baths, status, home type, etc.).
5. **Paginate** to gather enough results (increment `page` or follow
   `nextPageCursor`) — but cap it and tell the user how many pages/credits you used.
6. **De-dupe and rank** by the user's priority (price, $/sqft, newest, size).
7. **Present** the table below. State the filters applied and the result count.

## Output Format

```markdown
# Listings: {criteria} in {area}

Portal: {portal} · Filters: {beds/baths/price/type/status} · {N} results ({pages} pages)

| # | Address | Price | Beds/Baths | Size | $/sqft | Status | Link |
|--:|---------|------:|-----------|-----:|-------:|--------|------|

## Notes
- Sorted by: {criterion}
- Standouts: {best value / newest / etc.}
- Excluded: {dupes / out-of-range, if any}
```

## Common Pitfalls

- Confirm **buy vs. rent vs. sold** — the wrong status filter returns the wrong set.
- One search covers one portal/market. Don't claim "all listings" — say which portal.
- Respect credits: each page is a request. Cap pagination and report what you used.
- Keep the source link for every row so the user can open the real listing.
