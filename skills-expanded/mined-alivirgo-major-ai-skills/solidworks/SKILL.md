---
name: solidworks
description: "Automate SOLIDWORKS parts and assemblies with COM, Python, and VBA; inspect FeatureManager rebuild errors, configure mates, and batch-export CAD files."
category: cad
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["solidworks", "sldworks-api", "com", "batch-export", "step", "headless"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Dassault Systèmes SOLIDWORKS AI Skill Guide (Claude)

## Overview & Engine Architecture

SOLIDWORKS (pin **year** e.g. **2024 SP5**) exposes **COM automation** (`SldWorks.Application`), **VBA macros** (`.swp`), **.NET interop**, and **Document Manager** (headless metadata without full UI). Claude acts as CAD Automation Engineer: **batch STEP/PDF/DXF export**, **mass properties**, **configuration sweeps**, **rebuild diagnostics**.

**Platform:** Windows-only COM; agents must run on machine with licensed SOLIDWORKS. No true Linux headless GUI-less parity for all APIs.

```
┌─────────────────────────────────────────────────────────────┐
│  win32com → SldWorks.Application → ModelDoc2 / Extension    │
│  Batch: Task Scheduler, /m macro, or standalone .NET        │
│  Export: SaveAs3 / ExportToFile2 — check errors VARIANT     │
└─────────────────────────────────────────────────────────────┘
```

---

## When to use / when not to

**Use when:** parametric BOM/mass reports, configuration export matrices, drawing PDF batches, PDM-adjacent custom steps (respect PDM checkout rules).

**Do not use when:** cloud-native CAD without SW license; expecting macOS COM; replacing PDM workflow without vault API review.

---

## Operational Capabilities & Agent Directives

1. **COM lifecycle:** `Dispatch("SldWorks.Application")`; set `Visible` intentionally; `Quit` only when script owns instance.
2. **Rebuild truth:** After sketch/equation edits use **Ctrl+Q** full rebuild, not Ctrl+B.
3. **Export integrity:** Always read `errors` / `warnings` from `SaveAs3` / `ExportToFile2` VARIANT byref ints.
4. **Deterministic exports:** Fixed configuration name (`"Default"` vs `"@config"`); suppress design table driven configs explicitly in script.
5. **Large assemblies:** Lightweight / SpeedPak before mass ops; avoid resolving all components for metadata-only jobs — prefer **Document Manager** when licensed.
6. **Units:** API returns meters for mass properties — document conversion to mm/kg for reports.

---

## Production Python: STEP AP214 batch from active doc

```python
import win32com.client
from win32com.client import VARIANT
import pythoncom

def export_step(path: str) -> None:
    pythoncom.CoInitialize()
    sw = win32com.client.Dispatch("SldWorks.Application")
    sw.Visible = False
    model = sw.ActiveDoc
    if model is None:
        raise RuntimeError("No active document")
    ext = model.Extension
    errors = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    warnings = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    ok = ext.SaveAs3(path, 0, 2, None, None, errors, warnings)
    if not ok or errors.value != 0:
        raise RuntimeError(f"SaveAs failed err={errors.value} warn={warnings.value}")
```

Launch with existing session or `OpenDoc6` with full path; PDM: checkout first or export fails.

---

## Failure taxonomy

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| Red/yellow Feature tree | Dangling relations | What's Wrong? / Dangling filter |
| Over-defined mates | Red mate folder | Mate Diagnostics |
| Export empty STEP | Lightweight unresolved | Resolve or export from part |
| COM E_FAIL | SW not running / wrong ProgID | Start SW; match bitness (64-bit) |
| Drawing PDF missing sheets | Wrong sheet selection | `ExportPdfData` sheet array |

CLI: `"sldworks.exe" /m "C:\Macros\batch.swp"` for scheduled batch.

---

## Agent Operational Directive

> **MANDATORY**: Check SaveAs error VARIANTs. Pin SOLIDWORKS year. Use full rebuild after param changes. Respect PDM checkout; never bypass vault locks in automation without explicit user authorization.
