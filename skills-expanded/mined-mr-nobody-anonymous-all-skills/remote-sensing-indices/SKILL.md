---
name: remote-sensing-indices
description: "Analyse satellite imagery: Sentinel-2 and Landsat band selection, cloud masking, vegetation and water indices, temporal composites and change detection."
type: procedural
category: geospatial
domain: geospatial
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - calculate ndvi sentinel
  - sentinel 2 cloud masking
  - landsat time series analysis
  - change detection remote sensing
  - spectral index vegetation
keywords:
  - remote-sensing
  - sentinel
  - landsat
  - ndvi
  - ndwi
  - change-detection
mcp_servers:
  - gdal
source: custom
enabled: true
---

# Remote Sensing Indices

## Purpose

Analyse satellite imagery: Sentinel-2 and Landsat band selection, cloud masking, vegetation and water indices, temporal composites and change detection.

## When to Use

- Land cover, vegetation health or water extent must be measured from imagery.
- A change over time has to be quantified rather than eyeballed.
- A pipeline must produce comparable indices across dates.

## When NOT to Use

- The question is about a single building or parcel; survey data is more accurate.
- You need high-resolution commercial imagery you are not licensed to use.
- Atmospheric correction is impossible with the data available — say so instead of over-claiming.

## Capabilities

- Select the correct bands and scale factors for a sensor and processing level.
- Mask clouds and shadows with the scene classification layer or QA band.
- Compute NDVI, NDWI, NBR and other indices with documented formulas.
- Build median composites and detect change between periods.

## Inputs

- Sensor and processing level (L1C vs L2A), acquisition dates and tile ids.
- Area of interest geometry and the season window that makes dates comparable.
- Ground-truth samples for validating any classification.

## Workflow

1. Fetch scenes for the same season across years so phenology does not masquerade as change.
2. Mask clouds, shadows and snow using the provided QA/SCL band, then report the valid-pixel fraction.
3. Compute the index with the sensor's scale and offset applied (L2A reflectance is offset by -1000).
4. Composite (median or best-pixel) before comparing periods.
5. Validate against ground truth or a high-resolution reference and report uncertainty.

## Tools

- Sentinel Hub / Copernicus Open Access Hub
- Google Earth Engine or `stackstac`
- rasterio / xarray

## Examples

- `gdal_calc.py -A B04.tif -B B08.tif --outfile=ndvi.tif --calc="(B-A)/(B+A)"`
- `pystac-client search --collections sentinel-2-l2a --bbox 12.4,41.8,12.5,41.9`
- `allskills route "measure vegetation change from sentinel-2"`

## Safety

- Cloud-contaminated pixels bias indices strongly; never report an unmasked mean.
- Different sensors and processing levels are not directly comparable without harmonization.
- Do not present a classification as ground truth — report accuracy and confusion.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `gdal` | stdio | full | medium | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/geospatial/remote-sensing-indices`). First-party skill, maintained in this repository.

## Notes

- Composite over a window rather than picking a single date; one clear scene is often unrepresentative.
- Document the band math and scale factors in the output metadata.
- Pairs with: `geospatial/gdal-ogr-pipelines`, `scientific/geospatial-analysis`.
