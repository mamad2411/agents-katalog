---
name: davinci-resolve-mcp
description: "Use when automating DaVinci Resolve Studio 20 through its local MCP server — timeline editing, color grading, Fusion compositing, Fairlight audio, rendering, or media pool operations."
compatibility:
  requires:
    - DaVinci Resolve Studio 20.x (free version does NOT support external scripting)
    - samuelgursky/davinci-resolve-mcp server running locally
    - Resolve preference: General → External scripting using → Local
---

# DaVinci Resolve Studio 20 — MCP Automation Skill

## Quick Start

Before any tool call, verify connection with:
```
resolve → get_version
```
If no response, the MCP server isn't running or Resolve isn't open. Resolve must be running AND the scripting preference set to Local.

---

## MCP Tool Architecture

The server exposes **27 compound tools**. Each tool has an `action` parameter that selects the operation. Always match the tool to the correct API object — wrong tool for the wrong layer will return empty results or errors.

### Tool-to-Object Map

| Tool | API Object | Use for |
|------|-----------|---------|
| `resolve` | Resolve | App control, page navigation, version |
| `project_manager` | ProjectManager | Create/load/save/list/export projects, database ops |
| `project` | Project | Name, settings, get media pool, get gallery, get timeline |
| `media_storage` | MediaStorage | Browse volumes and filesystem, add items to pool |
| `media_pool` | MediaPool | Bins, import, timeline creation, clip selection |
| `folder` | Folder | Clip lists, subfolder traversal, transcribe audio |
| `media_pool_item` | MediaPoolItem | Clip name, metadata, markers, properties, proxy linking |
| `timeline` | Timeline | Track ops, markers, export, detect scene cuts, settings |
| `timeline_item` | TimelineItem | Per-clip properties, markers, grade copy, magic mask, stabilize |
| `timeline_item_fusion` | TimelineItem.Fusion | Add/import/export/delete Fusion compositions |
| `timeline_item_version` | TimelineItem.Versions | Grade versions (add/load/rename/delete) |
| `timeline_item_take` | TimelineItem.Takes | Take management for alternate source clips |
| `timeline_item_flags` | TimelineItem.Flags | Flag color, clip color labels |
| `timeline_item_stereo` | TimelineItem.Stereo | Stereoscopic 3D convergence/floating window |
| `timeline_item_node` | TimelineItem + Graph | LUT, CDL, node add/delete/graph on color nodes |
| `render` | Project.Render | Render queue add/delete/start/stop/status/formats |
| `gallery` | Gallery | Albums, stills navigation |
| `gallery_stills` | GalleryStillAlbum | Grab/export/import/apply/delete stills and PowerGrades |
| `layout_preset` | Resolve.Layout | UI layout save/load/update/delete |
| `color_group` | ColorGroup | Scene/shot color groups |
| `keyframe_mode` | Resolve | Keyframe mode: ALL(0), COLOR(1), SIZING(2) |
| `render_preset` | Project.RenderPreset | Load/save/delete/import/export render presets |
| `burn_in_preset` | Resolve + Project | Burn-in text overlay presets |
| `fairlight_preset` | Resolve + Project | Audio channel preset recall |
| `database` | ProjectManager.DB | Get/set/list databases |
| `cloud_project` | ProjectManager.Cloud | Cloud project create/load/import/restore |
| `fusion_comp` | Fusion Composition | Node graph: add/wire/set params/keyframe/render |

---

## Core Workflow Patterns

### 1. Page Navigation
```
resolve → open_page → page: "cut" | "edit" | "color" | "fusion" | "fairlight" | "deliver" | "media"
```

### 2. Project Lifecycle
```
project_manager → create_project → name: "ProjectName"
project_manager → load_project → name: "ExistingProject"
project_manager → save_project
project_manager → export_project → filePath: "/exports/project.drp"
```

### 3. Media Import → Timeline
```
media_pool → import_media → items: ["/path/file.mov", ...]
media_pool → add_sub_folder → name: "B-Roll"
media_pool → create_timeline_from_clips → name: "Assembly", clips: [...]
project → set_current_timeline → timeline: <timeline_object>
```

### 4. Clip Property Control
All via `timeline_item → set_property` with string key + value:

**Transform keys:** `Pan`, `Tilt`, `ZoomX`, `ZoomY`, `ZoomGang`, `RotationAngle`, `AnchorPointX`, `AnchorPointY`, `Pitch`, `Yaw`, `FlipX`, `FlipY`

**Crop keys:** `CropLeft`, `CropRight`, `CropTop`, `CropBottom`, `CropSoftness`, `CropRetain`

**Composite keys:** `CompositeMode` (int 0–29), `Opacity` (0–100)

**Retime keys:** `RetimeProcess` (0=Nearest, 1=Frame Blend, 2=Optical Flow, 3=Speed Warp), `MotionEstimation` (0–6)

**Lens:** `Distortion`, `LenCorrection`, `LenCorrectionStrength`

### 5. Color Node Operations
```
# Add a serial node (adds after current)
timeline_item_node → add_node

# Apply LUT to node index
timeline_item_node → set_lut → nodeIndex: 2, lutPath: "/path/to/lut.cube"

# Apply CDL values
timeline_item_node → set_cdl → {Slope: [r,g,b], Offset: [r,g,b], Power: [r,g,b], Saturation: 1.0}

# Grade versions
timeline_item_version → add_version → name: "Client v2"
timeline_item_version → load_version → name: "Client v2"
```

### 6. Gallery Stills
```
gallery_stills → grab_still              # Grabs still from current frame
gallery_stills → export_stills → folderPath: "/exports/stills", format: "dpx"
gallery_stills → apply_still → still: <still_obj>
```

### 7. Render Pipeline
```
render → set_render_settings → {FormatWidth: 3840, FormatHeight: 2160, ...}
render_preset → load → name: "YouTube"        # Apply preset first
render → add_render_job                        # Queue current settings
render → start_rendering                       # Start all jobs
render → get_render_job_status → jobId: "..."  # Poll status
render → get_render_formats                    # List available formats
```

### 8. Fusion Compositing
```
timeline_item_fusion → add_fusion_comp         # Add comp to clip
fusion_comp → add_node → node_type: "TextPlus"
fusion_comp → add_node → node_type: "Merge"
fusion_comp → wire_connection → from: "Text1", to: "Merge1"
fusion_comp → set_parameter → node: "Text1", param: "Size", value: 0.1
fusion_comp → set_keyframe → node: "Text1", param: "Size", frame: 30, value: 0.2
```

### 9. Timeline Track & Marker Ops
```
timeline → get_items_in_track → type: "video", index: 1
timeline → add_track → type: "audio"
timeline → add_marker → frameId: 100, color: "Blue", name: "VFX Shot", note: "cleanup needed"
timeline → detect_scene_cuts
timeline → export → fileName: "out.aaf", exportType: "EXPORT_AAF"
```

---

## Prompt Pattern Library

See `references/prompt-patterns.md` for the complete natural-language → MCP action mapping table (80+ patterns across all pages).

## Keyboard Shortcut Reference

See `references/keyboard-shortcuts.md` for the complete 370+ shortcut table organized by page.

## Page Capabilities Reference

See `references/page-capabilities.md` for deep-dive on Color page node types, Fusion node categories, Fairlight routing, and Deliver codec matrix.

---

## Composite Mode Values (CompositeMode property)

| Value | Mode | Value | Mode |
|-------|------|-------|------|
| 0 | Normal | 10 | Difference |
| 1 | Highlight | 11 | Exclusion |
| 2 | Shadow | 12 | Hue |
| 3 | Highlight+Shadow | 13 | Saturation |
| 4 | Color Burn | 14 | Color |
| 5 | Linear Burn | 15 | Luminosity |
| 6 | Color Dodge | 16 | Screen |
| 7 | Linear Dodge | 17 | Multiply |
| 8 | Overlay | 18 | Darken |
| 9 | Hard Light | 19 | Lighten |

---

## Render Format/Codec Quick Reference

| Format | Codecs |
|--------|--------|
| MP4 | H.264, H.265 |
| QuickTime | ProRes 422/HQ/LT/Proxy/4444/4444XQ, DNxHD, DNxHR, H.264, H.265 |
| MXF | DNxHD, DNxHR, JPEG2000, XDCAM, Sony XAVC |
| EXR | RGB Half, RGB Float, DWAA, DWAB |
| DCP | JPEG 2000 |
| Image Seq | DPX, TIFF, Cineon |

Alpha output requires ProRes 4444/4444XQ, DNxHR 444, Uncompressed, or EXR.

---

## Error Handling Patterns

**"No connection to Resolve"** → Resolve must be open + scripting set to Local in preferences.

**"Method not available"** → Check if using Studio (free version has no scripting). Confirm tool matches correct API object layer.

**"Timeline item not found"** → Must call `project → get_current_timeline` then `timeline → get_items_in_track` to get valid item references first.

**"LUT path not found"** → LUT files must be in a path Resolve can access. Use absolute paths. Relative paths fail.

**"Render job failed"** → Check codec/format availability with `render → get_render_formats` and `render → get_render_codecs` before setting.

---

## DaVinci Resolve 20 AI Features (Studio Only)

These are triggered via the UI (not MCP-scriptable), but worth noting for workflow guidance:
- **IntelliScript** — auto-assembles timeline from script + transcript sync
- **IntelliCut** — removes silences, checkerboards dialogue by speaker
- **Multicam SmartSwitch** — auto-selects camera angles by speaker
- **Audio Assistant** — generates professional mix automatically
- **Magic Mask v2** — AI person/object isolation (scriptable via `timeline_item → create_magic_mask`)
- **SuperScale Enhanced** — 2x/3x/4x AI upscaling (`set_property → SuperScale: 2`)
- **Voice Convert** — AI voice model transformation
- **Speed Warp** — highest-quality retiming (`RetimeProcess: 3`)
