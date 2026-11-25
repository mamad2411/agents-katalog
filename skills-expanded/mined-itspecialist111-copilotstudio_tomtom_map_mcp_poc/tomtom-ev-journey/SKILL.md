---
name: tomtom-ev-journey
description: |
  Plans electric-vehicle journeys and finds charging stations using TomTom. Use when the user asks
  to "plan an EV trip", "route my electric car from A to B with charging stops", "find EV chargers
  near ...", "where can I charge", "fast/rapid charging on the way", or mentions battery range,
  connector types, or charging. Plans the EV route or finds chargers and hands off to the
  tomtom-live-map skill to show them.
license: Apache-2.0
metadata:
  author: ABS
  version: "1.0"
---

# TomTom EV Journey

## What this skill does

Handles electric-vehicle needs end to end:

- **EV route planning** with automatic charging-stop optimisation based on battery/charging params,
- **finding charging stations** near a place or along a route, with connector types and availability.

## Tools

- `tomtom-ev-routing` — long-distance EV routing that inserts charging stops to keep the battery
  within range. Accepts battery/charging parameters.
- `tomtom-ev-search` — find EV charging stations near a coordinate (connector types, power, availability).
- `tomtom-search-along-route` — chargers (or other POIs) along an existing route corridor.
- For visualisation, the **`render_live_map`** tool (chargers as `markers`, EV route as `route`).

## Workflow

1. **Resolve places** to coordinates with the `tomtom-location-search` skill (origin, destination,
   or the "near" anchor) — include city/country to avoid ambiguity.
2. **Charger search:** for "find chargers near X", use `tomtom-ev-search` around X with a sensible
   radius; report connector types and (if available) live availability.
3. **EV route:** for "plan my EV trip", use `tomtom-ev-routing` with any battery/charging details
   the user provides (current charge, usable capacity, min charge at arrival). Summarise the route
   and each recommended charging stop.
4. **Gather missing details politely.** If essential battery parameters are missing, proceed with
   sensible defaults and state the assumptions, or ask one concise clarifying question.
5. **Visualise.** Hand off to the **`tomtom-live-map`** skill: `render_live_map` with the EV `route`
   and charging stops as `markers` (use a `category` like "EV Charging").

## Output format

- For chargers: a table of stations.

  | Station | Connector(s) | Power | Availability | Approx. distance |
  |---------|--------------|-------|--------------|------------------|
  | … | CCS, Type 2 | 150 kW | 2/4 free | 1.2 km |

- For EV routes: total distance/time, then an ordered list of charging stops (where, why, suggested
  charge added).
- Then the **map** via `tomtom-live-map` showing the route and chargers.

## Tips & disambiguation

- Connector vocabulary: CCS, CHAdeMO, Type 2, Tesla; "rapid/fast" usually means ≥ 50 kW DC.
- Availability is real-time and may change; note this and let the user open the live map to explore.
- If the user just wants directions for a non-EV vehicle, use the `tomtom-route-planning` skill.
