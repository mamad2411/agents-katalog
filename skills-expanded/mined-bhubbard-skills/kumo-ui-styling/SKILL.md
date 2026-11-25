---
name: kumo-ui-styling
description: Guidelines and best practices for styling with Kumo UI (@cloudflare/kumo). Covers semantic color tokens, light/dark mode via data-mode attributes, Tailwind CSS v4 setup, and helper utilities. Trigger when writing or reviewing styles in a Kumo UI project.
---

# Kumo UI Styling Guide

Kumo UI's design system is built on **semantic color tokens** that adapt to light and dark mode automatically. Never use raw Tailwind colors or `dark:` variants in Kumo projects.

---

## 1. Semantic Color Tokens

All color classes begin with `kumo-`. They adapt to the current theme automatically via CSS `light-dark()`.

### Surface Hierarchy (use in order, outermost → innermost)

| Token | Class | Purpose |
|---|---|---|
| Canvas | `bg-kumo-canvas` | Outermost page background |
| Base | `bg-kumo-base` | Default component/panel background |
| Elevated | `bg-kumo-elevated` | Card-like components that sit above base |
| Recessed | `bg-kumo-recessed` | Darker fill — segmented controls, inset areas |
| Tint | `bg-kumo-tint` | Table headers, hover states, active items |
| Contrast | `bg-kumo-contrast` | High-contrast inverted background |
| Overlay | `bg-kumo-overlay` | Dialogs, popovers, dropdown menus |
| Control | `bg-kumo-control` | Form controls — inputs, selects, buttons |

### Interaction & Fill States

| Class | Purpose |
|---|---|
| `bg-kumo-interact` | Interaction highlight backgrounds |
| `bg-kumo-fill` | Default fill for small UI elements |
| `bg-kumo-fill-hover` | Hover fill for small UI elements |

### Brand Colors

| Class | Purpose |
|---|---|
| `bg-kumo-brand` | Primary brand background |
| `bg-kumo-brand-hover` | Hover state for brand backgrounds |
| `text-kumo-brand` | Brand-colored text |

### Status Colors

Status colors come in **solid** (icons, dots) and **-tint** (badge/banner backgrounds) variants:

| Solid | Tint | Purpose |
|---|---|---|
| `bg-kumo-info` | `bg-kumo-info-tint` | Informational |
| `bg-kumo-success` | `bg-kumo-success-tint` | Success / positive |
| `bg-kumo-warning` | `bg-kumo-warning-tint` | Warning / caution |
| `bg-kumo-danger` | `bg-kumo-danger-tint` | Error / destructive |

> Use solid tokens for icons and dots; tint tokens for badge/banner background fills (often with opacity: `bg-kumo-danger-tint/70`).

### Text Colors

| Class | Purpose |
|---|---|
| `text-kumo-default` | Primary body text |
| `text-kumo-strong` | Headers and high-contrast labels |
| `text-kumo-subtle` | Muted — descriptions, captions, secondary labels |
| `text-kumo-inactive` | Disabled / inactive states |
| `text-kumo-placeholder` | Input placeholder text |
| `text-kumo-inverse` | Text on high-contrast/inverted backgrounds |
| `text-kumo-link` | Interactive links |
| `text-kumo-info` | Info-colored text (contrast-optimized) |
| `text-kumo-success` | Success-colored text |
| `text-kumo-warning` | Warning-colored text |
| `text-kumo-danger` | Error/destructive text |

### Borders & Focus Rings

| Class | Purpose |
|---|---|
| `border-kumo-hairline` | Thin border — separates flat surfaces |
| `border-kumo-line` | Thicker border — defines elevated surface edges |
| `ring-kumo-focus` | Keyboard focus ring |

---

## 2. Light / Dark Mode

Mode is controlled by a `data-mode` attribute — **not** Tailwind `dark:` variants.

### Setup (FOUC prevention)

Add this **blocking** script in `<head>` before any styles:

```javascript
(function () {
  const stored = localStorage.getItem("theme");
  if (stored) {
    document.documentElement.setAttribute("data-mode", stored);
  } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    document.documentElement.setAttribute("data-mode", "dark");
  }
})();
```

### Toggling

```html
<!-- Force light mode -->
<html data-mode="light">

<!-- Force dark mode -->
<html data-mode="dark">

<!-- Follows system preference (no attribute needed) -->
<html>
```

### Rules — Critical

```tsx
// ✅ CORRECT — semantic tokens adapt automatically
<div className="bg-kumo-base text-kumo-default border-kumo-hairline">
  <button className="bg-kumo-brand text-white">Primary</button>
  <button className="bg-kumo-control text-kumo-default">Secondary</button>
</div>

// ❌ WRONG — raw colors, manual dark: variants
<div className="bg-white dark:bg-gray-900 text-black dark:text-white">
  <button className="bg-blue-500 hover:bg-blue-600">Submit</button>
</div>
```

**Never use:**
- Raw Tailwind color utilities (`bg-white`, `text-black`, `bg-blue-500`)
- Tailwind `dark:` prefix with semantic or raw colors
- CSS variables that bypass the `kumo-` token system

---

## 3. Tailwind CSS v4 Setup

Tailwind v4 does **not** scan `node_modules/` by default. Without the `@source` directive, Kumo component classes will be missing from your build.

### Required CSS Setup

```css
/* app.css / main.css — ORDER MATTERS */

/* 1. Tell Tailwind to scan Kumo's compiled output */
@source "../node_modules/@cloudflare/kumo/dist/**/*";

/* 2. Import Kumo's theme tokens (registers kumo-* tokens) */
@import "@cloudflare/kumo/styles/tailwind";

/* 3. Import Tailwind itself */
@import "tailwindcss";

/* 4. Your own custom styles below */
```

> If you omit `@source`, Dialogs won't center, colors won't apply, and layout will break. This is the #1 setup mistake.

---

## 4. Helper Utilities

### `cn` — Class Name Merger

Merges conditional classes and resolves conflicts (wraps `clsx` + `tailwind-merge`):

```tsx
import { cn } from "@cloudflare/kumo";

function Card({ active, className }: { active?: boolean; className?: string }) {
  return (
    <div className={cn("p-4 bg-kumo-base border-kumo-hairline", active && "bg-kumo-tint", className)}>
      Content
    </div>
  );
}
```

### `safeRandomId` — SSR-Safe IDs

Generates random IDs that are safe during server-side rendering (no hydration mismatch):

```tsx
import { safeRandomId } from "@cloudflare/kumo";

const id = safeRandomId(); // e.g. "kumo-a3f9"
```

### `LinkProvider` — Router Integration

Configures the Kumo `Link` component to use your framework's router for client-side navigation:

```tsx
import { LinkProvider } from "@cloudflare/kumo";
import { Link as RouterLink } from "react-router-dom"; // or Next.js Link, Remix Link

export function App() {
  return (
    <LinkProvider component={RouterLink}>
      {/* All Kumo Link components inside will use RouterLink */}
    </LinkProvider>
  );
}
```
