---
name: mnemon-system
description: >-
  The Mnemon memory system as a whole: status, memory spaces, project documents, turn receipts, strategies,
  budgets, backup, export and import. Use when the user asks how memory is configured or stored, wants to see
  everything that is remembered, wants to change the memory strategy, or wants to move memory to another machine.
---

# The memory system

## Status first

`memory_admin` (`action: "status"`) reports the data directory, the active strategy and enhancements, budgets, and counts of memories, spaces, documents and pending candidates. Report the data directory whenever the user asks where memory lives — every file is plain text under it.

## The four stores

| Store | File | Purpose |
| --- | --- | --- |
| Persona | `runtime/PERSONA.md` | Permanent AI persona: injected at SessionStart, never truncated |
| Runtime memory | `runtime/USER.md`, `runtime/MEMORY.md` | Injected at SessionStart; keep it small and current |
| Project documents | `documents/<id>.md` | Searched, then read on demand; every write keeps a revision |
| Memory spaces | `spaces/<space>/memories.jsonl` | Durable facts, one JSON object per line; `pinned: true` = permanent |

Also on disk: `candidates/pending.jsonl` (facts awaiting review), `receipts/<date>.jsonl` (what each turn read and wrote), `receipts/heal-*.json` (recovery receipts), `revisions/` and `documents/.revisions/` (history), `snapshots/` (local daily gzip copy), `backups/`. With `--mirror-dir`, runtime volumes, space files and documents are mirrored to `<mirror>/latest/` and daily snapshots live in `<mirror>/snapshots/`.

## Durability

- Every write is atomic (temp file + fsync + rename) and mirrored immediately.
- `memory_admin` (`action: "mirror_sync"`) forces a mirror pass and writes today's snapshot if missing.
- `memory_admin` (`action: "verify_heal"`) checks every primary file and restores missing/zero-byte/corrupt ones from the mirror or newest snapshot; it also runs at startup.
- `memory_admin` (`action: "backup_verify"`) decodes a `.json.gz` backup with a real gzip decoder and returns its SHA-256.

## Inspecting

- `memory_manage` (`action: "space_list"`) — spaces with counts and last update.
- `memory_recall` (`action: "list"`) — memories, newest first; filter by `space` or `tag`.
- `memory_doc` (`action: "list"` / `"read"`) — project documents.
- `memory_recall` (`action: "entities"` / `"receipts"`) — entity links and recent turn receipts.
- `node scripts/mnemon.mjs status` — the same view from a terminal.

## Strategies and budgets

One main strategy runs at a time; see `references/strategies.md` for the table. Change it with `memory_admin` (`action: "config"`, e.g., `{"strategy": "light-context"}` or `{"enhancements": {"autoCapture": true}}`). Switching strategy never moves data.

## Resident memory

`memory_profile` (`action: "get"`) reads `PERSONA.md`, `USER.md` and `MEMORY.md`; `set_persona`, `set_user`, and `set_memory` edit them (`mode: "replace"` or `"append"`). Keep `PERSONA.md` to identity, voice and taste; `USER.md` to stable facts about the user; `MEMORY.md` to what future turns need — anything longer belongs in a document.

## Moving memory

- `memory_admin` (`action: "backup"`, `mode: "bundle"`) — one compressed pack, good for copying between machines.
- `memory_admin` (`action: "backup"`, `mode: "dir"`) — readable files preserving document frontmatter, good for a private git repository.
- `memory_admin` (`action: "restore"`, `file: ...`, `mode: "merge"|"replace"`) — merge deduplicates; replace overwrites runtime memory and spaces.

Backups contain private memory: treat them as secrets.

## Trust

Memory files are plain text you can read, edit and version. Remembered history never outranks current instructions; credentials are never stored in memory; deleting a memory is a soft delete unless `hard: true` is passed.
