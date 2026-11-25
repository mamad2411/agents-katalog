---
name: cross-linker
description: >-
  Use when the user wants to find and insert missing wikilinks across vault
  notes. Triggers on "cross-link", "find missing links", "weave links",
  "unlinked mentions", "add wikilinks", or "link notes together".
---

# Cross-Linker

Discover unlinked mentions of vault concepts and insert `[[wikilinks]]`. Complements `link-audit` (which finds broken/orphan links) by finding links that *should exist but don't*.

## Workflow

### Phase 1 — Build Page Registry

1. Call `obsidian_list_notes` on the target scope (default: `Engineering/`).
2. For each note, call `obsidian_read_note` and extract from frontmatter:
   - **Title** (from `# heading` or filename)
   - **Aliases** (from `aliases:` frontmatter field, if present)
   - **Type** (pattern, trap, decision, concept)
3. Build a registry: `{ title, aliases[], path, type }` for each note.

For large scopes (>50 notes), batch reads and process incrementally.

### Phase 2 — Scan for Unlinked Mentions

For each note in scope:
1. Call `obsidian_read_note` to get the full body text.
2. For each *other* page in the registry, check if the page's title or any alias appears in the body text **without** being wrapped in `[[...]]`.
3. Skip matches inside:
   - Existing wikilinks `[[...]]`
   - Code blocks (fenced or inline)
   - Frontmatter
   - The note's own title/heading
4. Record each match: `{ source_note, target_note, matched_text, line_context, confidence }`

### Phase 3 — Score and Rank

Assign confidence to each proposed link:
- **High** — exact title match (case-insensitive), target is a Pattern/Trap/Decision note
- **Medium** — alias match, or title match in a less structured note
- **Low** — partial match or only semantically related (use `obsidian_rag_query` to verify)

Sort findings: high confidence first, grouped by source note.

### Phase 4 — Present Findings

Show the user a report:

```
## Cross-Link Report for: Engineering/

### High Confidence (auto-apply)
- Engineering/Patterns/table-driven-tests.md
  Line 12: "table driven tests" → [[Table-Driven Tests]]

### Medium Confidence (confirm each)
- Engineering/Traps/mock-drift.md
  Line 8: "interface injection" → [[Interface Injection]]

### Low Confidence (review)
- working/appiary/knowledge/auth.md
  Line 23: "token" → possibly [[Token Rotation]] ?

### Summary
- X high-confidence links ready to apply
- Y medium-confidence links for review
- Z low-confidence suggestions
```

### Phase 5 — Apply Links

- **High confidence:** Apply automatically using `obsidian_replace_in_note`, replacing the first unlinked mention with `[[Target Title]]` or `[[path/to/note|display text]]`.
- **Medium confidence:** Apply one at a time, asking user to confirm each.
- **Low confidence:** List for reference only — don't auto-apply.

Only link the **first** unlinked mention of each target per source note. Repeated mentions stay as plain text (standard wiki convention).

## Arguments

- Optional scope: `/cross-linker Engineering/Patterns/` (default: `Engineering/`)
- Optional depth: `/cross-linker --deep` to include `working/` and `reference/` scopes

## Tips

- Run on a narrow scope first (`Engineering/Patterns/`) to calibrate before going vault-wide
- If a note has many false positives, it may need `aliases:` in frontmatter to disambiguate
- Short titles (1-2 words like "Testing" or "Auth") generate noise — prefer linking specific concept names
- After running, consider `/link-audit` to verify no broken links were introduced
