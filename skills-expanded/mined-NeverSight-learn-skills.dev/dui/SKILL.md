---
name: dui
description: Build frontend UIs using DUI, a Lit-based styled web component library with design tokens and two-layer inheritance. Use this skill whenever the user wants to build pages, layouts, forms, dashboards, or any frontend UI in a project that uses (or should use) DUI components — look for `@deepfuture/dui-components` or `@dui/components` imports, `dui-*` element tags, or design token variables like `--accent`, `--surface-1`. Also trigger when the user mentions "DUI", "dui components", or asks to add/use web components with design tokens. If a project has DUI installed, always use this skill for frontend work rather than building from scratch.
---

# DUI

DUI is a styled Lit web component library built on two-layer inheritance. Unstyled primitives (in a separate repo) provide structure and behavior; styled components extend them with aesthetic CSS and design tokens. Components self-register on import — no setup function, no configuration.

**Read `DESIGN.md` first.** Every DUI project has a `DESIGN.md` at the repo root. It defines the visual identity (colors, typography, spacing, radii, elevation) and interaction grammar (page archetypes, overlay hierarchy, form validation, state patterns, motion, accessibility, and more). The DESIGN.md is the authoritative source for all design decisions. This skill owns DUI implementation guidance: component selection, styling API, composition rules, inspector workflow, and code patterns. There is no overlap — DESIGN.md says *what the design looks like and how the app behaves*; this skill says *how to build it with DUI components*.

## Project detection

Before writing any DUI code, check the project's DUI status:

1. Check `package.json` for `@deepfuture/dui-components` deps, or `deno.json` for `@dui/components/*` import map entries
2. If found, note which packages are installed — components self-register on import, so look for `import "@deepfuture/dui-components/button"` or `import "@dui/components/button"` patterns
3. If DUI is not installed, follow the install instructions below
4. Check whether `@deepfuture/dui-inspector` (or `@dui/inspector`) is available — if so, use the inspector workflow below
5. Read `DESIGN.md` at the project root before writing any UI code

## Principles

1. **Read DESIGN.md first.** It defines colors, typography, spacing, component styling, page archetypes, overlay rules, form validation timing, and every other design decision. Follow it.
2. **Use DUI components first.** Before writing custom markup, check if a DUI component exists. Read `references/components.md` for the full catalog.
3. **Inspect before styling.** Before overriding any token or adding custom CSS, run `__dui_inspect('dui-component-name')` to see available tokens, parts, slots, and current values. The inspector is the ground truth — don't guess token names.
4. **Compose, don't reinvent.** A settings page = `dui-tabs` + `dui-input` + `dui-select` + `dui-switch`. A dashboard = `dui-sidebar` + `dui-data-table` + layout primitives.

## Installation

### npm

```bash
npm install @deepfuture/dui-components
```

### CDN (zero setup)

```html
<script type="module" src="https://cdn.jsdelivr.net/npm/@deepfuture/dui-cdn/dui.min.js"></script>
```

The CDN bundle registers all components automatically.

### Deno (from source)

Add `@dui/*` entries to your app's `deno.json` import map:

```json
{
  "imports": {
    "@dui/components/button": "../dui/packages/components/src/button/index.ts"
  }
}
```

### Usage

Components self-register on import. No setup function, no configuration:

```typescript
// À la carte — import only what you use
import "@deepfuture/dui-components/button";
import "@deepfuture/dui-components/dialog";

// Or register everything
import "@deepfuture/dui-components";
```

Each import registers the component and all its sub-components. Importing `dialog` registers `dui-dialog`, `dui-dialog-trigger`, `dui-dialog-popup`, and `dui-dialog-close`.

### Templates

Templates are pre-composed UI patterns. Install alongside the components:

```bash
npm install @deepfuture/dui-templates
```

```typescript
import "@deepfuture/dui-templates/feed";  // registers dui-feed-item etc.
```

## Typography & spacing implementation

DUI's text-box trimming (`text-box: trim-both cap alphabetic`) means **text elements have zero implicit spacing**. You must create all vertical rhythm explicitly. See DESIGN.md → Typography and Layout for the rules; here are the implementation patterns.

### Flex column with gap

```css
.page-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-bottom: var(--space-6);
}
```

```html
<div class="page-header">
  <h1>Dashboard</h1>
  <p>Overview of recent order activity and key metrics.</p>
</div>
```

### Inside cards and panels

```css
.stat-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.stat-label {
  font-size: var(--text-xs);
  color: var(--text-2);
}

.stat-value {
  font-size: var(--text-3xl);
  font-weight: var(--font-weight-semibold);
}

.stat-change {
  font-size: var(--text-sm);
  color: var(--accent);
}
```

### dui-prose for long-form content

For rendered markdown or CMS content, apply `class="dui-prose"` to the container. This restores automatic heading margins, paragraph spacing, and list indentation. For app UI (dashboards, forms, settings), use explicit flex/gap spacing instead.

```html
<div class="dui-prose">
  <h1>Release Notes</h1>
  <p>Version 2.0 brings major improvements...</p>
</div>
```

See `references/rules.md` for incorrect/correct code pairs.

## Component selection

Read `references/components.md` for the full catalog. Quick lookup:

| Need | Use |
| --- | --- |
| Button / action | `dui-button` with `variant` and `size` |
| Split button with dropdown | `dui-split-button` |
| Form inputs | `dui-input`, `dui-textarea`, `dui-select`, `dui-combobox`, `dui-checkbox`, `dui-radio-group`, `dui-switch`, `dui-slider`, `dui-number-field`, `dui-stepper`, `dui-dropzone` |
| Form field with label/error | `dui-field` wrapping a form control |
| Form field grouping | `dui-fieldset` |
| Toggle between options | `dui-toggle-group` |
| Data display | `dui-data-table`, `dui-badge`, `dui-avatar`, `dui-calendar`, `dui-progress`, `dui-spinner` |
| Navigation | `dui-sidebar-provider`, `dui-breadcrumb`, `dui-tabs` |
| Overlays | `dui-dialog` (modal), `dui-alert-dialog` (confirmation), `dui-popover`, `dui-tooltip`, `dui-menu`, `dui-command` |
| Disclosure | `dui-accordion`, `dui-collapsible` |
| Content containers (structured header/action/footer) | `dui-card`, `dui-card-grid` |
| Layout | `dui-scroll-area`, `dui-separator` — for rows/columns/centering/page margins, use standard CSS flexbox and grid |
| Text | `dui-trunc` (truncation with `max-lines` or `max-width`) |
| Utility | `dui-icon`, `dui-portal`, `dui-link` |
| Maps | `dui-map` + `dui-map-marker`, `dui-map-controls`, `dui-map-route`, `dui-map-region`, `dui-map-heatmap`, `dui-map-cluster-layer` |
| Charts | `dui-chart` (Observable Plot wrapper) |

### Use DUI components, not custom markup

| Instead of... | Use |
| --- | --- |
| `<hr>` or border divs | `dui-separator` |
| Custom styled `<span>` for tags/status | `dui-badge` |
| Custom `animate-spin` div | `dui-spinner` |
| Custom progress bar div | `dui-progress` |
| Raw `<svg>` with manual sizing | `dui-icon` + `lucide-static` import (`unsafeHTML(Home)`), or raw SVG in slot as fallback |
| `overflow: auto` div | `dui-scroll-area` |
| Raw `<a>` tag | `dui-link` |
| Structured content with header/action/footer | `dui-card` |
| Simple content containers (stat tiles, info boxes) | styled `<div>` with `--surface-1`, `--border`, `--radius-lg` |
| Label + input + error div | `dui-field` wrapping the input |

See `references/rules.md` for incorrect/correct code pairs.

## Theme configuration

DUI ships with default blue accent tokens. If the project has a DESIGN.md with different colors, fonts, or radius, apply them after importing DUI:

```typescript
import "@deepfuture/dui-components/button"; // or any component import
import { applyTheme } from "@deepfuture/dui-components/theme";

applyTheme({
  light: {
    background:  "oklch(0.97 0.00 0)",
    foreground:  "oklch(0.15 0.00 0)",
    accent:      "oklch(0.55 0.25 160)",
    destructive: "oklch(0.55 0.22 25)",
  },
  dark: {
    background:  "oklch(0.15 0.00 0)",
    foreground:  "oklch(0.93 0.00 0)",
    accent:      "oklch(0.75 0.18 160)",
    destructive: "oklch(0.70 0.18 25)",
  },
  fonts: { sans: "Inter", mono: "Geist Mono" },
  radius: "0.5rem",
});
```

The four color primitives are `background`, `foreground`, `accent`, `destructive`. All derived tokens (`--surface-1`, `--text-2`, `--border`, `--accent-subtle`, etc.) update automatically via `oklch(from var(...) ...)`.

**Dark mode derivation:** If you omit `dark`, it's auto-derived from `light` (inverted lightness, boosted accent). Provide both for precise control.

**Fonts:** `fonts.sans`, `fonts.mono`, `fonts.serif` override `--font-sans`, `--font-mono`, `--font-serif`. Pass the family name (e.g. `"Inter"`), not the full stack.

**Radius:** `radius` sets the base value (e.g. `"0.5rem"` or `"8px"`). The full scale (`--radius-xs` through `--radius-2xl`) is derived proportionally.

**Where to call it:** In your app's entry point / bootstrap file, after any DUI component import. Call it once. Safe to call again to change the theme at runtime.

**Reading from DESIGN.md:** Extract the OKLCH values from the `colors` comment block at the top of DESIGN.md, the font family from the `typography` section, and the base radius from the `rounded.md` value. Map them directly to the `applyTheme()` config.

## Sidebar layout

The sidebar compound component requires a specific layout structure. The `dui-sidebar` component uses `position: sticky; top: 0; height: 100dvh` internally, so it self-sizes correctly regardless of parent height context.

Canonical structure:

```html
<dui-sidebar-provider style="min-height: 100dvh;">
  <dui-sidebar>
    <dui-sidebar-header>...</dui-sidebar-header>
    <dui-sidebar-content>
      <dui-sidebar-group>
        <dui-sidebar-group-label slot="label">Section</dui-sidebar-group-label>
        <dui-sidebar-menu>
          <dui-sidebar-menu-item>
            <dui-sidebar-menu-button href="/page" active>Page</dui-sidebar-menu-button>
          </dui-sidebar-menu-item>
        </dui-sidebar-menu>
      </dui-sidebar-group>
    </dui-sidebar-content>
    <dui-sidebar-footer>...</dui-sidebar-footer>
  </dui-sidebar>

  <dui-sidebar-inset>
    <header style="display: flex; align-items: center; gap: var(--space-2); padding: var(--space-2) var(--space-4); border-bottom: var(--border-width-thin) solid var(--border);">
      <dui-sidebar-trigger></dui-sidebar-trigger>
      <dui-separator orientation="vertical" style="height: var(--space-4);"></dui-separator>
      <dui-breadcrumb>...</dui-breadcrumb>
    </header>
    <main style="padding: var(--space-6); display: flex; flex-direction: column; gap: var(--space-6);">
      <!-- page content -->
    </main>
  </dui-sidebar-inset>
</dui-sidebar-provider>
```

Key points:
- **Provider needs `min-height: 100dvh`** on the host or via a parent to fill the viewport.
- **Sidebar self-sizes** — no height or sticky positioning needed on the consumer side.
- **Inset is the main content area** — it adjusts width automatically when the sidebar opens/closes.
- **Top bar** — a `<header>` inside `dui-sidebar-inset` with the trigger, a vertical separator, and breadcrumbs.

See `references/blocks.md` → Page Shells for complete dashboard, settings, and list-view layouts.

## Page shells

Most app pages follow one of three patterns. See `references/blocks.md` → Page Shells for the full component trees:

| Page type | Key components inside `sidebar-inset` | Block |
|-----------|--------------------------------------|-------|
| **Dashboard** | `card-grid` (stat tiles) + `dui-card` (data table, chart) | `block-dashboard-shell` |
| **Settings** | `dui-tabs` → tab panels with `dui-field` + form controls | `block-settings-shell` |
| **List view** | filter bar (`dui-input` + `dui-select` + `dui-button`) + `dui-data-table` | `block-list-shell` |

All three share the same outer structure: `dui-sidebar-provider > dui-sidebar + dui-sidebar-inset > top-bar + main content`.

## Styling API

Two layers for styling DUI components:

| Layer | Mechanism | Best for |
|-------|-----------|----------|
| **CSS variables** | `dui-button { --button-bg: ... }` | Colors, sizes, spacing |
| **`::part(root)`** | `dui-button::part(root) { ... }` | Filters, transforms, shadows, clip-paths |

Variables cascade from ancestors. `::part()` must target the element directly.

### Theme attributes vs properties

Some attributes like `variant`, `appearance`, and `size` are **theme attributes** — reflected HTML attributes that the styled CSS layer selects on (`:host([variant="primary"])`):

```html
<dui-button variant="primary" size="lg">Save</dui-button>
<dui-badge variant="danger" appearance="soft">Error</dui-badge>
```

Behavioral **properties** like `disabled`, `open`, `value` are reactive Lit properties that affect component behavior and DOM structure.

### Composition rules

- **Slots** are the composition API — pass content via named/default slots, not wrapper divs.
- **Compound components stay together** — `dui-dialog-trigger` inside `dui-dialog`, `dui-select-option` inside `dui-select`.
- **Never reach into shadow DOM** — use CSS custom properties, `::part(root)`, or the inspector API.
- **Standard CSS for layout** — flexbox and grid directly. DUI has no layout wrapper components.
- **Complex-property components** — `dui-data-table`, `dui-chart`, `dui-select`, and `dui-combobox` have properties (`columns`, `data`, `spec`, `options`) that accept arrays/objects. These can't be set via HTML attributes. Set them imperatively in `firstUpdated()` via `querySelector` on your own light DOM. This is **not** the same as reaching into another component's shadow DOM — you own these elements.

```typescript
// Canonical pattern for complex-property components
import type { ColumnDef } from "@dui/components/data-table";

override firstUpdated() {
  const table = this.renderRoot.querySelector("dui-data-table") as any;
  if (table) {
    table.columns = COLUMNS;
    table.data = DATA;
    table.pageSize = 10;
  }
}
```

If the component is in your own Lit template (not inside another component's shadow DOM), `querySelector` on `this.renderRoot` (or `this.shadowRoot`) is the correct approach. Update the element's properties in `updated()` when reactive state changes.

## Event handling

### `dui-navigate` for link buttons

When `<dui-button href="...">` is clicked (without modifier keys), it fires `dui-navigate`. Wire into your router:

```typescript
document.addEventListener("dui-navigate", (e: CustomEvent<{ href: string }>) => {
  router.navigate(e.detail.href);
});
```

### Component events

Listen on the element:

```typescript
html`
  <dui-switch @checked-change=${(e: CustomEvent<{ checked: boolean }>) => {
    console.log("Switch toggled:", e.detail.checked);
  }}></dui-switch>
`;
```

## Inspector workflow

When `@dui/inspector` (or `@deepfuture/dui-inspector`) is installed, use the inspector to discover, verify, and prototype with DUI components at runtime. This is the most accurate way to understand what's available and how components behave.

**CRITICAL**: Use the inspector BEFORE writing any DUI styling code — not just for debugging. Run `__dui_inspect('dui-sidebar-menu-button')` before overriding sidebar tokens. Run `__dui_inspect('dui-data-table')` before customizing table appearance. The inspector shows which tokens actually exist, what they're called, and their current values. Guessing at token names wastes iterations.

The inspector provides console globals. If the project has a running dev server with a browser, use these in the browser console or via a Playwright/Puppeteer script.

### Discovery

```js
// See all DUI components on the page + full catalog of registered types
__dui_inspect()

// Inspect a specific component — get properties, tokens, slots, parts, events
__dui_inspect('dui-button')
__dui_inspect('[data-dui-id="5"]')
```

The `catalog` field from `__dui_inspect()` lists every registered `dui-*` tag with its property schema, slots, and parts — including components not currently rendered.

### Prototyping

```js
// Insert a component into the page
__dui_mutate.insertComponent('[data-dui-id="3"]', 'beforeend', 'dui-button',
  { variant: 'primary' }, 'Click me')

// Set a property
__dui_mutate.setProp('[data-dui-id="5"]', 'variant', 'danger')

// Change a design token globally
__dui_mutate.setToken('--radius-md', '1rem')

// Change a token on one instance
__dui_mutate.setComponentToken('[data-dui-id="5"]', '--button-bg', 'red')

// Replace slot content
__dui_mutate.setSlotContent('[data-dui-id="5"]', '', '<span>New label</span>')

// Remove or move components
__dui_mutate.removeComponent('[data-dui-id="5"]')
__dui_mutate.moveComponent('[data-dui-id="5"]', '[data-dui-id="10"]', 'beforeend')
```

### Verify → export → write

```js
// Export all mutations as structured source file changes
__dui_export()
// → [{ file: "...", changeType: "token"|"template", description: "...", ... }]
```

### Typical agent workflow

```
1. __dui_inspect()                              → discover available components via catalog
2. __dui_mutate.insertComponent(...)             → build the UI
3. __dui_mutate.setProp(selector, prop, value)   → configure components
4. __dui_inspect(selector)                       → verify state
5. __dui_export()                                → get structured source changes
6. Write changes to source files                  → done
```

When the inspector is not available, fall back to the static component reference in `references/components.md` and write code directly.

## Detailed references

- [references/components.md](references/components.md) — Full catalog of all 57 component families with properties, theme attributes, slots, parts, and CSS custom properties
- [references/rules.md](references/rules.md) — Incorrect/correct code pairs for every critical rule
- [references/blocks.md](references/blocks.md) — Real-world composition examples: settings forms, chat inputs, dashboards, maps, data tables, and more. Each entry summarizes the pattern and key CSS/layout techniques, with a pointer to the full source. **Read a block's source file when building something similar.**
- [references/inspector.md](references/inspector.md) — Complete inspector API reference
