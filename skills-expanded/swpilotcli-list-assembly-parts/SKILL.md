---
name: swpilotcli-list-assembly-parts
description: List all unique part files (.sldprt) referenced by the active SolidWorks assembly. Outputs a JSON array of full file paths. Use this to preview parts before batch processing, or to get part paths for further automation.
---

# SolidWorks List Assembly Parts

List all unique parts in the active assembly. Pure read-only — does not modify any document.

## Prerequisites

- **SolidWorks 2024+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime** on the system
- **Active SolidWorks assembly** (.sldasm) must be open

## What this Skill does

1. Reads all top-level components from the active assembly
2. Filters unique `.sldprt` files (de-duplicated, case-insensitive)
3. Outputs a JSON array of full file paths sorted alphabetically

## When to use

- **Preview** which parts are in an assembly before exporting
- **Get part paths** to feed into ExportPartToXt for LLM-orchestrated batch export
- **Audit** assembly structure without modifying anything

## Quick start

```bash
dotnet run --project ./sup_tools/swpilotcli-list-assembly-parts/scripts/ListAssemblyParts/ListAssemblyParts.csproj
```

Expected output:

```
Assembly: C:\Projects\MyAssembly.sldasm
Unique parts: 3

[
  "C:\\Projects\\PartA.sldprt",
  "C:\\Projects\\PartB.sldprt",
  "C:\\Projects\\PartC.sldprt"
]
```

## Examples

### Preview before batch export
```
User: 這個組合件有哪些零件？
Claude: I'll list all parts using this tool.
```

### LLM-orchestrated batch XT export
```
User: 把組合件所有零件轉成 XT
Claude: First list parts with ListAssemblyParts, then call ExportPartToXt for each.
```

## Reference

See [API_REFERENCE.md](API_REFERENCE.md) for output schema and return codes.

## Notes

- Read-only — safe to run at any time
- Top-level components only (`GetComponents(false)`)
- Sub-assemblies (.sldasm) are excluded from output
