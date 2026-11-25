---
name: schema-author
description: Evolve the local brain schema or page-type conventions when the current taxonomy cannot describe the material cleanly.
---

# Schema Author

Use this skill when the brain needs a new page type, folder convention, alias, or schema rule.

This is the local Codex adaptation of upstream GBrain's schema-pack authoring workflow. It keeps the current repo's lightweight file-backed conventions while leaving room for a future upstream `gbrain schema` integration.

## Workflow

1. Establish the current schema source:
   - inspect `brain/README.md`
   - inspect existing `brain/` folders and representative pages
   - if `gbrain` exists, read active schema status with read-only schema commands
2. Diagnose the gap:
   - untyped pages
   - overloaded folder
   - new domain entity
   - ambiguous relationship type
   - missing source or citation convention
3. Propose the smallest schema change:
   - a new page type
   - an alias
   - a folder prefix
   - a frontmatter field
   - a validation rule
4. Update docs or validation only after the proposed convention is clear.
5. Hand back to `brain-taxonomist` for future writes.

## Guardrails

- Do not add schema complexity for a one-off note.
- Do not rewrite the corpus as part of schema authoring unless explicitly requested.
- Keep local schema docs compatible with existing helper scripts.
