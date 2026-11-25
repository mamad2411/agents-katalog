---
name: entur
description: Look up public transit travel times and routes in Norway using the Entur APIs. Use when the user asks about travel time, transit routes, how to get somewhere, or distance between locations in Norway. Triggers on "travel time from X to Y", "how long from X to Y", "reisetid fra X til Y", "transit from X to Y", "kollektivt fra X til Y", /entur, or any question about getting between two places via public transport in Norway.
---

# Entur Transit Lookup

Look up public transit routes and travel times anywhere in Norway via Entur's open APIs. Uses curl via Bash.

## Known Location Shortcuts

| Shortcut | Address | Coordinates |
|----------|---------|-------------|
| home, hjemme | Sandakerveien 22E, Oslo | 59.934173, 10.760459 |
| office, kontoret, HQ | Torggata 4, Oslo | 59.913795, 10.747224 |

## Workflow

### Step 1: Resolve locations to coordinates

If the user provides a known shortcut, use the hardcoded coordinates above. Otherwise, geocode with this fallback chain:

**1a. Nominatim (best for addresses AND venue/business names):**

```bash
curl -s 'https://nominatim.openstreetmap.org/search?q=<URL_ENCODED_QUERY>&format=json&limit=1&countrycodes=no' \
  -H 'User-Agent: magnus-claude-code/1.0'
```

Extract: `[0].lat` and `[0].lon`. Verify `display_name` looks correct (not a different city).

Rate limit: max 1 request/second. For bulk lookups, add `sleep 1` between calls or use a single Python script with 1s delays.

**1b. Entur geocoder (fallback, best for transit stop names like "Hasle", "Jernbanetorget"):**

```bash
curl -s 'https://api.entur.io/geocoder/v1/autocomplete?text=<URL_ENCODED_QUERY>&size=1&lang=no' \
  -H 'ET-Client-Name: magnus-claude-code'
```

Extract: `features[0].geometry.coordinates` (returns `[longitude, latitude]`, note the order).

**1c. If both fail, ask the user for the street address.**

### Step 2: Query journey planner

```bash
curl -s -X POST 'https://api.entur.io/journey-planner/v3/graphql' \
  -H 'ET-Client-Name: magnus-claude-code' \
  -H 'Content-Type: application/json' \
  -d '{"query": "{ trip( from: { coordinates: { latitude: <FROM_LAT>, longitude: <FROM_LON> } } to: { coordinates: { latitude: <TO_LAT>, longitude: <TO_LON> } } numTripPatterns: 3 ) { tripPatterns { duration walkDistance legs { mode fromPlace { name } toPlace { name } expectedStartTime expectedEndTime duration line { publicCode name } } } } }" }'
```

To query for a specific departure time, add `dateTime: \"<ISO8601>\"` inside the `trip()` arguments:

```
trip( from: {...} to: {...} dateTime: "2026-04-21T17:00:00+02:00" numTripPatterns: 3 )
```

### Step 3: Format output

Present results concisely. For each trip pattern:

- **Total time**: `duration` field (in seconds, convert to minutes)
- **Walking**: `walkDistance` field (in meters)
- **Route**: list each leg as `mode line from -> to (time)`

Example output format:

**Option 1: 19 min** (5 min walk)
Walk to Torshov -> Tram 12 to Storgata (11 min) -> Walk to destination (4 min)

**Option 2: 22 min** (4 min walk)
Walk to Torshov -> Tram 17 to Stortorvet (13 min) -> Walk to destination (5 min)

## Notes

- Nominatim returns `lat`/`lon` as strings. Cast to float before using in journey planner.
- Entur geocoder returns `[lon, lat]` (GeoJSON order). Journey planner expects `latitude:` and `longitude:` separately.
- Duration is in seconds. Divide by 60 for minutes.
- All APIs are public and free. Nominatim requires a `User-Agent` header. Entur requires `ET-Client-Name`.
- For bulk lookups: Entur has no rate limit (parallelize freely). Nominatim allows max 1 req/s (use sequential calls with delays).
