---
name: no-duplicate-ui
description: Scans Vue files for duplicate component names and similar template overlap. Use during PR review or when refactoring UI to enforce DRY architecture.
paths:
  - "**/*.vue"
---


# No Duplicate UI

## When to use

- PR adds a new Button/Card wrapper similar to existing ones
- Refactoring to consolidate forked components
- Pre-merge gate optional duplicate scan

## Instructions

1. Run `python scripts/find_duplicate_ui.py --project-root <root>`.
2. Review pairs with high template similarity or matching filenames.
3. Consolidate into shared components under `@/components/ui/`.
