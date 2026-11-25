---
name: links
description: >-
  Use when the user wants to explore connections between notes, see what links
  to or from a note, or says "links", "backlinks", "connections", or "graph".
---

# Explore Note Connections

Map the link graph around a specific note.

## Workflow

1. Call `obsidian_get_links` on the specified note to find outgoing links
2. Call `obsidian_get_backlinks` on the same note to find incoming links
3. Present a connection map:
   - **Outgoing links**: Notes this note references
   - **Incoming links**: Notes that reference this note

## Arguments

The note path or name follows the skill invocation. Example: `/links Projects/MyProject.md`

## Tips

- If the user provides just a name (no path), try searching for it first with `obsidian_search_notes`
- For `obsidian_get_backlinks`, pass the note name without the `.md` extension
- For `obsidian_get_links`, pass the full relative path with `.md`
