---
name: frontmatter-guard
description: Audit and repair local brain page frontmatter before malformed pages break search, ingest, or future sync.
---

# Frontmatter Guard

Use this skill when the user asks to validate frontmatter, fix frontmatter, run a brain lint, or check local brain page structure.

## Workflow

1. Start read-only:
   - inspect representative brain pages
   - run `python3 scripts/brain_doctor.py` if available
   - if the upstream `gbrain` CLI exists, prefer read-only `gbrain frontmatter audit --json`
2. Classify issues:
   - missing opening or closing `---`
   - YAML parse errors
   - empty frontmatter
   - slug/path mismatch
   - null bytes or non-text content in markdown files
   - missing citation or source fields when local conventions require them
3. For mechanical fixes, show the intended file list before writing.
4. For ambiguous fixes, ask for the intended title, type, or source instead of guessing.
5. Re-run the audit after fixes.

## Validation Classes

- file framing: opening and closing delimiters, UTF-8 text, and no null bytes
- YAML syntax: valid mappings, arrays, quoted scalars, and parseable dates
- schema: required fields, supported page type, and expected value shapes
- identity: slug, title, and path agreement
- provenance: source and citation fields required by the local page convention

Support four explicit modes: whole-corpus audit, single-path validation, scoped mechanical repair, and optional pre-commit validation. Quote scalar values when they contain YAML-significant punctuation, and prefer real YAML arrays over comma-packed strings.

## Guardrails

- Do not auto-fix user-authored pages without a before/after plan.
- Do not remove citations while normalizing frontmatter.
- Do not treat citation repair as the same job; use `citation-fixer` for citation semantics.
- Never install a pre-commit hook without explicit user authorization.
