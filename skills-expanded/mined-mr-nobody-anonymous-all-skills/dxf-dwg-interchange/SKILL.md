---
name: dxf-dwg-interchange
description: "Exchange CAD data reliably: DXF/DWG versions, units and layers, blocks and xrefs, round-trip validation and conversion with ODA/LibreDWG tooling."
type: procedural
category: cad
domain: cad
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - dxf conversion problems
  - dwg version compatibility
  - dxf units layers
  - cad file round trip
  - libredwg odafileconverter
keywords:
  - dxf
  - dwg
  - interchange
  - libredwg
  - oda
  - blocks
  - units
source: custom
enabled: true
---

# DXF and DWG Interchange

## Purpose

Exchange CAD data reliably: DXF/DWG versions, units and layers, blocks and xrefs, round-trip validation and conversion with ODA/LibreDWG tooling.

## When to Use

- Data must move between CAD systems or into GIS.
- A consultant delivered a DWG your tool cannot read.
- Geometry imports at the wrong scale or in the wrong place.

## When NOT to Use

- Both sides use the same native format and version.
- The geometry is a mesh, where STL/OBJ/glTF is the right interchange.
- Only a rendered image is needed.

## Capabilities

- Choose the DXF/DWG version the receiving tool supports.
- Preserve layers, blocks, linetypes and units across the round trip.
- Convert with ODA File Converter or LibreDWG without silent degradation.
- Validate by comparing extents, entity counts and a measured baseline.

## Inputs

- Source format and version, and the consumer's supported versions.
- The unit convention (mm, m, imperial) and the intended coordinate origin.
- Which entities matter: geometry only, or also annotation and blocks.

## Workflow

1. Record the source version and unit code before conversion.
2. Convert to a version the consumer supports; never convert down twice.
3. Compare entity counts and extents before and after.
4. Open in the consumer and measure two known dimensions.
5. Archive the original alongside the converted file and the conversion command.

## Tools

- ODA File Converter / LibreDWG (`dwg2dxf`)
- QGIS with the DXF importer
- ezdxf (Python) for inspection

## Examples

- `dwg2dxf -o plan.dxf plan.dwg`
- `python -c "import ezdxf; d=ezdxf.readfile('plan.dxf'); print(d.header['$INSUNITS'], len(d.modelspace()))"`
- `ogr2ogr -f GPKG plan.gpkg plan.dxf -nln plan`

## Safety

- Silent loss of xrefs turns an assembly into disconnected fragments.
- Unit header mismatches import drawings 1000x too large or small.
- Proprietary DWG versions newer than your converter fail or corrupt — check first.

## Source

All-Skills canonical library (`skills/cad/dxf-dwg-interchange`). First-party skill, maintained in this repository.

## Notes

- DXF R12 is the most compatible but loses newer entity types.
- `ezdxf` audits a file for structural errors before you trust it.
- Pairs with: `cad/autocad-drafting`, `geospatial/gdal-ogr-pipelines`.
