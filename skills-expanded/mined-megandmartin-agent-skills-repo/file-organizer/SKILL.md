---
name: file-organizer
description: Organizes a messy folder — proposes a naming convention and folder taxonomy, shows the complete move plan as a dry-run table, executes only after explicit confirmation, and writes an undo.sh before touching anything. Use when the user says "organize this folder", "clean up my Downloads", "sort these files", or "my desktop is a mess". Don't use for deleting or deduplicating files (this skill never deletes) or summarizing file contents (use meeting-notes-actions for notes files).
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Productivity, Files, Organization]
    related_skills: [weekly-review, meeting-notes-actions]
---

# File Organizer

Turns a chaotic folder into a clean, documented structure — with a full dry-run plan, an explicit go/no-go, and a working `undo.sh` written *before* the first move. The standard: the user sees every single move before it happens, nothing is ever deleted or overwritten, and one command reverses everything.

## When to Use

- "Organize my Downloads", "sort this project folder", "impose some order here".
- Before archiving a finished project or handing a folder to someone else.
- **Not for:** deleting or deduplicating files (this skill never deletes) or summarizing file *contents* (use `meeting-notes-actions` for notes files).

## Quick Reference

| Action | Command / Call |
|---|---|
| Inventory | `find "$DIR" -maxdepth 2 -type f \| head -200` and `ls -la "$DIR"` |
| Profile types | `find "$DIR" -maxdepth 2 -type f \| sed 's/.*\.//' \| sort \| uniq -c \| sort -rn` |
| Collision check | `[ -e "$dest" ] && echo "COLLISION: $dest"` for every planned destination |
| Create structure | `mkdir -p "$DIR/subfolder"` |
| Move (never overwrite) | `mv -n "src" "dest"` — `-n` is mandatory |
| Undo log | Write `undo.sh` with one reverse `mv -n` per move, before any move runs |

## Procedure

1. **Precheck** — confirm the target folder exists and count files (`find "$DIR" -maxdepth 2 -type f | wc -l`). Over ~300 files: propose organizing the newest or one file-type first. Never operate on `/`, `~` itself, or any system/app directory — named subfolders only.
2. **Inventory** — profile by extension, size, and modified date. Skim names for natural clusters (invoices, screenshots, drafts, exports). Read-only step: nothing is created or moved.
3. **Propose the scheme** — a taxonomy of 4–8 folders with one-line rules ("Invoices/ — PDFs with invoice/receipt in the name") and a naming convention such as `YYYY-MM-DD_project_description.ext` (renames are opt-in — default plan moves only). Get the user's reaction before building the plan.
4. **Build the dry-run table** — the FULL move plan, every file, in the template below. No "...and 47 more": every row shown. Check every destination for collisions; on collision, plan a suffixed name (`report_2.pdf`), never an overwrite.
5. **Write undo.sh** — before anything moves: `undo.sh` in the target folder, starting `#!/bin/sh` + a timestamp comment, then one `mv -n "dest" "src"` per planned move in reverse order. `chmod +x undo.sh`. This file exists before the first `mv` runs — non-negotiable.
6. **Confirm** — state: "{N} moves into {M} folders, 0 deletions, undo.sh ready at {path}. Type yes to execute." Execute only on an explicit yes. Anything else, stop and adjust.
7. **Execute** — `mkdir -p` the folders, then run each `mv -n`. If any `mv` fails or skips (destination existed), record it and continue; report skips at the end.
8. **Report** — moved/skipped counts, the new tree (`find "$DIR" -maxdepth 2 -type d`), and the undo instruction: `sh "$DIR/undo.sh"`.

## Output Template

```
# Move Plan — {folder} ({N} files) — DRY RUN, nothing moved yet

Proposed taxonomy: {Folder1}/ · {Folder2}/ · ...
Naming convention: {pattern or "keep original names"}

| # | Current name | → Destination | Rule applied |
|---|---|---|---|
| 1 | {file.ext} | {Subfolder}/{file.ext} | {rule} |
| ... every file, no truncation ... |

Collisions handled: {n} (suffixing, never overwriting)
Deletions: 0 (always)
Undo: undo.sh will be written to {folder} BEFORE any move.

Reply "yes" to execute, or tell me what to change.
```

## Pitfalls

- **`mv` without `-n` silently overwrites a same-named file** — that's data loss with no undo. Every move and every undo line uses `mv -n`; collisions are resolved by suffixing in the plan, never at execution time by chance.
- **undo.sh written after the moves (or never)** — a crash mid-run then leaves no recovery. Write and `chmod +x` undo.sh in step 5, verify it exists (`ls -l undo.sh`) before the first `mv`. If execution halts midway, undo.sh still reverses the completed portion (`mv -n` makes re-running it safe).
- **Plan truncated ("moving 200 files, here are the first 20")** — the user can't consent to moves they haven't seen. Show all rows; if the table is unwieldy, that's the signal to shrink scope (one file type or date range per pass), not to hide rows.
- **Overreaching scope** — hidden files, `.git/`, `node_modules/`, app bundles, or files outside the target folder get swept into the plan. Exclude dotfiles and known system/tooling directories by default; touch only what's directly in the agreed folder.
- **User says "looks good" to the taxonomy and the agent starts moving** — approving the *scheme* (step 3) is not approving the *plan* (step 6). Only an explicit yes after the full dry-run table authorizes execution.

## Verification

- [ ] Dry-run table listed every file (row count == inventory count) before any move
- [ ] undo.sh existed and was executable before the first mv ran
- [ ] All moves used `mv -n`; zero files deleted or overwritten
- [ ] Post-run: moved + skipped == planned; skips reported by name
- [ ] `sh undo.sh` would restore original paths (spot-check 2 lines against the plan)
- [ ] Nothing outside the target folder was touched
