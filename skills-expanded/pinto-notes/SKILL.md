---
name: pinto-notes
description: Use the person's notes in Pinto Notes (pintonotes.com) through the pinto-notes MCP server. Use when they mention their notes, Pinto Notes, Amber Notes, a checklist, a work log, a standup, a timesheet or tracker, or ask to save, look up or update something "in my notes".
---

# Pinto Notes

Pinto Notes is the person's own notes app on Mac and iPhone. The `pinto-notes` MCP server reads and edits the same notes they see in the app. Every change you make shows up there with Undo, and the previous version stays in the note's history. It was called Amber Notes until October 2026; it's the same app.

## If the tools are missing

The server needs a one-time sign-in. If no `pinto-notes` tools turn up, or a call says to sign in, tell the person to run `/mcps`, select `pinto-notes` and press `i` to authenticate. A browser opens at pintonotes.com/connect: they open Pinto Notes or sign in there, then choose Read and Edit, or Read Only. They need the free app (pintonotes.com/download) and an account.

A read-only connection only has the reading tools. If a change is refused for that reason, say so; don't look for a way around it.

## The tools

The server's tools work like a file system over the notes. In Grok Build they're named `pinto-notes__<tool>`; find them with `search_tool` and call them with `use_tool`.

- `list`: folders, a note's sub-notes and files, newest first. Start here.
- `search`: ranked full-text search, or a line-by-line pattern like grep.
- `fetch`: read a note or file, with line numbers.
- `edit`: an exact find and replace in one note.
- `write`: write a whole note or file.
- `create`: a new note or folder.
- `move`: move or rename a note, folder or file.
- `delete`: move a note or file to Recently Deleted for 30 days.
- `history` and `restore`: earlier versions, and bringing back a version or a deleted note.
- `pin`: pin a note to the top of the list, or unpin it.

## How to work with the notes

- The notes are files. Each note is a markdown file at a path like `Work/Acme.md`; its name is its title. A note's sub-notes and files sit in the folder with its name (`Work/Acme/Agenda.md`). Deleted notes are in `Recently Deleted/`.
- Find before you write: `list` for folders and recent notes, `search` for anything specific. Read a note with `fetch` before you change it; a change to a note you haven't read, or that changed since, is refused.
- Checklists are `- [ ] item` lines; tables are markdown tables. A tracker has a `<!-- pane-table: … -->` line above its table that gives each column's type. Keep values in range.
- Make the smallest change that does the job: `edit` is an exact find and replace (copy the text from `fetch`, without the line numbers). Tick an item by editing `- [ ]` to `- [x]`; add a row to a table the same way. Use `write` only when the person asks for a full rewrite.
- `edit` and `write` answer with checks, such as a tracker value out of range or a checklist line that no longer shows as one. Fix what they report.
- Deleting is recoverable: `delete` moves a note to Recently Deleted for 30 days, and `restore` brings it back. `history` and `restore` with a version undo an edit.
- A note with `locked: true` is encrypted on the person's devices. Only its title is visible; don't try to read or change it.
- When you're done, name the note you changed and what you changed, in one line.

## Good uses from a coding session

- Write today's standup into a note, from the commits since yesterday.
- Add a decision to the project's note, under a "Decisions" heading.
- Keep a dated work log: `edit` under today's date.
- Read a checklist note (a release checklist, say) and go through it, ticking items as they're done.
