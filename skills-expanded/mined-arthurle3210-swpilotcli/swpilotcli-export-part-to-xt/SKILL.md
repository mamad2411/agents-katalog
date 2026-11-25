---
name: swpilotcli-export-part-to-xt
description: Export a single SolidWorks part (.sldprt) to Parasolid (.x_t) format. Uses the active document if no path is given. Accepts optional part path and output directory arguments. Use for single-part export or as the per-item step in LLM-orchestrated batch workflows.
---

# SolidWorks Export Part to XT

Export a single SolidWorks part to Parasolid `.x_t` format.

## Prerequisites

- **SolidWorks 2024+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime** on the system
- A `.sldprt` file — either open as active document, or specified by path

## What this Skill does

1. Resolves the target part (active doc or argument path)
2. Opens the part silently if not already open
3. Exports to `.x_t` using `SaveAs3`
4. Closes the part if it was not already open

## When to use

- **Single-part export**: convert the currently open part
- **LLM batch workflow**: called once per part after ListAssemblyParts
- For full assembly batch in one shot, use `swpilotcli-export-assembly-parts-to-xt`

## Quick start

```bash
# Export active part (to same directory)
dotnet run --project ./sup_tools/swpilotcli-export-part-to-xt/scripts/ExportPartToXt/ExportPartToXt.csproj

# Export specified part
dotnet run --project ./sup_tools/swpilotcli-export-part-to-xt/scripts/ExportPartToXt/ExportPartToXt.csproj -- "C:\path\to\part.sldprt"

# Export to specified output directory
dotnet run --project ./sup_tools/swpilotcli-export-part-to-xt/scripts/ExportPartToXt/ExportPartToXt.csproj -- "C:\path\to\part.sldprt" "C:\output\dir"
```

Expected output:

```
Part:   C:\Projects\Part001.sldprt
Output: C:\Projects\Part001.x_t
OK -> C:\Projects\Part001.x_t
```

## Examples

### Export current part
```
User: 把這個零件轉成 XT
Claude: I'll export the active part using this tool.
```

### Per-item step in batch workflow
```
# After ListAssemblyParts returns a JSON array:
dotnet run ... -- "C:\Parts\PartA.sldprt"
dotnet run ... -- "C:\Parts\PartB.sldprt"
```

## Reference

See [API_REFERENCE.md](API_REFERENCE.md) for arguments, output, and return codes.

## Notes

- Output filename matches the source filename (`.sldprt` → `.x_t`)
- Parts already open in SolidWorks are not closed after export
- Output directory is created automatically if it does not exist
