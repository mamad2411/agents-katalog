---
name: acl-anthology
description: Search the ACL Anthology and add papers (PDF, text, BibTeX) to an acl-paper project. Use when looking for NLP/CL papers from ACL, EMNLP, NAACL, EACL, Findings, TACL, COLING, LREC or workshops, when an Anthology id or URL comes up, or when another skill needs an Anthology paper or its BibTeX.
---

Search and fetch from the ACL Anthology through the `acl-anthology` package. Reading and citing what you fetch follows the `literature` skill.

`PK` means `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/paperkit.py`, run from the project root. It switches to the project's Python env by itself.

## Search

```
PK search acl-anthology "<query>" [--limit 10] [--year-from 2020] [--year-to 2025]
```

Ranking is keyword overlap: title words weigh most, abstract words count too. Use the task's technical terms ("aspect sentiment quad prediction"), and run a second search with synonyms or the abbreviation spelled out when the first one is thin. Each hit shows its Anthology id and whether it is already in the library.

The first search in a fresh setup clones the Anthology metadata (about 300 MB) into `~/.cache/acl-paper/anthology`. `PK anthology-update` pulls newer data, worth doing when looking for papers from the last few weeks.

Present hits as a short list (title, year, venue, id). The abstract snippet is for triage only: pick what to fetch and read, then judge the paper after reading its body.

## Add

```
PK add acl-anthology <anthology-id> [--key <key>]
```

`<anthology-id>` is the id from the search or the URL (`2023.acl-long.1`); the Anthology bibkey works too. The command stores the official Anthology BibTeX in `literature/archive.bib`, downloads the PDF, converts it to Markdown and creates the notes file. The entry moves into the paper bib once the paper is cited.

`--key` only when `key_scheme` in `paper.config.json` is not `native`: build the key by that scheme.

On "a bib entry with the same title exists": the paper is already in the library under that key (often the arXiv version). Ask the user which version to keep and cite.
