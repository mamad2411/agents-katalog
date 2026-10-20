---
name: import-bibtex
description: >
  Full BibTeX import and abstract enrichment pipeline running entirely in Cowork. Parses
  BibTeX files, creates research libraries, enriches missing abstracts via OpenRouter/Gemini,
  deduplicates, and inserts structured citations into Supabase.
  Use this skill whenever the user says "import my BibTeX," "upload my bibliography,"
  "import this into my research library," "process this BibTeX," "add these papers,"
  "start a new research project" with an attached file, "load my references," or any request
  to import academic references from a BibTeX file into the research pipeline. Also trigger
  when a .bib file is uploaded or when the user mentions BibTeX in the context of getting
  started with the research pipeline.
version: 0.1.0
---

# Import BibTeX

Parse, enrich, deduplicate, and load a BibTeX file into the research pipeline — entirely
within Cowork.

## Prerequisites

- **Supabase MCP** — for creating libraries and inserting citations
- **Google Drive MCP** — for uploading the annotated bibliography
- **OpenRouter API key** — for calling OpenRouter (abstract enrichment via Gemini). Shares Council's `scripts/openrouter_dispatch.py`, which resolves the key via `scripts/openrouter_key.py` — first the `OPENROUTER_API_KEY` env var, then the team-shared file at `MoxyWolf Vault/_Shared Knowledge/Agents and Plugins/openrouter.env`. Requires Council v0.7.0+ installed.

## Step 1: Receive the File

The user will either:
- Upload a `.bib` file directly in the conversation
- Paste BibTeX content as text
- Reference a file path

If the file is uploaded, read it from the uploads path. If pasted, capture the full text.

## Step 2: Create or Select Library

Ask the user what to name this research project, or let them pick an existing library.

**New library:**
```sql
INSERT INTO research_libraries (name, description, metadata)
VALUES ('{name}', '{description}', '{"created_by": "dorian"}'::jsonb)
RETURNING id, name
```

**Existing library:**
```sql
SELECT id, name FROM research_libraries ORDER BY created_at DESC
```

Store the `library_id` for all subsequent operations.

## Step 3: Parse BibTeX

Use the bundled parser script at `references/bibtex-parser.py`:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/research-pipeline/references/bibtex-parser.py /path/to/input.bib /tmp/parsed_citations.json
```

Or parse inline if the file is small (<50 entries):

Split the content on `@type{` patterns. For each entry extract:
- `citation_key` — the key after `@type{`
- `entry_type` — article, misc, inproceedings, etc.
- `title`, `authors`, `year`, `journal`, `abstract`, `doi`, `arxiv_id`, `url`
- `bibtex_raw` — the original entry text

Deduplicate by `citation_key + abstract` signature. Report to the user:
"Found [X] entries, [Y] unique after deduplication, [Z] already have abstracts."

## Step 4: Enrich Missing Abstracts

For entries without meaningful abstracts (empty, placeholder text, or missing entirely):

### Batch Strategy

Group entries into batches of 10-15 for efficient LLM processing. For each batch,
build one job in a `bibtex-enrich-jobs.json` array — one job per batch, each with
a unique `id` like `"batch-001"`. Then dispatch all batches in parallel via
Council's helper:

```bash
python3 "${COUNCIL_PLUGIN}/scripts/openrouter_dispatch.py" \
    --jobs "${WORKSPACE_OUTPUTS}/bibtex-${LIBRARY_ID}/enrich-jobs.json" \
    --out  "${WORKSPACE_OUTPUTS}/bibtex-${LIBRARY_ID}/enriched" \
    --timeout 180
```

Each job shape:

```json
{
  "id": "batch-001",
  "model": "google/gemini-3-pro-preview",
  "messages": [
    {"role": "system", "content": "...enrichment prompt..."},
    {"role": "user", "content": "...batch of entries as JSON..."}
  ],
  "temperature": 0.2,
  "max_tokens": 4000
}
```

Read each `enriched/batch-XXX.json` back, extract `response.choices[0].message.content`,
parse the JSON output, and update Supabase.

**Lightweight fallback (no API key, or LLM optional):**

For each entry missing an abstract:
1. Check if it has a DOI or URL
2. If DOI exists, fetch metadata from CrossRef directly via `WebFetch` or `curl`:
   `https://api.crossref.org/works/{doi}` — returns an abstract field when available
3. If no API abstract is available, leave the abstract blank rather than fabricate

### Enrichment Prompt

For each batch sent to the LLM:

```
You are processing BibTeX entries that need abstracts. For each entry:

1. If a meaningful abstract exists, preserve it exactly
2. If the abstract is missing or placeholder text:
   a. If a DOI or URL is provided, describe what the paper likely covers based on
      the title, authors, journal, and year
   b. Generate a 2-4 sentence academic abstract that:
      - States the central aim or problem
      - Synthesizes likely main arguments or methods
      - Highlights potential implications
   c. Mark generated abstracts with [AI-generated] prefix

Output each entry as JSON with fields: citation_key, abstract, abstract_source
where abstract_source is "original", "crossref", or "generated"
```

## Step 5: Insert into Supabase

For each parsed and enriched citation, insert into the `citations` table:

```sql
INSERT INTO citations (
  library_id, citation_key, entry_type, title, authors, year,
  journal, abstract, doi, arxiv_id, url, bibtex_raw,
  verification_status, source
) VALUES (
  {library_id}, '{citation_key}', '{entry_type}', '{title}', '{authors}',
  {year}, '{journal}', '{abstract}', '{doi}', '{arxiv_id}', '{url}',
  '{bibtex_raw}', 'unverified', 'bibtex_import'
)
ON CONFLICT (library_id, citation_key) DO UPDATE SET
  abstract = EXCLUDED.abstract,
  updated_at = now()
```

Use `ON CONFLICT ... DO UPDATE` so re-imports update abstracts without creating duplicates.

Process in batches of 50 for efficiency.

## Step 6: Upload to Google Drive

Generate an annotated bibliography markdown file:

```markdown
# Annotated Bibliography: {library_name}
Generated: {date}
Total citations: {count}

## Citations

### {citation_key_1}
**{title}** ({year})
{authors}
*{journal}*
DOI: {doi}

{abstract}

---

### {citation_key_2}
...
```

Upload to Google Drive in the user's preferred folder.
Store the Google Drive link.

## Step 7: Summary Report

Present the final results:

```
BibTeX Import Complete
══════════════════════

Library: {name} (ID: {library_id})
Total entries parsed:    {total}
Duplicates removed:      {dupes}
Citations inserted:      {inserted}
  ├─ With original abstracts:  {original_count}
  ├─ Abstracts from CrossRef:  {crossref_count}
  ├─ AI-generated abstracts:   {generated_count}
  └─ No abstract available:    {no_abstract_count}

Annotated Bibliography: {google_drive_link}

Next steps:
  → "Verify my citations" — run 4-layer reference validation
  → "Find more papers" — discover related literature
  → "Synthesize my research" — build thematic maps + perspective
```

## Handling Large Files (200+ entries)

For large BibTeX files:
1. Parse all entries first (this is fast, no LLM needed)
2. Insert all entries into Supabase immediately with whatever abstracts exist
3. Then enrich missing abstracts in background batches
4. Update Supabase as each batch completes

This way the user has their library available immediately and can start synthesis
while enrichment continues.

## Error Handling

- If a BibTeX entry can't be parsed (malformed braces, etc.), skip it and log the
  citation key in a "skipped entries" list
- If OpenRouter/Gemini is unavailable, insert entries without enrichment and mark
  them for later processing
- If Supabase insert fails for a specific entry, log it and continue with the rest
- Always report what worked and what didn't at the end
