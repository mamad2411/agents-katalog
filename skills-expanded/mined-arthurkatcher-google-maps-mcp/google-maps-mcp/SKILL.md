---
name: google-maps-mcp
description: Google Maps MCP tools — places search, directions, geocoding, reverse geocoding, place details. Use for restaurants, coffee shops, landmarks, travel time, walking/driving routes, addresses, GPS coordinates, anything near a real-world location.
---

# Using the google-maps-mcp MCP server

This skill teaches you how to use the `google-maps-mcp` MCP server effectively when it's available in the session. The server exposes six Google Maps tools that hit the real Google Maps Platform APIs (Places API New, Directions API, Geocoding API).

## When to use this skill

Use the google-maps-mcp tools whenever the user's request involves real-world geographic data:

- **Place discovery**: "find", "show me", "recommend", "where can I get" + any business/landmark
- **Place details**: "reviews", "is it open", "do they deliver", "hours", "phone number", "website"
- **Directions/routing**: "how do I get to", "directions", "route", "how long", "driving time"
- **Coordinates**: "latitude", "longitude", "GPS coordinates", "coordinates of"
- **Addresses**: "address of", "what's at these coordinates", "where is this"
- **Proximity**: "nearby", "near me", "within", "closest", "walking distance"

Do NOT use these tools for: general geography trivia Claude already knows (capitals, populations), historical location questions, or non-location business questions.

## Which tool for which job

| User asks | Tool | Why |
|---|---|---|
| "find ramen in Tokyo" | `search_places` | Text search, business type + location |
| "what are the reviews of the first one?" | `get_place_details` | Need reviews + amenities for a specific place |
| "cafes within 500m of the Eiffel Tower" | `geocode` → `search_nearby` | No coordinates yet, need to geocode first |
| "cafes within 500m of 48.858,2.294" | `search_nearby` | Already have coordinates |
| "how do I walk from A to B?" | `get_directions` | Origin + destination + mode |
| "what are the coordinates of X?" | `geocode` | Address/landmark → lat/lng |
| "what's at 37.8199, -122.4783?" | `reverse_geocode` | Coordinates → address |

## Tool reference (quick)

### search_places
Text search. Input: `query` (str, required), `max_results` (int, default 10, max 20).
Returns: `query`, `total_results`, `places[]` with name, address, phone, website, rating, hours, location, google_maps_url.

### get_place_details
Rich details for a known place. Input: `place_id` (str, required — get this from a prior `search_places` result).
Returns: everything from search_places plus top 5 reviews, amenities (delivery, dine_in, takeout, outdoor_seating, reservable, live_music), editorial_summary.

### search_nearby
Radius search around coordinates. Input: `latitude` (float), `longitude` (float), `radius_meters` (int, default 1000, max 50000), `place_type` (str optional — "restaurant", "cafe", "bar", "hotel", "gas_station", "pharmacy", etc.), `max_results` (int).
Returns: center, radius_meters, place_type, places[] with same fields as search_places.

### get_directions
Step-by-step route. Input: `origin` (str — address, landmark, or "lat,lng"), `destination` (str, same), `mode` (str — "driving" default, "walking", "bicycling", "transit").
Returns: routes[] with legs[] containing distance, duration, duration_in_traffic (driving only), and steps[].

### geocode
Address → coordinates. Input: `address` (str).
Returns: formatted_address, latitude, longitude, place_id.

### reverse_geocode
Coordinates → address. Input: `latitude` (float), `longitude` (float).
Returns: formatted_address, place_id, address_components[].

## Common patterns — tool chaining

### Pattern 1: "Find cafes near the Eiffel Tower"
The user names a landmark but doesn't give coordinates. Two-step:
1. Call `geocode("Eiffel Tower, Paris")` → get latitude, longitude
2. Call `search_nearby(latitude=..., longitude=..., radius_meters=500, place_type="cafe")`
3. Present the results

### Pattern 2: "Tell me more about the first result"
After `search_places`, the user wants deeper info on one item:
1. Grab the `place_id` from the first element of `places[]`
2. Call `get_place_details(place_id=...)`
3. Present reviews, amenities, hours

### Pattern 3: "How long to walk from my hotel to the museum?"
Both strings can go directly to directions:
1. Call `get_directions(origin="Hotel Name, City", destination="Museum Name, City", mode="walking")`
2. Report total duration and distance from `routes[0].legs[0]`

### Pattern 4: "What's a good restaurant in this area?" (with coordinates)
If the user provides coordinates (lat,lng or context has them):
1. Call `search_nearby(latitude=..., longitude=..., radius_meters=1000, place_type="restaurant", max_results=5)`
2. For the most interesting result, call `get_place_details(place_id=...)` for reviews
3. Recommend based on rating, reviews, and amenities

## Presenting results to the user

**Do:**
- Lead with the most-relevant information first (name, why it's a match, rating, open-now status)
- Include the Google Maps URL so the user can tap through (the `google_maps_url` field)
- Mention the number of reviews alongside the rating ("4.7 stars from 1,200 reviews")
- For directions: state total time and distance up front, then offer step-by-step if the user wants it
- For multiple results: present 3–5 items as a compact list, not 10+
- Respect the user's locale — if they're asking in Spanish about "San Francisco", the places are still in English but your response should be in Spanish

**Don't:**
- Dump the entire raw JSON response
- Include every field when only a handful are relevant
- Return a bullet list of 20 places when the user asked for "a coffee shop"
- Make up details the API didn't return (don't invent reviews, phone numbers, or hours)

## Error handling

### `BILLING_DISABLED` / 403 Forbidden
The Google Cloud project backing the API key doesn't have billing enabled. Tell the user:
> "The Google Maps API returned a billing error — your API key's GCP project needs billing enabled. Go to https://console.cloud.google.com/billing, link a card (the $200/month free tier covers all normal use), wait 2-3 minutes for propagation, and try again."

### Empty `places` list
The search returned nothing. Don't pretend it returned something. Options:
1. Suggest broadening the query ("try 'cafes in San Francisco' instead of 'specialty coffee in SoMa'")
2. Suggest a larger radius if using `search_nearby`
3. Ask the user to clarify

### `No location found for this address`
Geocoding failed on an ambiguous input. Ask for more context (city? country?) or suggest a specific landmark.

### Network/timeout errors
The underlying httpx request failed. Surface the error, don't retry silently — let the user decide.

## Pitfalls

- **`search_nearby` needs real coordinates, not addresses.** If the user gives an address, call `geocode` first.
- **`get_place_details` needs a real `place_id` from a prior `search_places` call.** Don't fabricate place IDs.
- **Max 20 results per search.** If the user asks for "all coffee shops in Seattle", you can't return all — paginate or recommend narrowing.
- **Radius caps at 50,000 meters** (50 km) for `search_nearby`. Larger searches → use `search_places` with a text query.
- **Distances/durations are returned as human strings** ("1.2 km", "8 mins"), not numeric values. Don't try to do math on them directly.
- **Opening hours may be missing.** Not every place has `opening_hours` populated. Handle `None`.
- **Traffic-aware duration is only returned for driving mode**, and only if there's current traffic data for the route.

## Related files

- The MCP server source lives in the repo root. If you need to understand exact return shapes, read `src/google_maps_mcp/client.py` and `src/google_maps_mcp/tools.py`.
- For the API key setup walkthrough, see `README.md` in the repo root.
- For real usage examples with the OpenAI Agents SDK, see `examples/openai_agents_demo.py`.
