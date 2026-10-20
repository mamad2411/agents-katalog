---
name: substance-painter
description: "Automate Substance 3D Painter texturing and mesh-map baking with Python and batch tools; inspect PBR export workflows."
category: 3d
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["substance-painter", "pbr-texturing", "substance-api", "substance-automation-toolkit", "mesh-baking", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Adobe Substance 3D Painter AI Skill Guide (Claude)

## Overview & Engine Architecture
Adobe Substance 3D Painter is the industry-standard PBR material authoring and 3D texture painting application. Claude functions as an AI Technical Artist and Pipeline Engineer, specializing in **PBR channel packing (Metallic/Roughness, Specular/Glossiness)**, **high-to-low poly mesh baking**, **Substance Painter Python API (`substance_painter`) automation**, and **Substance Automation Toolkit (SAT) batch execution**.

### Substance 3D Painter Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Substance 3D Painter Engine                 │
│                                                             │
│  Painting & Projection Engine                               │
│  ├── Layer Stack (Fill Layers, Paint Layers, Anchor Points) │
│  ├── UV / Triplanar Projection & UV Tile / UDIM Painting    │
│  └── GPU Raytraced Baker (Curvature, AO, Thickness, Normal) │
│                                                             │
│  Pipeline & Automation Stack                                │
│  ├── `substance_painter` Python API (In-app Python 3 engine)│
│  ├── Substance Automation Toolkit (SAT - CLI `sbsrender`)   │
│  └── JSON-based Export Presets (Unreal, Unity, Arnold, USD) │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Python API Automation (`substance_painter`)**: Write scripts to automate project creation, texture set resolution adjustment, channel packing, and batch texture export.
2. **Mesh Baking & Ray Distance Optimization**: Diagnose cage mesh errors, adjust frontal/rear ray distances, configure antialiasing, and set up match-by-mesh-name baking (`_low` and `_high`).
3. **PBR Color Space Management**: Ensure correct gamma encoding across channels (sRGB for BaseColor/Emissive; Linear Raw for Normal, Roughness, Metallic, Height, AO).
4. **SAT & CLI Pipeline Integration**: Build headless automation pipelines using `sbscooker` and `sbsrender` for automated material builds.

---

## Production Python Automation: Batch Texture Exporter Plugin

Run this script within Substance Painter's Python scripting environment to programmatically export all texture sets using a specified export preset:

```python
"""
Substance 3D Painter: Automated Batch Texture Exporter
Exports all texture sets to target directory using Unreal Engine 5 Packed Preset.
"""

import os
import substance_painter.project
import substance_painter.export
import substance_painter.resource

def batch_export_textures(output_dir: str, preset_name: str = "Unreal Engine 5 (Packed)", resolution: int = 2048):
    if not substance_painter.project.is_open():
        print("Error: No project is currently open in Substance Painter.")
        return

    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Locate Export Preset Resource
    url = substance_painter.resource.ResourceSearch(preset_name).next()
    if not url:
        print(f"Error: Export preset '{preset_name}' not found.")
        return

    # 2. Build Export Configuration
    export_config = {
        "exportShaderParams": False,
        "exportPath": output_dir,
        "defaultExportPreset": url.as_url(),
        "exportList": []
    }

    # Add all texture sets in project
    for texture_set in substance_painter.textureset.all():
        export_config["exportList"].append({
            "rootPath": texture_set.name(),
            "exportPreset": url.as_url(),
            "exportParameters": [
                {
                    "parameters": {
                        "padding": "infinite",
                        "dithering": True,
                        "resolution": [resolution, resolution]
                    }
                }
            ]
        })

    # 3. Trigger Asynchronous Export
    print(f"Exporting textures to {output_dir} at {resolution}x{resolution}...")
    result = substance_painter.export.export_project_textures(export_config)
    
    if result.status == substance_painter.export.ExportStatus.Success:
        print(f"Successfully exported {len(result.textures)} texture maps.")
    else:
        print(f"Export failed: {result.message}")

if __name__ == "__main__":
    batch_export_textures("C:/Project/Exported_Textures", resolution=4096)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Normal Map Baking Artifacts (Ray Misses & Inverted Seams)** | Frontal/Rear ray distances too small, or low/high poly mesh names do not match suffix naming conventions. | 1. Ensure object naming follows `*_low` and `*_high` pattern.<br>2. In Baker settings, set **Match** to `By Mesh Name`.<br>3. Increase **Max Frontal/Rear Distance** or supply an explicit cage mesh file (`.fbx`). |
| **GPU TDR Crash during 4K/8K Baking (`Display driver stopped responding`)** | Windows GPU Timeout Detection and Recovery (TDR) aborts long raytracing compute kernels. | 1. In Windows Registry (`HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers`), create `TdrDelay` (DWORD) and set value to `60` (seconds).<br>2. Restart workstation.<br>3. Bake maps individually or lower Antialiasing to 2x2. |
| **Unreal Engine Normal Map Inverted (Green Channel Y-)** | DirectX vs OpenGL normal map standard mismatch (DirectX uses Y-, OpenGL uses Y+). | 1. In Project Settings, verify Normal Map format is set to **DirectX** (for Unreal) or **OpenGL** (for Unity/Blender).<br>2. Alternatively, invert the Green channel in the Export Preset configuration. |
| **Missing Texture Set after Mesh Reimport** | Reimported FBX modified material slot names, breaking layer stack associations. | 1. In 3D DCC, preserve exact material slot assignment names.<br>2. In Painter, use *Edit $\rightarrow$ Re-project Layer Stack* to transfer painted layers to new geometry. |

---

## Command Line Syntax & Substance Automation Toolkit (SAT)

```bash
# Windows CLI: Launch Substance Painter with Mesh and Project
"C:\Program Files\Adobe\Adobe Substance 3D Painter\Adobe Substance 3D Painter.exe" --mesh "C:\Assets\Robot_Low.fbx"

# Substance Automation Toolkit: Compile SBS to SBSAR via CLI
sbscooker.exe --inputs "C:\Materials\metal_damaged.sbs" --output-path "C:\Materials\Compiled" --output-name "metal_damaged"

# Substance Automation Toolkit: Headless Batch Texture Rendering
sbsrender.exe render --input "C:\Materials\metal_damaged.sbsar" --output-path "C:\Textures\Batch" --set-value "$outputsize@11,11"
```

### Key Configuration Locations
- **Windows User Preferences**: `%USERPROFILE%\Documents\Adobe\Adobe Substance 3D Painter`
- **Windows Python Plugins**: `%USERPROFILE%\Documents\Adobe\Adobe Substance 3D Painter\python\plugins`
- **Windows Shelf & Assets**: `%USERPROFILE%\Documents\Adobe\Adobe Substance 3D Painter\assets`
- **macOS User Preferences**: `~/Library/Application Support/Adobe/Adobe Substance 3D Painter`

---

## Agent Operational Directive
> **MANDATORY**: When configuring export presets for game engines, ensure normal maps match the target API (DirectX for Unreal, OpenGL for Unity) and non-color data (Roughness, Metallic, AO) is exported with Linear gamma encoding.
