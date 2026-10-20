---
name: frontend-daisyui
description: Use when reaching for semantic component classes on top of Tailwind — themes, customization, when DaisyUI beats hand-rolled or shadcn.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [frontend-tailwind, frontend-shadcn-ui, frontend-design-essentials]
---

# DaisyUI

**Iron Law: DaisyUI is opinionated. Use it when you want fast component density without per-component CSS. Customize with themes; don't fight the class system.**

Tailwind plugin adding **semantic component classes** (`btn`, `card`, `modal`, `input`) and a theming system. Sits between raw Tailwind utilities and a full headless component library.

## What you get / what it isn't

| Get                                                                   | Don't get                                                    |
| --------------------------------------------------------------------- | ------------------------------------------------------------ |
| ~50 component classes (`btn`, `card`, `alert`, `dropdown`, `tabs`...) | Headless behaviour — ARIA, focus trap, keyboard nav is yours |
| Modifier classes (`btn-primary`, `btn-sm`, `btn-outline`)             | Copy-paste source — CSS lives in the plugin                  |
| ~30 built-in themes + custom theme system                             | Renamable semantics — `primary` is `primary`, accept it      |
| Framework-agnostic (React, Vue, Svelte, Astro, HTML)                  |                                                              |

## DaisyUI vs alternatives

| Need                                   | Pick                            | Why                                         |
| -------------------------------------- | ------------------------------- | ------------------------------------------- |
| Prototype/internal tool, speed > brand | **DaisyUI**                     | Zero per-component CSS, one-attr theme swap |
| Marketing page, light interactivity    | **DaisyUI**                     | Looks good by default                       |
| Heavy custom design language           | **shadcn / hand-rolled**        | Daisy's classes will fight you              |
| Production a11y-critical app           | **shadcn / Radix / React Aria** | Real focus/keyboard/ARIA                    |
| Already own a design system            | **hand-rolled**                 | Daisy's vocabulary will clash               |

## Install (v5, Tailwind v4)

```css
@import "tailwindcss";
@plugin "daisyui";
```

Tailwind v3 → `npm i daisyui@latest` + `plugins: [require("daisyui")]`.

## Component quick-ref

| Class                       | Purpose                     | Notable modifiers                                                                                                            |
| --------------------------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `btn`                       | Button                      | `btn-primary/ghost/outline`, `btn-sm/lg`, `btn-circle`                                                                       |
| `card`                      | Card                        | `card-body`, `card-title`, `card-actions` (border via Tailwind `border border-base-300` — `card-bordered` was removed in v5) |
| `alert`                     | Status                      | `alert-info/success/warning/error`                                                                                           |
| `badge`                     | Inline tag                  | `badge-primary/outline`, `badge-xs..lg`                                                                                      |
| `input`/`select`/`textarea` | Form input                  | `input-error`, `input-sm` (border via Tailwind utilities — `input-bordered` was removed in v5)                               |
| `modal`                     | Native `<dialog>`           | `modal-open`, `modal-backdrop`, `modal-action`                                                                               |
| `dropdown`                  | `<details>` or focus-driven | `dropdown-end`, `dropdown-hover`                                                                                             |
| `tabs`                      | Radio-input tabs            | `tab-active`, `tabs-boxed`, `tabs-lifted`                                                                                    |
| `drawer`                    | Checkbox+label sidebar      | `drawer-side`, `drawer-content`, `drawer-overlay`                                                                            |
| `navbar`                    | Header bar                  | `navbar-start/center/end`                                                                                                    |

## Theme variables (can't be renamed)

| Variable                                          | Role                              |
| ------------------------------------------------- | --------------------------------- |
| `--color-primary` / `-content`                    | Brand action + foreground         |
| `--color-secondary` / `-content`                  | Secondary action                  |
| `--color-accent` / `-content`                     | Highlight/CTA                     |
| `--color-neutral` / `-content`                    | Neutral surface (sidebar, footer) |
| `--color-base-100/200/300` / `-content`           | App surface layers + text         |
| `--color-info/success/warning/error` / `-content` | Status                            |
| `--radius-box/btn/badge`                          | Per-shape radius                  |
| `--border`                                        | Default border width              |

## Built-in themes

```html
<html data-theme="dark">
  <html data-theme="cupcake"></html>
</html>
```

Enable a subset to keep CSS small:

```css
@plugin "daisyui" {
  themes:
    light --default,
    dark --prefersdark,
    cupcake;
}
```

## Custom theme

DaisyUI v5 declares a custom theme via the `daisyui/theme` plugin block. The main `@plugin "daisyui" { themes: ... }` form only enables/disables BUILT-IN themes — listing a new name there silently no-ops because the name isn't in the built-in registry.

```css
@plugin "daisyui/theme" {
  name: "devkit";
  default: true;
  color-scheme: light;
  --color-primary: oklch(60% 0.18 250);
  --color-primary-content: white;
  --color-base-100: oklch(98% 0 0);
  --color-base-content: oklch(20% 0 0);
  --radius-box: 0.5rem;
}
```

Alternative — plain CSS variable overrides on a `[data-theme]` selector (works without the daisy plugin block; full control):

```css
[data-theme="devkit"] {
  color-scheme: light;
  --color-primary: oklch(60% 0.18 250);
  --color-base-100: oklch(98% 0 0);
  /* ...rest of the tokens... */
}
```

Then activate with `<html data-theme="devkit">`. Map design tokens onto Daisy's slots. See `Skill(devkit:frontend-design-essentials)`.

## Usage

```html
<button class="btn btn-primary">Save</button>
<div class="card bg-base-100 shadow">
  <div class="card-body"><h2 class="card-title">T</h2></div>
</div>
```

Mix freely with Tailwind: `<button class="btn btn-primary rounded-full px-8">Go</button>`.

## Interactivity gotcha

DaisyUI styles native HTML: **Modal** uses `<dialog>` + `dialog.showModal()`; **Dropdown** uses `<details>` or focus tricks; **Drawer** uses hidden checkbox + label (no JS!); **Tabs** uses radio inputs. **ARIA and keyboard behaviour beyond native elements is yours.** For production widgets, wrap with Radix/Headless UI; borrow only Daisy's styling.

## Customisation

| Need                      | How                                                                        |
| ------------------------- | -------------------------------------------------------------------------- |
| Tweak one instance        | Tailwind utility after the class: `class="btn btn-primary bg-emerald-600"` |
| System-wide colour change | Custom theme (don't edit Daisy's CSS)                                      |
| Force a conflict win      | `!` suffix (v4: `bg-red-500!`) — sparingly                                 |
| Programmatic merge        | `tailwind-merge` (de-dupes, won't fix specificity)                         |

## Theme switcher

```ts
const toggle = () => {
  const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = next;
  localStorage.setItem("theme", next);
};
```

Apply pre-paint via inline `<head>` script to avoid flash.

## Anti-patterns

- Overriding component CSS via `!important` chains instead of custom theme
- Building brand-critical apps on Daisy then trying to escape — you'll fight every component
- Mixing component libs (Daisy + shadcn, Daisy + Mantine) — overlapping vocabularies, double the CSS
- Skipping ARIA on CSS-only modal/dropdown patterns in production
- Loading all 30 themes when you ship 2

## Red flags

| Thought                         | Reality                                        |
| ------------------------------- | ---------------------------------------------- |
| "I'll add `!important` here"    | Third one means custom theme.                  |
| "DaisyUI is faster than shadcn" | Until brand control matters. Then it's slower. |
| "I'll mix shadcn + Daisy"       | Two vocabularies, conflicts, bloat. Pick one.  |

## Hand-off

Tailwind base: `Skill(frontend-tailwind)`. Full-control alternative: `Skill(frontend-shadcn-ui)`. Tokens, colour systems, design-system layering: `Skill(frontend-design-essentials)`.
