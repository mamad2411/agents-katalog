---
name: openstreetmap-data
description: "Work with OpenStreetMap data: Overpass queries, extracts, tag semantics, conflation with authoritative data, and ODbL attribution obligations."
type: procedural
category: geospatial
domain: geospatial
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - overpass api query
  - osm extract download
  - openstreetmap tagging
  - osm data quality
  - conflate osm with official data
keywords:
  - openstreetmap
  - osm
  - overpass
  - odbl
  - tags
  - geofabrik
mcp_servers:
  - gdal
  - postgres
source: custom
enabled: true
---

# OpenStreetMap Data

## Purpose

Work with OpenStreetMap data: Overpass queries, extracts, tag semantics, conflation with authoritative data, and ODbL attribution obligations.

## When to Use

- You need roads, buildings, POIs or landuse without buying a dataset.
- A basemap of your own data must be rendered offline.
- Official data and OSM need to be combined for routing or analysis.

## When NOT to Use

- Legal boundaries or cadastral data are required — OSM is not authoritative.
- The task needs a guaranteed update cadence and SLA.
- Redistribution would violate ODbL share-alike obligations you cannot meet.

## Capabilities

- Write Overpass QL queries with correct filters and timeouts.
- Extract regional data from Geofabrik and convert with osmium or GDAL.
- Interpret tagging conventions (`highway=*`, `building=*`, `access=*`).
- Conflate by distance and attribute, recording match confidence.

## Inputs

- The extract area and the object classes required.
- The authoritative dataset used for comparison or enrichment.
- Licensing context: public map, internal analysis, or redistribution.

## Workflow

1. Query the smallest area possible with Overpass and always set a timeout.
2. Convert to GeoPackage with `ogr2ogr` so attributes and geometry types are explicit.
3. Inspect tag completeness; OSM attributes are sparse and inconsistent by design.
4. Conflate with official data using a distance threshold plus attribute similarity, then review the ambiguous band manually.
5. Publish attribution `© OpenStreetMap contributors, ODbL` wherever the data appears.

## Tools

- Overpass API / overpass-turbo
- osmium-tool
- ogr2ogr with the OSM driver

## Examples

- `curl -sG https://overpass-api.de/api/interpreter --data-urlencode "data=[out:json][timeout:60];way[highway=primary](41.8,12.4,41.9,12.5);out geom;"`
- `osmium extract -b 12.4,41.8,12.5,41.9 italy-latest.osm.pbf -o rome.osm.pbf`
- `ogr2ogr -f GPKG rome.gpkg rome.osm.pbf points lines multipolygons`

## Safety

- ODbL requires attribution and share-alike for derived databases; check before publishing.
- OSM is crowd-sourced: verify critical geometry against an authoritative source.
- Respect Overpass rate limits — heavy repeated queries get blocked.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `gdal` | stdio | full | medium | — |
| `postgres` | stdio | standard | medium | `POSTGRES_URL` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/geospatial/openstreetmap-data`). First-party skill, maintained in this repository.

## Notes

- `osmium` is far faster than GDAL for raw .osm.pbf processing.
- Tag completeness differs by region; never assume a field exists everywhere.
- Pairs with: `geospatial/qgis-map-production`, `geospatial/postgis-spatial-sql`.
