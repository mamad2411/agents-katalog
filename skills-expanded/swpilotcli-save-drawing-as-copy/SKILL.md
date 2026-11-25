---
name: swpilotcli-save-drawing-as-copy
description: Save a SolidWorks drawing (.slddrw) as a copy to a new file path, without changing the original document's path or closing it. Requires two arguments: source drawing path and output path. Use when you need to duplicate a drawing under a new name or location while keeping the original open and unmodified. Useful as a building block in LLM-orchestrated batch rename/copy workflows.
---

# SolidWorks Save Drawing As Copy

Save a copy of a SolidWorks drawing to a new path using the Copy flag, so the original document remains unaffected.

## Prerequisites

- **SolidWorks 2024+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime** on the system
- A valid `.slddrw` source file path

## What this Skill does

1. Opens the source drawing silently (or reuses it if already open)
2. Calls `SaveAs3` with `swSaveAsOptions_Copy | swSaveAsOptions_Silent`
3. The original document path is NOT changed — the file stays open as-is
4. Reports output file size on success

## Quick start

```bash
dotnet run --project ./sup_tools/swpilotcli-save-drawing-as-copy/scripts/SaveDrawingAsCopy/SaveDrawingAsCopy.csproj -- "C:\source\drawing.slddrw" "C:\output\drawingAA.slddrw"
```

## Return codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Missing arguments or general error |
| 2 | Cannot connect to SolidWorks |
| 4 | Cannot open source file |
| 5 | SaveAs3 failed |

## Notes

- Only supports `.slddrw` output format
- For other formats (PDF, DWG, etc.) use `swpilotcli-save-drawing-as` instead
