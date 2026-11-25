---
name: vector-tile-web-maps
description: "Publish web maps with vector tiles: MVT/PMTiles generation, style specification, MapLibre or Leaflet clients, attributions and cache strategy."
type: procedural
category: geospatial
domain: geospatial
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - vector tiles from postgis
  - pmtiles static map
  - maplibre style json
  - tile server performance
  - web map performance
keywords:
  - vector-tiles
  - mvt
  - pmtiles
  - maplibre
  - leaflet
  - tileserver
  - map-style
mcp_servers:
  - mapbox
source: custom
enabled: true
---

# Vector Tile Web Maps

## Purpose

Publish web maps with vector tiles: MVT/PMTiles generation, style specification, MapLibre or Leaflet clients, attributions and cache strategy.

## When to Use

- A web application needs a fast, zoomable map of your own data.
- Raster tiles are too heavy or too blurry at high zoom.
- A static deployment needs maps without running a tile server.

## When NOT to Use

- A single static image is enough; export a PNG from QGIS.
- The dataset is tiny and GeoJSON loads instantly.
- The map must show realtime data streaming at sub-second latency.

## Capabilities

- Generate MVT tiles from PostGIS with `ST_AsMVT` or from files with tippecanoe.
- Package tiles as PMTiles for serverless hosting.
- Author a MapLibre style with sources, layers and sprite/glyph references.
- Control zoom ranges, simplification and attribute size per layer.

## Inputs

- Source geometry with a stable id and minimal attributes per zoom level.
- Client framework and the hosting model (server, object storage, CDN).
- Attribution and licensing requirements for every data source.

## Workflow

1. Decide the zoom range and which attributes each zoom needs; drop the rest at generation time.
2. Generate tiles (tippecanoe for files, `ST_AsMVT` for PostGIS) with simplification per zoom.
3. Package or serve the tiles and confirm `Content-Encoding: gzip` and cache headers.
4. Write the style with explicit `source-layer`, `minzoom` and `maxzoom`.
5. Test on a phone-sized viewport and check label collisions and load time.

## Tools

- tippecanoe / `ST_AsMVT`
- PMTiles + object storage
- MapLibre GL JS or Leaflet

## Examples

- `tippecanoe -o roads.pmtiles -Z5 -z14 --drop-densest-as-needed roads.geojson`
- `SELECT ST_AsMVT(tile, 'roads', 4096, 'geom') FROM (SELECT ST_AsMVTGeom(geom, ST_TileEnvelope(14, 8710, 5862)) AS geom, name FROM roads) tile;`
- `npx serve -C dist   # local check of the style + tiles`

## Safety

- High zoom levels multiply tile count; estimate storage before generating z18 nationwide.
- Attribute bloat at every zoom makes tiles huge — strip fields you do not render.
- Never ship tiles whose licence forbids redistribution or caching.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `mapbox` | stdio | full | medium | `MAPBOX_ACCESS_TOKEN` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/geospatial/vector-tile-web-maps`). First-party skill, maintained in this repository.

## Notes

- PMTiles removes the tile-server dependency entirely; a range request serves the archive.
- Overzoom keeps low-zoom data usable at street level without generating extra tiles.
- Pairs with: `geospatial/cartographic-design`, `web/frontend-design`.
