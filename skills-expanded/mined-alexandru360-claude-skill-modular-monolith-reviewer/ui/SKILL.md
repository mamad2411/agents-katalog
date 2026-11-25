---
name: ui
description: >-
  LEGO CONNECT Design System architecture and UI implementation guidance.
  Use when: designing component APIs, extending CONNECT primitives, implementing themed UI,
  auditing token usage, planning component migration, or building new feature UI.
  Covers: token strategy, data-mode theming, Tailwind v4 integration, component composition,
  accessibility, FDA boundary compliance, and adoption planning.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
model: sonnet
version: 1.0
---

# UI — CONNECT Design System Architecture Skill

## Role

Senior Design System Architect specializat in React, TypeScript, TailwindCSS v4, LEGO CONNECT Design System v3 (`@lego/connect-components-react`), Feature-Driven Architecture, accessibility-first UI foundations, `data-mode` scoped theming, `--ds-*` CSS custom properties.

## Objective

Proiecteaza si implementeaza UI consistent, extensibil, tipat, accesibil si usor de intretinut in BI-Layouter — folosind exclusiv `--ds-*` semantic tokens, Tailwind v4 semantic utilities, `data-mode` theming, si boundary rules impuse de `eslint-plugin-boundaries`.

## Reference Loading

Before answering, load relevant CONNECT references from `.agents/skills/connect-design-system/references/`:
- `core-tokens.md` — all `--ds-*` token definitions
- `core-theming.md` — data-mode setup, Tailwind v4 integration
- `core-setup.md` — package installation and configuration
- `feature-*.md` — specific component API when discussing that component

## Architecture Layers

```
--ds-* tokens (CSS custom properties from @lego/connect-theme-enterprise)
  └─ data-mode theming (light/dark + compact/touch/default + brand/legacy)
      └─ CONNECT primitives (@lego/connect-components-react)
          └─ shared patterns (src/components/)
              └─ feature components (src/features/<name>/)
```

Dependency direction is strictly top-down. `eslint-plugin-boundaries` enforces feature isolation.

## Token Strategy

All tokens use `--ds-` prefix. Tailwind v4 strips `ds-` for utility classes.

### Color Tokens

| Category | CSS Variable Pattern | Tailwind Utility |
|----------|---------------------|-----------------|
| Foreground | `--ds-color-content-*` | `text-content-*` |
| Controls | `--ds-color-interactive-{intent}-{state}` | `bg-interactive-*` |
| Backgrounds | `--ds-color-surface-*` | `bg-surface-*` |
| Borders | `--ds-color-stroke-*` | `border-stroke-*` |
| Status | `--ds-color-support-{intent}-{variant}` | `text-support-*`, `bg-support-*` |

### Layout Tokens

| Token | Scale | Note |
|-------|-------|------|
| `--ds-layout-spacing-*` | 0–600 | Numeric suffix is scale index, NOT px |
| `--ds-layout-size-*` | 100–400 | Density-aware (compact/touch) |

### Tailwind v4 Setup (import order matters)

```css
@import "tailwindcss";
@import '@lego/connect-theme-enterprise/css/color';
@import '@lego/connect-theme-enterprise/tailwindcss/color';
```

### FORBIDDEN

- `bg-blue-500`, `text-white`, any raw Tailwind color
- Hardcoded hex/rgb/hsl values in components
- Treating token scale suffix as pixel value (spacing-100 = 8px, NOT 100px)

## Theming Strategy

### Color Modes
- `data-mode="light"` — force light
- `data-mode="dark"` — force dark
- No attribute — follows OS `prefers-color-scheme`

### Density Modes (independent, nestable with color)
- `data-mode="default"` — standard spacing
- `data-mode="compact"` — reduced spacing for data-dense UIs
- `data-mode="touch"` — enlarged touch targets

### Font Modes
- `data-mode="brand"` — LEGO Typewell
- `data-mode="legacy"` — Cera Pro

### Rules
- NO ThemeProvider, NO CSS-in-JS
- Innermost `data-mode` wins when nested
- Color + density modes are independent and composable

## Component Strategy

### CONNECT-First Policy

Use CONNECT components directly when available. Full list:
`Button`, `TextField`, `Checkbox`, `RadioButton`, `Toggle*`, `Dropdown*`, `Table*`, `Badge`, `Card`, `Modal`, `Drawer`, `Popover`, `Tooltip`, `Toggletip`, `Toast`, `ContentSwitcher`, `Menu`, `Breadcrumb`, `Pagination`, `ProgressBar`, `ProgressCircle`, `InlineAlert`, `Image`, `Tag`, `TextLink`, `UtilityButton`, `Divider`, `Avatar`, `Label`, `HelpText`, `Overlay`, `CharCount*`

(*) = experimental — wrap with isolation layer for API stability.

### Custom Component Rules

- `Readonly<Props>` mandatory on all props interfaces
- Named exports only (no default exports)
- CVA for variant systems + `clsx` + `tailwind-merge`
- `className` escape hatch: allowed but documented
- No polymorphic APIs unless proven necessary (YAGNI)

### Wrapper Policy

Create a wrapper ONLY when:
1. Adding project-specific default props consistently
2. Isolating experimental CONNECT API instability
3. Composing multiple CONNECT components into a reusable pattern
4. Adding feature-specific behavior (e.g., analytics tracking)

Do NOT wrap just to "own" the component or add a re-export layer.

## Accessibility Strategy

- CONNECT components provide a11y foundation (focus, keyboard, ARIA)
- Use `<Label>`, `<HelpText>`, `<InlineAlert>` from CONNECT for form patterns
- Semantic HTML first — ARIA only when no native equivalent exists
- Verify color contrast in BOTH light and dark modes
- Test density modes (compact reduces spacing — ensure touch targets remain adequate)
- Respect `prefers-reduced-motion` for animations

## FDA Boundary Rules

- Features in `src/features/<name>/` MUST NOT import other features
- Cross-feature communication via Redux only
- Shared UI goes in `src/components/` (importable by all features)
- Shared hooks go in `src/hooks/`
- `eslint-plugin-boundaries` enforces at lint time

## Code Conventions

- No `console.log` or `console.warn` — use `console.debug` guarded by `if (import.meta.env.DEV)`
- No `as` casts inline — write type guards
- No `any` — use `unknown` + narrowing
- No default exports
- Props wrapped in `Readonly<>`
- File naming: UpperCamelCase for components, lowerCamelCase for utilities

## Quality Gates

Run before marking work as done:
```bash
pnpm typecheck
pnpm lint
pnpm test
```

## Anti-Patterns

| Anti-pattern | Fix |
|-------------|-----|
| `bg-blue-500` or `text-white` | Use `bg-interactive-primary-enabled`, `text-content-on-primary` |
| Hardcoded `#1a1a1a` | Use `--ds-color-surface-*` via Tailwind semantic class |
| Giant Button wrapper adding no value | Use CONNECT `<Button>` directly |
| Custom dropdown ignoring CONNECT `<Dropdown>` | Use experimental Dropdown + isolation wrapper |
| `spacing-100` treated as 100px | It's 8px — read token scale docs |
| Inline `as Record<string, unknown>` | Extract a type guard function |
| Cross-feature import | Move to `src/components/` or communicate via Redux |
| `ThemeProvider` or styled-components theming | Use `data-mode` attribute |
| Multiple `useStore(s => s.field)` calls | Use `useShallow` from `zustand/react/shallow` |

## Trade-Offs Guide

| Decision | Option A | Option B | When to pick A |
|----------|----------|----------|----------------|
| Token access | CSS variables (`--ds-*`) | Tailwind utilities | Need JS runtime access or non-Tailwind context |
| Component | CONNECT directly | Custom wrapper | Always prefer A unless wrapper criteria met |
| Experimental | CONNECT experimental | Fully custom | A with isolation layer unless CONNECT is severely broken |
| API strictness | Strict typed props | Flexible escape hatches | Default to strict; add escape hatch only after 3+ use cases demand it |
| Scope | Feature-scoped | Shared (`src/components/`) | A until 2+ features need it |

## Maturity Checklist

- [ ] `pnpm typecheck` passes
- [ ] `pnpm lint` passes (including boundaries)
- [ ] `pnpm test` passes
- [ ] Zero raw Tailwind colors in codebase
- [ ] Zero hardcoded hex/rgb/hsl in components
- [ ] All `data-mode` variants verified (light/dark x default/compact/touch)
- [ ] Experimental CONNECT components wrapped with isolation layer
- [ ] `Readonly<Props>` on all custom component interfaces
- [ ] Named exports only (no default exports)
- [ ] Colocated stories for all shared components (`*.stories.tsx`)
