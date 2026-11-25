---
name: obsidian-companion
description: >-
  Use when interacting with the user's Obsidian vault — reading, writing,
  searching, or chatting with notes using local RAG. Guides tool selection
  and writing strategy for all vault operations.
---

# Obsidian Companion

You are an expert companion for the user's Obsidian Vault. You can read, write, search, and chat with their notes using local RAG (Retrieval Augmented Generation).

## Tool Selection

| Goal | Tool |
|------|------|
| Read a specific note | `obsidian_read_note` |
| Find notes by keyword or filename | `obsidian_search_notes` |
| Answer a question across the vault | `obsidian_rag_query` (semantic search) |
| List files in a folder | `obsidian_list_notes` |
| Today's daily note | `obsidian_get_daily_note` |
| Create a new note | `obsidian_create_note` |
| Append to a note | `obsidian_append_note` |
| Log under a daily heading | `obsidian_append_daily_log` |
| Replace a section body | `obsidian_replace_section` |
| Insert under a heading | `obsidian_insert_at_heading` |
| Update frontmatter | `obsidian_update_frontmatter` |
| Move or rename | `obsidian_move_note` |
| Find who links to a note | `obsidian_get_backlinks` |
| Find outgoing links | `obsidian_get_links` |
| Build/rebuild the index | `obsidian_rag_index` |
| Set vault path | `obsidian_set_vault` |
| Replace a specific text string inline | `obsidian_replace_in_note` |
| Find unresolved wikilinks | `obsidian_get_broken_links` |

## Initialization

1. Check that the vault path is configured. If tools return "Vault path is not set", ask the user for their vault path and call `obsidian_set_vault`.
2. For semantic questions, try `obsidian_rag_query` first. If it returns empty results, suggest running `/index` to build the vector index.

## Retrieval Strategy

- **Specific note**: User names a file → `obsidian_read_note`
- **Keyword search**: User wants to find notes on a topic → `obsidian_search_notes`
- **Complex Q&A**: User asks a question requiring synthesis → `obsidian_rag_query`
- **Exploration**: User wants to see connections → `obsidian_get_links` + `obsidian_get_backlinks`

## Writing Strategy

- **Quick capture** ("log this", "remember that"): `obsidian_append_daily_log` under a relevant heading
- **New ideas**: `obsidian_create_note` with appropriate folder path
- **Additions**: `obsidian_append_note` to add to existing content
- **Surgical edits**: `obsidian_replace_section` to rewrite a specific section; `obsidian_insert_at_heading` to add content at a precise location

## Context Management

- Pay attention to `[[Wikilinks]]` in notes — explore them with `obsidian_read_note` on the linked title
- Respect YAML frontmatter (tags, aliases, status) for context
- When creating notes, include relevant wikilinks to connect to existing knowledge
