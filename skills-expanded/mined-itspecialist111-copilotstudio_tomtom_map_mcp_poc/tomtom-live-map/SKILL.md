---
name: tomtom-live-map
description: |
  Renders TomTom maps inside the conversation: an inline map image plus a link to a
  live, interactive map (pan, zoom, live traffic). Use whenever the user asks to
  "show on a map", "render a map", "display a live map", "visualise this location/route",
  "map these places", "show me where", or after finding coordinates with the search,
  routing, traffic, or EV skills. This is the visualisation step other TomTom skills
  hand off to.
license: Apache-2.0
metadata:
  author: ABS
  version: "1.0"
---

# TomTom Live Map

## What this skill does

Turns coordinates, places, and routes into a visual the user can see and explore. It calls
the **`render_live_map`** connector tool, which returns two things in one response:

1. an **inline map image** (rendered server-side by TomTom — markers, routes, traffic), and
2. a **link to the live, interactive map** (full pan, zoom, and a live-traffic overlay).

This is the rendering hub for the TomTom plugin. The location, routing, traffic, and EV skills
all finish by calling this skill so the user always gets a map, not just text.

## When to use it

- The user explicitly asks to see, show, render, display, map, or visualise something.
- You have just produced coordinates, a route, traffic incidents, or charging stops with another
  TomTom tool and a map would make the answer clearer.

## Tools

- **`render_live_map`** — the preferred rendering tool. Inputs:
  - `title` — caption above the map.
  - `markers` — array of `{ lat, lon, label, category?, address? }` for places to pin.
  - `route` — `{ origin {lat,lon,label?}, destination {lat,lon,label?}, waypoints?, travelMode? }`
    for a road-following route.
  - `traffic` — `true` to overlay live traffic.
  - `animate` — `true` to return an **animated map**: a looping GIF that flies/zooms in to the
    location, rendered inline. Use it when the user asks to "animate", "fly to", "zoom into", or
    wants something cinematic. Optional `animationEffect` is `zoom-in` (default) or `zoom-out`.
  - `overlays` — array of live-data layers to add to the **interactive** map (heatmap + clustered
    markers, or coloured areas/lines). Allowed values:
    - `earthquakes` — global seismic activity, USGS, last 30 days (M2.5+).
    - `uk-crime` — Police.uk street crime near the map centre (set `center` to a UK location).
    - `uk-floods` — Environment Agency flood-warning areas.
    - `uk-bikes` — London cycle hire (TfL Santander Cycles) docking stations.
    - `uk-tube` — live London Underground line status (lines drawn in their colours; delays
      highlighted with a dashed overlay). Centre on London.
  - `center`, `zoom`, `width`, `height` — optional; auto-calculated when omitted.
- `tomtom-dynamic-map` — advanced/manual rendering (polygons, circles, multiple route plans). Prefer
  `render_live_map` unless you need shapes or several independent routes on one image.

> **Overlays render on the interactive map** (the "Open the interactive live map" link), which has a
> live map engine for heatmaps, clustering, and coloured regions/lines. The inline static image shows
> the base map; tell the user to open the interactive map to explore the overlay. Example prompt that
> maps to an overlay: *"Visualise global earthquake activity from the past 30 days as a heatmap"* →
> `render_live_map({ title: "Global earthquakes (30 days)", overlays: ["earthquakes"] })`.

## Workflow

1. **Gather coordinates first.** If you only have place names, use the `tomtom-location-search`
   skill (geocode / search) to get precise `lat`/`lon`. Never guess coordinates.
2. **Choose what to show:**
   - Single place or several places → `markers`.
   - Directions between places → `route` (and set `traffic: true` if traffic is relevant).
   - "Traffic near X" → put incident points in `markers` and set `traffic: true`.
3. **Call `render_live_map`** with a clear `title` and the smallest set of fields needed.
4. **Present the result:** show the returned map image inline, then offer the live interactive
   link for exploration. Add a one-line text summary (what's on the map).

## Output format

The `render_live_map` tool result contains the exact markdown to show, plus a
`structuredContent` object with `imageUrl` and `interactiveUrl`. Always reply with,
in this order:

1. A short sentence describing the map (e.g. "Here's Cardiff Castle with live traffic.").
2. The **map as a clickable image**: `[![<title>](<imageUrl>)](<interactiveUrl>)` using the
   `imageUrl` and `interactiveUrl` from the tool result. Tapping the map opens the full
   interactive (pan / zoom / live‑traffic) map. This is the only way the picture appears in
   Cowork — do **not** skip it, and never paste raw base64.
3. The **interactive map link** as text too: `[Open the interactive live map](<interactiveUrl>)` —
   a fallback so the map is reachable even if the inline image is dropped. Always include it.

> Cowork renders the map from a normal markdown image URL. It does **not** display
> sandboxed map widgets or raw image content blocks, so the inline preview must be a
> markdown image and true pan/zoom happens via the interactive link.

## Tips & disambiguation

- Coordinates are `lat, lon` in decimal degrees (e.g. Cardiff Castle ≈ `51.4816, -3.1791`).
- If a place name is ambiguous, resolve it with city + country first (see `tomtom-location-search`).
- Keep markers to the handful that matter; large numbers reduce label clarity.
- The image is generated on demand from a URL, so it always reflects current data when opened.

## Additional resources

- **`references/rendering-and-coordinates.md`** — argument shapes, coordinate conventions,
  and worked examples for markers, routes, and traffic.
