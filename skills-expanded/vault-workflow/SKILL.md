---
name: vault-workflow
description: Use when the user asks you to search, read, or reason about notes in their markdown vault — guides when to use which vault tool and how to chain them for good results.
---

# Working effectively with the markdown vault

When the user mentions "my vault", "my notes", or asks a question that could
be answered from their knowledge base, use the markdown-vault-mcp tools as
follows.

## Search strategy

- **Default to `search` with `mode="hybrid"`** — combines BM25 keyword and
  embedding similarity, gives the best recall for conceptual questions.
- Fall back to `mode="keyword"` only when the user gives an exact phrase or
  tag they want matched literally.
- If hybrid returns nothing and the query is a proper noun, retry with
  `mode="keyword"` — embeddings miss exact names.

## Reading and context

- After finding a relevant note with `search`, call `get_context` on the top
  hit before reading the full body. Context returns backlinks, outlinks,
  similar notes, folder peers, and tags in one call — usually enough to
  answer without reading the file.
- Only call `read` when the user asks for the text itself or when
  `get_context` does not give enough signal.

## Link-graph questions

- "What notes reference X?" → `get_backlinks`.
- "What does this note link to?" → `get_outlinks`.
- "How are these two notes connected?" → `get_connection_path`.
- "What is orphaned?" → `get_orphan_notes`.
- "What is most cited?" → `get_most_linked`.

## Writes (only if read-only mode is disabled)

- Prefer `edit` over `write` for targeted changes — `edit` fails safely if
  the old text is not unique, preventing accidental overwrites.
- Use `rename(update_links=True)` for moves, never `write` to a new path plus
  `delete` of the old path — the `update_links` flag repairs internal
  references.
- Never call `reindex` after writes; the server updates its index inline.

## Do not

- Do not use `list_documents` as a search substitute — it is a flat
  enumeration, not ranked.
- Do not read a note and then re-search for it; remember the path from the
  first result.
