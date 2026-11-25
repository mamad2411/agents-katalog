---
name: compound
description: >-
  Use when the user wants to promote cross-project knowledge to the global
  Engineering/ folder, or says "promote knowledge", "compound notes",
  "knowledge synthesis", or "find repeated ideas across projects".
---

# Compound Knowledge Promotion

Identify knowledge that has crystallized across multiple projects and promote it to a global Engineering/ note.

## Workflow

1. **Scan project knowledge dirs** — Call `obsidian_list_notes` with `subfolder: "working"`.
   Filter results to paths matching `working/*/knowledge/*.md`.

2. **Semantic clustering** — For each knowledge note path, call `obsidian_rag_query`
   with the note filename (without extension) as query, `limit: 8`.
   Track which notes appear in results from 2+ different projects — these are candidates.

3. **Read candidates** — Call `obsidian_read_note` on shortlisted files.
   Look for shared definitions, patterns, or insights worth generalizing.

4. **Draft global note** — Compose a new `Engineering/<ConceptName>.md` with:
   - Frontmatter: `type: concept`, `created: <today>`
   - Synthesized body (not copy-paste — rewrite for clarity)
   - `## Source Notes` section with `[[wikilinks]]` back to originating notes

5. **Show draft to user** — Present the proposed note content and path before creating.
   Ask for confirmation.

6. **Create on approval** — Call `obsidian_create_note` with the approved content.

7. **Report cross-links** — List which project knowledge notes should now add `[[ConceptName]]`
   to avoid re-discovering this knowledge next time.

## Arguments

Optional topic hint: `/compound authentication patterns`

## Tips

- If `obsidian_rag_query` returns no results, suggest running `/index` first
- If no notes appear in 2+ projects, report that and suggest manual promotion
