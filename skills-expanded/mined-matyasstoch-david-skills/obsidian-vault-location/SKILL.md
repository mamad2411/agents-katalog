---
name: obsidian-vault-location
description: Use when David asks where Obsidian is installed, where his notes/vault/journal/writing live, or wants to read/find/edit a note from his Obsidian vault. Triggers on "Obsidian", "my notes", "my vault", "my journal", "private writing", "where do I write".
---

# Obsidian Vault Location

## Install
- App: `/Applications/Obsidian.app`
- Config: `~/Library/Application Support/obsidian/obsidian.json` (lists active vault paths)

## Main vault (where the notes live)
`~/Documents/notes/private_writing`

Personal journal + writing. `.md` files only (ignore `.obsidian/` config dir).

## Structure
- Monthly folders: `01-2026/`, `02-2026/`, `03-2026/`, `04-2026/`, `05-2026/` — dated journal entries / reflections.
- `timeless/` — permanent notes not tied to a date:
  - `original thoughts.md`
  - `Grand Things I Could Do.md`
  - `PLANE TOPICS.md`
  - `reasons for God's existence.md`
- `private/` — sensitive/business notes.
- `prompts/` — e.g. `Writing Analysis Framework.md`.
- `keyboard_shortcuts/` — Obsidian shortcut notes.

## Usage
- To find a note: `find "$HOME/Documents/notes/private_writing" -iname "*<keyword>*" -not -path "*/.obsidian/*"`
- Note titles contain spaces — quote paths.
