---
name: swpilotcli-export-assembly-parts-to-xt
description: Batch export all unique parts (.sldprt) in the active SolidWorks assembly to Parasolid (.x_t) format. Outputs all files to an "xt/" subfolder next to the assembly. Use when you need to convert an entire assembly's parts to XT in one operation.
---

# SolidWorks Export Assembly Parts to XT

Batch export all unique parts in the active assembly to Parasolid `.x_t` format.

## Prerequisites

- **SolidWorks 2024+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime** on the system
- **Active SolidWorks assembly** (.sldasm) must be open

## What this Skill does

1. Reads all top-level components from the active assembly
2. Filters unique `.sldprt` files (de-duplicated)
3. Opens each part silently, exports to `.x_t`, then closes it
4. Outputs all `.x_t` files to an `xt/` subfolder next to the assembly file
5. Restores the original assembly as the active document when done

## When to use

- **Batch export** all parts in an assembly to XT format
- **Preparing files** for downstream CAD/CAM systems that require Parasolid
- For single-part export, use `ExportPartToXt` instead

## Quick start

```bash
dotnet run --project ./sup_tools/swpilotcli-export-assembly-parts-to-xt/scripts/ExportAssemblyPartsToXt/ExportAssemblyPartsToXt.csproj
```

Expected output:

```
Active document: MyAssembly.sldasm
Output folder: C:\Projects\MyAssembly\xt
Found unique part files: 5
OK  PartA.sldprt -> PartA.x_t
OK  PartB.sldprt -> PartB.x_t
...
Summary: exported=5, skipped=0, failed=0
```

## Examples

### Export all parts in active assembly
```
User: 把這個組合件的所有零件轉成 XT
Claude: I'll batch export all parts using this tool.
```

### Check parts first, then export
```
User: 先查有哪些零件，再批次轉 XT
Claude: I'll use ListAssemblyParts first, then ExportPartToXt for each.
```

## Reference

See [API_REFERENCE.md](API_REFERENCE.md) for output schema and return codes.

## Notes

- Output directory: `<assembly_dir>/xt/` (auto-created)
- Duplicate filenames get a `_2`, `_3` suffix automatically
- Parts already open in SolidWorks are not closed after export
- Execution time scales with number of parts
