---
name: css-canon
description: >
  Apply this skill whenever writing or editing CSS, Tailwind classes, or styling for React/web UIs — building
  layouts, components, pages, dashboards, forms, or theming a project. Trigger on: flexbox, grid, spacing,
  positioning, responsive design, shadcn/ui theming, design tokens, dark mode, or any time a UI needs structural
  or visual CSS, even for a single element. The goal is CSS that stays simple and maintainable: work top-down
  (theme → layout → component → element), lean on a token scale instead of magic numbers, use relative units so
  the UI scales and stays accessible, and write the fewest properties that produce the correct result. Use this
  to stop agents from producing over-engineered, hack-laden, hard-to-debug styling.
---

# CSS Architecture

The point of this skill is maintainability. Styling rots when it's built bottom-up out of one-off magic numbers and clever hacks: every component invents its own spacing, nothing scales together, and six months later nobody can touch the CSS without breaking something three screens away. The fix is to work in the same order a designer thinks — broad decisions first, details last — and to make those broad decisions *once*, as tokens, so the details have something consistent to reference.

## The workflow: build from the top down

Think of it as an inverted triangle. You start wide (decisions that affect everything) and narrow toward the specific. Each layer depends on the one above it, so doing them out of order means redoing work.

```
  ┌─────────────────────────────────────┐
  │  1. THEME / TOKENS                    │  colors, spacing scale, radii, type — set once
  │      ┌───────────────────────────┐   │
  │      │  2. LAYOUT                 │   │  page regions: header / sidebar / main / footer
  │      │      ┌─────────────────┐   │   │
  │      │      │  3. COMPONENT    │   │   │  internal structure of one card / form / list
  │      │      │   ┌─────────┐    │   │   │
  │      │      │   │ 4. ELEM  │    │   │   │  individual button / icon / text tweaks
  │      │      │   └─────────┘    │   │   │
  │      │      └─────────────────┘   │   │
  │      └───────────────────────────┘   │
  └─────────────────────────────────────┘
```

**Resist the urge to style the thing in front of you first.** If the request is "build a settings page," don't start by styling the save button. Confirm the tokens exist, block out the page regions, then the panel structure, then the button. Styling a leaf element before its container is set is how you end up fighting the layout with `!important` and negative margins later.

### Step 1 — Theme / tokens (do this first on any new project)

For a shadcn/ui project this is the theming step you already start with: the CSS variables in `globals.css` (`--background`, `--primary`, `--radius`, etc.) and the Tailwind theme. Get this right before building screens, because everything downstream references it.

What belongs here: the color palette (as CSS variables, with light/dark values), the spacing scale, border radii, and the type scale. The goal is that no component later needs a raw color or a random pixel value — it reaches for a token.

See `references/tokens.md` for the shadcn variable setup, a spacing scale, and how to wire it into Tailwind. Read it whenever you're setting up or extending a theme.

### Step 2 — Layout

Block out the page's major regions before touching what's inside them. This is one Grid or Flex container deciding where the header, sidebar, main, and footer go. Don't style the contents yet — just prove the skeleton holds.

### Step 3 — Component

Now the internal structure of a single unit — a card, a form, a list row. Again, structure before decoration: get the alignment and spacing of the parts right, then style them.

### Step 4 — Element

The leaves: a button's padding, an icon's size, a label's weight. By now everything around them is stable, so these changes stay local and don't ripple.

Steps 2–4 are all "structural CSS" and share one rule set — see **Layout rules** below and `references/layout-patterns.md` for copy-ready snippets.

---

## Sizing & units: relative, not fixed

Fixed pixels break accessibility. When a user bumps their browser's base font size (a common, legitimate accommodation), `px` values ignore it and the layout doesn't scale. `rem`/`em` respect it. So:

- **Type and spacing → `rem`** (or the Tailwind scale, which is rem under the hood). `gap`, `padding`, `margin`, `font-size`, `width`/`max-width` of content containers.
- **Borders and hairlines → `px` is fine.** A `1px` border is meant to be one crisp device pixel; scaling it with font size makes it blurry or chunky. `1px`/`2px` borders, ring widths, and the like are the intended exception.
- **Avoid arbitrary Tailwind values** like `p-[13px]` or `text-[15px]`. They're the utility-class version of a magic number. Use a scale step (`p-3`, `text-sm`). If nothing on the scale fits, that's usually a sign the scale needs a token, not that this one element needs an exception.

Quick test: if you're typing a pixel number that isn't a border, stop and reach for a scale step or token instead.

---

## Spacing: one scale, consistently

Inconsistent spacing is the most visible symptom of bottom-up CSS — `gap: 1rem` here, `gap: 14px` there, `margin: 18px` somewhere else. Pick the scale (Tailwind's default `0.25rem` step is fine) and use only its steps. Beyond consistency:

- Space **inside** a flex/grid container with `gap`, not margins on children. One declaration on the parent beats N margins that you have to keep in sync.
- Space **between** independent components with `margin`.
- Space **within** a component (breathing room around its content) with `padding`.
- Don't stack `margin` + `padding` + `gap` on one element unless each is doing a genuinely distinct job.

---

## Layout rules (structural CSS for steps 2–4)

**Use the minimum properties that produce the correct result.** Identify what the layout must *do* (align, stack, space, contain, overlap, scroll), pick the single best tool, write only what's needed.

| Need | Use |
|------|-----|
| Align items in a row or column | flexbox |
| Two-dimensional grid (rows + columns) | CSS Grid |
| Child placed relative to a parent | `position: absolute` on child + `position: relative` on parent |
| Element pinned to viewport | `position: fixed` |
| Scrolls with page, sticks at an edge | `position: sticky` |
| Normal-flow spacing | `margin` / `padding` / `gap` |
| Overlapping elements | `position: absolute` + `z-index` |

**Don't combine tools to solve one problem.** If flexbox centers it, don't also add a float or an absolute position. One layout problem, one tool.

Prefer **intrinsic responsiveness** (`flex-wrap`, `grid-template-columns: repeat(auto-fit, minmax(...))`) over media queries; add a breakpoint only when intrinsic sizing genuinely can't express the change. One breakpoint per layout change.

For the full set of copy-ready patterns (centering, sidebar+main, card grids, sticky headers, modals, footer-to-bottom) and the anti-pattern list, read `references/layout-patterns.md`.

---

## Accessibility (build it in, don't bolt it on)

These are cheap if done as you go and expensive to retrofit:

- **Semantic HTML first.** A `<button>` is a button; a clickable `<div>` is a bug. Real elements come with keyboard and screen-reader behavior for free — reaching for ARIA usually means you picked the wrong element.
- **Visible focus states.** Never `outline: none` without a replacement. Keyboard users navigate by the focus ring; removing it strands them. shadcn's `focus-visible:ring-*` is the right pattern.
- **Color contrast.** Body text aims for WCAG AA (4.5:1). Don't encode meaning in color alone (add an icon or label).
- **Hit targets** of roughly `2.75rem` (~44px) for touch controls.
- **Respect `prefers-reduced-motion`.** Wrap non-essential animation/transitions so they're reduced or removed for users who ask for it:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
  }
  ```
- **Keyboard navigation** must reach and operate every interactive element in a sensible order. Manage focus for overlays/modals.
- **ARIA only when semantics can't carry it** — custom widgets (tabs, comboboxes, dialogs without `<dialog>`). For anything shadcn/Radix provides, the accessibility is already wired; don't re-add it.

---

## Before you finish, check

- [ ] Did I work top-down (tokens → layout → component → element), not start at the leaf?
- [ ] Does every color/space/radius come from a token or scale step — no raw hex, no `[13px]`?
- [ ] Type and spacing in `rem`/scale; only borders/hairlines in `px`?
- [ ] One layout tool per problem, only the properties this element needs?
- [ ] `gap` inside containers, `margin` between components, `padding` within?
- [ ] Semantic elements, visible focus, AA contrast, reduced-motion handled?
