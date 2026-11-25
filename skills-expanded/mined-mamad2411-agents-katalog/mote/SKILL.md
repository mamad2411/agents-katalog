---
name: mote
version: 1.0.0
description: Read, write, and manage Mote notes. Use when the user mentions "mote" — e.g. "add to mote", "write to mote", "put this in mote", "save to mote", "mote note", "read my mote", "create a mote note".
---

# Mote Integration

Mote is a floating markdown editor for macOS. Notes are plain markdown files on disk. You interact with them using your standard Read, Write, and Edit tools.

## File Locations

- **Notes directory:** `~/.mote/notes/`
- **State file:** `~/.mote/state.json`
- **Metadata:** `~/.mote/metadata.json` (DO NOT modify — Mote manages this)

## Finding the Active Note

Read `~/.mote/state.json` to get `activeNotePath`. If it exists, Mote will live-reload when you write. If it doesn't, just write directly to `~/.mote/notes/` — the note will be there when Mote opens.

## Operations

### Read the active note
Read the file at `activeNotePath` from state.json.

### Write to the active note
Read state.json, then Write or Edit the file at `activeNotePath`. Mote live-reloads automatically.

### Append to the active note
Read the note, append your content, write the full file back.

### Create a new note
1. Read `~/.mote/state.json` to get `notesDirectory`
2. Create a file named `YYYY-MM-DD-<slug>.md` where slug is a lowercase, hyphenated summary (max 40 chars)
3. Write the markdown content to that file
4. Do NOT modify `metadata.json` — Mote will discover the note when the user opens the note switcher (Cmd+O)
5. Tell the user: "I created a new note. Open the note switcher (Cmd+O) to see it."

### List all notes
1. List files in `~/.mote/notes/` — each `.md` file is a note

### Open a file in Mote
To open any markdown file in Mote's floating editor:
```
open "mote://open?path=/absolute/path/to/file.md"
```
The file opens in the editor with auto-save. The user can press Esc to close it and return to their previous note.

## Important

- **Never modify `~/.mote/metadata.json`** — Mote overwrites it from memory on every save. Your changes will be lost.
- **Mote auto-saves 1 second after typing stops.** If you read a note right after the user typed something, you might get slightly stale content.
- **If the user is actively typing in the note, avoid writing to it.** Mote will skip your update to protect the user's work, and its next auto-save will overwrite your file. After the user stops typing, wait at least 2 seconds before writing to the active note. Prefer creating a new note or confirming with the user first.
- **Live reload only works for local notes** in `~/.mote/notes/`. If the state file shows a vault note path (outside that directory), writing to it will update the file but Mote won't auto-refresh the editor.
- Notes are plain markdown. No frontmatter required, no special format.
