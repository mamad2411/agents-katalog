---
name: web-gis
description: Build or modify web mapping features — MapLibre, OpenLayers, Leaflet, or similar — including layers, sources, styling, interactions, vector and raster tiles, GeoJSON handling, projections, and spatial data performance. Use for any map-rendering or geospatial front-end work.
---

# Web GIS

Related: `database-design` for spatial storage and indexing; `frontend-architecture` for component structure.

## When this applies

Interactive maps in the browser, the data pipeline feeding them, and geospatial
data handling on the client.

## Detect before you write

- **Map library and version** — MapLibre GL, Mapbox GL, OpenLayers, Leaflet,
  deck.gl, Cesium. APIs and styling models are not interchangeable.
- **Data sources** — vector tiles (MVT), raster/XYZ/WMTS, WMS, GeoJSON, WFS,
  COG, or a feature API — and who serves them.
- **Style management** — a style JSON document, programmatic layer definitions,
  or a hosted style. Follow the existing one.
- **Projection and CRS** — the display projection and the CRS of each source.
  Web Mercator (EPSG:3857) display with WGS84 (EPSG:4326) data is common but
  never assume it; OpenLayers projects are frequently in a national CRS.
- **State integration** — how map state (center, zoom, selection, filters) is
  held and whether it is reflected in the URL.
- **Backend** — PostGIS, a tile server, or static tiles, and how tiles are built
  and cached.

## Workflow

1. Inspect the library, sources, and CRS setup; read an existing layer definition.
2. Confirm the data contract: geometry types, coordinate order and units,
   property names and types, feature ID field, and tile zoom range.
3. Add sources and layers following the project's existing pattern, keeping
   layer IDs and ordering conventions intact.
4. Wire interactions — hover, click, selection, popups — with correct hit
   testing and cleanup.
5. Verify visually at several zoom levels and at the data's edges, then check
   performance with a realistic feature count.

## Decision principles

- **Coordinate order is the classic bug.** GeoJSON and most web APIs use
  `[longitude, latitude]`; many other formats and libraries use lat/lon. Confirm
  per source rather than per habit.
- **Reproject once, at a defined boundary** — ideally server-side — and keep a
  single canonical CRS in the client.
- **Vector tiles for large or frequently-rendered datasets**; raw GeoJSON only
  for small, bounded collections. Loading a large FeatureCollection into the
  browser is the usual cause of a frozen map.
- **Filter and simplify server-side** — by bounding box, zoom, and attribute —
  rather than shipping everything and hiding it in the client.
- **Style data-driven, not per-feature.** Use expressions and feature state for
  hover and selection instead of mutating sources or adding a layer per feature.
- **Respect zoom semantics.** Set `minzoom`/`maxzoom` on sources and layers,
  choose simplification per zoom level, and do not label at zooms where features
  are unreadable.
- **Clean up.** Remove listeners, layers, sources, popups, and markers on
  unmount; a map instance leaked across route changes will accumulate.

## Important checks

- Geometry validity: self-intersections, unclosed rings, winding order, and
  antimeridian crossing.
- Null and empty geometries handled without throwing.
- Tile requests bounded — no fetching the world at zoom 0 from a feature API.
- Layer order and `beforeId` correct so labels are not buried.
- Popup and label content escaped; feature properties are untrusted input.
- Attribution present for every basemap and data source, as licensing requires.
- Accessibility: keyboard panning and zooming, and a non-map path to the same
  information where the map is the only access to it.
- Coordinate precision trimmed — six decimals is roughly 0.1 m; more is payload
  waste.

## Expected output

The map changes with the sources, layers, and CRS handling stated explicitly,
what you verified visually and at which zoom levels, and performance
observations with a realistic dataset.
