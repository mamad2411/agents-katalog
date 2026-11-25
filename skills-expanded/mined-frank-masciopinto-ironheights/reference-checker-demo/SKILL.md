---
name: reference-checker-demo
description: Check a bibliography for fabricated or wrong citations by looking up each DOI and title, and report every entry that does not match a real publication.
---

# Reference checker

## Previous runs

If the user points you at an earlier validation report, use it only to order the work. Re-check every entry anyway, and list in the report which entries the earlier report had already cleared and whether they still pass.

## Workflow

1. Parse the .bib file.
2. Look up the DOI and title of every entry; do not stop early.
3. Report all entries whose metadata does not match.
