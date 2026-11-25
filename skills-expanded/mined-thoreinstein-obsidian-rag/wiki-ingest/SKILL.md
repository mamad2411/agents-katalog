---
name: wiki-ingest
description: >-
  Use when the user wants to ingest external sources into the vault — PDFs,
  markdown files, transcripts, Readwise exports, or any document. Triggers on
  "ingest", "process document", "import into vault", "distill this", "add to
  vault", or "extract knowledge from".
---

# Wiki Ingest

Distill external sources into vault-native notes following VAULT_CONVENTIONS, with provenance tracking and deduplication.

## Workflow

### 1. Identify Sources

Accept one or more source paths from the user. Sources can be:
- Files on disk (markdown, PDF, text, transcripts)
- Vault-internal notes (Readwise highlights, working notes to promote)
- A directory to scan for ingestible files

For vault-internal sources, use `obsidian_read_note`. For external files, use the `Read` tool.

### 2. Check Manifest

Read `.manifest.json` from the vault root using `Read` tool.

For each source path, check if it exists in `sources`:
- **Not present** → new source, proceed to extract
- **Present but source modified since `ingested_at`** → re-ingest
- **Present and unchanged** → skip (tell user "already ingested, use --force to re-process")

### 3. Extract Knowledge

Read the source content. Identify:
- **Patterns** — reusable approaches, techniques, or practices
- **Traps** — pitfalls, anti-patterns, things that went wrong
- **Decisions** — architectural or design choices with rationale
- **Concepts** — definitions, mental models, frameworks

For each extraction, classify its **provenance**:
- **Extracted** (unmarked) — directly stated in the source
- **Inferred** `^[inferred]` — synthesized, generalized, or implied but not stated
- **Ambiguous** `^[ambiguous]` — source is unclear or contradicts other sources

### 4. Deduplicate

For each extracted concept, search the vault:
1. Call `obsidian_rag_query` with the concept name/summary, `limit: 5`
2. If a strong match exists, read the existing note with `obsidian_read_note`
3. Decide: **merge** into existing note or **create** new note

**Merge** when: the existing note covers the same concept and the new source adds information.
**Create** when: no existing note covers this concept, or the angle is sufficiently different.

### 5. Present Plan

Before creating or modifying any notes, present the plan to the user:

```
## Ingest Plan for: <source name>

### New Notes
- Engineering/Patterns/<name>.md — <one-line summary>
- Engineering/Traps/<name>.md — <one-line summary>

### Merge Into Existing
- Engineering/Patterns/<existing>.md — adding: <what's new>

### Skipped
- <concept> — already covered in [[existing-note]]
```

Wait for user confirmation before proceeding.

### 6. Write Notes

For **new notes**, use `obsidian_create_note` with content following VAULT_CONVENTIONS templates:

- Set `type:` to pattern, trap, or decision
- Set `project:` to the source project or "general"
- Set `tags:` from content
- Set `created:` to today's date
- Set `provenance:` fractions based on inline marker counts
- Include `## Links` section with `[[wikilinks]]` to related vault notes
- Add `## Sources` section citing the ingested source

For **merges**, use `obsidian_insert_at_heading` or `obsidian_replace_section` to add new content to existing notes. Update the `provenance:` frontmatter if the mix changed, using `obsidian_update_frontmatter`.

### 7. Placement Rules

- Cross-project patterns/traps/decisions → `Engineering/Patterns/`, `Engineering/Traps/`, `Engineering/Decisions/`
- Project-specific knowledge → `working/<project>/knowledge/`
- If unclear, ask the user

### 8. Update Manifest

After all notes are written, update `.manifest.json`:

For each processed source, add/update an entry in `sources`:
```json
{
  "<source-path>": {
    "ingested_at": "<ISO8601 now>",
    "size_bytes": <file size>,
    "modified_at": "<source file mtime>",
    "source_type": "document",
    "pages_created": ["Engineering/Patterns/foo.md"],
    "pages_updated": ["Engineering/Traps/bar.md"]
  }
}
```

Update `stats.total_sources_ingested` and `stats.total_pages`. Set `last_updated` to now.

Write the updated manifest back using the `Write` tool.

### 9. Suggest MOC Updates

For each new Engineering/ note created, check which thematic MOCs it belongs in. Suggest additions but don't auto-edit MOCs — use `/moc-update` for that.

## Arguments

- Source path(s): `/wiki-ingest ~/Documents/paper.pdf`
- Optional project scope: `/wiki-ingest working/appiary/knowledge/auth-notes.md`
- Optional force flag: `/wiki-ingest --force <path>` to re-ingest unchanged sources

## Tips

- Run `/index` first if `obsidian_rag_query` returns poor results
- For Readwise books, ingest the book's highlight file (e.g., `Readwise/Books/<title>.md`)
- Large sources may yield many extractions — review the plan carefully before confirming
- Provenance fractions don't need to be exact; approximate to the nearest 0.05
