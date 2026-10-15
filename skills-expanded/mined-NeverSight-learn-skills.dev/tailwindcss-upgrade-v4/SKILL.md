---
name: tailwindcss-upgrade-v4
description: "Use this skill when upgrading Tailwind CSS v3 projects to v4 or diagnosing v3 patterns in a v4 project. Covers `npx @tailwindcss/upgrade`, Node.js 20+ requirement, browser support, package split (`@tailwindcss/postcss`, `@tailwindcss/vite`, `@tailwindcss/cli`), replacing `@tailwind` directives with `@import`, moving config to CSS `@theme`, removed/renamed utilities, opacity modifier replacements, outline/ring/shadow/radius/blur changes, and manual review strategy. Triggers on: upgrade Tailwind v4, migrate v3, @tailwind base, tailwind.config.js, content config, bg-opacity, flex-shrink, shadow-sm changed, outline-none, @tailwindcss/upgrade."
license: MIT
---

Tailwind CSS v4 is a breaking release. Use the official upgrade tool first when possible, then review the diff and test the UI in the browser.

## Quick Start

```bash
npx @tailwindcss/upgrade
```

Requirements:

- Run in a new branch.
- Node.js 20 or higher for the upgrade tool.
- Browser support must meet Tailwind v4 requirements: Safari 16.4+, Chrome 111+, Firefox 128+.

**Related skills:** `tailwindcss-installation`, `tailwindcss-compatibility`, `tailwindcss-theme`, `tailwindcss-source-detection`, `tailwindcss-functions-directives`.

## Migration Checklist

### 1. Decide whether v4 is allowed

Stay on v3.4 if the product must support browsers older than the v4 baseline.

### 2. Run the upgrade tool

```bash
npx @tailwindcss/upgrade
```

Review all changes. The tool handles most common migrations but complex projects may need manual edits.

### 3. Update package integration

PostCSS:

```js
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

Vite:

```ts
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss()],
});
```

CLI:

```bash
npx @tailwindcss/cli -i input.css -o output.css
```

### 4. Replace CSS entry directives

Wrong in v4:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Correct:

```css
@import "tailwindcss";
```

### 5. Move config toward CSS

Prefer `@theme`, `@source`, `@utility`, and `@custom-variant`. Use `@config` only as an incremental bridge for legacy JavaScript config.

```css
@theme {
  --font-display: Inter, sans-serif;
  --color-brand-500: oklch(0.68 0.18 245);
}
```

### 6. Replace removed utility patterns

Use slash opacity modifiers:

```html
<div class="bg-black/50 text-white/80 border-gray-950/10"></div>
```

Use modern short names:

| v3 | v4 |
|---|---|
| `flex-shrink-*` | `shrink-*` |
| `flex-grow-*` | `grow-*` |
| `overflow-ellipsis` | `text-ellipsis` |
| `decoration-slice` | `box-decoration-slice` |
| `decoration-clone` | `box-decoration-clone` |

### 7. Review renamed scale defaults

Some default scale names changed to make bare and named values consistent:

| v3 | v4 |
|---|---|
| `shadow-sm` | `shadow-xs` |
| `shadow` | `shadow-sm` |
| `drop-shadow-sm` | `drop-shadow-xs` |
| `drop-shadow` | `drop-shadow-sm` |
| `blur-sm` | `blur-xs` |
| `blur` | `blur-sm` |
| `backdrop-blur-sm` | `backdrop-blur-xs` |
| `backdrop-blur` | `backdrop-blur-sm` |
| `rounded-sm` | `rounded-xs` |
| `rounded` | `rounded-sm` |
| `outline-none` | `outline-hidden` when preserving forced-colors accessibility behavior |
| `ring` | `ring-3` |

Test visual diffs rather than assuming the names are equivalent.

## Common Mistakes

### [HIGH] Migrating package names but leaving v3 CSS directives

`@tailwind base/components/utilities` is v3 syntax. Use `@import "tailwindcss";`.

### [HIGH] Treating `tailwind.config.js` as the v4 source of truth

CSS is the primary configuration surface in v4. Keep `@config` only as a temporary bridge when needed.

### [MEDIUM] Skipping browser QA

The upgrade tool is mechanical. Verify key screens, dark mode, responsive layouts, forms, third-party widgets, and any CSS modules/component style blocks.

### [MEDIUM] Missing dynamic class issues exposed by v4 source detection

If styles disappear, load `tailwindcss-source-detection` and replace dynamic class construction with complete class maps.

## API Reference

- Upgrade guide: `https://tailwindcss.com/docs/upgrade-guide`
- Compatibility: `https://tailwindcss.com/docs/compatibility`
- Functions and directives: `https://tailwindcss.com/docs/functions-and-directives`
