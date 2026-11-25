---
name: tomtom-location-search
description: |
  Finds places and converts between addresses and coordinates using TomTom. Use when the user
  asks "where is...", "find ... near ...", "what's the address of ...", "geocode ...",
  "search for [restaurants/hotels/hospitals/shops] near ...", "what's at these coordinates",
  or needs precise lat/lon for a place. Resolves a place to coordinates and hands off to the
  tomtom-live-map skill to show results on a map.
license: Apache-2.0
metadata:
  author: ABS
  version: "1.0"
---

# TomTom Location Search

## What this skill does

Resolves locations both ways and finds nearby points of interest:

- **Geocode** a name/address → coordinates.
- **Reverse-geocode** coordinates → a readable address.
- **Search** for businesses/POIs (fuzzy text, by category, near a point, or within an area).

It produces precise coordinates that the other TomTom skills (routing, traffic, EV, live-map) rely on.

## Tools

- `tomtom-geocode` — address/place name → coordinates.
- `tomtom-reverse-geocode` — coordinates → address.
- `tomtom-fuzzy-search` — free-text search with typo tolerance ("thai food near Cardiff Castle").
- `tomtom-poi-search` — search by business/POI name or brand.
- `tomtom-poi-categories` — list available POI category codes when you need to filter precisely.
- `tomtom-nearby` — POIs within a radius of a coordinate.
- `tomtom-area-search` — POIs within a bounding box / area.

## Workflow

1. **Disambiguate the place.** Place names are often ambiguous. ALWAYS include city and country
   when the user implies them (e.g. search `"Cardiff Castle, Cardiff, Wales, UK"`, not just
   `"Cardiff Castle"`). If a result looks wrong (far from the expected region), re-query with more
   context or pass a country/region bias.
2. **Pick the right tool:**
   - Known address or landmark → `tomtom-geocode`.
   - "near X" with a category (restaurants, hotels, EV, hospitals) → geocode X first, then
     `tomtom-nearby` (or `tomtom-fuzzy-search` for free text).
   - Coordinates given → `tomtom-reverse-geocode`.
3. **Confirm the match.** Briefly state what was found (name + locality) so the user can catch a
   wrong hit early.
4. **Visualise.** Hand the resulting coordinates to the **`tomtom-live-map`** skill (call
   `render_live_map` with the places as `markers`) so the user sees them on a map.

## Output format

- A short answer line: the resolved place/address and its coordinates.
- For multi-result searches, a compact table:

  | # | Name | Address | Approx. distance |
  |---|------|---------|------------------|
  | 1 | … | … | … |

- Then the **map** via `tomtom-live-map` (pins for each result).

## Tips & disambiguation

- Coordinates are `lat, lon` decimal degrees.
- Prefer one precise query over many broad ones. Add city/country/postcode to narrow results.
- For "nearest" questions, geocode the anchor first, then use `tomtom-nearby` with a sensible radius
  (e.g. 1000–5000 m) and a small result limit.
- If the user gives coordinates, reverse-geocode them before reasoning about the place.
