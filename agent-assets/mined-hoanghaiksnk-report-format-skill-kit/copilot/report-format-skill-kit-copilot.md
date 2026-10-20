# Copilot Instructions

This repository documents a reusable AI skill for reproducing strict report formats.

## Primary Goal

Help an AI agent turn approved reference artifacts into a repeatable DOCX generation workflow with explicit acceptance rules.

## Working Rules

- Treat the approved report form as the source of truth.
- Do not assume HTML preview parity means Word or PDF parity.
- Separate data correctness from layout correctness.
- Prefer a single canonical report model reused by all output paths.
- When a mismatch is found, identify the correct fix layer:
  - data mapping
  - template structure
  - post-processing
  - XML-level correction
- Do not invent acceptance criteria. Use the report profile and acceptance checklist.
- Do not publish or paste real protected forms, datasets, or internal identifiers into this repository.

## Expected Deliverables

- the active report path
- the canonical format specification summary
- the recommended fix layer
- the verification summary against the approved form
