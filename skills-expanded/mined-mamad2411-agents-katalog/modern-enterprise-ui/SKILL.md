---
name: modern-enterprise-ui
description: "Look-and-feel playbook for modern, data-dense enterprise application screens — admin worklists, data grids, filter bars, pagers, forms, side navigation — including CSS-only restyling of legacy ASP.NET WebForms/GridView pages. Owns layout, density, hierarchy and interaction. Use when asked to restyle or modernise a screen (\"looks 2010\"), or to design a data grid, worklist, admin screen, filter row, pager, dense table, sidebar or legacy WebForms UI."
user-invocable: true
---

# Modern enterprise UI - look and feel

**Division of labour:**
- Colours and type come from the owning project's tokens (e.g.
  `_mockups/tokens/`, `_memory/conventions.md`) when it has them; a project
  with none sets its own palette and keeps it consistent. Hold the WCAG AA
  contrast floor (≥4.5:1 body text) regardless of source.
- **This skill decides how the screen is shaped:** hierarchy, density, spacing,
  component shapes, states, and the CSS techniques that make it work on legacy
  markup. Pair it with `frontend-design` when a screen needs a distinctive
  direction rather than a solid default.

Read `references/enterprise-screen-principles.md` for the design rules and
`references/legacy-webforms-css.md` before touching any GridView / master-page
based portal. Both are short.

## Workflow

1. **Tokens first.** Read the owning project's token files (or its
   conventions) — palette, type scale, contrast floor. Everything below is
   drawn in those; if none exist, define the palette once and reuse it.
2. **Measure the screen you are changing** - in the DOM, not a screenshot:
   row heights, column widths, container width, overflow. Write the numbers
   down; they are the before.
3. **Decide the density tier** (see principles): Worklist / Form / Dashboard.
   Enterprise users scan hundreds of rows; density is a feature, not a
   compromise.
4. **Apply the grid recipe** (principles, section 3): underline not box, one
   strong header rule, hairline rows, tint zebra, mono for tabular figures,
   worded status, quiet filter row, pager as chrome, full-width card.
5. **Budget the width.** Count columns x min content + padding. If it does not
   fit the container, fix layout with column proportions - never by shrinking
   padding below 6px or the type below 12.5px.
6. **States.** Hover, focus-visible, selected, disabled, empty, loading, error.
   A grid with no empty state and no focus ring is not finished.
7. **Verify against the DOM again** - the after. Show both numbers in the
   hand-off. Overflow must be zero; every colour must trace to a token.
8. **On legacy portals,** every selector passes the nested-table test in
   `legacy-webforms-css.md` before it ships.

## What "modern" means here (and what it does not)

Modern = clear hierarchy, generous but disciplined whitespace, one accent used
sparingly, underlines and tints instead of boxes and fills, consistent 8px
rhythm, obvious interactive affordances, fast to scan.

Modern is **not** = rounded everything, gradients, shadows on every element,
oversized type, cards inside cards, icons for their own sake, or whitespace
that costs rows. On an operations screen those read as decoration and slow
the user down.

## Hand-off

State: density tier chosen, before/after DOM numbers, every deviation from the
project's token set and why, and every colour used with its token name.
Anything not measured this session is tagged UNVERIFIED.
