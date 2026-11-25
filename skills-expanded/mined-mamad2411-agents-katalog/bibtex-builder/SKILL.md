---
name: bibtex-builder
description: >
  This skill should be used when the user asks to "build a bibliography",
  "create a BibTeX file", "generate abstracts for URLs", "enrich my BibTeX",
  "add abstracts to my bibliography", "process these URLs into citations",
  "build a .bib file", "convert URLs to BibTeX", "enrich this .bib file",
  or any request involving creating or enriching BibTeX bibliographies with
  abstracts generated from web content. Also trigger when the user uploads
  a .bib file and wants abstracts added, or provides a list of URLs for
  bibliography construction.
version: 0.1.0
---

# BibTeX Builder

Build and enrich BibTeX bibliographies with AI-generated abstracts from web content.

## Input Modes

This skill supports three input modes:

1. **Single URL** — Fetch one URL, extract metadata, generate abstract, output BibTeX entry
2. **URL list** — Process multiple URLs into a complete .bib file
3. **Existing .bib file** — Parse an uploaded BibTeX file, fetch URLs for entries missing abstracts, generate and insert abstracts

Detect the input mode from context:
- If the user provides one URL → single URL mode
- If the user provides multiple URLs (pasted, comma-separated, or in a file) → URL list mode
- If the user uploads or references a .bib file → enrich mode

## Workflow

### Step 1: Determine Output Location

Use AskUserQuestion to ask the user where to save the output .bib file. Suggest a descriptive filename based on the topic or source material.

### Step 2: Fetch Content

For each URL, use the WebFetch tool to retrieve the page content.

- If WebFetch fails for a URL, log it as a warning and continue processing other URLs
- Extract the main article/page content, ignoring navigation, ads, and boilerplate
- If the page has an existing abstract or summary, note it for reference but still generate a fresh one

### Step 3: Extract Bibliographic Metadata

From the fetched content, extract:

- **author** — Article author(s). Use "Unknown" if not found.
- **title** — Article or page title (required)
- **year** — Publication year. Extract from the page, URL, or metadata. Use the current year if unavailable.
- **url** — The source URL
- **journal / booktitle / howpublished** — Publication venue. For web articles, use the site name.
- **entry type** — Determine the best BibTeX type:
  - `@article` for journal/magazine articles
  - `@inproceedings` for conference papers
  - `@techreport` for technical reports, whitepapers
  - `@misc` for blog posts, web pages, general web content
  - `@book` or `@incollection` when applicable

### Step 4: Generate Abstract

Write a 2–4 sentence abstract following these rules:

1. **Sentence 1**: State the central aim or problem of the article clearly and concisely
2. **Sentence 2-3**: Synthesize the main arguments, methods, and key findings — avoid repetition or surface summaries
3. **Sentence 3-4**: Highlight implications, practical applications, or broader significance (if applicable)

Abstract quality requirements:
- Express complex ideas in clear, accessible language with an academic yet readable tone
- Maintain logical flow: problem → approach → result → relevance
- Use factually accurate summarization without invented claims
- Preserve the original context and intent of the source material
- Write in plain language suitable for academic audiences
- Do NOT start with "This article..." — vary the opening construction

### Step 5: Generate BibTeX Key

Create a citation key using the pattern: `{first_author_lastname}_{significant_word}_{year}`

- Lowercase, underscores for separators
- Use the first author's last name (or "unknown" if no author)
- Pick one distinctive word from the title
- Append the 4-digit year

Examples: `smith_resilience_2024`, `nist_framework_2023`, `unknown_compliance_2025`

### Step 6: Assemble BibTeX Entry

Format each entry following strict BibTeX conventions. See `references/bibtex-format.md` for the complete formatting specification.

### Step 7: Compile and Save

- Combine all entries into a single .bib file
- Sort entries alphabetically by citation key
- Add a header comment with generation date and source count
- Save to the user's chosen location
- Present a summary: total entries processed, any failures, and the file location

## Handling Enrichment of Existing .bib Files

When processing an existing .bib file:

1. Parse all existing entries using the Bash tool with a Python script (see `references/bibtex-parser.md`)
2. For entries that already have an abstract field, preserve it unchanged
3. For entries missing an abstract:
   - If a `url` field exists, fetch the URL and generate an abstract
   - If no `url` field exists, generate a brief abstract from the title and any available metadata fields (this will be less detailed — note this in a comment)
4. Preserve ALL original fields and formatting choices
5. Output the complete file with abstracts inserted

## Error Handling

- **WebFetch failure**: Log the URL, skip the entry, include it in the summary as "failed to fetch"
- **No extractable content**: Create the BibTeX entry with available metadata and add `abstract = {Content could not be extracted from the source URL.}`
- **Duplicate URLs**: Detect and skip duplicates, warning the user
- **Malformed BibTeX input**: Attempt best-effort parsing; list unparseable entries in the summary

## Additional Resources

- **`references/bibtex-format.md`** — Complete BibTeX formatting specification with field ordering and escaping rules
- **`references/bibtex-parser.md`** — Python parsing script for reading existing .bib files
