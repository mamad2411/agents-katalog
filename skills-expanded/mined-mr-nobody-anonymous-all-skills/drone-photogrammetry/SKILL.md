---
name: drone-photogrammetry
description: "Turn drone imagery into accurate products: flight planning and overlap, ground control points, OpenDroneMap/WebODM processing, orthomosaics, DSM and accuracy reports."
type: procedural
category: geospatial
domain: geospatial
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - drone orthomosaic processing
  - opendronemap workflow
  - ground control points gcp
  - photogrammetry accuracy report
  - dsm from drone photos
keywords:
  - photogrammetry
  - drone
  - orthomosaic
  - odm
  - gcp
  - dsm
  - uav
mcp_servers:
  - gdal
  - qgis
source: custom
enabled: true
---

# Drone Photogrammetry

## Purpose

Turn drone imagery into accurate products: flight planning and overlap, ground control points, OpenDroneMap/WebODM processing, orthomosaics, DSM and accuracy reports.

## When to Use

- A site survey must produce an orthomosaic, DSM or point cloud.
- Repeat flights must be comparable over time.
- A deliverable needs a documented positional accuracy.

## When NOT to Use

- Legal survey accuracy is required; photogrammetry is not a substitute for a total station.
- The flight had insufficient overlap; reprocessing will not recover it.
- Airspace or privacy rules prohibit flying the area.

## Capabilities

- Plan flights with adequate overlap, altitude and ground sample distance.
- Design and measure ground control for vertical and horizontal accuracy.
- Run ODM/WebODM with reproducible parameters.
- Produce an accuracy report with checkpoints and residuals.

## Inputs

- Flight images with EXIF/GPS, camera model and flight log.
- Ground control and checkpoint coordinates with their own accuracy.
- Deliverable contract: GSD, CRS, resolution, formats.

## Workflow

1. Check overlap (≥75% forward, ≥60% side) and image exposure before processing.
2. Place and survey GCPs across the area, plus independent checkpoints.
3. Run the reconstruction with GCPs enabled and a fixed output CRS.
4. Validate at checkpoints and report RMSE horizontally and vertically.
5. Deliver orthomosaic/DSM as COG with a processing report.

## Tools

- ODM / WebODM
- QGIS for GCP QA and visual check
- GPS/GNSS for control survey

## Examples

- `docker run -ti --rm -v "$PWD/images:/code/images" -v "$PWD/odm:/code/odm_texturing" opendronemap/odm --project-path /code --gcp /code/gcp.txt`
- `gdalinfo -stats odm/odm_orthophoto/odm_orthophoto.tif`
- `allskills route "process drone images into an orthomosaic"`

## Safety

- Flying without airspace authorisation is illegal in most jurisdictions.
- GCP survey error propagates into every product; document the control accuracy.
- Avoid publishing imagery of identifiable people or private property without consent.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `gdal` | stdio | full | medium | — |
| `qgis` | stdio | full | medium | `QGIS_MCP_PORT` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/geospatial/drone-photogrammetry`). First-party skill, maintained in this repository.

## Notes

- Checkpoint RMSE is the honest accuracy number — GCP residuals alone overstate it.
- Consistent altitude and camera settings make repeat flights comparable.
- Pairs with: `geospatial/lidar-point-clouds`, `geospatial/spatial-reference-systems`.
