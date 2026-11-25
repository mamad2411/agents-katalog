---
name: swpilotcli-delete-orphan-sketches
description: Delete all orphaned sketches in the active SolidWorks part — sketch features not absorbed by any extrusion, cut, or other parent feature. Iterates the feature tree, removes every top-level `ProfileFeature`, then rebuilds. Use for cleanup after discarded geometry experiments, or to remove leftover construction sketches before saving.
---

# SolidWorks Delete Orphan Sketches

Remove every sketch in the active document that is not consumed by a parent feature (extrude, cut, revolve, sweep, etc.).

## Prerequisites

- **SolidWorks 2024+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime**
- An active SolidWorks document

## What this Skill does

- Exits any active sketch first
- Walks the feature tree from `FirstFeature()`
- For each feature whose `GetTypeName2()` returns `ProfileFeature` (= unabsorbed sketch), selects and deletes it with `swDelete_Absorbed`
- Rebuilds and redraws
- Reports how many orphan sketches were deleted

## When to use

- After running draft sketches that you do not plan to extrude
- Before saving, to keep the feature tree clean
- As a one-shot reset of "orphan" construction geometry

## Quick start

```bash
dotnet run --project ./sup_tools/swpilotcli-delete-orphan-sketches/scripts/DeleteOrphanSketches/DeleteOrphanSketches.csproj
```

## Return codes

| Code | Meaning |
|------|---------|
| 0 | Success (0 or more orphans removed) |
| 1 | General error |
| 2 | Cannot connect to SolidWorks |
| 3 | No active document |
