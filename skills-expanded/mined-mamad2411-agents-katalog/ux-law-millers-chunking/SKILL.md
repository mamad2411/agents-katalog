---
name: ux-law-millers-chunking
description: Use when displaying a list of items, form fields, or steps that the user must hold in working memory — Miller's Law (average working memory holds about 7±2 chunks). Triggers on "long list of options", "how many items to show", "navigation with many links", "wizard step count".
allowed-tools: Read, Edit, Grep, Glob
---

# Miller's Law (7±2 chunks)

Working memory reliably holds only ~4-7 chunks at once. Don't design as if users can track more unaided.

## Rules of thumb
- Chunk related items into groups of ~5-7 rather than one long flat list (phone numbers, nav menus, form sections).
- For navigation, keep top-level items to ~7 or fewer; push overflow into submenus/categories.
- For multi-step flows, show a progress indicator so the user isn't relying on memory to track "which step am I on."
- Don't require the user to remember information from one screen to use on the next (e.g., a code shown on screen A, typed on screen B) — keep it visible or auto-fill it.

## Review checklist
1. Count top-level choices/items presented at once; if beyond ~7, chunk or paginate ([[list-pagination-required]]).
2. Check whether any flow depends on the user remembering something across screens.
