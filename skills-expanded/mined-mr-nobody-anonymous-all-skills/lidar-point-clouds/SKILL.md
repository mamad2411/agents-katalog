---
name: lidar-point-clouds
description: "Process LiDAR point clouds: LAS/LAZ structure, PDAL pipelines, ground classification, DEM/DSM generation, and point-cloud quality control."
type: procedural
category: geospatial
domain: geospatial
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - lidar point cloud processing
  - pdal pipeline
  - las to dem classification
  - point cloud ground filter
  - laz file qc
keywords:
  - lidar
  - point-cloud
  - las
  - laz
  - pdal
  - dem
  - dsm
  - classification
source: custom
enabled: true
---

# LiDAR Point Clouds

## Purpose

Process LiDAR point clouds: LAS/LAZ structure, PDAL pipelines, ground classification, DEM/DSM generation, and point-cloud quality control.

## When to Use

- Terrain, canopy or building heights must come from LiDAR rather than imagery.
- A point cloud needs classification, thinning or tiling for downstream tools.
- A LiDAR deliverable must be checked against its specification.

## When NOT to Use

- Only a coarse global DEM is needed; use an existing product.
- The data is photogrammetric without ground control and cannot support centimetre claims.
- You need realtime visualization of a streaming sensor.

## Capabilities

- Read LAS/LAZ metadata: point format, scale, offset, CRS and classification codes.
- Build PDAL pipelines for filtering, classification and rasterization.
- Generate DEM and DSM with explicit resolution and NoData policy.
- QC against the specification: density, accuracy, coverage, classification balance.

## Inputs

- Point cloud files plus the survey specification (density, accuracy, classification scheme).
- Whether ground and/or non-ground products are required.
- Target grid resolution and CRS for raster outputs.

## Workflow

1. Inspect metadata first (`pdal info --summary`); unit and scale errors are the most common defect.
2. Reproject to the project CRS before classification so filters use metres.
3. Classify ground (SMRF/PMF) and validate against control points or a known flat area.
4. Rasterize to DEM/DSM at a resolution supported by the actual point density.
5. Report density, vertical error and coverage gaps alongside the product.

## Tools

- PDAL (`pdal info`, `pdal pipeline`)
- LAStools / CloudCompare
- GDAL for rasterization and COG output

## Examples

- `pdal info --summary tile.laz`
- `pdal pipeline classify.json --input tile.laz --output tile_classified.laz`
- `pdal translate tile.laz ground.laz -f filters.range --filters.range.limits="Classification[2:2]"`
- `pdal ground tile.laz dem_1m.tif --readers.las.filename=tile.laz --writers.gdal.resolution=1.0`

## Safety

- Assuming feet when the file is metres (or vice versa) scales topography by 3.28x.
- A DEM built at 0.5 m from 1 m-spaced points invents detail that is not in the data.
- Classifying ground under dense vegetation needs tuning; verify against control.

## Source

All-Skills canonical library (`skills/geospatial/lidar-point-clouds`). First-party skill, maintained in this repository.

## Notes

- `Classification` codes 2=ground, 6=building, 5=high vegetation under ASPRS conventions.
- LAZ saves ~10x storage and is the interchange default.
- Pairs with: `geospatial/gdal-ogr-pipelines`, `geospatial/drone-photogrammetry`.
