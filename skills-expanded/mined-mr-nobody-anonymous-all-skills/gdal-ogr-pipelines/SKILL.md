---
name: gdal-ogr-pipelines
description: "Build reproducible raster and vector pipelines with GDAL/OGR: format conversion, warping, mosaicking, COG output, clipping and batch processing."
type: procedural
category: geospatial
domain: geospatial
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - gdalwarp reproject raster
  - ogr2ogr convert geojson
  - create cloud optimized geotiff
  - merge raster tiles
  - gdal batch processing
aliases:
  - gdal
keywords:
  - gdal
  - ogr
  - raster
  - vector
  - cog
  - warp
  - mosaic
mcp_servers:
  - gdal
source: custom
enabled: true
---

# GDAL and OGR Data Pipelines

## Purpose

Build reproducible raster and vector pipelines with GDAL/OGR: format conversion, warping, mosaicking, COG output, clipping and batch processing.

## When to Use

- Data must be converted, reprojected, clipped or mosaicked before analysis.
- A raster deliverable should be a Cloud Optimized GeoTIFF for web serving.
- A repeatable batch must process hundreds of tiles with the same parameters.

## When NOT to Use

- Interactive editing or symbology is needed; use QGIS.
- The transformation requires domain judgement that a blind batch would corrupt.
- The dataset fits in memory and a dataframe library is simpler.

## Capabilities

- Convert between vector formats without losing schema, CRS or encoding.
- Warp, resample and align rasters to a common grid and CRS.
- Produce COGs with overviews and correct nodata handling.
- Batch over many inputs with consistent naming and verification.

## Inputs

- Input formats, CRS, resolution and nodata conventions.
- Target grid: CRS, pixel size, extent and resampling method.
- Output contract: format, compression, overview levels, naming.

## Workflow

1. Inspect the source with `gdalinfo` / `ogrinfo` and record CRS, extent, nodata and band count.
2. Decide the target grid once and reuse it for every layer (same `-te`, `-tr`, `-t_srs`).
3. Run the transformation with explicit resampling (`-r bilinear` for continuous, `-r near` for categorical).
4. Build overviews and write COG (`-of COG -co COMPRESS=DEFLATE -co OVERVIEWS=AUTO`).
5. Verify extent, CRS, statistics and a visual sample before shipping.

## Tools

- GDAL/OGR CLI (`gdalwarp`, `gdal_translate`, `ogr2ogr`, `gdalinfo`)
- Python bindings / rasterio
- Makefile or shell loop for batches

## Examples

- `gdalinfo -stats dem.tif`
- `gdalwarp -t_srs EPSG:3857 -tr 10 10 -r bilinear dem.tif dem_3857.tif`
- `gdal_translate -of COG -co COMPRESS=DEFLATE -co OVERVIEWS=AUTO dem_3857.tif dem_cog.tif`
- `ogr2ogr -f GPKG roads.gpkg roads.geojson -nln roads -t_srs EPSG:4326`

## Safety

- `-r near` on continuous data (elevation, temperature) creates staircase artefacts.
- Overwriting inputs in place (`ogr2ogr` onto its own source) destroys data — always write to a new path.
- Large uncompressed rasters exhaust disk; check size and use compression plus overviews.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `gdal` | stdio | full | medium | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/geospatial/gdal-ogr-pipelines`). First-party skill, maintained in this repository.

## Notes

- COG is the interchange format for rasters on object storage; plain GeoTIFF forces full downloads.
- `-te`/`-tr` alignment across layers avoids resampling surprises in later mosaic steps.
- Pairs with: `geospatial/remote-sensing-indices`, `geospatial/lidar-point-clouds`.
