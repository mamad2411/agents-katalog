---
name: adobe-after-effects
description: "Create and update After Effects compositions, expressions, and render queues using ExtendScript and Essential Graphics workflows."
category: video-editing
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["after-effects", "extendscript", "expressions", "render-queue", "mograph", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Adobe After Effects Motion Graphics AI Skill Guide (Claude)

## Overview & Engine Architecture
Adobe After Effects is a layer-based compositing and motion design tool organized around **Projects → Compositions → Layers**, with **expressions** (JavaScript-like), **effects**, **masks/shapes**, **3D cameras**, and the **Render Queue / Media Encoder** delivery path. Automation uses **ExtendScript (JSX)** against the AE DOM (`app.project`, `CompItem`, `AVLayer`). Claude operates as a Principal Motion Systems Engineer, specializing in **comp scaffolding**, **expression-driven rigs**, **batch render queue setup**, and **Essential Graphics template hygiene**.

### After Effects Composition & Scripting Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 After Effects Architecture                  │
│                                                             │
│  Project Graph                                              │
│  ├── FootageItem / FolderItem / CompItem                    │
│  ├── Layer types (AV, Shape, Text, Camera, Light, Null)     │
│  └── Properties / Keyframes / Expressions                   │
│                                                             │
│  Automation                                                 │
│  ├── ExtendScript DOM + JSON polyfills as needed            │
│  ├── Expressions engine (time, value, thisComp, thisLayer)  │
│  └── renderQueue items & output modules                     │
│                                                             │
│  Delivery                                                   │
│  ├── Render Queue / AME                                     │
│  ├── Essential Graphics (.mogrt)                            │
│  └── Dynamic Link with Premiere                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Comp Spec First**: Define width, height, frame rate, and duration before creating layers.
2. **Expressions vs Keyframes**: Prefer expressions for procedural/linked motion; keyframes for intentional animation curves.
3. **Render Queue Automation**: Create `OutputModule` settings explicitly (format, path, post-render actions).
4. **Null / Parent Rigs**: Build controller nulls for reusable motion systems instead of hardcoding layer indices.
5. **Version Portability**: Avoid undocumented scripting quirks; test JSX against the studio's AE major version.

---

## Production ExtendScript: Build Lower-Third Comp + Queue Render

```javascript
// ==============================================================================
// After Effects ExtendScript: create a lower-third comp and add to render queue
// ==============================================================================
(function () {
  app.beginUndoGroup("Create Lower Third");

  var proj = app.project;
  var comp = proj.items.addComp("LT_Hero", 1920, 1080, 1.0, 5.0, 30);
  var solid = comp.layers.addSolid([0.05, 0.55, 0.9], "Bar", 640, 96, 1.0);
  solid.position.setValue([420, 860]);

  var textLayer = comp.layers.addText("Product Launch");
  var textProp = textLayer.property("Source Text");
  var textDoc = textProp.value;
  textDoc.fontSize = 48;
  textDoc.fillColor = [1, 1, 1];
  textDoc.font = "Arial-BoldMT";
  textProp.setValue(textDoc);
  textLayer.position.setValue([420, 860]);

  // Simple slide-in via expression on Position
  solid.property("Position").expression =
    "var t = time; var x = ease(t, 0, 0.6, -200, 420); [x, 860]";

  var rq = app.project.renderQueue.items.add(comp);
  var om = rq.outputModule(1);
  // Apply a named template if present in the user's AE install:
  try {
    om.applyTemplate("H.264 - Match Render Settings - 15 Mbps");
  } catch (e) {
    // Fallback: leave default module; user picks preset
  }
  om.file = new File("~/Desktop/LT_Hero_Out.mp4");

  app.endUndoGroup();
  alert("Lower-third comp created and queued: " + comp.name);
})();
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Expression errors (yellow banner)** | Syntax / missing property path. | Open expression editor; use `thisComp.layer("Name")` carefully. |
| **Render queue template missing** | Output module template name not installed. | Catch applyTemplate errors; instruct user to pick local preset. |
| **Text font substitution** | Font not on machine. | Use licensed studio fonts; check Character panel font list. |
| **Dynamic Link stale frames** | Premiere/AE cache desync. | Refresh Dynamic Link / purge memory & disk cache. |

---

## Essential Expression Snippets

```javascript
// Smooth follow of another layer's position
var target = thisComp.layer("Controller");
ease(time, 0, 1, target.transform.position, target.transform.position)
// Better: use linear interpolation toward target each frame via loopOut or valueAtTime patterns
```

### Essential Paths
- **Scripts**: AE `Scripts` / `ScriptUI Panels`
- **Preferences**: Media & Disk Cache
- **mogrt**: Essential Graphics export for Premiere

---

## Agent Operational Directive
> **MANDATORY**: Wrap project mutations in `beginUndoGroup` / `endUndoGroup`. Set comp specs explicitly. Treat output module template names as environment-specific and fail gracefully when missing.
