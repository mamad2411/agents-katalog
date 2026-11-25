---
name: swpilotcli-undo-one-step
description: Execute one SolidWorks undo action on the active document (equivalent to pressing Ctrl+Z once). Use when you need to roll back the most recent operation quickly.
---

# Undo One Step

Execute one undo action on the active SolidWorks document.

## Prerequisites

- SolidWorks is running
- A document is open and active (`.sldprt`, `.sldasm`, or `.slddrw`)

## What this Skill does

1. Connects to the running SolidWorks instance
2. Gets the active document
3. Calls `IModelDoc2.EditUndo2(1)`
4. Redraws graphics

## When to use

- You want Ctrl+Z behavior in automation
- You just ran a tool and need to revert one step
- You need a deterministic one-step rollback command

## Quick start

```bash
dotnet run --project ./sup_tools/swpilotcli-undo-one-step/scripts/UndoOneStep/SolidWorksConsole.csproj
```

Expected output:

```
Undo executed: 1 step.
```

## Reference

See [API_REFERENCE.md](API_REFERENCE.md) for return codes and API details.

## Notes

- This tool always undoes exactly one step
- The exact effect depends on current SolidWorks undo stack state
