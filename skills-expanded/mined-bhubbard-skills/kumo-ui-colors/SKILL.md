---
name: kumo-ui-colors
description: Complete reference for Kumo UI's color token system — all semantic, status, text, border, and badge tokens with exact light/dark mode values from theme-kumo.css. Covers the light-dark() function, token groups, and the FedRAMP alternate theme. Trigger when choosing colors, debugging styling issues, or understanding how Kumo's design tokens work at the CSS level.
---

# Kumo UI Colors & Theming

Kumo's color system is built on CSS `light-dark()` — tokens automatically switch between light and dark values based on the `data-mode` attribute. All values are defined in `theme-kumo.css` (auto-generated from `scripts/theme-generator/config.ts`).

> **Source of truth:** [`theme-kumo.css`](https://github.com/cloudflare/kumo/blob/main/packages/kumo/src/styles/theme-kumo.css) and [`kumo-binding.css`](https://github.com/cloudflare/kumo/blob/main/packages/kumo/src/styles/kumo-binding.css)

---

## How `light-dark()` Works

Kumo sets `color-scheme: light` on `:root` and `color-scheme: dark` on `[data-mode="dark"]`. The browser's native `light-dark()` function reads this and picks the correct value automatically:

```css
/* In theme-kumo.css */
--text-color-kumo-default: light-dark(
  var(--color-neutral-900),  /* light mode */
  var(--color-neutral-100)   /* dark mode  */
);
```

You never call `light-dark()` yourself — the tokens handle it. Just use the `kumo-*` Tailwind classes.

---

## Text Color Tokens

| Tailwind Class | Light Mode | Dark Mode | Use |
|---|---|---|---|
| `text-kumo-default` | neutral-900 | neutral-100 | Primary body text |
| `text-kumo-strong` | neutral-950 | neutral-50 | High-contrast headers |
| `text-kumo-subtle` | neutral-500 | neutral-400 | Secondary, muted labels |
| `text-kumo-inactive` | neutral-300 | neutral-600 | Disabled / inactive text |
| `text-kumo-placeholder` | neutral-400 | neutral-500 | Input placeholders |
| `text-kumo-inverse` | neutral-100 | neutral-900 | Text on inverted backgrounds |
| `text-kumo-brand` | `#f6821f` | `#f6821f` | Cloudflare orange (same in both modes) |
| `text-kumo-link` | blue-800 | blue-400 | Hyperlinks |
| `text-kumo-info` | blue-800 | blue-400 | Informational text |
| `text-kumo-success` | emerald-800 | emerald-200 | Success / positive text |
| `text-kumo-danger` | red-700 | red-400 | Error / destructive text |
| `text-kumo-warning` | yellow-800 | yellow-400 | Warning text |

### Badge-Specific Text Colors

| Tailwind Class | Light | Dark | Use |
|---|---|---|---|
| `text-kumo-badge-orange-subtle` | orange-800 | orange-200 | Badge text (orange variant) |
| `text-kumo-badge-teal-subtle` | teal-800 | teal-200 | Badge text (teal variant) |
| `text-kumo-badge-neutral-subtle` | neutral-800 | neutral-200 | Badge text (neutral variant) |

---

## Background Color Tokens

### Surface Hierarchy (use outermost → innermost)

| Tailwind Class | Purpose |
|---|---|
| `bg-kumo-canvas` | Outermost page/app background |
| `bg-kumo-base` | Default component/panel background |
| `bg-kumo-elevated` | Cards, panels sitting above base |
| `bg-kumo-overlay` | Dialogs, popovers, dropdown menus |
| `bg-kumo-recessed` | Inset areas, segmented controls |
| `bg-kumo-tint` | Table headers, row hover states, active nav items |
| `bg-kumo-contrast` | High-contrast inverted panels |

### Interactive Backgrounds

| Tailwind Class | Purpose |
|---|---|
| `bg-kumo-control` | Form control backgrounds (input, select, button) |
| `bg-kumo-interact` | Hover/focus highlight backgrounds |
| `bg-kumo-fill` | Small element fills (icons, badges) |
| `bg-kumo-fill-hover` | Hover state for small element fills |

### Brand

| Tailwind Class | Purpose |
|---|---|
| `bg-kumo-brand` | Primary orange brand background (`#f6821f`) |
| `bg-kumo-brand-hover` | Hover state for brand backgrounds |

### Status (Solid + Tint)

Use **solid** for icons/dots, **tint** (`-tint`) for badge/banner backgrounds:

| Solid | Tint | Use |
|---|---|---|
| `bg-kumo-info` | `bg-kumo-info-tint` | Blue informational |
| `bg-kumo-success` | `bg-kumo-success-tint` | Green success |
| `bg-kumo-warning` | `bg-kumo-warning-tint` | Yellow warning |
| `bg-kumo-danger` | `bg-kumo-danger-tint` | Red error/destructive |

> **Opacity modifier**: Tint backgrounds often work well with opacity: `bg-kumo-danger-tint/70`

### Badge-Specific Backgrounds

| Tailwind Class | Light | Dark |
|---|---|---|
| `bg-kumo-badge-orange-subtle` | orange-100 | orange-950 |
| `bg-kumo-badge-teal-subtle` | teal-100 | teal-950 |
| `bg-kumo-badge-neutral-subtle` | neutral-100 | neutral-800 |

---

## Border Tokens

| Tailwind Class | Purpose |
|---|---|
| `border-kumo-hairline` | Thin separator between flat surfaces (low emphasis) |
| `border-kumo-line` | Thicker border — defines elevated surface edges |

### Focus Ring

| Tailwind Class | Purpose |
|---|---|
| `ring-kumo-focus` | Keyboard focus ring color |
| `ring-kumo-brand` | Brand-colored focus ring (used on interactive elements) |

Usage pattern:
```html
<button class="focus:outline-none focus-visible:ring-2 focus-visible:ring-kumo-brand">
```

---

## Primitive Color Scale (Extended Neutrals)

Defined in `kumo-binding.css` as custom OKLCH values that extend Tailwind's neutral palette:

| Token | OKLCH Value | Relative Lightness |
|---|---|---|
| `--color-kumo-neutral-50` | `oklch(98.75% 0 0)` | Near-white |
| `--color-kumo-neutral-75` | `oklch(98% 0 0)` | Off-white |
| `--color-kumo-neutral-125` | `oklch(96.5% 0 0)` | Very light grey |
| `--color-kumo-neutral-450` | `oklch(89% 0 0)` | Light grey |
| `--color-kumo-neutral-750` | `oklch(32% 0 0)` | Dark grey |
| `--color-kumo-neutral-850` | `oklch(24% 0 0)` | Very dark grey |
| `--color-kumo-neutral-925` | `oklch(17% 0 0)` | Near-black |
| `--color-kumo-neutral-950` | `oklch(15% 0 0)` | Near-black |
| `--color-kumo-neutral-975` | `oklch(12% 0 0)` | Almost black |
| `--color-kumo-neutral-1000` | `oklch(10% 0 0)` | Darkest |

These extend standard Tailwind neutral steps to provide finer granularity for Cloudflare's dark dashboard UIs.

---

## Themes

Kumo ships two themes via `kumo-binding.css`:

```css
@import "./theme-kumo.css";     /* Standard Kumo theme */
@import "./theme-fedramp.css";  /* FedRAMP-compliant theme variant */
```

The FedRAMP theme uses the same token names but may map to different underlying colors for government compliance contexts. You switch themes by changing which CSS file is loaded.

---

## Animation & Transition Tokens

Defined in `kumo-binding.css`:

| CSS Variable | Value | Use |
|---|---|---|
| `--ease-bounce` | `cubic-bezier(0.2, 0, 0, 1.5)` | Springy interactions |
| `--default-transition-duration` | `100ms` | Default transition speed |
| `--animate-refresh` | `refresh 0.5s ease-in-out infinite` | Spinner/refresh animation |
| `--animate-right` | `right 15s linear infinite` | Horizontal scroll animation |

---

## Helper CSS Classes (from kumo-binding.css)

| Class | Purpose |
|---|---|
| `no-scrollbar` | Hide scrollbar (both WebKit + standard) |
| `no-input-spinner` | Remove number input arrows |
| `link-current` | Low-opacity underline for active nav links; full opacity on hover |
| `link-external-icon` | External link icon — thicker stroke in dark mode for visibility |

---

## The Golden Rules

```tsx
// ✅ ALWAYS use kumo-* semantic tokens
<div className="bg-kumo-base text-kumo-default border border-kumo-hairline">
  <span className="text-kumo-danger">Error message</span>
  <div className="bg-kumo-danger-tint/70 text-kumo-badge-neutral-subtle px-2 py-1 rounded">
    Badge
  </div>
</div>

// ❌ NEVER use raw colors or dark: variants
<div className="bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-100">
  <span className="text-red-600 dark:text-red-400">Error</span>
</div>
```

1. **Never use `dark:` prefix** — the `data-mode` attribute + `light-dark()` handle this automatically
2. **Never use raw Tailwind colors** (`bg-white`, `text-gray-900`, `bg-blue-500`)
3. **Use the surface hierarchy** — canvas → base → elevated → overlay for layered UIs
4. **Solid vs tint status colors** — solid for icons/dots, tint for backgrounds
