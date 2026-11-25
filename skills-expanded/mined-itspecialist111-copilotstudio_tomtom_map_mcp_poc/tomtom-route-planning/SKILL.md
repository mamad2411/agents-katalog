---
name: tomtom-route-planning
description: |
  Plans driving, truck, cycling, and walking routes with TomTom. Use when the user asks to
  "get directions", "plan a route from A to B", "how do I drive/walk/cycle to ...",
  "how long does it take to get to ...", "fastest/shortest route", "multi-stop trip",
  "optimise the order of stops", or "how far can I get in 30 minutes". Calculates the route and
  hands off to the tomtom-live-map skill to draw it (with optional live traffic).
license: Apache-2.0
metadata:
  author: ABS
  version: "1.0"
---

# TomTom Route Planning

## What this skill does

Calculates routes and travel reachability, then visualises them:

- point-to-point and **multi-stop** routes (car, truck, bicycle, pedestrian),
- **reachable range** ("how far in 30 min / 50 km"),
- POIs **along a route** corridor (e.g. fuel or food on the way).

## Tools

- `tomtom-routing` — calculate a route between an origin and a destination, including via points.
  Returns distance, travel time, and geometry.
- `tomtom-reachable-range` — isochrone/isodistance: the area reachable within a time or distance budget.
- `tomtom-search-along-route` — find POIs within a detour distance of a route.
- For drawing, the **`render_live_map`** tool's `route` input (road-following) — or
  `tomtom-dynamic-map` with `routePlans` for several routes on one image.

## Workflow

1. **Resolve endpoints to coordinates.** Use the `tomtom-location-search` skill to geocode the
   origin, destination, and any stops (include city/country to avoid ambiguous matches).
2. **Calculate the route** with `tomtom-routing`. State the key facts: total distance and estimated
   travel time; mention the travel mode used (default car).
3. **Multi-stop:** pass the stops as waypoints. If the user wants the best visiting order, ask the
   routing tool to optimise the waypoint order, then report the optimised sequence.
4. **Coverage questions** ("how far can I get…"): use `tomtom-reachable-range`.
5. **On-the-way searches:** use `tomtom-search-along-route` with a max detour.
6. **Visualise.** Hand the route to the **`tomtom-live-map`** skill — call `render_live_map` with
   the `route` (origin/destination/waypoints) and set `traffic: true` when traffic matters.

## Output format

- A summary line: **distance**, **estimated time**, **mode** (and optimised stop order if relevant).
- Optional turn-by-turn highlights only if the user asks.
- Then the **map** via `tomtom-live-map`, showing the route (with traffic overlay when requested).

## Tips & disambiguation

- Confirm travel mode if unclear (car vs walking changes time and path significantly).
- Travel times are estimates; set `traffic: true` on the map for current conditions, and use the
  `tomtom-live-traffic` skill if the user asks specifically about incidents/delays.
- For long EV trips that need charging stops, use the `tomtom-ev-journey` skill instead.
- Keep waypoints in the order the user states unless they explicitly ask for optimisation.
