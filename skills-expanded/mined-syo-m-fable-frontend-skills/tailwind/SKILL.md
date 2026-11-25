---
name: tailwind
description: Tailwind CSS (v4) conventions — @theme design tokens, class ordering, variants, dark mode, responsive/container queries, when NOT to use arbitrary values. Use when styling or visually adjusting components with utility classes, or editing global CSS/@theme in a Tailwind project. For animations/transitions/motion use the `motion` skill instead. 日本語の依頼例:「スタイルを当てて」「見た目を整えて」「デザイン調整」「Tailwindで」「ダークモード」「レスポンシブ対応」。
---

# Tailwind CSS (v4)

Assumes Tailwind v4: CSS-first configuration — `@import "tailwindcss"` and design tokens declared
with `@theme` in CSS. `tailwind.config.js` is the legacy v3 mechanism; do not add one to a v4
project (check the installed major before assuming either way).

## Design tokens

- Tokens live in `@theme` (colors, spacing, radii, fonts, breakpoints) — ONE file, the single
  source of truth. `@theme` variables compile to CSS custom properties, so non-Tailwind CSS can
  consume the same tokens via `var(--color-…)`.
- A raw value appearing twice is a token that hasn't been promoted yet. Never scatter arbitrary
  values (`p-[13px]`, `text-[#3366ff]`) for recurring design decisions — add the token to `@theme`
  and use the generated utility. Arbitrary values are for genuine one-offs only.

## Classes in markup

- **No dynamic class concatenation**: `` `text-${color}-500` `` produces classes the compiler
  never sees — silently unstyled. Write full class names; branch with `clsx`/`cva` over complete
  strings (`isError ? 'text-red-600' : 'text-gray-900'`).
- Class order is machine-enforced by `prettier-plugin-tailwindcss` — install it and stop thinking
  about order. Don't hand-sort.
- Long class lists are a smell of a missing component, not a missing `@apply`. Extract a React
  component (variants via `cva`); reach for `@apply` only in small, justified doses (e.g. styling
  third-party markup you don't control).
- State styling: prefer `aria-*` and `data-*` variants (`aria-expanded:rotate-180`,
  `data-[state=open]:…`) — they force the markup to carry real semantics (pairs with `a11y`).

## Responsive & dark mode

- Mobile-first: unprefixed = smallest; add `sm: md: lg:` upward. Component-level responsiveness
  uses container queries (`@container` + `@sm:` variants), not viewport breakpoints.
- Dark mode: pick ONE strategy for the project (media `dark:` default, or class/data-attribute
  strategy declared via `@custom-variant`) and document it in the `@theme` file. Tokens that
  change with theme are defined once as CSS variables, not re-specified per-utility everywhere.

## Boundaries

- Do not mix styling systems: no CSS Modules, no CSS-in-JS, no inline `style` attributes
  (dynamic values that must be inline — e.g. computed positions — go through a CSS variable:
  `style={{ '--x': … }}` consumed by `[--x]`-based utilities or plain CSS).
- Escape hatch for genuinely un-utility-able CSS (complex keyframes, third-party overrides):
  one co-located `.css` file layered with `@layer components`, consuming `@theme` tokens.
- `prefers-reduced-motion`: gate animation utilities with `motion-safe:`/`motion-reduce:`
  (see `motion` for what to animate at all).

## Enforcement

- `prettier-plugin-tailwindcss` (class order) is the one mandatory tool.
- Lint plugins for Tailwind v4 vary in maturity — verify current v4 support before adding one
  (see `tooling`'s "verify the installed major" doctrine); do not assume the v3-era plugin works.
