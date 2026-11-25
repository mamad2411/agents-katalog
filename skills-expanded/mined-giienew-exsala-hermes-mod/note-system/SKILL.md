---
name: note-system
description: Use when managing notes vault via note.sh.
---

# Personal notes vault

User keeps durable cross-session notes at `~/app/` managed by CLI `~/.hermes/scripts/note.sh`. Use it to record permanent facts and task state instead of leaving them only in chat. Terse Indonesian replies stay the norm — this skill is about the files, not the phrasing.

## Layout
- `notes/core/` — permanent preferences and stack facts. Root `INDEX.md` lists entries.
- `notes/tasks/` — open task list. Root `INBOX.md`. State values: 🔴 urgent, 🟡 active, 🟢 done, 🟣 backlog, 🔵 todo. Marked items are removed, not kept.
- `notes/projects/` — per-project notes; root `INDEX.md` tracks status and links. Follow the cleanup rule (see memory): finished/cancelled projects update INDEX first, then remove failed experiments, keep proven-working ones.

Every bucket keeps a root INDEX.md/INBOX.md that must stay in sync.

## Commands
`~/.hermes/scripts/note.sh` (subcommands: add | list | walk | done | rm)
- `add <bucket> <title> [belongs_to]` — body from stdin; writes `notes/<bucket>/<id>.md` with front-matter `created`/`belongs_to`/`status: active`; prints created path.
- `list` — all notes files.
- `walk <title>` — find note with exact heading `# <title>`.
- `done <title>` — flip `status: active` → `status: done`.
- `rm <title>` — delete note file.

## Pitfalls
- `walk` greps exact `# <title>` so titles must be globally unique; re-using a title returns the first match. Pick distinct titles.
- `note add` writes the file but NEVER updates the bucket INDEX/INBOX — you must do that by hand. The index is the only thing that shows up in `list`-based workflows.
- Subcommand set is minimal; before promising a capability check the usage string. Missing capability (e.g. `rm`) is a ~6-line patch to the case block, not a rewrite.
- Notes are cheap to create, so index drift is the real cost. Every `add` should be followed by an index edit in the same turn.

## Support files
- templates/INDEX.md — skeleton for a bucket's index file
