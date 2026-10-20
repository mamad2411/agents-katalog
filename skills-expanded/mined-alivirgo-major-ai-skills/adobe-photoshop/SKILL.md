---
name: adobe-photoshop
description: "Automate Photoshop image-processing tasks with UXP or ExtendScript, Actions, batch jobs, and Smart Objects."
category: design
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["photoshop", "extendscript", "uxp", "actions", "batch", "smart-objects", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Adobe Photoshop Image Pipeline AI Skill Guide (Claude)

## Overview & Engine Architecture
Adobe Photoshop is a pixel/layer compositor for retouching, compositing, and design production. Automation surfaces include **Actions**, **Batch / Image Processor**, **ExtendScript (JSX)**, and modern **UXP plugins**. Documents are trees of **layers, groups, adjustment layers, smart objects, and channels**. Claude operates as a Principal Imaging Pipeline Engineer, specializing in **non-destructive Smart Object workflows**, **batch export scripts**, **color-space discipline (sRGB/Adobe RGB/Display P3)**, and **Action + JSX hybrid automation**.

### Photoshop Document & Automation Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Photoshop Architecture                      │
│                                                             │
│  Document Model                                             │
│  ├── Layer / LayerSet / ArtLayer                            │
│  ├── Smart Objects / Linked Assets                          │
│  └── Channels / Paths / Histories                           │
│                                                             │
│  Automation                                                 │
│  ├── Actions & Batch                                        │
│  ├── ExtendScript DOM (app.activeDocument)                  │
│  └── UXP plugins (modern JS + manifest)                     │
│                                                             │
│  Color & Export                                             │
│  ├── Color profiles / bit depth                             │
│  ├── Export As / Save for Web legacy                        │
│  └── Generator / Asset export naming                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Non-Destructive First**: Prefer Smart Objects + adjustment layers over flattening early.
2. **Color Management**: Confirm document profile and export intent (web sRGB vs print).
3. **Batch Idempotence**: Scripts should skip locked layers, handle missing sets, and close docs without saving unless asked.
4. **Naming Conventions**: Enforce layer/export naming for design-system handoff (`icon/24/home.png`).
5. **UXP vs JSX**: Prefer UXP for new panels; keep JSX when studio pipelines already depend on it.

---

## Production ExtendScript: Batch Resize & sRGB Export Folder

```javascript
// ==============================================================================
// Photoshop ExtendScript: resize folder of images to max edge 2048, save sRGB JPEG
// ==============================================================================
(function () {
  var inputFolder = Folder.selectDialog("Select input folder");
  var outputFolder = Folder.selectDialog("Select output folder");
  if (!inputFolder || !outputFolder) return;

  var files = inputFolder.getFiles(/\.(jpg|jpeg|png|tif|tiff)$/i);
  for (var i = 0; i < files.length; i++) {
    var doc = open(files[i]);
    var maxEdge = 2048;
    var w = doc.width.as("px");
    var h = doc.height.as("px");
    var scale = Math.min(1, maxEdge / Math.max(w, h));
    if (scale < 1) {
      doc.resizeImage(
        UnitValue(w * scale, "px"),
        UnitValue(h * scale, "px"),
        null,
        ResampleMethod.BICUBICSHARPER
      );
    }

    // Convert to sRGB when profile present
    try {
      doc.convertProfile("sRGB IEC61966-2.1", Intent.RELATIVECOLORIMETRIC, true, true);
    } catch (e) {}

    var outFile = new File(outputFolder + "/" + doc.name.replace(/\.[^\.]+$/, "") + "_2048.jpg");
    var opts = new JPEGSaveOptions();
    opts.quality = 10;
    opts.embedColorProfile = true;
    doc.saveAs(outFile, opts, true);
    doc.close(SaveOptions.DONOTSAVECHANGES);
  }
  alert("Processed " + files.length + " files.");
})();
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`activeDocument` null** | No file open. | Open/create document before DOM calls. |
| **convertProfile throws** | Missing profile / already unmanaged. | Wrap in try/catch; assign profile first if needed. |
| **Batch skips files** | Filter regex or permissions. | Verify extensions; run Photoshop as user with folder ACL. |
| **Smart Object rasterized unexpectedly** | Script used raster-only ops. | Prefer Edit Contents / export SO instead of rasterize. |

---

## Essential Action + Script Pattern

```text
1. Record Action for retouch steps that need human brush intent
2. Call Action from JSX via doAction("ActionName", "SetName")
3. Keep exports in script for deterministic paths/quality
```

### Essential Paths
- **Actions**: Window → Actions
- **Scripts**: File → Scripts
- **Color Settings**: Edit → Color Settings

---

## Agent Operational Directive
> **MANDATORY**: Default to non-destructive Smart Object workflows. Always specify color profile intent on export. Close batch documents with `DONOTSAVECHANGES` unless the user requested in-place saves.
