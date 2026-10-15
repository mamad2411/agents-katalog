---
name: task-notes
description: Create and update Joplin task notes — the durable record of one task (description, working directory, checklist, log, links). Use when the user wants a Joplin note tracking a task, or when another skill needs the task-note format or update conventions.
allowed-tools: mcp__joplin__semantic_search_notes mcp__joplin__search_notes mcp__joplin__list_notebooks mcp__joplin__create_notebook mcp__joplin__create_note mcp__joplin__update_note
---

A task note is a Joplin to-do holding the true state of one task.
Anyone — or any fresh agent — reading only the note must be able to resume the work.
The title, body structure, and entry formats are defined in [TASK-FORMAT.md](./TASK-FORMAT.md).

## Creating a task note

1. Get the `Agents` notebook id from `list_notebooks`; create it with `create_notebook` if missing.
2. Search for an existing open note for the same work: `semantic_search_notes` scoped to the `Agents` `notebook_id` with a query describing the task, then confirm any promising match is still open with `read_note` or `search_notes` (`notebook:Agents type:todo iscompleted:0 <keywords>`).
   If semantic search errors (embeddings not enabled in Joplin's AI settings) or turns up nothing relevant, fall back to plain `search_notes` with `notebook:Agents type:todo iscompleted:0 <keywords>`.
   If one exists, update it per the conventions below instead of creating a duplicate.
3. Allocate the task number.
   Search `notebook:Agents` with **no** `iscompleted` filter (completed tasks keep their numbers so none is ever reused), read every title's leading `[NNNN]`, take the highest, and add one.
   Start at `[0001]` when the notebook has no numbered notes yet.
4. Create the note with `create_note`: `is_todo: true`, title and body per [TASK-FORMAT.md](./TASK-FORMAT.md).

Done when the note exists in `Agents` **as a to-do** (it appears under `type:todo` in `search_notes` — if not, the `is_todo` flag was dropped; fix it before proceeding) and you have reported its number, id, and title back to the caller.

## Update conventions

All updates go through `update_note` partial ops; never rewrite the full body.

- **Log an event:** `append` one entry in the log-entry format, ending with a real trailing newline — an actual line break, never the literal characters backslash-`n`, which run the entries together (see [TASK-FORMAT.md](./TASK-FORMAT.md)).
- **Record durable knowledge:** `append` a log entry tagged `Decision:`, `Finding:`, or `Dead end:` per [TASK-FORMAT.md](./TASK-FORMAT.md).
  If a finding changes the shape of the work, also add a checklist item or amend `## Task` — the note's current truth lives there, not in the log.
- **Update status:** `replace_text` with `status: <current>` → `status: <new>` (in the frontmatter block), using the valid status values.
- **Check off an item:** `replace_text` with find `- [ ] <exact item>`, replace `- [x] <exact item>`.
  If the item has sub-items, check each sub-item off first; only check the parent after all its sub-items are checked.
- **Add a line to a section:** `replace_text` on the *next* section's heading, replacing it with the new line, a blank line, then the heading — headings are the only guaranteed-unique anchors.
- **Maintain the Notes section:** when current-state knowledge outgrows the log, create the optional `## Notes` section per [TASK-FORMAT.md](./TASK-FORMAT.md) with `replace_text` on the `## Links` heading (new section, a blank line, then the heading).
  Revise or delete its entries with `replace_text` when they stop being true; never leave stale notes standing.
- **Block the task:** mark the title with `🛑` and insert a blocked section, both per [TASK-FORMAT.md](./TASK-FORMAT.md).
  Insert it with `replace_text` on the `## Task` heading, replacing it with the blocked section, a blank line, then the heading — a plain `prepend` would land above the frontmatter and break it.
- **Unblock the task:** restore the title, log the user's response or the resolution, and remove the whole blocked section with `replace_text` (replace with nothing).
- **Close the task:** when every checklist item is checked, set `todo_completed: true` **first** — that single op drops the note out of `iscompleted:0` searches, so do it before any other close bookkeeping — then append a final log entry with the outcome.
  Never route a finished task through `status: available`: it reopens the note to other workers in the gap before it closes.
