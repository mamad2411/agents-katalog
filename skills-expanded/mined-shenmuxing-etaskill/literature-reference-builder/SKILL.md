---
name: literature-reference-builder
description: Chrome-dependent academic paper fetching and BibTeX curation. Use when the user provides a planNN.md, paper list, citation list, or literature plan and wants Codex to use Google, Google Scholar, publisher pages, DBLP, arXiv, and the user's Chrome-accessible permissions to fetch the best available PDFs and create or update references.bib.
---

# Literature Reference Builder

## Overview

Convert a literature plan or paper list into local paper files plus a curated `references.bib`. Prefer high-quality published versions and reliable BibTeX, while recording unresolved access or metadata issues instead of silently guessing.

## Dependency

This skill depends on the Codex Chrome plugin. Use Chrome for Google, Google Scholar, publisher pages, and sites where the user's logged-in academic or institutional access may determine whether a PDF is available.

Do not bypass paywalls, defeat access controls, enter credentials without explicit user action, or use dubious mirror sites. If a paper cannot be accessed through normal search, publisher pages, author pages, arXiv, or the user's available Chrome session, mark it unresolved.

## Inputs And Outputs

Inputs:

- A `planNN.md` from `literature-idea-planner`, or
- A user-provided list of titles, DOIs, arXiv IDs, URLs, or rough citation notes.

Default outputs, unless the user specifies another layout:

- `references.bib` in the working directory.
- `papers/` containing downloaded PDFs with stable, readable filenames.
- `paper-sources.md` recording the PDF source, BibTeX source, chosen version, and unresolved items.

If `references.bib` already exists, preserve existing entries and comments, append or update only the target papers, and deduplicate by DOI, arXiv ID, normalized title, and existing citation key.

## Version Priority

For each paper, search in this order and choose the best legally accessible version:

1. Published version of record from the publisher, conference, journal, or proceedings site.
2. Official open-access published PDF or proceedings PDF.
3. Author-accepted manuscript from the author's page or institutional repository.
4. arXiv version, when no published PDF is available or the paper is only on arXiv.
5. No local PDF, with status recorded in `paper-sources.md`.

Use the published metadata in `references.bib` when the paper has a published version, even if the accessible PDF is an author manuscript or arXiv copy. Use arXiv metadata only for papers that are genuinely arXiv-only or unpublished.

## Workflow

1. Read the plan or paper list.
   - Extract title, authors, venue, year, DOI, arXiv ID, preferred source, and fetch notes.
   - Identify ambiguous entries before browsing. Ask only when ambiguity cannot be resolved by search.

2. Search with Chrome.
   - Start with Google queries such as `"<title>" pdf`, `"<title>" DOI`, `"<title>" site:arxiv.org`, and `"<title>" DBLP`.
   - Use Google Scholar's "Cite" flow for BibTeX when it is available and appropriate.
   - Use DBLP's compact BibTeX for computer-science conference and journal papers when it is cleaner than Scholar.
   - Use publisher, DOI, Crossref, arXiv, OpenReview, conference, or author pages when they provide more authoritative metadata.

3. Fetch and verify PDFs.
   - Save PDFs under `papers/` using `firstauthor-year-short-title.pdf`.
   - Open or inspect each downloaded PDF enough to verify title and authors.
   - Do not keep HTML landing pages renamed as `.pdf`.
   - If the download filename is unstable, rename it to the stable filename after verification.

4. Build `references.bib`.
   - Prefer Google Scholar BibTeX, DBLP compact BibTeX, publisher BibTeX, DOI/Crossref BibTeX, or arXiv BibTeX according to which source best matches the chosen publication status.
   - Normalize keys to a stable style such as `SurnameYearShortTitle`, unless the existing file has a clear local convention.
   - Preserve important fields: `author`, `title`, `booktitle` or `journal`, `year`, `doi`, `url`, `eprint`, `archivePrefix`, and `primaryClass` when applicable.
   - Remove obvious tracking URLs, duplicated fields, broken escaping, and placeholder values.

5. Write `paper-sources.md`.
   - Include one row per requested paper:

```markdown
| BibTeX key | Title | PDF status | PDF path | Chosen version | BibTeX source | Source URLs | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

6. Final verification.
   - Confirm every requested paper has either a BibTeX entry or an explicit unresolved note.
   - Confirm every downloaded PDF has a matching BibTeX key in `references.bib`.
   - Report unresolved items, access limitations, and any entries where the PDF version differs from the metadata version.

## Reporting

Keep the final user response short:

- number of papers processed;
- number of PDFs saved;
- number of BibTeX entries added or updated;
- unresolved papers and why;
- paths to `references.bib`, `papers/`, and `paper-sources.md`.
