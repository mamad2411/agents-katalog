---
name: 3d-slicer
description: "Automate 3D Slicer research workflows with MRML, VTK/ITK, DICOM data, and Segment Editor. Use for software workflows, not clinical interpretation."
category: medical
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["3d-slicer", "mrml-scene", "dicom-processing", "vtk-itk", "segment-editor", "medical-imaging", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# 3D Slicer Medical Image Computing AI Skill Guide (Claude)

## Overview & Engine Architecture
3D Slicer is the premier open-source platform for medical image informatics, clinical visualization, and surgical planning. Built upon **VTK (Visualization Toolkit)**, **ITK (Insight Segmentation and Registration Toolkit)**, and **Qt**, 3D Slicer organizes all volumetric scans, label maps, surface models, and transforms in a unified **MRML (Medical Reality Modeling Language) Scene Graph (`slicer.mrmlScene`)**. Slicer embeds a full **Python 3 environment (`PythonSlicer.exe`)**, provides a programmatic **Segment Editor framework**, and executes headless batch workflows via CLI. Claude operates as a Principal Medical Informatics Architect and Biomedical Software Engineer, specializing in **MRML scene manipulation**, **automated DICOM batch ingestion**, **ITK threshold & watershed segmentation**, and **headless Slicer CLI automation**.

### 3D Slicer MRML & VTK/ITK Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 3D Slicer System Architecture               │
│                                                             │
│  Presentation & MRML Scene Layer                            │
│  ├── MRML Scene Graph (`slicer.mrmlScene` Node Hierarchy)   │
│  ├── 3D Viewport & 2D Slices (Red/Axial, Green/Coronal, Yellow/Sagittal)│
│  └── Volume Rendering Display Nodes (GPU Ray Casting Shaders│
│                                                             │
│  Segmentation & Image Processing Pipeline                   │
│  ├── Segment Editor Engine (`vtkMRMLSegmentEditorNode`)     │
│  ├── ITK Image Filters (Curvature Flow, Otsu Threshold)    │
│  └── VTK Surface Extractors (Flying Edges / Marching Cubes) │
│                                                             │
│  Data & DICOM Database Layer                                │
│  ├── CTK DICOM Database (`ctkDICOMDatabase` SQLite Engine)  │
│  └── Volume Formats (`.nrrd`, `.nii.gz`, Multi-Frame DICOM) │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **MRML Scene Automation via Python**: Author Python scripts interacting with `slicer.mrmlScene`, querying nodes by class (`slicer.util.getNodesByClass('vtkMRMLScalarVolumeNode')`), and managing transform hierarchies.
2. **Automated Segment Editor Scripting**: Construct automated segmentation routines using thresholding, masking, and island removal effects to extract anatomical structures (bones, lungs, vessels).
3. **3D Surface Model Generation & STL Export**: Convert segmented labelmaps into smoothed polygonal surface models (`vtkMRMLModelNode`) and export to STL/OBJ for surgical guide 3D printing.
4. **Headless CLI Execution**: Orchestrate batch clinical image pipelines using `Slicer.exe --no-splash --no-main-window --python-script <script.py>`.

---

## Production Python Automation: Automated Bone Segmentation & STL Exporter (`3D Slicer`)

Save this script as `batch_segment_bone.py` and run via `Slicer.exe --no-splash --no-main-window --python-script batch_segment_bone.py`:

```python
"""
3D Slicer Headless Python Automation: Automated Bone Segmentation & STL Export
Loads a CT volume (.nrrd / DICOM), segments bone (Hounsfield threshold), and exports STL.
"""

import sys
import os
import slicer

def process_ct_volume(input_volume_path: str, output_stl_path: str, min_hu: float = 200.0, max_hu: float = 3000.0):
    print(f"--- [3D SLICER MEDICAL IMAGE PROCESSING PIPELINE] ---")
    print(f"Loading CT Volume: {input_volume_path}...")

    # 1. Load Volume into MRML Scene
    volume_node = slicer.util.loadVolume(input_volume_path)
    if not volume_node:
        print("Error: Failed to load scalar volume into MRML scene.")
        slicer.app.exit(1)

    # 2. Create Segmentation Node and Setup Segment Editor
    segmentation_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
    segmentation_node.CreateDefaultDisplayNodes()
    segmentation_node.SetReferenceImageGeometryParameterFromVolumeNode(volume_node)

    # Add 'Bone' Segment
    bone_segment_id = segmentation_node.GetSegmentation().AddEmptySegment("Bone")

    # Initialize Segment Editor Logic
    segment_editor_widget = slicer.qMRMLSegmentEditorWidget()
    segment_editor_widget.setMRMLScene(slicer.mrmlScene)
    segment_editor_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
    segment_editor_widget.setMRMLSegmentEditorNode(segment_editor_node)
    segment_editor_widget.setSegmentationNode(segmentation_node)
    segment_editor_widget.setMasterVolumeNode(volume_node)

    # 3. Apply Threshold Effect for Bone (HU: 200 - 3000)
    print(f"Applying Thresholding Filter (HU: {min_hu} - {max_hu})...")
    segment_editor_widget.setActiveEffectByName("Threshold")
    effect = segment_editor_widget.activeEffect()
    effect.setParameter("MinimumThreshold", str(min_hu))
    effect.setParameter("MaximumThreshold", str(max_hu))
    effect.self().onApply()

    # 4. Generate Closed Surface 3D Representation
    print("Generating 3D Closed Surface Mesh (Flying Edges)...")
    segmentation_node.CreateClosedSurfaceRepresentation()

    # 5. Export 3D Mesh to STL
    print(f"Exporting 3D Mesh to: {output_stl_path}...")
    slicer.modules.segmentations.logic().ExportSegmentsClosedSurfaceRepresentationToFiles(
        output_stl_path,
        segmentation_node,
        [bone_segment_id],
        "STL"
    )

    print("✅ Pipeline complete! STL exported successfully.")
    slicer.app.exit(0)

if __name__ == "__main__":
    # Example test execution within Slicer
    input_file = "C:/Data/Sample_CT_Head.nrrd"
    output_dir = "C:/Data/Exported_Models"
    os.makedirs(output_dir, exist_ok=True)
    process_ct_volume(input_file, output_dir)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Volume Rendering Shows Blank Screen on Windows** | GPU ray casting shader fails on integrated graphics lacking OpenGL 4.5 capabilities. | 1. In Volume Rendering module $\rightarrow$ Set Rendering Method to **CPU Ray Casting**.<br>2. In Volume Display Node, adjust **Scalar Opacity Mapping** transfer curve window/level. |
| **DICOM Import Skips Series: `Unrecognized SOP Class`** | Enhanced multi-frame DICOM IOD or Radiation Therapy (RTSTRUCT) object missing dedicated plugin. | In Extension Manager, install **QuantitativeReporting** and **SlicerRT** extensions $\rightarrow$ Re-import DICOM. |
| **Headless Script Fails: `slicer.app.exit()` Freezes** | Script finished processing but background Qt event loop worker held an active timer. | Use `slicer.app.exit(0)` instead of `sys.exit(0)` to ensure clean Slicer application teardown. |
| **Out-Of-Memory During High-Res Mesh Generation** | Generating un-decimated marching cubes surface from massive $512\times 512\times 1000$ voxel grid. | In Segmentation node representation settings, enable **Decimate Target Reduction = 0.5** and **Smoothing Factor = 0.5**. |

---

## Command Line Syntax & Batch Processing

```bash
# 1. Run Headless Slicer Python Script
"C:\Program Files\Slicer 5.6\Slicer.exe" --no-splash --no-main-window --python-script "C:\Scripts\batch_segment_bone.py"

# 2. Run Standalone Python Interpreter Bundled with Slicer
"C:\Program Files\Slicer 5.6\bin\PythonSlicer.exe" -m pip install pydicom scikit-image

# 3. Launch Slicer and Load Volume Immediately
Slicer.exe --volume "C:\Data\scan.nrrd"
```

### Essential File Locations
- **Slicer Preferences**: `%APPDATA%\NA-MIC\Slicer.ini` (Windows) or `~/.config/NA-MIC/Slicer.ini` (Linux)
- **DICOM Database Root**: `~/Documents/SlicerDICOMDatabase/`

---

## Agent Operational Directive
> **MANDATORY**: In headless 3D Slicer batch scripts, always exit using `slicer.app.exit(0)` rather than `sys.exit()` to avoid Qt event loop deadlocks and memory corruption.
