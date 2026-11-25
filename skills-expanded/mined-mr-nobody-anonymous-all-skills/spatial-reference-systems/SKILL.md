---
name: spatial-reference-systems
description: "Choose and transform coordinate reference systems correctly: EPSG codes, datums, projected versus geographic units, grid shifts and area/distance error control."
type: procedural
category: geospatial
domain: geospatial
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - which epsg code
  - reproject coordinates
  - datum transformation accuracy
  - wgs84 to utm
  - crs mismatch layer
aliases:
  - crs
keywords:
  - crs
  - epsg
  - projection
  - datum
  - reprojection
  - utm
  - geodesy
source: custom
enabled: true
---

# Spatial Reference Systems and Reprojection

## Purpose

Choose and transform coordinate reference systems correctly: EPSG codes, datums, projected versus geographic units, grid shifts and area/distance error control.

## When to Use

- Layers do not line up, or distances and areas are computed in degrees.
- Data must be transformed between datums for a legal or engineering deliverable.
- A map area or length calculation needs a projected CRS with acceptable distortion.

## When NOT to Use

- Everything is already in one CRS and no measurement is performed.
- The task is purely attribute data with no geometry.
- You are choosing a web map display CRS only — that is EPSG:3857 by convention, not analysis.

## Capabilities

- Identify a CRS from metadata, extent plausibility and known control points.
- Pick a projected CRS whose distortion is acceptable for the area of interest.
- Apply datum transformations explicitly and state the resulting accuracy.
- Convert between geographic and projected coordinates without silent unit errors.

## Inputs

- The declared CRS (or the absence of one) for each dataset, and the data's provenance.
- The area of interest and the accuracy the decision needs (metres? centimetres?).
- Whether the output is measured (area, length, buffer) or only displayed.

## Workflow

1. Read the CRS from the file metadata; if it is missing, infer from the coordinate magnitudes and verify against a control point.
2. Decide the working CRS: projected for measurement, geographic for storage and interchange.
3. Choose the transformation (e.g. a 7-parameter Helmert or a national grid shift) and note its stated accuracy.
4. Reproject once at the start of the pipeline, not repeatedly at each step.
5. Verify by measuring a known baseline (a road, a building footprint) in both CRSs.

## Tools

- PROJ (`projinfo`, `cs2cs`)
- GDAL/OGR (`gdalwarp -t_srs`)
- pyproj / GeoPandas `.to_crs()`

## Examples

- `projinfo EPSG:32633`
- `echo "12.4922 41.8902" | cs2cs EPSG:4326 EPSG:32633`
- `gdalwarp -t_srs EPSG:32633 -r bilinear dem.tif dem_utm.tif`
- `gdf = gdf.to_crs(32633); gdf.area  # square metres, not degrees`

## Safety

- A missing CRS silently assumed as EPSG:4326 corrupts every downstream measurement.
- Datum shifts matter: WGS84 to a national datum can move features by 100+ metres.
- Never mix geographic and projected layers in one measurement without transforming first.

## Source

All-Skills canonical library (`skills/geospatial/spatial-reference-systems`). First-party skill, maintained in this repository.

## Notes

- EPSG:3857 is for display only; its scale distortion grows with latitude.
- Store data in geographic coordinates, analyse in a projected CRS suited to the area.
- Pairs with: `geospatial/qgis-map-production`, `geospatial/postgis-spatial-sql`.
