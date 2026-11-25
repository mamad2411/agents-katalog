---
name: arcgis-pro
description: "Automate ArcGIS Pro geoprocessing with ArcPy, enterprise geodatabases, and Spatial Analyst workflows."
category: gis
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["arcgis-pro", "arcpy", "gis-mapping", "spatial-analyst", "geodatabase", "geoprocessing", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Esri ArcGIS Pro Enterprise GIS AI Skill Guide (Claude)

## Overview & Engine Architecture
Esri ArcGIS Pro is the industry-standard 64-bit multi-threaded desktop Geographic Information System (GIS), engineered for 2D cartography, 3D voxel/scene modeling, spatial statistics, and enterprise geodatabase management. ArcGIS Pro embeds the **ArcPy Python 3 runtime (`propy.bat`)**, integrates with **ArcGIS Enterprise (Portal / SDE)**, features the **Spatial Analyst / Image Analyst raster engines**, and provides programmatic map layout publishing via **`arcpy.mp`**. Claude operates as a Principal GIS Architect and Spatial Data Science Lead, specializing in **ArcPy batch geoprocessing**, **Coordinate Reference System (CRS) transformations**, **Enterprise SDE versioning reconcile/post operations**, and **spatial automation pipelines**.

### ArcGIS Pro Multi-Threaded Architecture & ArcPy Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 ArcGIS Pro Architecture                     │
│                                                             │
│  Presentation & Cartography Layer                           │
│  ├── 2D Multi-Pane Maps & 3D Global/Local Scenes            │
│  ├── Map Series & Layout Engine (`arcpy.mp` Automation)     │
│  └── Vector Tile & Dynamic Symbology Renderers              │
│                                                             │
│  Geoprocessing & Analysis Core                              │
│  ├── ArcPy Python 3 C-Extensions & NumPy Array Interop      │
│  ├── Spatial Analyst (Zonal Statistics, Surface Slope/Aspect│
│  └── ModelBuilder Workflow Engine                           │
│                                                             │
│  Data & Persistence Layer                                   │
│  ├── File Geodatabase (`.gdb`) & Mobile Geodatabase (`.geodk│
│  └── Enterprise SDE (PostgreSQL, Oracle, SQL Server)        │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **ArcPy Scripting & Automation**: Author performant Python scripts using `arcpy.da.SearchCursor` / `UpdateCursor`, `arcpy.management`, and `arcpy.sa` Spatial Analyst modules with in-memory workspace optimization (`in_memory\` or `memory\`).
2. **Spatial Data Quality & Coordinate Transformations**: Prevent spatial distortion by applying correct Geographic Datum Transformations (`arcpy.management.Project`) across NAD83, WGS84, and local State Plane / UTM projections.
3. **Enterprise SDE Versioning Management**: Script automated reconciliation and posting routines (`arcpy.management.ReconcileVersions`) for Branch Versioning and Traditional Versioning multi-user edits.
4. **Automated Map Series Generation**: Author `arcpy.mp` scripts to iterate through map series index features, update dynamic title text, and export publication-ready high-resolution PDFs.

---

## Production Python Automation: Automated Spatial Buffer & Zonal Statistics Pipeline (`ArcPy`)

Save this script as `run_spatial_analysis.py` and execute using `propy.bat run_spatial_analysis.py`:

```python
"""
ArcGIS Pro ArcPy Spatial Buffer & Zonal Statistics Pipeline
Performs multi-ring buffering around sensitive assets and calculates elevation statistics.
"""

import sys
import os
import arcpy
from arcpy.sa import ZonalStatisticsAsTable

def execute_spatial_pipeline(assets_fc: str, elevation_raster: str, output_gdb: str):
    # Enable Spatial Analyst Extension
    arcpy.CheckOutExtension("Spatial")
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_gdb

    print(f"--- [STARTING ARCPY GEOPROCESSING PIPELINE] ---")

    # 1. Verify Spatial Reference and Re-Project to Target UTM Zone
    target_crs = arcpy.SpatialReference(32618) # WGS 84 / UTM Zone 18N (Metric Units)
    projected_assets = os.path.join(output_gdb, "Assets_UTM18N")
    
    print("Step 1: Reprojecting input features to Metric Projected CRS (UTM 18N)...")
    arcpy.management.Project(assets_fc, projected_assets, target_crs)

    # 2. Generate Multi-Ring Buffer Zones (100m, 250m, 500m)
    buffered_output = os.path.join(output_gdb, "Asset_Buffers")
    print("Step 2: Generating Multi-Ring Buffer Zones (100m, 250m, 500m)...")
    arcpy.analysis.MultipleURLRingBuffer(
        projected_assets,
        buffered_output,
        [100, 250, 500],
        "Meters",
        "Distance",
        "ALL",
        "FULL"
    )

    # 3. Calculate Zonal Statistics on Elevation Raster
    zonal_table = os.path.join(output_gdb, "Buffer_Elevation_Stats")
    print("Step 3: Calculating Zonal Statistics (Mean & Max Elevation)...")
    ZonalStatisticsAsTable(
        in_zone_data=buffered_output,
        zone_field="Distance",
        in_value_raster=elevation_raster,
        out_table=zonal_table,
        ignore_nodata="DATA",
        statistics_type="ALL"
    )

    # 4. Display Results Summary via SearchCursor
    print("\n--- [SPATIAL ANALYSIS SUMMARY] ---")
    fields = ["Distance", "MEAN", "MIN", "MAX"]
    with arcpy.da.SearchCursor(zonal_table, fields) as cursor:
        for dist, mean_val, min_val, max_val in cursor:
            print(f"• Buffer Zone: {dist:>4} m | Mean Elev: {mean_val:>7.2f} m | Range: [{min_val:.1f} - {max_val:.1f}] m")

    arcpy.CheckInExtension("Spatial")
    print("\nGeoprocessing pipeline executed successfully!")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: propy.bat run_spatial_analysis.py <assets_fc> <elevation_raster> <output_gdb>")
        sys.exit(1)
    execute_spatial_pipeline(sys.argv[1], sys.argv[2], sys.argv[3])
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Geoprocessing Tool Hangs at `Executing (99%)...`** | Schema lock (`.sr.lock` / `.rd.lock`) on target File Geodatabase or scratch disk out of space. | 1. In ArcPy script, use `in_memory\` or `memory\` workspace for intermediate scratch layers.<br>2. Close ArcGIS Pro GUI instances holding locks on the `.gdb`.<br>3. Run `arcpy.management.Compact(gdb_path)` to clean locks. |
| **Layers Misaligned / Offset by 10-100 Meters on Map** | On-the-fly projection applied without a valid geographic datum transformation (e.g. NAD27 to WGS84). | In Map Properties $\rightarrow$ *Coordinate Systems $\rightarrow$ Transformations*, specify explicit transformation method (e.g. `NAD_1927_To_WGS_1984_79_CONUS`). |
| **Enterprise SDE Versioning Error: `Version has conflicts`** | Multiple editors modified identical feature geometries in separate child versions. | 1. Open *Version Changes* tool in ArcGIS Pro.<br>2. Review conflicts $\rightarrow$ Choose resolution: **In Favor of Edit Version** or **In Favor of Target Version**.<br>3. Run `arcpy.management.ReconcileVersions`. |
| **`ExecuteError: ERROR 000824: Tool is not licensed`** | Spatial Analyst or 3D Analyst extension was not checked out prior to tool invocation. | Add `arcpy.CheckOutExtension("Spatial")` at script initialization and `arcpy.CheckInExtension("Spatial")` at completion. |

---

## Command Line Syntax & Propy Automation

```bash
# 1. Run Standalone ArcPy Python Script with ArcGIS Pro Runtime
"C:\Program Files\ArcGIS\Pro\bin\Python\scripts\propy.bat" "C:\Scripts\run_spatial_analysis.py"

# 2. Create New File Geodatabase via Python One-Liner
python -c "import arcpy; arcpy.management.CreateFileGDB('C:/Data', 'Analysis.gdb')"

# 3. Compact Geodatabase to Release Schema Locks and Free Space
python -c "import arcpy; arcpy.management.Compact('C:/Data/Analysis.gdb')"
```

### Essential File Locations
- **ArcGIS Pro Python Interpreter**: `C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe`
- **Batch Propy Runner**: `C:\Program Files\ArcGIS\Pro\bin\Python\scripts\propy.bat`
- **ArcGIS Pro User Settings**: `%LOCALAPPDATA%\ESRI\ArcGISPro`

---

## Agent Operational Directive
> **MANDATORY**: Execute standalone ArcPy scripts strictly using `propy.bat` or the active `arcgispro-py3` Conda environment. Always check out required extensions (`arcpy.CheckOutExtension`) and use the `memory\` workspace for intermediate processing layers.
