---
name: swpilotcli-list-features
description: List features in the active SolidWorks document's Feature Tree, printing each feature's type and name. Walks from `FirstFeature()` via `GetNextFeature()`. Accepts an optional integer argument to limit output count (default: all features). Use to locate named reference planes, inspect feature order, or find features by name before operations like `move-rollback-bar`, `sketch-on-face`, or deletion.
---

# SolidWorks List Features

Print the active document's Feature Tree as `[TypeName] Name` lines.

## Prerequisites

- **SolidWorks 2024+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime**
- An active SolidWorks document

## What this Skill does

- Walks the feature tree starting from `swDoc.FirstFeature()`, advancing with `GetNextFeature()`
- Prints each feature as `[<TypeName>] <FeatureName>` where TypeName comes from `Feature.GetTypeName2()`
- Optionally stops after N features if an integer is passed as the first argument

## When to use

- Find the name of a reference plane before selecting it (e.g. `Front Plane`, `Right Plane`, or custom `Plane1`)
- Check whether a specific feature exists / verify order
- Inspect feature structure before `move-rollback-bar`, deletion, or debugging

## Quick start

```bash
# List all features
dotnet run --project ./sup_tools/swpilotcli-list-features/scripts/ListFeatures/ListFeatures.csproj

# List only the first 20 features
dotnet run --project ./sup_tools/swpilotcli-list-features/scripts/ListFeatures/ListFeatures.csproj -- 20
```

## Return codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Cannot connect to SolidWorks |
| 3 | No active document |
