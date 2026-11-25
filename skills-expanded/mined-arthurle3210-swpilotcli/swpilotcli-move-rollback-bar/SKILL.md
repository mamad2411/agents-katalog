---
name: swpilotcli-move-rollback-bar
description: Move the SolidWorks Rollback Bar to a specified feature position. Use this to suppress features by moving the rollback bar before or after any feature in the Feature Tree.
---

# Move Rollback Bar

## Prerequisites

- SolidWorks must be running
- An active Part (.sldprt) or Assembly (.sldasm) document must be open
- The target feature must exist in the Feature Tree

## What this Skill does

Moves the Rollback Bar (歷程條) in the Feature Manager to a specified position relative to a feature. This allows you to:
- Suppress features that come after the rollback bar
- Temporarily exclude features from model evaluation
- Roll back the model to an earlier state in the design history

## When to use

- You want to suppress a feature and all features after it
- You need to temporarily return the model to an earlier design state
- You want to edit features that depend on features created later in the tree

## Quick start

**First, view all features:**
```bash
dotnet run --project ./sup_tools/swpilotcli-move-rollback-bar/scripts/MoveRollbackBar/MoveRollbackBar.csproj
```
This displays the complete feature list with indices.

### Move rollback bar by index (recommended):
```bash
# Move before feature [18]
dotnet run --project ./sup_tools/swpilotcli-move-rollback-bar/scripts/MoveRollbackBar/MoveRollbackBar.csproj -- 18 before
```

### Move rollback bar by feature name:
```bash
dotnet run --project ./sup_tools/swpilotcli-move-rollback-bar/scripts/MoveRollbackBar/MoveRollbackBar.csproj -- "草圖1" before
```

### Move rollback bar to end (restore all):
```bash
dotnet run --project ./sup_tools/swpilotcli-move-rollback-bar/scripts/MoveRollbackBar/MoveRollbackBar.csproj -- "" end
```

## Examples

**Example 1: List all features with indices**
```bash
dotnet run --project ./sup_tools/swpilotcli-move-rollback-bar/scripts/MoveRollbackBar/MoveRollbackBar.csproj
```
Output shows:
```
[0] 備註
[1] 最愛
...
[18] 草圖1
[19] 本體-移動/複製1
...
```

**Example 2: Move rollback bar before feature at index 20**
```bash
dotnet run --project ./sup_tools/swpilotcli-move-rollback-bar/scripts/MoveRollbackBar/MoveRollbackBar.csproj -- 20 before
```

**Example 3: Move rollback bar after "草圖1" (by name)**
```bash
dotnet run --project ./sup_tools/swpilotcli-move-rollback-bar/scripts/MoveRollbackBar/MoveRollbackBar.csproj -- "草圖1" after
```

**Example 4: Return to end (unsuppress all)**
```bash
dotnet run --project ./sup_tools/swpilotcli-move-rollback-bar/scripts/MoveRollbackBar/MoveRollbackBar.csproj -- "" end
```

## Reference

### Command Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `targetFeature` | string\|int | (required) | Feature name (string) or index number (int). Leave empty for "end" location. |
| `location` | string | "before" | Position relative to feature: `before`, `after`, `end`, `previous` |

### Argument Formats

- **By Index**: `18` or `25` - Use feature index from the displayed list
- **By Name**: `"草圖1"` or `"Pad1"` - Use exact feature name (case-sensitive)
- **For "end"**: Use empty string `""` to move to end

### Location Options

- **before**: Move rollback bar before the specified feature
- **after**: Move rollback bar after the specified feature
- **end**: Move rollback bar to the end (restore all features, activate full model)
- **previous**: Restore previous rollback position

### Return Codes

- **0**: Success
- **1**: Failed to move rollback bar (feature not found or invalid)
- **2**: Unable to attach to SolidWorks
- **3**: No active document

## Notes

- Feature names are case-sensitive
- Use "end" to restore all features (remove rollback)
- The rollback bar position is saved with the document
