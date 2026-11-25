---
name: swpilotcli-sketch-exit
description: Exit the active SolidWorks sketch and report its constraint status (Fully Defined / Under-Constrained / Over-Constrained). Call this after swpilotcli-sketch-draw to commit geometry and check if the sketch is fully constrained.
---

# swpilotcli-sketch-exit

Commit and exit the active sketch, then report constraint status.

## Prerequisites

- SolidWorks is running
- A sketch is currently being edited (active sketch exists)

## What this Skill does

1. Calls `EditRebuild3()` — commits sketch and exits editing mode
2. Calls `GetConstrainedStatus()` — reads solver result
3. Reports: Fully Defined / Under-Constrained / Over-Constrained

## Quick start

```bash
dotnet run --project ./sup_tools/swpilotcli-sketch-exit/scripts/SketchExit/SketchExit.csproj
```

Expected output:

```
Sketch status: Fully Defined
```

## Notes

- Always call this after swpilotcli-sketch-draw when the user is done drawing
- If Under-Constrained, the sketch needs more relations or dimensions
- If Over-Constrained, there are conflicting constraints to resolve
