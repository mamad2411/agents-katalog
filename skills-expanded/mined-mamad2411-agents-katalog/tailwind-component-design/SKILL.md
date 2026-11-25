---
name: tailwind-component-design
description: Use when designing or reviewing TailwindCSS component patterns — covering utility composition, responsive design, dark mode, design tokens, Headless UI integration, and accessibility.
---

# TailwindCSS Component Design

## Specialization

Provide expert-level guidance for designing and reviewing TailwindCSS component patterns across utility composition, responsive breakpoints, dark mode, design tokens, Headless UI integration, class ordering, and WCAG-aligned accessibility.

This skill covers component-level design patterns. Build pipeline and project setup is handled by `tailwind-setup`. Quality gate review of a completed implementation is handled by `tailwind-quality-gate`.

**Design language model**: When shadcn/ui is present in the project, use `shadcn-component-design` for shadcn-registered components. Use this skill for Tailwind-only surfaces alongside a shadcn project — layouts, prose content, marketing pages, data-dense grids, and animation — where Tailwind utilities deliver capability that shadcn does not cover. Both skills can be active in the same project; coordinate on token naming and dark mode strategy so Tailwind utilities consume shadcn CSS variables rather than defining independent tokens.

## Trigger Conditions

- Designing or reviewing a new UI component that uses TailwindCSS utilities.
- Establishing a reusable design-token strategy (`@theme` custom properties or CSS variables).
- Implementing responsive layouts, container queries, or adaptive breakpoints with Tailwind.
- Adding dark mode to an existing component library.
- Integrating Headless UI components with Tailwind styling.
- Auditing a component library for class-ordering consistency, accessibility gaps, or utility anti-patterns.

## When Not to Use

- Project setup, build pipeline, or v3 → v4 migration (use `tailwind-setup`).
- Quality gate decision for a release candidate (use `tailwind-quality-gate`).
- Source freshness check before adopting a new Tailwind feature (use `tailwind-source-curation`).

## Inputs

- Target component or component library scope.
- Design token inventory or Figma/design handoff artifacts if available.
- Framework in use (React, Vue, Svelte, Astro, Blazor, etc.).
- Accessibility requirements and target WCAG level (default: AA).
- Dark mode strategy already chosen or to be decided.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Component pattern set | Utility class compositions for each component, co-located or in a component file |
| Design token map | `@theme` custom properties or CSS variables mapped to semantic roles (brand, surface, border, text, status) |
| Responsive strategy | Breakpoint choices, container query adoption decision, and mobile-first composition rules |
| Dark mode implementation | Strategy choice (`dark:` class vs. `prefers-color-scheme`) with token mapping for both modes |
| Headless UI integration notes | Component wiring pattern for any interactive components (dialog, menu, combobox, listbox, tabs) |
| Class ordering record | Prettier plugin active; ordering verified for all components |
| Accessibility annotation | Contrast, focus-visible, reduced-motion, and keyboard interaction requirements met for each component |
| Readiness summary | Open risks, known edge cases, and deferred patterns |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Implement one styled component with Tailwind | Component renders correctly across breakpoints with accessible contrast |
| L2 Practical Delivery | Deliver a component library slice | Token map, responsive strategy, and accessibility annotation complete for all delivered components |
| L3 Design System Alignment | Align Tailwind tokens with a design system | `@theme` block maps 1:1 with design tokens; visual drift between design and implementation is zero |
| L4 Expert Standardization | Reusable cross-project component patterns | Documented pattern library with token conventions, accessibility baseline, and dark-mode contract usable by any project |

## Design Token Strategy

### v4 CSS-First Tokens (`@theme`)

Define all design tokens in the CSS entry point using the `@theme {}` block:

```css
@import "tailwindcss";

@theme {
  --color-brand-500: oklch(0.6 0.2 260);
  --color-surface-base: var(--color-white);
  --font-sans: "Inter", ui-sans-serif, system-ui;
  --spacing-page: 1.5rem;
}
```

- Use semantic names (`brand`, `surface`, `border`, `text-primary`) over raw names (`blue-500`).
- Map dark mode tokens in a `@media (prefers-color-scheme: dark) {}` or `.dark {}` block.
- Expose tokens as CSS custom properties so non-Tailwind CSS can consume them.

### Token Semantic Roles

| Role | Examples | Usage |
|---|---|---|
| Brand | `--color-brand-500`, `--color-brand-600` | Primary CTAs, links, focus rings |
| Surface | `--color-surface-base`, `--color-surface-raised` | Page background, card background |
| Border | `--color-border-default`, `--color-border-strong` | Input borders, dividers |
| Text | `--color-text-primary`, `--color-text-muted` | Body copy, secondary labels |
| Status | `--color-status-success`, `--color-status-error` | Alerts, badges, inline validation |

## Responsive Design Rules

- Always write mobile-first: unprefixed utilities apply at all breakpoints; `md:`, `lg:` prefixes override upward.
- Use Tailwind's built-in breakpoints (`sm` 640px, `md` 768px, `lg` 1024px, `xl` 1280px, `2xl` 1536px) unless a custom breakpoint is justified in the token map.
- Prefer container queries (`@container`) over viewport breakpoints for components designed to be reused at different widths.
- Do not use arbitrary breakpoint values without documenting the reason in the component.

## Dark Mode Patterns

| Strategy | When to Use | Configuration |
|---|---|---|
| `media` (default) | User OS preference drives mode; no toggle needed | `@variant dark (&:where(.dark, .dark *))` or default media query |
| `class` | App provides a manual dark/light toggle | Add `dark` class to `<html>`; use `dark:` prefix in components |
| CSS variable hybrid | Design system provides tokens for both modes | Redefine `@theme` tokens inside `.dark {}` or `@media` block |

## Headless UI Integration Patterns

Use Headless UI for interactive components that require ARIA patterns:

| Component | Headless UI | Styling Rule |
|---|---|---|
| Modal / Dialog | `<Dialog>` | `backdrop-blur-sm`, `fixed inset-0`, `z-50` pattern |
| Dropdown Menu | `<Menu>` | `absolute`, shadow, and `ring-1` for boundary |
| Listbox / Select | `<Listbox>` | Same visual treatment as `<Menu>` with scroll-snap for long lists |
| Combobox | `<Combobox>` | Input styling plus floating list; use `transition` utilities for open/close |
| Tabs | `<Tab.Group>` | `border-b`, active state via `aria-selected` data attribute or `ui-selected:` |

- Do not re-implement ARIA keyboard behavior; delegate entirely to Headless UI.
- All Headless UI components expose `data-*` attributes; use `data-[state]:` variants for state-driven styling.

## Class Ordering Rules

Enforce using `prettier-plugin-tailwindcss`. The canonical order is:

1. Layout (display, position, inset, z-index)
2. Box model (width, height, padding, margin, overflow)
3. Flexbox/Grid (flex, grid, gap, align, justify)
4. Typography (font, text, leading, tracking)
5. Visual (bg, border, shadow, ring, opacity)
6. Interactive (cursor, pointer-events, resize)
7. State variants (hover:, focus:, disabled:, dark:)
8. Responsive variants (sm:, md:, lg:)

## Accessibility Component Checklist

Run for every interactive component before marking complete:

- [ ] Color contrast: text on background ≥ 4.5:1 (normal text), ≥ 3:1 (large text). Verify using `text-*` and `bg-*` token pairs.
- [ ] Focus ring: `focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2` or equivalent on all interactive elements.
- [ ] Reduced motion: animation utilities wrapped in `motion-safe:` or `motion-reduce:` as appropriate.
- [ ] Keyboard navigation: tab order is logical; no focus trap outside modals and drawers.
- [ ] Screen reader: Headless UI components provide ARIA; custom components include explicit `role`, `aria-label`, or `aria-labelledby`.
- [ ] Touch targets: interactive elements are at minimum `h-11 w-11` (44×44 CSS px) on touch-first surfaces.

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Correction |
|---|---|---|
| Arbitrary color values in component classes (`text-[#3b82f6]`) | Bypasses token system; breaks dark mode | Map color to a `@theme` token and use semantic utility |
| Rebuilding ARIA patterns without Headless UI | Keyboard and screen reader bugs | Use Headless UI for all interactive ARIA roles |
| Inline styles alongside Tailwind | Specificity conflicts and inconsistency | Convert to utilities or extend `@theme` |
| `!important` utilities (`!text-red-500`) | Signals specificity debt | Restructure component hierarchy instead |
| Dynamic class name construction via string concatenation | Classes not detected by content scanner; purged in production | Use complete class names; safeList only as last resort |

## Done Criteria

- [ ] Design token map is complete with semantic roles covering brand, surface, border, text, and status.
- [ ] Responsive strategy is documented; mobile-first composition applied.
- [ ] Dark mode strategy is chosen and token map covers both modes.
- [ ] Headless UI used for all interactive ARIA-bearing components.
- [ ] Prettier plugin enforces class ordering across all component files.
- [ ] Accessibility checklist passes for every interactive component.
- [ ] No anti-patterns present in delivered components.
- [ ] Readiness summary written with open risks and deferred patterns.

## References

- [Source Catalog](./references/source-catalog.md)
