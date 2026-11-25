---
name: schematize
description: "Decompose a note, a folder or a topic from the folder silica-core indexes into one Markdown table (components, phases, dimensions). Use when the user asks for a schema, a breakdown or an at-a-glance table of something these documents cover; --save=<path> also writes it as a note."
argument-hint: "<note|folder|topic> [--save=<path>]"
compatibility: "Requires the silica-core MCP server (silica_files, silica_search, silica_read; silica_write_note for --save)."
metadata:
  silica-core-managed: "true"
---
Schematize from the indexed folder: $ARGUMENTS

Resolve the target: it may be a note (path or title), a folder (list it with silica_files and skim its notes), or a general topic (search with silica_search, then read the top matches with silica_read).
Output in chat: a one-line caption, then a Markdown table whose rows/columns best decompose what you found (components, phases, comparison dimensions, whatever shape fits); do not force a fixed template.
READ-ONLY: do not create, edit, patch, or move any note, unless the arguments carry --save=<path>. Then write the table to the note at that path using silica_write_note (create it if missing, overwrite if present): the table is the entire body, plus a one-line title.
