---
name: maintain-design-system-page
description: How to build and keep current the /design-system page (the in-site component catalog) and its sibling /brand-kit page on any Astro Knots site — the replacement for Storybook. Use when a site has no /design-system page yet; whenever a component is created, changed, given a variant, or extracted from a spike; when refactoring a spike into components; when knot-check reports uncatalogued components; or when the user mentions "design system page", "component catalog", "brand kit", or "Storybook". Encodes the two pages' scopes, the required entry for each component, the theme and mode contract, noindex, the same-change rule, and how to catch up a catalog that has drifted.
---

# Maintain the design system page

Every Astro Knots site ships two internal reference pages instead of Storybook:

| | `/brand-kit` | `/design-system` |
|---|---|---|
| For | Stakeholders, client marketing | Developers and agents |
| Answers | "What does this brand look and feel like?" | "What component do I use, and how?" |
| Changes | Rarely, when the brand evolves | With every component |

They render components in the site's real theme, modes, fonts and layout, so
the catalog can't drift from production the way a separate tool does. The
reasoning and full contract are in the astro-knots blueprint
`Maintain-Design-System-and-Brandkit-Motions`. This skill is the procedure.

## The rule that keeps it alive

**A component change and its catalog entry land in the same change.** New
component, new variant, new prop, a component extracted from a spike: the
`/design-system` entry is updated in the same commit, never "later".

Brand changes (a new token, font or mark) go to `/brand-kit` **first**, then
to the rest of the site.

## Setting it up (when it's missing)

- `src/pages/design-system/index.astro` (rename a legacy
  `component-library.astro` to this when you touch it), and
  `src/pages/brand-kit/index.astro`.
- Both use the site's base theme layout, show the **theme and mode toggle at
  the top**, render correctly in light, dark and vibrant, and emit
  `<meta name="robots" content="noindex, nofollow">`.
- Not linked from public navigation. Nothing confidential on them: assume the
  URL gets shared by accident.
- When the index gets long, split into sub-pages by family
  (`src/pages/design-system/cards.astro`, `.../people.astro`) and keep the
  index as a linked table of contents. `sites/dark-matter` is the reference
  for sub-page granularity.

## One entry per component (or family)

1. **Name** and one line on what it's for.
2. **Live render**, using the real component with realistic content, not a
   mock wrapper.
3. **Variants** side by side: every meaningful prop combination.
4. **Props**: name, type, default, one-line meaning.
5. **CSS contract**: the semantic tokens it reads (`--color-*`, `--fx-*`) and
   any required ancestor (`[data-mode]`, a theme class).
6. **Usage**: a short import-and-use code block.
7. **Accessibility**, only when non-trivial: keyboard, ARIA, focus.

`/brand-kit` carries: color tokens (named and semantic, all three modes),
typography at each scale, brand marks in light and dark, illustration style,
and signature layouts such as hero variants.

## Catching up a catalog that has drifted

Most sites have more components than catalog entries. To catch up:

1. Run `knot-check components` (from the Astro Knots plugin, or
   `pnpm dlx --package=github:lossless-group/astro-knots-mcp knot-check components .`).
   It lists components no design-system page mentions, and open `@spike` files.
2. Group the list into families, most-used first.
3. Add entries a family at a time; a stub entry (name, purpose, live render,
   link to the source) beats no entry. Fill in props and CSS contract next.
4. Delete components nothing uses instead of cataloging them.

## The theme is part of the design system

The catalog shows components; `/brand-kit` shows the theme they're built on
(named and semantic tokens in all three modes, type scale, effects). Both
drift the same way: a spike hard-codes colors and fonts, ships, and the theme
no longer describes the site. When cataloging a component, check that it
reads only semantic tokens; when a value has no token yet, add it to
`theme.css` and `/brand-kit` rather than to the component.

## Checks

- Every component in `src/components/` is mentioned on a `/design-system`
  page (`knot-check components`).
- No raw colors or fonts outside the theme files (`knot-check components`
  reports them as `raw-design-value`).
- The page renders in all three modes without anything unreadable or broken.
  A component that looks wrong in a mode is a bug in the component; the
  catalog's job is to make it visible.
- `noindex, nofollow` is present on both pages.

Related: `spike-then-refactor-into-components` (where most new catalog
entries come from), `theme-system`, `maintain-design-md` (the written
contract the catalog renders).
