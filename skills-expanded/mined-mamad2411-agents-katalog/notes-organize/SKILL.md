---
name: notes-organize
description: Reorganize macOS Notes deliberately - create folders (incl. nested subfolders), move notes between folders, rename folders, and merge/empty a folder into another. Every destructive-ish verb supports --dry-run, and the workflow REQUIRES a notes-export snapshot first. Use when folderizing sporadic notes, splitting an oversized folder, consolidating near-empty folders, or executing a notes-audit proposal. TRIGGERS - organize my notes, move this note, create notes folder, folderize, merge folders, clean up notes folders, rename notes folder.
allowed-tools: Bash, Read
---

# notes-organize — the reorganization primitives

> **Self-Evolving skill** — if a verb misbehaves (path resolution, ambiguity handling, `move` semantics), fix this SKILL.md and the AppleScript payloads in `scripts/notes.ts`; see the Post-Execution Reflection at the bottom.

The folderization verbs, built on the shared hardened engine (path-based folder resolution,
transient-error retry). Folder **paths** use `/` between segments (`To-Do / Done`) because
names are not unique across the tree.

```bash
NC="$HOME/.claude/plugins/marketplaces/cc-skills/plugins/notes-commander/scripts/notes.ts"

bun "$NC" mkdir "Projects"                                   # top-level folder (iCloud default)
bun "$NC" mkdir "Archive" --parent "Projects"                # nested subfolder
bun "$NC" move-note "Meeting notes" --from "Notes" --to "Projects" --dry-run   # preview
bun "$NC" move-note "Meeting notes" --from "Notes" --to "Projects"             # execute
bun "$NC" rename-folder "NAD+ Biz" --to "NAD+ Business"
bun "$NC" merge-folder "Test Folder" --into "Archive" --dry-run                # preview count
bun "$NC" merge-folder "Test Folder" --into "Archive"        # moves ALL notes out of source
bun "$NC" doctor                                             # end-to-end health round-trip
```

All verbs accept `--account A` (default `iCloud`; your Google/Exchange accounts by name).

## The safety protocol (ALWAYS follow, in order)

1. **Snapshot first** — run the `notes-export` skill. No snapshot → no reorganization.
2. **Dry-run** any `move-note`/`merge-folder` and show the operator what will happen.
3. **Execute**, then re-run `inventory` to confirm the resulting counts.
4. Ambiguous titles: `move-note` refuses when several notes share the title and prints their ids — re-run with `--id x-coredata://…`.

## Deliberate limitations (guard rails, not gaps)

- **No delete verb.** Notes are only ever MOVED; folders are never deleted by this tool. `merge-folder` empties the source but leaves the (now-empty) folder for the operator to delete in the Notes UI after visual confirmation. This keeps the worst possible outcome "a note is in the wrong folder", never "a note is gone".
- Tags (`#tag`) have **no AppleScript API** — organizing is folder-based. If tag hygiene matters, note it in the audit output for manual action.
- Moves between DIFFERENT accounts are not supported by Notes' AppleScript `move` (same-account only). Cross-account moves are a manual drag in the UI.

## Evolution log

- **2026-07-19 — first real reorganization (260 moves, 399-note library), three verified lessons.** (1) `merge-folder` originally indexed `item 1 of (notes of src)` live and failed with **-1728** once membership changed mid-loop; fixed by iterating a pre-captured `every note of src` reference list (refs are by id, stay valid across moves) — 17 merges/129 notes then ran clean. (2) **Notes silently culls EMPTY (0-char) notes on move** — one empty "New Note" went to Recently Deleted instead of its destination; expect a ±1 count on folders receiving empty notes (recoverable, not a loss). (3) Post-move count verification needs care: osascript `name of every note` output is comma-separated and breaks on titles containing commas — verify with `count notes of folder …`, never by splitting names. Also: moving by manifest **id** (`--id`) proved immune to duplicate titles ("New Note" ×2, two "Done" folders) — prefer it for scripted batches.

## Post-Execution Reflection

After any reorganization, check: (1) did post-move `inventory` counts match the dry-run prediction? A mismatch means `resolveFolder` or `move` semantics drifted — fix the payloads in `scripts/notes.ts` and document here. (2) Did an ambiguous-title refusal print usable ids? (3) Did anything require bypassing the snapshot-first protocol? If so, that's a process failure to write down, not a tooling gap. Update only for real, reproducible drift.
