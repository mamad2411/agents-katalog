---
name: notes-export
description: Export/back up EVERY macOS Notes note (all accounts, all folders) to local storage as markdown files plus a JSON manifest — the safety net to run BEFORE any reorganization, and the corpus the notes-audit skill analyzes. Read-only against Notes; writes only to ~/.local/share/notes-commander/export/. TRIGGERS - export my notes, back up notes, notes snapshot, dump notes to disk, notes backup before reorganizing.
allowed-tools: Bash, Read
---

# notes-export — full local snapshot of Apple Notes

> **Self-Evolving skill** — if export behavior drifts (AE size caps, chunk failures, encoding), fix this SKILL.md and `scripts/notes.ts` `OSA_EXPORT` (+ a test in `notes-core.test.ts` for any pure helper change); see the Post-Execution Reflection at the bottom.

One command captures everything Notes holds into a timestamped local snapshot:

```bash
NC="$HOME/.claude/plugins/marketplaces/cc-skills/plugins/notes-commander/scripts/notes.ts"
bun "$NC" export                     # → ~/.local/share/notes-commander/export/<stamp>/
bun "$NC" export --out /path/to/dir  # explicit destination
```

What a snapshot contains:

- **One markdown file per note**, under `<account>/<folder>/…` mirroring the Notes hierarchy. Each file has YAML frontmatter (`account`, `folder`, `id`, `modified`) and the note body as plain text (decoded via `textutil`, UTF-8-safe, CJK-safe).
- **`manifest.json`** — every folder (with counts) and every note (id, name, modified, relative file path, char count). This is the machine-readable index for audits and diffs.
- Filenames are sanitized (`safeFilename`) and suffixed with the note's core-data id (`.p1234.md`), so same-titled notes never collide.

## Rules

- **Run this before any `notes-organize` operation** — it is the undo story. Notes has no API-level undo; a snapshot does.
- The default root (`~/.local/share/notes-commander/export/`) is deliberately OUTSIDE any git repo so note content can never be accidentally committed. Don't redirect `--out` into a repo.
- Snapshots are full (not incremental); each run creates a new timestamped dir. Old snapshots are plain dirs — delete them manually when no longer wanted.
- `Recently Deleted` is deliberately skipped (restore a note in the Notes UI first if you want it captured).

## MemPalace bridge (if `mempalace` is on PATH)

After a successful export, re-mine the snapshot into the local MemPalace semantic index so the notes are searchable by meaning (multilingual — verified on 中文 content):

```bash
command -v mempalace >/dev/null && mempalace mine "<snapshot-dir>" --wing apple-notes --agent terry
```

Idempotent (unchanged notes are skipped). Recall then works via `mempalace search "<query>" --wing apple-notes`. Skip silently when mempalace isn't installed — the bridge is an enhancement, not a dependency.

- A large library takes a few minutes (verified live: 400 notes ≈ 2.5 min) — bodies are fetched in chunks of 20 because one giant Apple Event reply blows the AE size cap (`-1741`). A failed chunk degrades to per-note fetches; a still-failing note becomes a warning + exit code 3 (partial export is LOUD, never silent). Transient `-600`/`-1712` launch races retry automatically.

## Post-Execution Reflection

After an export, check: (1) exit code 0 and note count ≈ live inventory total? Exit 3 means some notes were skipped — read the `⚠` lines and investigate before trusting the snapshot as a backup. (2) Spot-check one CJK/emoji-titled file — mojibake means the `<meta charset="utf-8">` textutil prefix or `safeFilename` drifted. (3) New `-1741`s despite chunking → shrink the chunk size in `OSA_EXPORT`. Update this SKILL.md only for real, reproducible drift.
