---
name: qgis-map-production
description: "Produce publication-ready maps in QGIS: project structure, layer styling and labelling, print layouts with atlases, expression-driven symbology and PyQGIS automation."
type: procedural
category: geospatial
domain: geospatial
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - make a map in qgis
  - qgis print layout atlas
  - qgis expression labelling
  - qgis layer styling
  - pyqgis automation script
aliases:
  - qgis
keywords:
  - qgis
  - gis
  - map
  - print-layout
  - atlas
  - pyqgis
  - symbology
mcp_servers:
  - qgis
source: custom
enabled: true
---

# QGIS Map Production

## Purpose

Produce publication-ready maps in QGIS: project structure, layer styling and labelling, print layouts with atlases, expression-driven symbology and PyQGIS automation.

## When to Use

- A dataset must become a legible printed or on-screen map.
- The same layout must be repeated per feature (atlas: one map per district, site or page).
- Map production has to be reproducible after the data updates.

## When NOT to Use

- The output is a chart or dashboard rather than a geographic map.
- You need a live web map service; that is tile publishing, not desktop cartography.
- The data has no verified coordinate system yet — settle the CRS first.

## Capabilities

- Build a QGIS project whose layers, styles and layouts are versioned and reproducible.
- Drive symbology, labels and filters with expressions instead of manual edits.
- Generate atlas layouts with per-feature extents, scale bars and dynamic text.
- Automate repeated exports headlessly with PyQGIS.

## Inputs

- The source layers (GeoPackage, shapefile, PostGIS, GeoJSON) and their declared CRS.
- The map purpose and audience: page size, dpi, required legend and attribution text.
- The feature field used to page an atlas (district, site id, permit number).

## Workflow

1. Load every layer into a GeoPackage project and confirm each layer's CRS before styling.
2. Style with data-defined overrides (categorized, graduated) so restyling is a rule change, not a click-fest.
3. Label with expression templates and collisions enabled; test at final scale, not at 1:1.
4. Compose the print layout with map frame, legend, scale bar, north arrow and credits.
5. Enable the atlas on the paging field, export to PDF, and inspect the first, middle and last pages.

## Tools

- QGIS desktop (layout designer, expression builder)
- PyQGIS via the Python console
- gdal/ogr for pre-processing

## Examples

- `qgis_process run native:reprojectlayer -- INPUT=roads.gpkg TARGET_CRS=EPSG:3857 OUTPUT=roads_3857.gpkg`
- `qgis_process run native:joinattributesbylocation -- INPUT=a.gpkg JOIN=b.gpkg PREDICATE=intersects OUTPUT=joined.gpkg`
- `python -c "from qgis.core import QgsApplication; QgsApplication.setPrefixPath('/usr', True)"`
- `allskills route "make an atlas map per district"`

## Safety

- Publishing a map in the wrong CRS misplaces features by hundreds of metres — verify with a known landmark.
- Do not redistribute basemap tiles outside their licence; record attribution in the layout.
- Sensitive locations (protected species, private addresses) need generalization before publication.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `qgis` | stdio | full | medium | `QGIS_MCP_PORT` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/geospatial/qgis-map-production`). First-party skill, maintained in this repository.

## Notes

- A GeoPackage project is one file to version; shapefiles fragment into six and break on 2 GB.
- Expressions keep styling reproducible; manual symbol overrides do not survive a re-import.
- Pairs with: `geospatial/spatial-reference-systems`, `geospatial/cartographic-design`.
