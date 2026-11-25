---
name: swpilotcli-ActionGroup-replace-notes
description: "[ActionGroup] Batch replace text inside Note annotations across all SolidWorks drawings (.slddrw) in a specified folder (root only)." For each drawing, opens it silently, finds all Notes containing the search text, replaces every occurrence, saves a copy with a custom suffix to a specified output folder, then closes the original without saving. Reports which files were changed and how many notes were replaced per file. Use when you need to find-and-replace note text across multiple drawings in one shot.
---

# swpilotcli-ActionGroup-replace-notes

## Prerequisites

- SolidWorks is running
- Target folder exists and contains .slddrw files

## What this Skill does

1. Scans the source folder for all `.slddrw` files (root only, no subdirectories)
2. For each drawing:
   - Opens it silently
   - Iterates all sheets → views → Note annotations
   - Replaces every occurrence of `<find>` with `<replace>`
   - If any notes were changed: saves a copy to the output folder with a filename suffix
   - Closes the drawing without saving (original is untouched)
3. Reports a summary of all modified files

## When to use

Use when the user wants to batch-update note text across many drawings in one operation.
For single-file note replacement, use `swpilotcli-replace-note-text` instead.

## Quick start

```bash
dotnet run --project ./sup_tools/swpilotcli-ActionGroup-replace-notes/scripts/ReplaceNotes/ReplaceNotes.csproj -- "<sourceFolder>" "<outputFolder>" "<find>" "<replace>" "<suffix>"
```

## Examples

```bash
# Replace 頂峰 with 廠商, save copies to a subfolder with _廠商 suffix
dotnet run --project ... -- "H:\drawings" "H:\drawings\output" "頂峰" "廠商" "_廠商"
```

## Arguments

| # | Name | Description |
|---|------|-------------|
| 1 | sourceFolder | Folder containing source .slddrw files |
| 2 | outputFolder | Folder where modified copies are saved (created if not exists) |
| 3 | find | Text to search for (case-sensitive) |
| 4 | replace | Replacement text |
| 5 | suffix | Filename suffix added before .slddrw extension |

## Notes

- Original files are never modified.
- Output folder is created automatically if it does not exist.
- Only root-level .slddrw files are processed (no subdirectory recursion).
- Drawings with no matching notes are skipped (no copy saved).
