---
name: citation-and-bibliography-management
description: "BibTeX hygiene, DOI normalization, Zotero collections, stable citation keys."
---

# Citation & bibliography management

- Prefer **DOIs**; resolve every reference through CrossRef when possible.
- Citation keys: `<firstAuthorLower><year><firstWordOfTitle>` (e.g. `tao2006restriction`). Stable across drafts.
- Maintain a single `references.bib` per paper under `/agent-filesystem/papers/<slug>/references.bib`.
- When David uses Zotero, sync via the Web API or BibTeX export; do not duplicate entries.
- Validate the `.bib` with `biber --tool-resolve-xdata --output-format=bibtex` before compiling.
