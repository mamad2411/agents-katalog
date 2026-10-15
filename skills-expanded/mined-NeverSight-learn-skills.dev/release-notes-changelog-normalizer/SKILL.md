---
name: release-notes-changelog-normalizer
description: Vendor-neutral skill to normalize raw release notes into Keep a Changelog-style entries with consistent headings.
---

## When to invoke
- You have messy release notes from commits/tickets and need a clean changelog entry.
- You need to standardize categories (Added/Changed/Fixed/Deprecated/Removed/Security).

## Inputs needed
- A JSON file with:
  - `version` (string)
  - `date` (string)
  - `items[]` (strings), each a raw note line

## Workflow
1. Normalize text: trim, de-duplicate, enforce sentence casing.
2. Classify each item into a changelog category using keyword heuristics.
3. Output a structured changelog entry suitable for inclusion in CHANGELOG.md.

## Output format
- Markdown text written to an output file.

## Guardrails
- Do not fabricate features; only reformat and categorize provided items.
- Keep original meaning; avoid rewriting beyond light normalization.

## Reference code
- `release_notes_changelog_normalizer.py` reads JSON and writes a markdown changelog entry.
