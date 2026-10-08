---
name: amber-notes
description: Use the person's Amber Notes (ambernotes.app) through the amber-notes MCP server. Use when they mention their notes, Amber Notes, a checklist, a work log, a standup, a timesheet or tracker, or ask to save, look up or update something "in my notes".
---

# Amber Notes

Amber Notes is the person's own notes app on Mac and iPhone. The `amber-notes` MCP server reads and edits the same notes they see in the app. Every change you make shows up there with Undo, and the previous version stays in the note's history.

## If the tools are missing

The server needs a one-time sign-in. If no `amber-notes` tools are available, or a call says to sign in, tell the person to run `/mcp`, pick `amber-notes`, and choose Authenticate. A browser opens at ambernotes.app/connect: they open Amber Notes or sign in there, then choose Read and Edit, or Read Only. They need the free app (ambernotes.app/download) and an account.

A read-only connection only has the reading tools. If a change is refused for that reason, say so; don't look for a way around it.

## How to work with the notes

- Find before you write: `get_overview` for folders, pinned and recent notes; `search_notes` for anything specific. Read a note with `read_note` before editing it.
- Notes are markdown. The first line is the title. Checklists are `- [ ] item` lines; tables are markdown tables.
- Make the smallest change that does the job: `edit_note` (exact find and replace, copied from `read_note`) or `append_to_note` (end of a note, or under a heading). Use `replace_note_body` only when the person asks for a full rewrite.
- Tick items with `set_checklist_item`. For tables and trackers, call `read_table` first, then `log_table_row`, so the column names and values are right.
- Deleting is recoverable: `delete_note` moves a note to Recently Deleted for 30 days, and `restore_note` brings it back. `note_history` and `restore_revision` undo an edit.
- A note with `locked: true` is encrypted on the person's devices. Only its title is visible; don't try to read or change it.
- When you're done, name the note you changed and what you changed, in one line.

## Good uses from a coding session

- Write today's standup into a note, from the commits since yesterday.
- Append a decision to the project's note, under a "Decisions" heading.
- Keep a dated work log: `append_to_note` under today's date.
- Read a checklist note (a release checklist, say) and go through it, ticking items as they're done.
