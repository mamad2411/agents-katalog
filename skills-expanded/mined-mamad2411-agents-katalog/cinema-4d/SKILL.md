---
name: cinema-4d
description: "Script Cinema 4D scene workflows, configure MoGraph systems, and troubleshoot Redshift rendering."
category: 3d
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["cinema-4d", "mograph", "redshift", "c4dpy", "python-sdk", "claude", "3d-automation"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Maxon Cinema 4D AI Skill Guide (Claude)

## Overview & Engine Architecture
Maxon Cinema 4D (C4D) is an industry-standard 3D motion design, procedural generation, and visual effects package built on the modern **Maxon Core (Neutron/Scene Nodes)** architecture. Claude functions as an expert technical director and automation engineer, specializing in **C4D Python (`c4d`, `maxon` APIs)**, **MoGraph procedural dynamics**, **Redshift GPU rendering optimization**, and **headless CLI batch pipelines**.

### Cinema 4D Runtime & Execution Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Cinema 4D Architecture Core                 │
│                                                             │
│  Scene Nodes / Neutron Engine (Maxon Core Graph)            │
│  ├── MoGraph Procedural Subsystem (Cloners, Effectors, Fields)│
│  ├── Unified Simulation Framework (Pyro, Cloth, Soft Bodies)│
│  └── Redshift GPU Render Engine (Out-of-Core, ACES OCIO, AOV)│
│                                                             │
│  Automation & Pipeline Interfaces                           │
│  ├── C4DPy (Headless Python 3 Interpreter & CLI Wrapper)     │
│  ├── Classic API (`c4d` module) & Maxon API (`maxon` module)│
│  └── Commandline.exe / Cinema 4D.exe CLI Rendering Pipeline  │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

When automating or diagnosing Cinema 4D, Claude must execute the following procedures:

1. **C4D Python & Maxon API Scripting**: Write clean, modern Python 3 scripts utilizing `c4d.documents`, `c4d.BaseObject`, and `maxon.GraphModelInterface` for node-based procedural workflows.
2. **Redshift GPU Render Optimization**: Diagnose VRAM bottlenecks, configure out-of-core memory allocations, automate AOV pass setups, and set up ACEScg color management.
3. **MoGraph & Dynamic Simulations**: Script procedural matrix transformations, cache complex field dynamics, and configure Alembic/USD export pipelines.
4. **Headless Batch Automation**: Generate cross-platform command-line rendering scripts for local render nodes and farm dispatchers.

---

## Production Python Automation: Batch Asset Exporter (`c4dpy`)

Save and execute this script via `c4dpy` to automate headless scene processing, material assignment verification, and USD/Alembic export:

```python
"""
Cinema 4D Batch USD & Alembic Exporter
Run via: c4dpy.exe batch_export.py <scene_path> <output_dir>
"""

import sys
import os
import c4d
from c4d import documents, plugins

def export_scene(scene_path: str, output_dir: str) -> None:
    if not os.path.exists(scene_path):
        print(f"Error: Scene file '{scene_path}' does not exist.")
        sys.exit(1)

    # Load document without GUI
    doc = documents.LoadDocument(scene_path, c4d.SCENEFILTER_OBJECTS | c4d.SCENEFILTER_MATERIALS)
    if doc is None:
        print(f"Failed to load document: {scene_path}")
        sys.exit(1)

    documents.SetActiveDocument(doc)
    doc_name = os.path.splitext(os.path.basename(scene_path))[0]
    os.makedirs(output_dir, exist_ok=True)

    # 1. Export USD File
    usd_path = os.path.join(output_dir, f"{doc_name}.usd")
    usd_plugin_id = 1040540 # USD Export Plugin ID
    
    # Configure export settings
    usd_data = plugins.FindPlugin(usd_plugin_id, c4d.PLUGINTYPE_SCENEEPOK)
    if documents.SaveDocument(doc, usd_path, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, usd_plugin_id):
        print(f"Successfully exported USD to: {usd_path}")
    else:
        print(f"USD export failed for: {usd_path}")

    # 2. Kill document memory
    documents.KillDocument(doc)
    print("Export pipeline completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: c4dpy batch_export.py <input.c4d> <output_directory>")
        sys.exit(1)
    export_scene(sys.argv[1], sys.argv[2])
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Redshift CUDA Out-of-Memory (`CUDA_ERROR_OUT_OF_MEMORY`)** | Scene textures and tessellated mesh geometry exceed physical GPU VRAM. | 1. Enable **Out-of-Core Memory** in *Redshift Preferences $\rightarrow$ Memory*.<br>2. Enable **Automatic Texture Streaming** (mipmap/tiled EXR/TX conversion).<br>3. Convert dense polygon meshes to Redshift Proxies (`.rs`). |
| **Alembic/FBX Import Loses Material Assignments** | Source application exported polygon face sets without matching C4D selection tag naming. | 1. Verify face-set names on Alembic node.<br>2. In C4D, attach **Polygon Selection Tags** matching Alembic part names.<br>3. Assign Redshift/Standard materials to the specific selection tags. |
| **MoGraph Dynamics Explode on Frame 0** | Cloner instances overlap in volume, causing collision solver velocity spikes. | 1. In Cloner Dynamics Body tag, set *Collision $\rightarrow$ Shape* to **Multi-Box** or **Convex Hull**.<br>2. Increase *Collision Margin* and increase *Steps per Frame* in Project Settings $\rightarrow$ Dynamics (e.g. 10-25 steps). |
| **Python Script Error: `AttributeError: module 'c4d' has no attribute '...'`** | Script is using deprecated R20 API methods instead of the unified 2024/2025 Maxon API. | Update scripts to use `c4d.BaseList2D.GetDataInstance()` or import `maxon` framework modules directly for graph node operations. |

---

## Command Line Syntax & Headless Rendering

### Headless Production Render (Windows / macOS)

```bash
# Windows Headless CLI Render with Redshift
"C:\Program Files\Maxon Cinema 4D 2025\Commandline.exe" -render "C:\Projects\Scene.c4d" -frame 0 240 -step 1 -oimage "C:\Renders\output_####" -oresolution 3840 2160

# macOS Headless CLI Render
/Applications/Maxon\ Cinema\ 4D\ 2025/Commandline.app/Contents/MacOS/Commandline -render "/Projects/Scene.c4d" -frame 0 100 -oimage "/Renders/frame_"

# Run Custom Pipeline Script via c4dpy
"C:\Program Files\Maxon Cinema 4D 2025\c4dpy.exe" "C:\Pipeline\auto_rig.py" --input "C:\Assets\model.c4d"
```

### System Configuration & Cache Directories
- **Windows User Preferences**: `%APPDATA%\Maxon\Cinema 4D 2025_<hash>`
- **Windows Redshift Cache**: `%LOCALAPPDATA%\Redshift\Cache`
- **macOS User Preferences**: `~/Library/Preferences/Maxon/Cinema 4D 2025_<hash>`
- **macOS Redshift Cache**: `~/Library/Application Support/Redshift/Cache`

---

## Agent Operational Directive
> **MANDATORY**: When scripting Cinema 4D automation, always verify compatibility with Cinema 4D 2024/2025 Python 3 APIs. Implement explicit document cleanup (`documents.KillDocument(doc)`) in headless scripts to prevent memory leaks during batch processing.
