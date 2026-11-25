---
name: citation-fixer
description: GBrain-inspired citation audit for Codex. Use when the local brain corpus needs citation normalization or a pass over remaining uncited lines.
---

# Citation Fixer

Use this skill when the user wants citation cleanup or when a brain-writing change touched enough pages that citation drift is a risk.

This port is adapted from `garrytan/gbrain` at commit `0b47afbf402a4e27a648bb9d131ce584461461ea`.

## Workflow

1. Audit first:
   - `python3 scripts/brain_citations.py --verbose`
2. Normalize formatting when useful:
   - `python3 scripts/brain_citations.py --fix --verbose`
3. Read the remaining gaps manually.
4. Fix missing citations with real sources or leave them explicitly unresolved.

## Current Upstream Coverage

Resolve broken social-post citations by extracting searchable text, locating the canonical post, verifying author/date/content, and patching only after confirmation. In batch mode prioritize missing primary sources, then broken URLs, then weak secondary citations; respect rate limits and report unresolved references.

## Guardrails

- Do not invent citations for unsupported facts.
- Do not bulk-normalize without reading the remaining unresolved lines.
- Treat this as a quality pass, not a reason to rewrite unrelated content.
