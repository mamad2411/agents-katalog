---
name: postgis-spatial-sql
description: "Run spatial SQL in PostGIS: geometry versus geography types, GiST indexes, ST_ spatial predicates and constructors, tiling and query performance."
type: procedural
category: geospatial
domain: geospatial
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - postgis spatial join
  - postgis gist index
  - st_intersects slow query
  - geometry vs geography postgis
  - spatial query optimization
keywords:
  - postgis
  - postgresql
  - geometry
  - gist
  - st_intersects
  - spatial-index
mcp_servers:
  - postgres
source: custom
enabled: true
---

# PostGIS Spatial SQL

## Purpose

Run spatial SQL in PostGIS: geometry versus geography types, GiST indexes, ST_ spatial predicates and constructors, tiling and query performance.

## When to Use

- Spatial analysis belongs in the database next to the attribute data.
- A spatial join is slow or returns wrong matches.
- An application needs server-side spatial filtering with pagination.

## When NOT to Use

- The data is a one-off file better handled with GeoPandas or GDAL.
- You need cartographic rendering, which belongs in QGIS or a tile server.
- The geometry is already reduced to a simple bounding box check.

## Capabilities

- Choose geometry (planar) versus geography (spheroidal) per column and justify it.
- Write spatial predicates that use the GiST index instead of scanning.
- Build ST_ constructors, transforms and aggregates correctly.
- Keep large spatial tables fast with `ST_Subdivide` and proper indexing.

## Inputs

- The PostGIS version and the SRID of each geometry column.
- Row counts and expected result sizes for the join or filter.
- Whether distances must be geodesic (metres on the ellipsoid) or planar.

## Workflow

1. Confirm the SRID with `Find_SRID` and transform analysis layers to a metric CRS.
2. Write the predicate so both sides are indexed (`ST_Intersects(a.geom, b.geom)` with GiST on both).
3. Read `EXPLAIN (ANALYZE, BUFFERS)` and confirm a Bitmap Index Scan, not a Seq Scan.
4. For very large polygons, `ST_Subdivide` before indexing to shrink bounding boxes.
5. Validate a sample of results against a known correct intersection.

## Tools

- psql
- PostGIS (`ST_*` functions)
- QGIS or GeoServer for visual checks

## Examples

- `CREATE INDEX roads_geom_idx ON roads USING GIST (geom);`
- `SELECT a.id, b.name FROM parcels a JOIN districts b ON ST_Intersects(a.geom, b.geom);`
- `SELECT ST_Area(ST_Transform(geom, 32633)) / 10000 AS hectares FROM parcels;`
- `SELECT Find_SRID('public', 'parcels', 'geom');`

## Safety

- `ST_Distance` on geometry in degrees returns degrees, not metres — transform first.
- Unindexed spatial joins on large tables can lock the database for minutes.
- Never assume SRID 4326: mixed SRIDs raise errors or silently mis-measure.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `postgres` | stdio | standard | medium | `POSTGRES_URL` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/geospatial/postgis-spatial-sql`). First-party skill, maintained in this repository.

## Notes

- `geography` is correct but slower; use it for geodesic distance over wide areas.
- Bounding-box prefilter (`&&`) is what the GiST index actually accelerates.
- Pairs with: `databases/postgresql`, `geospatial/spatial-statistics`.
