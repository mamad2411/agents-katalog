---
name: swpilotcli-open-doc
description: Open a SolidWorks document (.sldprt, .sldasm, .slddrw) by file path and activate it. Requires a file path argument. Use when the user wants to open a specific file in SolidWorks.
---

# SolidWorks Open Document

Open and activate a SolidWorks document by file path.

## Prerequisites

- **SolidWorks 2024+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime** on the system
- A valid `.sldprt`, `.sldasm`, or `.slddrw` file path

## What this Skill does

1. Connects to the running SolidWorks instance
2. Opens the specified file silently (no dialogs)
3. Activates the document so it becomes the active doc

## Quick start

```bash
# Open a part
dotnet run --project ./sup_tools/swpilotcli-open-doc/scripts/OpenDoc/OpenDoc.csproj -- "C:\path\to\part.sldprt"

# Open an assembly
dotnet run --project ./sup_tools/swpilotcli-open-doc/scripts/OpenDoc/OpenDoc.csproj -- "C:\path\to\assembly.sldasm"

# Open a drawing
dotnet run --project ./sup_tools/swpilotcli-open-doc/scripts/OpenDoc/OpenDoc.csproj -- "C:\path\to\drawing.slddrw"
```

Expected output:

```
成功開啟: C:\path\to\part.sldprt
```

## Return codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Cannot connect to SolidWorks |
| 3 | File path argument missing |
| 4 | OpenDoc failed (check error code in output) |
