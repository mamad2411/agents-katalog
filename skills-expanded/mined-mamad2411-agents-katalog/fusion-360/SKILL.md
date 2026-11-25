---
name: fusion-360
description: "Automate Autodesk Fusion parametric models with the Python API, inspect timeline features, and prepare CAM workflows for review."
category: cad
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["fusion-360", "adsk-python", "parametric", "cam", "batch-export", "cloud-hub"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Autodesk Fusion AI Skill Guide (Claude)

## Overview & Engine Architecture

Autodesk Fusion (pin **monthly build** — `Help → About`) runs **in-process Python 3.x** via `adsk.core`, `adsk.fusion`, `adsk.cam`. Designs live in **cloud hubs** with local cache. Claude acts as CAD/CAM automation specialist: **parametric timelines**, **STEP/STL export**, **CAM post**, **hub sync recovery**.

**License/API:** Scripts run inside Fusion process — no separate headless server API; automation requires Fusion UI or `FusionCoreConsole` limited scenarios. **Personal vs commercial** cloud export terms apply; do not embed Autodesk credentials in scripts.

```
┌─────────────────────────────────────────────────────────────┐
│  adsk.core.Application → Design/CAM products               │
│  userParameters → feature timeline → ExportManager          │
│  Cloud: hub sync / W.Cache — batch blocked if upload stuck   │
└─────────────────────────────────────────────────────────────┘
```

---

## When to use / when not to

**Use when:** parametric generators, drawing exports, CAM toolpath sanity checks, configuration sweeps via parameters.

**Do not use when:** unattended farm without Fusion session; replacing Vault/PLM without Data Management API review.

---

## Operational Capabilities & Agent Directives

1. **Add-in structure:** `run(context)` entry; `commands.start()` for UI commands; `try/except` + `ui.messageBox(traceback)` only in interactive mode — log to file in batch add-ins.
2. **Parameters:** Drive dimensions via `design.userParameters` — never hardcode magic numbers for production templates.
3. **Export pipeline:** `exportManager.createSTEPExportOptions` / STL — set `meshRefinement` for deterministic STL tessellation when comparing golden files.
4. **Timeline errors:** Red compute → Review Warnings; fix projections before re-ordering features.
5. **CAM:** Verify stock, tool diameter, `minimumCuttingRadius`; post via `.cps` — validate G-code simulator before shop floor.
6. **Sync:** Stuck upload → close Fusion, clear W.Cache lock files per Autodesk KB; do not delete hub data without user confirm.

---

## Production Python: export STEP from active design

```python
import adsk.core, adsk.fusion, traceback

def run(context):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    if not design:
        raise RuntimeError("Active product is not a Fusion design")
    export_mgr = design.exportManager
    file = adsk.core.FileDialog.create()
    file.isMultiSelectEnabled = False
    file.filter = "STEP (*.stp)"
    if file.showSave() != adsk.core.DialogResults.DialogOK:
        return
    opts = export_mgr.createSTEPExportOptions(file.filename)
    opts.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
    export_mgr.execute(opts)
```

Run via **Scripts and Add-Ins** or registered command; for CI-style regression, compare STEP hash after fixed parameter set.

---

## Failure taxonomy

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| Red timeline extrude | Open profile / lost proj | Edit sketch, re-project |
| T-spline to BREP fail | Non-manifold | Repair Body |
| Empty toolpath | Tool too large / bad stock | CAM setup |
| Upload pending loop | Cache lock | W.Cache cleanup, relaunch |
| API None | Wrong workspace (CAM vs Design) | `activeProduct` cast check |

---

## Agent Operational Directive

> **MANDATORY**: Parameterize features. Set explicit mesh refinement for deterministic mesh exports. Handle cloud sync failures before batch export. Never store Autodesk passwords in repo.
