---
name: css-modules
description: CSS Modules and styling conventions — design tokens, naming, variants, responsive design, layout, dark mode/theming. Use when styling or visually adjusting components, or editing any *.module.css, tokens, or global styles. For animations/transitions/motion use the `motion` skill instead. 日本語の依頼例:「スタイルを当てて」「見た目を整えて」「デザイン調整」「ダークモード」「レスポンシブ対応」「CSS書いて」。
---

# CSS Modules

## Files & naming

- One module per component, colocated: `UserCard.tsx` + `UserCard.module.css`.
- Class names: camelCase (`primaryButton`, not `primary-button`) — enables `styles.primaryButton` without bracket access.
- Name by role, not appearance: `.errorMessage` not `.redText`. The module scope already namespaces — no BEM prefixes needed.
- Import as `styles`: `import styles from './UserCard.module.css'`.

## Design tokens — single source of truth

- All colors, spacing, radii, shadows, typography, z-index live as CSS custom properties in `src/styles/tokens.css`, defined on `:root`.
- Component modules consume tokens only — the semantic/component tier where tiers exist (see `design-system`), never primitives like `--blue-600`. A raw hex/px value for a themable property in a component module is a bug.
- Spacing on a scale (`--space-1` … `--space-8`); z-index from a fixed ladder (`--z-dropdown`, `--z-modal`, `--z-toast`) — never `z-index: 9999`.
- Theming (dark mode) by redefining tokens — components never branch on theme themselves. Default to `prefers-color-scheme`; add `[data-theme]` only when a user-facing toggle is required, set pre-paint by a tiny inline script (CSP nonce applies — see `frontend-security`) to avoid a wrong-theme flash.

## Variants & state

- Variants via data attributes, not class string concatenation:

```tsx
<button className={styles.button} data-variant={variant} data-size={size}>
```

```css
.button[data-variant='danger'] { background: var(--color-danger); }
```

- Boolean UI state the same way (`data-open`, `aria-expanded`) — style off ARIA attributes when one exists: `.menu[aria-expanded='true']`.
- `clsx` has exactly one job here: merging a consumer-passed `className` prop with the base class. Enumerated variants and boolean state always go through data attributes, never conditional class lists; a component wanting 3+ conditional classes should be restructured into variants.

## Layout & responsive

- Mobile-first: base styles, then `@media (min-width: …)` upward. Breakpoints documented once in `tokens.css` comments (custom properties don't work in media queries — keep the canonical list there).
- Prefer modern layout primitives: flex `gap` / grid over margin hacks; `aspect-ratio`; container queries for components that adapt to their container, media queries only for page-level layout.
- Aspect-preserving media: give the box a defined `aspect-ratio` and use `object-fit: contain`/`cover`. Never size an image with `max-width`/`max-height` inside a flex item — the main-axis shrink sizes width independently of the height cap and stretches the image (a mixed-aspect-ratio thumbnail grid is where this bites).
- Logical properties (`margin-inline`, `padding-block`, `inset-inline-start`) over physical ones — free RTL support (the foundation the `i18n` skill builds on).
- No fixed heights on text containers; min-height if needed.

## Globals — the only allowed global CSS

`src/styles/` contains exactly: `tokens.css`, `reset.css`, `globals.css` (base element styles: body, headings, links). Nothing else is global. No `:global()` in component modules except to target third-party library DOM you don't control — with a comment saying which library.

In Astro projects, the per-component styling primitive is the single-file scoped `<style>` block instead of `*.module.css` — see `astro`. The token/naming/variant rules here still apply.

## Motion

- Animate `transform` and `opacity` only (compositor-friendly); never animate `width/height/top/left` for transitions.
- Every significant animation (anything beyond a subtle hover/focus transition) respects `@media (prefers-reduced-motion: reduce)` — same threshold as the `a11y` skill.
- Durations/easings as tokens (`--duration-fast`, `--ease-out`).
- These are the invariants only — escalation (keyframes / WAAPI / animation libraries), View Transitions, entrance/exit animations, and scroll effects live in the `motion` skill.

## Enforcement

The token/`var()` and class-naming rules above are machine-enforced by Stylelint — see `tooling` for the exact rules and the shipped `templates/stylelint.config.mjs`.
