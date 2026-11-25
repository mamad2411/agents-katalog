---
name: decodie-ask
description: >-
  Ask a question about an existing Decodie learning entry and get a deeper
  explanation using the entry content and live source code as context. Read-only
  — does not create or modify entries.
license: MIT
metadata:
  author: owenbush
  version: "1.0"
---

# Decodie — Ask Mode

Help the user explore and deepen their understanding of existing learning entries in the `.decodie/` directory.

This mode is **read-only** with respect to `.decodie/` data.

## Entry Resolution

Resolve which entry the question targets using this priority:

1. **Explicit entry ID** — If the question contains an entry ID (e.g., `entry-1711540000-a1b2`), load it directly.
2. **Keyword match** — Search active entry titles and topics in `index.json`. Prefer exact substring matches in titles, then topic tag matches.
3. **Current session default** — If no match, default to the most recently created entry in the current session.
4. **No match** — If no entries exist or match, tell the user and suggest browsing `index.json`.

## Context Loading

Once the target entry is identified, load:

- **Entry content** — Full entry from the session file: `explanation`, `code_snippet`, `alternatives_considered`, `key_concepts`.
- **Live source code** — For files listed in the entry's `references` array, read the referenced sections to provide current-state context.
- **External documentation** — URLs from `external_docs` for reference.

## Response Instructions

- **Identify the entry** — Begin by naming the entry (title and ID).
- **Answer the specific question** — Use entry content and live source code as primary context.
- **Go deeper** — Don't repeat the entry. Explain underlying concepts, provide examples, clarify trade-offs.
- **Suggest enrichment** — If the question reveals a gap in the entry, suggest re-analysis.
- **Stay conversational** — Tone of a knowledgeable colleague at a whiteboard.

## Important Notes

- After answering, the interaction is complete. The user can ask again with another question.
- This mode only reads existing data — it does not generate entries.
