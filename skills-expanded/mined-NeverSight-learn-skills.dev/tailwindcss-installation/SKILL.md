---
name: tailwindcss-installation
description: "Use this skill when installing Tailwind CSS v4 or fixing project setup. Covers choosing Vite, PostCSS, Tailwind CLI, webpack, framework guides, and Play CDN; packages `tailwindcss`, `@tailwindcss/vite`, `@tailwindcss/postcss`, `@tailwindcss/cli`, `@tailwindcss/webpack`, and `@tailwindcss/browser`; CSS entry imports, build commands, and common missing-output failures. Triggers on: install tailwind, setup tailwind, Vite, PostCSS, CLI, webpack, Play CDN, @tailwindcss/vite, @tailwindcss/postcss, @tailwindcss/cli, @tailwindcss/browser."
license: MIT
---

Tailwind CSS v4 setup is CSS-first: install the integration package for the build tool, import Tailwind from the CSS entry file, then let Tailwind scan source files and generate output CSS.

## Quick Start

Use Vite when the project uses Vite or a Vite-powered framework:

```bash
npm install tailwindcss @tailwindcss/vite
```

```ts
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss()],
});
```

```css
@import "tailwindcss";
```

**Related skills:** `tailwindcss-source-detection` (missing classes), `tailwindcss-functions-directives` (`@import` and `@source`), `tailwindcss-compatibility` (browser/build constraints), `tailwindcss-upgrade-v4` (v3 setup migration).

## Choose an integration

| Project shape | Use | Install |
|---|---|---|
| Vite or Vite-powered framework | Vite plugin | `npm install tailwindcss @tailwindcss/vite` |
| Next.js, Angular, PostCSS pipeline | PostCSS plugin | `npm install tailwindcss @tailwindcss/postcss postcss` |
| Plain static site or custom build | Tailwind CLI | `npm install tailwindcss @tailwindcss/cli` |
| webpack pipeline | webpack loader | `npm install tailwindcss @tailwindcss/webpack` |
| Browser-only demo | Play CDN | `<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>` |

Prefer Vite where it is already in the toolchain. Prefer the official framework guides when a framework has specific wiring.

## Core Patterns

### Vite

```bash
npm install tailwindcss @tailwindcss/vite
```

```ts
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss()],
});
```

```css
@import "tailwindcss";
```

Run the existing dev script, usually:

```bash
npm run dev
```

### PostCSS

```bash
npm install tailwindcss @tailwindcss/postcss postcss
```

```js
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

```css
@import "tailwindcss";
```

Use this for frameworks where CSS already flows through PostCSS.

### Tailwind CLI

```bash
npm install tailwindcss @tailwindcss/cli
```

```css
/* src/input.css */
@import "tailwindcss";
```

```bash
npx @tailwindcss/cli -i ./src/input.css -o ./src/output.css --watch
```

Link the generated CSS file in HTML or import it through the app's entry point.

### webpack

The Tailwind CSS v4.3 release notes document the dedicated `@tailwindcss/webpack` loader and state that it landed in v4.2. Use it in webpack projects instead of routing Tailwind through PostCSS only to reach the compiler.

```bash
npm install tailwindcss @tailwindcss/webpack
```

Add the loader in the CSS rule after the CSS loader/extraction loader used by the project. Verify exact loader order against the project and the official package README.

### Play CDN

Use the browser package for demos and quick experiments:

```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

Add custom Tailwind CSS features with:

```html
<style type="text/tailwindcss">
  @theme {
    --color-demo-500: oklch(0.7 0.18 245);
  }
</style>
```

Do not recommend Play CDN for production builds.

## Framework guides

The official docs include framework guides for common stacks such as Next.js, React Router, Angular, Astro, Laravel, Nuxt, SvelteKit, Solid, Qwik, Rails, Phoenix, Gatsby, Ember, Parcel, Rspack, Symfony, and others. If the user names a framework, prefer its guide over a generic recipe at `https://tailwindcss.com/docs/installation/framework-guides`.

## Common Mistakes

### [HIGH] Using v3 installation directives in v4

Wrong in a v4 project:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Correct:

```css
@import "tailwindcss";
```

### [HIGH] Installing only `tailwindcss` for CLI or PostCSS work

In v4 the CLI and PostCSS plugin are separate packages. Use `@tailwindcss/cli` for CLI builds and `@tailwindcss/postcss` for PostCSS.

### [MEDIUM] Generated CSS is not included in the page

If classes are present but styles do not appear, verify the compiled CSS file is linked in HTML or imported by the framework entry point. Tailwind may be building correctly while the app is serving another CSS file.

### [MEDIUM] Treating Play CDN as production setup

The browser package is for development and demos. Use a build integration for production.

## API Reference

- Official installation docs: `https://tailwindcss.com/docs/installation`
- Vite: `https://tailwindcss.com/docs/installation/using-vite`
- PostCSS: `https://tailwindcss.com/docs/installation/using-postcss`
- CLI: `https://tailwindcss.com/docs/installation/tailwind-cli`
- Play CDN: `https://tailwindcss.com/docs/installation/play-cdn`
- Framework guides: `https://tailwindcss.com/docs/installation/framework-guides`
