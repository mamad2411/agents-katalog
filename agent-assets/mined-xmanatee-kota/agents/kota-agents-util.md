# Util

Shared infrastructure utilities used across core and modules.

- JSON file I/O with atomic writes and typed errors.
- Keep lightweight legacy schema checks separate from explicit dialect validation.
  Network schema references are never fetched implicitly. Synchronous dialect
  compilation and validation need execution deadlines: serialized schema size
  does not bound reference expansion or regular-expression work.
- Frontmatter parsing and serialization.
- Git worktree status and head SHA helpers.
- Log formatting (text and JSON modes).
- Path scope validation for scoped searches.

Keep utilities small, pure where possible, and free of domain-specific logic.
Do not add domain-specific tools, workflow helpers, or module-owned code here.
