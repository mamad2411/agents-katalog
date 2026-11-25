---
name: koreforge-docs-standard
description: "Use when creating, renaming, classifying, reviewing, or standardizing KoreForge documentation: specification, detailed design, user guide, developer guide, structure, notes, documentation inventory, or skills docs."
---

# KoreForge Documentation Standard

Use this skill whenever adding or reorganizing durable documentation.

## Standard Types

Use these document types:

1. Specification
2. Detailed design
3. User guide
4. Developer guide
5. Structure
6. Deeper explanation notes, only when complexity justifies them

## Inspect First

1. `docs/README.md`.
2. `docs/ecosystem/documentation-standard.md`.
3. `docs/ecosystem/documentation-inventory.md`.
4. The target repo `README.md` and `doc/` or `docs/` folder.

## Canonical Child Repo Layout

```text
README.md
LICENSE.md
doc/
  specification.md
  detailed-design.md
  user-guide.md
  developer-guide.md
  structure.md
  notes/<topic>.md
```

Not every repo needs every file.

## Writing Rules

- Make `README.md` the entry point.
- Keep durable docs checked in under `doc/` for child repos.
- Keep generated reports under `artifacts/`, not `doc/`.
- Classify legacy docs before moving them.
- Rename legacy docs to canonical names when touching that repo for real work.
- Update links when files move.
- Update `documentation-inventory.md` when adding, removing, or reclassifying docs.

## Validation

- New docs fit one standard type.
- Links to moved docs still resolve.
- No generated docs or reports are checked in unless intentionally treated as durable API reference.
- The root docs index links to new workspace-level docs.

## Avoid

- Creating new categories for one-off thoughts.
- Adding vague documents like `misc.md` or `notes.md` without a topic.
- Duplicating another repo's docs into an app unless the content is intentionally vendored as template output. In normal repos, link instead of copy.
