---
name: swpilotcli-replace-note-text
description: Find and replace text inside all Note annotations in the active SolidWorks drawing. Requires two arguments: the text to find and the replacement text. Scans every sheet and view, replaces all matching notes, and reports how many were changed. Use as an atomic building block in LLM-orchestrated batch workflows (e.g. open-doc → replace-note-text → save-drawing-as-copy → close-doc). Does NOT save the file — caller is responsible for saving or discarding.
---

# swpilotcli-replace-note-text

## Prerequisites

- SolidWorks is running
- A drawing (.slddrw) is the active document

## What this Skill does

Iterates over all sheets → views → annotations in the active drawing.
For every Note whose text contains `<find>`, replaces all occurrences with `<replace>`.
Prints each substitution and a final count summary.

## When to use

Use as a single-purpose step in LLM-orchestrated batch workflows:

```
swpilotcli-open-doc <file>
swpilotcli-replace-note-text "<find>" "<replace>"
swpilotcli-save-drawing-as-copy <src> <dst>   ← only if replacements > 0
swpilotcli-close-doc nosave
```

Do NOT use when you need to modify dimensions, BOM tables, or other annotation types — this tool only touches Notes.

## Quick start

```bash
dotnet run --project ./sup_tools/swpilotcli-replace-note-text/scripts/ReplaceNoteText/ReplaceNoteText.csproj -- "頂峰" "廠商"
```

## Examples

```bash
# Replace vendor name in notes
dotnet run --project ... -- "頂峰" "廠商"

# Replace revision marker
dotnet run --project ... -- "REV-A" "REV-B"
```

## Reference

- INote::GetText — reads note text
- INote::SetText — writes note text
- IAnnotation::GetType / swAnnotationType_e.swNote — filters note annotations
- DrawingDoc::GetViews — enumerates all sheets and views

## Notes

- The document is left in a modified (dirty) state after replacement.
- Caller must explicitly save or discard changes.
- Matching is case-sensitive.
- If no notes contain the find text, exits with code 0 and reports 0 replacements.
