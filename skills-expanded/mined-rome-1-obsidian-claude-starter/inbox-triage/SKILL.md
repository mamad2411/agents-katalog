---
name: inbox-triage
description: Processes everything in the vault's Inbox/ folder, one item at a time, filing each into the right place (an existing project or person note, a new research note, a task checkbox) or archiving it, and leaves the inbox empty. Use when the user says "triage my inbox", "process the inbox", "clear my captures", "file these notes", runs /inbox-triage, or when the session-start summary shows inbox items waiting and the user asks what to do with them. Not for email inboxes.
---

# Inbox triage

`Inbox/` holds raw captures. The job is to give each one a home, keeping the user's words, and leave `Inbox/` holding nothing but its `README.md`.

## 1. List

List files in `Inbox/` except `README.md`, oldest first.
If there are more than about 15, say how many and propose doing the oldest batch first.

## 2. Decide, item by item

For each item, read it, then pick one destination:

| The item is... | Do this |
|---|---|
| About an existing project | Append to that project's note (`## Log` or `## Next actions`), or to `Current-State.md` for a folder project |
| About a person | Add a dated line under `## Interactions` or `## Things to remember` in their note; update `last_contact` / `next_action` if it changes them |
| Something to do | A `- [ ]` checkbox in the relevant project note (or a bead, if `.beads/` exists) |
| Something learned, or a link worth keeping | A note in `Knowledge/` from `System/Templates/Research-Note.md`, or a line in an existing one. For anything substantial, follow the `research-capture` skill |
| A new project idea | A new project note with `status: idea` |
| Meeting notes | Follow the `meeting-notes` skill |
| No longer relevant | Move to `Archive/` |

Search for existing notes before creating new ones (Grep the name or topic across `Projects/`, `People/`, `Knowledge/`).

Ask before acting when the destination is unclear, or when an item would create a new folder or a new note type.
Batch the questions: show a short table of item → proposed destination, and let the user correct it in one reply.

## 3. File

- Keep the user's original wording; add a link back to context if useful.
- Set `updated:` on every note you change.
- Remove the inbox file only after its content is in the new place.
  A file that is a pure link or a single line can be deleted once filed; anything longer, move into `Archive/` if the user prefers to keep originals.

## 4. Check and report

- Run `python3 scripts/check_vault.py`.
- Report: how many items, where each went (one line each, with links), and anything left in `Inbox/` and why.
- Commit with `vault: triage inbox - N items` if the user has agreed to agent commits.
