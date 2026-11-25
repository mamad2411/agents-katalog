---
name: moc-update
description: >-
  Use after creating a new Engineering/ note to suggest which Maps of Content
  (MOCs) it belongs in. Triggers on "update MOC", "add to MOC", "which MOCs",
  or when the user has just created an Engineering/ note.
---

# MOC Update After New Note

Find the Maps of Content (MOCs) that should link to a newly created note and suggest the additions.

## Workflow

1. **Identify the new note** — Path follows the skill invocation. If not provided, ask.

2. **Semantic MOC search** — Call `obsidian_rag_query` with the note title as query, `limit: 10`.
   Flag results that are MOC-style notes (path contains "MOC", filename ends in "-MOC", or
   `type: moc` frontmatter).

3. **Keyword fallback** — Call `obsidian_search_notes` with key terms from the note title
   to catch MOCs that aren't yet indexed.

4. **Present suggestions** — For each candidate MOC, show:
   - The MOC path
   - Which heading the link should go under (if readable)
   - A proposed link line: `- [[NoteName]] — one-line description`

5. **Append on confirmation** — Call `obsidian_insert_at_heading` (preferred) or
   `obsidian_append_note` to add the link. Never edit without user approval.

## Arguments

New note path: `/moc-update Engineering/AuthPatterns.md`

## Tips

- If the vault has no MOCs yet, offer to create a starter one at `MOCs/<Topic>-MOC.md`
- Daily Notes are not MOCs — skip them in results
