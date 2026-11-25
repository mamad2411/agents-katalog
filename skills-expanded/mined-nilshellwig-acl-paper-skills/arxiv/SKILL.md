---
name: arxiv
description: Search arXiv and add preprints (PDF, text, BibTeX) to an acl-paper project. Use when looking for preprints or recent work not yet in a venue, when an arXiv id or URL comes up, or when another skill needs an arXiv paper or its BibTeX.
---

Search and fetch from arXiv through the `arxiv` package; BibTeX comes from `arxiv.org/bibtex/<id>`. Reading and citing what you fetch follows the `literature` skill.

`PK` means `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/paperkit.py`, run from the project root. It switches to the project's Python env by itself.

## Search

```
PK search arxiv "<query>" [--limit 10] [--year-from 2023] [--year-to 2025]
```

The query uses arXiv's syntax. Plain words match loosely; field prefixes are sharper:

- `ti:"aspect sentiment"` title phrase, `abs:quadruple` abstract, `au:Hellwig` author, `cat:cs.CL` category
- combine with `AND`, `OR`, `ANDNOT`: `ti:"sentiment quad" AND cat:cs.CL`

arXiv allows one request every three seconds, so batch what you need into few searches.

Present hits as a short list (title, year, id). The abstract snippet is for triage only: pick what to fetch and read, then judge the paper after reading its body.

## Add

```
PK add arxiv <arxiv-id> [--key <key>]
```

`<arxiv-id>` as in the search (`1706.03762`); versioned ids and abs/pdf URLs work too. The command stores arXiv's BibTeX in `literature/archive.bib`, downloads the PDF, converts it to Markdown and creates the notes file. The entry moves into the paper bib once the paper is cited.

`--key` only when `key_scheme` in `paper.config.json` is not `native`: build the key by that scheme.

On "a bib entry with the same title exists": the paper is already in the library under that key (often the Anthology version). Ask the user which version to keep and cite.
