---
name: design-system
description: Design system and visual consistency — token tiers, typography, iconography, shared component API design, implementing Figma designs. Use when building shared/reusable UI components, defining tokens, type scales, or icon sets, or translating Figma/design mockups into code. 日本語の依頼例:「共通コンポーネント作って」「デザインシステム」「デザイントークン定義」「Figma通りに実装して」「アイコン整備」「タイポグラフィ設計」。
---

# Design System

## Token tiers — extend the scale, never bypass it

Builds on the active styling skill's token rules (`css-modules`: `tokens.css`; `tailwind`: the `@theme` block — both compile to CSS custom properties; no styling skill installed → keep tokens wherever the project already defines them). Structure tokens in tiers:

1. **Primitive**: raw values, never used directly in components (`--blue-600`, `--size-4`).
2. **Semantic**: meaning-bearing aliases components consume (`--color-action`, `--color-text-muted`, `--space-inline-md`).
3. **Component** (only when needed): `--button-height-md` referencing semantic tokens.

- Components consume semantic/component tokens only. A new design value means extending the scale deliberately — never a one-off raw value in a component module.
- Every new token gets a value for every theme (`[data-theme='dark']` etc.) at creation time; a token defined for light only is a bug.

## Typography

- One modular type scale as tokens (`--text-sm` … `--text-2xl`), sizes in `rem`, line-height unitless. No ad-hoc `font-size` values in components.
- Max line length for body text (`max-inline-size: 65ch` or a token).
- Fonts: prefer one variable font over many static weights; loading rules (framework loader, `woff2`, `font-display`, preload, subsetting) live in `images-media`.

## Iconography

- One icon system per repo: SVG-as-component (SVGR or framework equivalent), sized via tokens, colored via `currentColor` so icons inherit text color.
- Decorative icons: `aria-hidden="true"`. Icon-only buttons: `aria-label` (see `a11y`). Never mix icon libraries casually — adding a second icon set is a dependency decision.

## Shared component API

- Consistent vocabulary across all components: the same variant names (`variant`, `size` with the same scale `sm/md/lg`) mean the same thing everywhere. Don't invent `kind`/`appearance`/`type` synonyms per component.
- Shared components accept `className` (merged onto the root with `clsx`) and forward `ref`; spread remaining valid DOM props onto the root element so consumers can set `data-*`/`aria-*`.
- Inputs ship controlled AND uncontrolled support where native inputs do; document which.
- Every shared component has stories for all visual states (see `storybook`) — the catalog IS the design-system documentation.

## Implementing from Figma

- Figma values are intent, not law: map every color/space/radius/shadow to the nearest existing token. A value with no close token is a conversation (new token or designer adjustment), not a hardcoded pixel value copied from the inspect panel.
- Auto-layout maps to flex/grid + `gap` — don't transcribe absolute positions.
- Designs are drawn at one viewport in one state. Before calling it done, resolve what the mock doesn't show: responsive behavior, focus/hover/active, loading/error/empty, long text and overflow, keyboard interaction, dark theme.
- Match the design system's existing component before building new: if the mock looks 90% like `<Card>`, extend `<Card>`, don't fork it.
