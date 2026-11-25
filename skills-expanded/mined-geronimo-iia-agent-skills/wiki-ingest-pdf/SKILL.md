---
name: wiki-ingest-pdf
description: >-
  Use when adding one or more PDF files as sources in a llm-wiki knowledge base.
  Covers source folder creation, PDF extraction, structured analysis, index update,
  and wiki ingest. Triggers on: "add this PDF to the wiki", "ingest this paper",
  "create a source for this file", "add as source in my wiki".
metadata:
  version: "1.0.0"
---

# Wiki Ingest PDF

Add one or more PDFs as first-class wiki sources: folder layout, extraction,
structured analysis, index update, and ingest in one repeatable pipeline.

**Required sub-skills (read before starting):**
- `geronimo-skills:pdf-parse` — extraction tool selection and xberg invocation
- `geronimo-skills:research-paper` — structured analysis pipeline and anti-slop
- `geronimo-skills:kb-conventions` — frontmatter schema, annotation markers, layout
- `llm-wiki:bootstrap` — orient to the target wiki before touching files
- `llm-wiki:content` — create and update wiki pages with correct frontmatter

## Step 0 — Orient to the wiki

Run `llm-wiki:bootstrap` for the target wiki. Identify:
- Wiki root path (from `wiki_config`)
- The `sources/` section slug and its `index.md` path
- Existing source slugs (avoid collisions)

## Step 1 — Derive slug and paths

From the PDF filename, derive a lowercase-hyphenated slug.
Convention: `<author>-<short-topic>` or `<author>-<year>-<short-topic>`.

```
PDF:  Psychisme_modele_constructible_cardon.pdf
Slug: cardon-psychisme
```

Paths:
```
<wiki_root>/sources/<slug>/
  original.pdf          ← PDF moved/copied here
  extracted/
    content.md          ← xberg output
  analysis/
    <slug>.md           ← structured analysis
    README.md           ← analysis index
  source.md             ← wiki page (paper.json schema)
```

## Step 2 — Create folder layout and move PDF

```bash
mkdir -p <wiki_root>/sources/<slug>/extracted
mkdir -p <wiki_root>/sources/<slug>/analysis
mv <inbox_path> <wiki_root>/sources/<slug>/original.pdf
```

If the PDF is already in the right place, skip the move.

## Step 3 — Create stub source.md

Use the `paper` type schema from `geronimo-skills:kb-conventions`.
Fill `title`, `tags`, `read_when` from the filename and any known context.
Set `status: draft`, `confidence: 0.0`, leave `tldr` and `claims` empty.

## Step 4 — Extract PDF

Follow `geronimo-skills:pdf-parse` to select the right tool.

**xberg (machine-readable PDFs):**
```bash
# Detect
pdfinfo original.pdf   # check Characters: > 0

# Extract — xberg writes WARN lines to stdout; redirect and strip
xberg extract original.pdf --content-format markdown --page-markers true \
  > /tmp/<slug>_raw.md
grep -vE "^WARN" /tmp/<slug>_raw.md > extracted/content.md

# Verify
wc -w -l extracted/content.md   # sanity: > 500 words for a real doc
```

**marker-pdf (scanned/image PDFs):**
```bash
uvx marker-pdf marker_single original.pdf --output_dir extracted/
```

## Step 5 — Produce structured analysis

Follow `geronimo-skills:research-paper` §Step 4.
Output: `analysis/<slug>.md`.

Required sections:
1. Publication details
2. Core thesis (`[DIRECT]`)
3. Key contributions (annotated)
4. Mathematical foundations (or `∅ NOT FOUND IN SOURCES`)
5. Algorithms / pseudocode (or `∅`)
6. Architecture / system design
7. Experimental results (or `∅`)
8. Limitations and open problems
9. Relation to existing KB (use `> ✦ NEW:`, `> ⚠ DIVERGES FROM KB:`, `> ∅ NOT FOUND IN SOURCES:`)
10. Glossary

Apply `geronimo-skills:anti-slop` before saving.

Create `analysis/README.md` — one-line entry per analysis file (no frontmatter needed; indexer skips it by design).

## Step 5b — Verify analysis frontmatter

Every file in `analysis/` that should be indexed **must** have valid frontmatter.
Use `llm-wiki:content` to verify and fix if needed.

Required fields per `geronimo-skills:kb-conventions`:

```yaml
---
title: "Analysis: <Document Title>"
type: note
summary: "<one-line summary>"
read_when:
  - <retrieval condition>
status: active
last_updated: "<YYYY-MM-DD>"
source: "sources/<slug>/original.pdf"
---
```

**Checklist before proceeding:**
- [ ] `type:` field present (most common omission — indexer silently skips pages without it)
- [ ] `status: active`
- [ ] `summary` is one line, not a paragraph
- [ ] `source` points to `sources/<slug>/original.pdf`

`extracted/content.md` and `analysis/README.md` intentionally have no frontmatter — leave them as-is.

## Step 6 — Update source.md

After analysis, fill in:
- `tldr`: one-sentence key takeaway
- `status: active`
- `concepts`: slugs of wiki concept pages this source informs
- `confidence`: 0.8–1.0 for `[DIRECT]`; 0.5–0.7 for `[INFERRED]`; 0.1–0.4 for `[SPECULATIVE]`
- `claims`: 3–7 key claims using the claim schema in `kb-conventions`

## Step 7 — Update sources/index.md

Add a row to the sources table:

```markdown
| [<slug>](sources/<slug>/source.md) | <Title> | paper | <tags> | active |
```

## Step 8 — Ingest

Use `llm-wiki:content` to review the final page set, then commit and index with `wiki_ingest`:

```
wiki_ingest(wiki: "<wiki-name>", path: "sources/<slug>")
```

Check the response:
- `pages_validated` should cover `source.md` + all `analysis/*.md` files with frontmatter
- Warnings about `no frontmatter` on `extracted/content.md` and `analysis/README.md` are expected — ignore
- `informs` edge warnings (`target has type 'note', expected concept`) mean a slug in `concepts:` points to a non-concept page — fix the target type or remove the slug and add a `[[wikilink]]` in the body instead
- All other warnings need investigation before proceeding

After ingest, run `wiki_lint` and check for orphan warnings:
- An orphan warning on `analysis/<slug>.md` means `source.md` has no link to the analysis file — add a `[[sources/<slug>/analysis/<slug>]]` wikilink in the `source.md` body and re-run ingest
- 0 errors and 0 warnings (excluding expected no-frontmatter) is the acceptance bar

## Multiple PDFs

Run Steps 1–8 for each PDF independently. Do not batch-create slugs or
merge analyses. Each PDF gets its own folder and analysis.

## Common mistakes

| Mistake | Fix |
|---|---|
| Using `--output` flag with xberg | Flag doesn't exist; use stdout redirect + grep |
| Skipping `pdfinfo` check | Machine-readable vs scanned requires different tool |
| `type: note` on analysis files | Set `type: note` (analysis files are notes, not papers) |
| Linking `concepts:` to synthesis docs or sections | Only `type: concept` pages; use `[[wikilink]]` in body for others |
| Forgetting `type:` field in analysis frontmatter | Required; wiki indexer skips pages without it |
| Leaving `confidence: 0.0` in source.md after analysis | Update to reflect actual annotation level |
