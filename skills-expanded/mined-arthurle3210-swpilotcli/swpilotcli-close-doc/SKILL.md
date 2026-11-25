---
name: swpilotcli-close-doc
description: Close SolidWorks document(s). Supports three modes via argument: no argument or "nosave" closes the active document without saving; "save" silently saves then closes the active document (if file has never been saved, forces close without saving); "all" closes every open document without saving. Use when the user wants to close the current file, close and save, or close everything.
---

# SolidWorks Close Document

Close the active SolidWorks document, with optional save. Or close all open documents at once.

## Prerequisites

- **SolidWorks 2024+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime** on the system
- At least one document open in SolidWorks

## What this Skill does

- `nosave` (default): closes active document silently, no save, no dialog
- `save`: silently saves active document first, then closes; if file has no path (never saved), forces close without saving
- `all`: calls `CloseAllDocuments(true)` — closes every open document including unsaved ones

## Quick start

```bash
# Close active document, no save (default)
dotnet run --project ./sup_tools/swpilotcli-close-doc/scripts/CloseDoc/CloseDoc.csproj

# Close active document after saving
dotnet run --project ./sup_tools/swpilotcli-close-doc/scripts/CloseDoc/CloseDoc.csproj -- save

# Close ALL open documents
dotnet run --project ./sup_tools/swpilotcli-close-doc/scripts/CloseDoc/CloseDoc.csproj -- all
```

## Return codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Cannot connect to SolidWorks |
| 3 | No active document |
