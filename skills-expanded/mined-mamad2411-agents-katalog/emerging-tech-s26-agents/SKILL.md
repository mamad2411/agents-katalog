# AGENTS.md — Coding Agent Guidelines

This file provides guidance for agentic coding agents working in this repository.

## Project Overview

Course syllabus website for **PSAM 2802: Photo Processes: Emerging Technologies** (Spring 2026).
Built with **Astro 5** (static site generator), deployed to GitHub Pages.

**Live site**: https://taipinc.github.io/emerging-tech-s26  
**Dev server**: http://localhost:4321/emerging-tech-s26

---

## Build & Development Commands

```bash
# Install dependencies
npm install

# Start dev server (localhost:4321/emerging-tech-s26)
npm run dev

# Build production site to ./dist/
npm run build

# Preview production build locally
npm run preview
```

### No test, lint, or format scripts are configured.

There is no test framework, no ESLint, and no Prettier in this project. The only type-checking
available is via the Astro toolchain:

```bash
# Run Astro's TypeScript type-checker (uses @astrojs/check)
npx astro check
```

Run `npx astro check` after any significant changes to `.astro` files or TypeScript to catch
type errors before deploying.

---

## Architecture & Key Files

| File / Directory | Purpose |
|---|---|
| `src/layouts/MainLayout.astro` | Base HTML layout: two-column split, collapse button, p5.js & highlight.js CDN tags |
| `src/pages/index.astro` | Main page: all build-time data loading, markdown parsing, schedule rendering, client-side routing |
| `src/styles/global.css` | All styles (layout, typography, tables, mobile responsive) |
| `src/content/menu.md` | Left-column course info & description |
| `src/content/weeks/*.md` | Weekly schedule entries with frontmatter (`order`, `date`, `theme`, `status`) |
| `src/content/assignments/*.md` | Assignment content loaded dynamically |
| `src/content/readings/*.md` | Reading content loaded dynamically |
| `src/content/workshops/*.md` | Workshop content loaded dynamically |
| `src/content/projects/*.md` | Project content loaded dynamically |
| `src/content/default.md` | Default right-column landing page (supports `heroImage` frontmatter) |
| `src/content.config.ts` | Astro Content Collections schema definitions |
| `astro.config.mjs` | Astro config (`site` + `base` for GitHub Pages) |
| `public/files/` | Static PDFs and documents |
| `public/images/` | Static images |
| `public/sketches/` | p5.js sketch `.js` files embedded in markdown |
| `.github/workflows/deploy.yml` | GitHub Actions: build and deploy to GitHub Pages on push to `main` |

---

## Content Loading Pattern

Content is **not** loaded via Astro's `getCollection()` API at runtime. Instead, all markdown
files are read at **build time** inside the `---` frontmatter block of `index.astro` using
Node's `fs/promises`:

```ts
// Pattern used in index.astro
import { readdir, readFile } from 'node:fs/promises';
import { join, relative, extname } from 'node:path';
```

A recursive `readContentDir()` function builds a flat `Record<string, string>` keyed by
relative path (e.g., `"assignments/week-01-a"`). This entire map is serialized to JSON and
embedded in a `<script type="application/json">` tag for client-side routing.

---

## Link Formats in Markdown

| Syntax | Behavior |
|---|---|
| `[Label](@assignments/week-01-a)` | Internal link — loads content from `src/content/` |
| `[Label](https://...)` | External — opens in new tab; "Lecture" prefix gets emoji |
| `[Label](/emerging-tech-s26/files/doc.pdf)` | File link (.pdf, .doc, etc.) — opens in new tab |

Internal link emoji prefixes (applied automatically by `transformLinks()`):
- `@workshops/...` → 🧰
- `@assignments/...` → 🧩
- `@readings/...` → 📙
- `@projects/...` → 🚀
- `@presentations/...` → 🖼️

---

## p5.js Sketch Embedding

Use the custom `<sketch>` element in markdown to embed interactive p5.js sketches:

```html
<sketch src="sketch-name.js"></sketch>
```

Sketches are loaded from `public/sketches/`. Each sketch runs in p5.js instance mode.
Active instances are tracked and cleaned up on content navigation.

---

## Code Style Guidelines

### TypeScript

- **Strict mode** is enabled via `astro/tsconfigs/strict` — never disable or bypass it.
- Use explicit types for function parameters and return values.
- Define interfaces for complex data shapes (e.g., `interface WeekData { ... }`).
- Use `as TypeName` casts only when necessary and the type is genuinely known.
- `moduleResolution: "bundler"` — use ESM-style imports everywhere.

### Astro Components

- **Indentation**: 4 spaces (not tabs).
- Keep build-time logic inside the `---` frontmatter block; keep the HTML template clean.
- Use `set:html` directive for injecting pre-rendered HTML strings.
- Use `<Fragment set:html={...} />` to inject HTML without wrapper elements.
- Use `is:inline` on `<script>` tags when the script must run without Astro bundling (e.g.,
  simple DOM setup, CDN-loaded library initialization).
- Use `import.meta.env.BASE_URL` for asset paths to ensure correct GitHub Pages prefixing.
- Named slots: `slot="left"`, `slot="right"` in `MainLayout.astro`.

### JavaScript / Client-side Scripts

- All client-side code lives in `<script>` tags within `.astro` files — no separate `.js` modules.
- Hash-based routing: listen for `hashchange` and `load` events; swap `innerHTML` of the
  content container.
- Mobile breakpoint: `max-width: 768px` — detect with `window.matchMedia`, not CSS classes.
- Never use `document.write()` or synchronous XHR.

### CSS

- **No CSS preprocessor** — plain CSS only.
- CSS custom properties (variables) are defined on `:root`:
  - `--color-menu`, `--color-content`, `--color-schedule`, `--color-menu-hover`
- Use `box-sizing: border-box` universally (already set via `* { box-sizing: border-box }`).
- Layout: flexbox for columns; CSS Grid (`display: grid` on `<table>`) for the schedule table.
- Transitions: `0.3s ease` for layout shifts, `0.15s ease` for opacity fades.
- Single responsive breakpoint at `@media (max-width: 768px)`.
- Indentation: 4 spaces.

### Markdown Content Files

- Week files (`src/content/weeks/*.md`) require frontmatter fields: `order` (number),
  `week` (number or string), `date` (string), and optionally `theme` and `status`.
- Use `## Content` and `## Due` section headers in week files — these are parsed by regex.
- File names: use kebab-case, no spaces (e.g., `week-01-a.md`, `my-document.pdf`).
- Avoid spaces in filenames anywhere under `public/` — use URL-encoded paths or rename.

### Naming Conventions

- **Files**: kebab-case for all content and asset files.
- **CSS classes**: BEM-like, descriptive (`.left-column`, `.menu-collapsed`, `.schedule-table`).
- **TypeScript interfaces**: PascalCase (e.g., `WeekData`).
- **Variables**: camelCase; prefer `const` over `let`; avoid `var`.
- **Functions**: camelCase, descriptive verb-noun (e.g., `readContentDir`, `transformLinks`).

### Error Handling

- In build-time `async` frontmatter code, allow errors to propagate — Astro will surface them
  during `npm run build` with a clear error message.
- In client-side scripts, use `try/catch` around `fetch()` calls and dynamic content
  operations; log errors to `console.error()`.
- p5.js sketch errors should be caught per-sketch and logged without crashing the page.

---

## Deployment Notes

- Deploys automatically via **GitHub Actions** on push to `main` branch.
- Workflow file: `.github/workflows/deploy.yml`
- Always run `npm run build` locally before merging to `main` to catch build-time errors.
- The `base: '/emerging-tech-s26'` in `astro.config.mjs` must remain set for GitHub Pages
  asset paths to resolve correctly.
- Never commit build artifacts (`dist/`) — they are gitignored and generated by CI.

---

## What Does Not Exist (Do Not Add Without Discussion)

- No linter (ESLint) — do not add linting config unless asked.
- No formatter (Prettier/Biome) — do not auto-format files; preserve existing style.
- No test framework — do not add test files unless explicitly requested.
- No React, Vue, Svelte, or other UI framework integrations.
- No CSS preprocessor (Sass, Less, PostCSS).
- No Astro middleware, server endpoints, or SSR — this is a purely static site.
