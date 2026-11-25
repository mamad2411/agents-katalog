---
name: boxel-ui-guidelines
description: Use when IMPLEMENTING or REVIEWING UI in Boxel templates (writing a template, or reviewing a change, diff or pull request that touches one) — applying var(--*) theme tokens in <style scoped>, choosing between @fields and @model, using Pret UI components (Button, Chip, Avatar, Select) and the boxel-ui components Pret UI does not have yet (FittedCard, KanbanPlane, FilterList), controlling embedded-card chrome, or fixing layout/overflow issues. This is the template-implementation layer. Visual-language decisions belong to boxel-design; the Theme card artifact itself belongs to boxel-theme-development.
boxel:
  kind: skill
---

# Boxel UI Guidelines

_Ensures Pret UI components (and boxel-ui where Pret UI has no equivalent) are used in templates and theming guidelines are followed_

You are a Boxel UI specialist. Whenever you write or review GTS templates and card definitions, you must follow these guidelines:

## Pair with

- **`boxel`** — for the underlying CardDef/FieldDef and `@fields` vs `@model` rules.
- **`boxel-design`** — for the visual decisions these templates implement.
- **`source-code-editing`** — for the actual template edits.

## Don't use for

- Visual design choices (color, mood, typography) — that's `boxel-design`.
- Field schema decisions (`contains` vs `linksTo`) — that's `boxel`.

---

## Sections (load on demand)

- `references/theme-token-contract.md` — The single inventory of every theme token (colors, typography roles, spacing, radius, shadows) and how the contract behaves at card boundaries. Other skills point here instead of listing tokens.
- `references/use-boxel-design-tokens-for-theming.md` — Use Boxel Design Tokens for Theming: fallback rule, spacing/typography options, the color-pairing rules (`--*` tokens paint, `--*-foreground` writes), the list of contrast pairings the theme guarantees, and why a component that opts out of the theme uses its own `--prefix-*` constants instead of reassigning contract token names.
- `references/font-loading-theme-card-owns-imports.md` — Font Loading — Theme Card Owns Imports
- `references/field-rendering-fields-vs-model.md` — Field Rendering: @fields vs @model
- `references/template-patterns.md` — Template Patterns. Includes the entrance-animation invisibility trap and keyed single-item `{{#each}}` remounting when an animation must replay after tracked state changes.
- `references/print-and-published-output.md` — Multi-page host-mode printing, ancestor unclipping, SVG semantic marks, cross-browser fill rules, and PDF verification.
- `references/use-container-queries-not-viewport-units.md` — Use Container Queries, Not Viewport Units
- `references/prevent-content-overflow.md` — Prevent Content Overflow
- `references/prefer-component-apis-write-new-components-when-needed.md` — Prefer Component APIs; Write New Components When Needed
- `references/use-boxel-ui-components.md` — Use Pret UI components first, with the boxel-ui-to-Pret UI replacement table; boxel-ui only for components Pret UI does not have yet
- `references/style-budget.md` — Style budget — keep `<style>` blocks ≤40% of file, deduplicate across formats
- **`references/delegated-render-control.md`** — How the host wraps `<@fields.X @format='...' />` chrome (CardContainer + field-component classes) and how the parent shapes it via the theme cascade, a `class` on the field, or `@displayContainer={{false}}` — not `:deep()`. **Critical reading when embedding child cards in a parent that has its own design language.** Covers:
  - **Divider strategy is binary** — parent draws lines (AND passes `@displayContainer={{false}}` on the items), OR child halo IS the boundary (no parent borders). Both at once = "drop shadow fighting a thin border."
  - **Picking the format** — fitted vs embedded by who owns the cell size (the most common rendering bug is fitted-with-short-content leaving empty box space).
  - **Plural-field wrapper trap** — the one-tag render inserts `.plural-field` + per-item wrappers between your grid and the cards; loop `{{#each @fields.plural as |Item|}}<Item class='…' />{{/each}}` instead, so the classed cards are the grid's children.
  - **Atom alignment & surfaces** — `class` on the atom field for baseline/padding; `@displayContainer={{false}}` for plain inherited-color text, or a classed chip recolored to match the surface.
  - **Stagger animations** — `:nth-child` on the looped, classed cards sets `--stagger-d`; `animation-delay` reads it.
  - **Embedded MarkdownDef preview** — MarkdownDef uses the shared FileDef shells; tune the renderer with the `--md-preview-background` / `--md-preview-foreground` / `--md-preview-padding` custom properties. A framework-driven embedded render takes no component args, so an inherited custom property is the cross-boundary lever.
  - Embedded grids, isolated previews, corners (the wrapper follows the theme's `--radius`; the interact ring copies the CardContainer's radius, so a one-off change goes on the field's class and nowhere else), and what NOT to override (child container queries, fitted's width/height, wrapper `overflow`).
  - The child-side contract — what every format MUST NOT decorate on its outermost element.
- **`references/ui-review-procedure.md`** — The ordered procedure for reviewing or updating a template's UI: grep the mechanical tells, fix the theme posture, then colors, typography, spacing, geometry, child-card chrome, components, markup, and verify. Run it whole on every UI review; the checklist is its final tick list.
- `references/checklist.md` — Checklist
