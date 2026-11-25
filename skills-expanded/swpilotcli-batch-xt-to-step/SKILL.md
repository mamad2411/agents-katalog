---
name: swpilotcli-batch-xt-to-step
description: Batch convert Parasolid `.x_t` and `.xt` files in a specified folder to STEP `.step` files in the same folder. Scans the folder root only, creates same-name `.step` outputs, suppresses template-selection prompts by forcing default part templates, and closes each temporary import document after export. Use when you need one-shot XT to STEP conversion for a local folder.
---

# SolidWorks Batch XT to STEP

Batch convert Parasolid `.x_t` and `.xt` files in a specified folder to STEP `.step` files in the same folder.

## Prerequisites

- **SolidWorks 2025+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime** on the system
- A target folder containing `.x_t` or `.xt` files
- A usable SolidWorks part template, or permission for the tool to set one automatically

## What this Skill does

1. Validates the target folder path
2. Scans the folder root for `.x_t` and `.xt` files only
3. Forces SolidWorks to use default templates and disables import diagnostics prompts
4. Creates a temporary part document from the default part template
5. Imports each XT file using `InsertImportedFeature`
6. Exports each imported model to same-name `.step`
7. Closes the temporary import document after each file
8. Prints per-file status and a final summary

## When to use

- **One-shot folder conversion**: convert a batch of XT files in a local folder
- **Neutral-format handoff**: prepare STEP deliverables from Parasolid source files
- For a single currently open SolidWorks part to XT, use `swpilotcli-export-part-to-xt`

## Quick start

```bash
dotnet run --project ./sup_tools/swpilotcli-batch-xt-to-step/scripts/BatchXtToStep/BatchXtToStep.csproj -- "C:\path\to\folder"
```

Expected output:

```text
Default part template: C:\Templates\Part.prtdot
Folder: C:\Parts\xt
Found: 3 file(s)

Input:  C:\Parts\xt\PartA.x_t
Output: C:\Parts\xt\PartA.step
Status: OK

Summary: success=3, failed=0, total=3
```

## Examples

### Convert one folder in place

```text
User: 幫我把這個資料夾裡的 xt 都轉成 step
Claude: I'll run the batch XT-to-STEP tool on that folder and write the STEP files next to the XT files.
```

## Reference

See [API_REFERENCE.md](API_REFERENCE.md) for arguments, output, and return codes.

## Notes

- Scans the specified folder only; does not recurse into subfolders
- Output filename matches source filename with `.step` extension
- Existing `.step` files at the same path are overwritten by export
- The tool closes its temporary import document after each file
