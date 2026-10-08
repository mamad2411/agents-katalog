# CLAUDE.md

Guidance for working in the Danet documentation site.

## What this is

This repo is the **documentation website** for
[Danet](https://github.com/Savory/Danet) (`@danet/core`), the NestJS-inspired
backend framework for Deno. It is a [VitePress](https://vitepress.dev) site
published to [docs.danet.land](https://docs.danet.land) (the `Savory/docs`
GitHub repo). It contains **only docs** — no framework source code lives here.

Content is plain Markdown under `src/`. The sidebar is generated automatically
from the directory structure, so most contributions are just adding or editing
a `.md` file with the right frontmatter.

## Commands

This is a Node project (not Deno). A `yarn.lock` is checked in (a
`package-lock.json` is also present); prefer `yarn`.

```bash
# Install dependencies (no node_modules is checked in)
yarn install

# Run the docs locally with hot reload
yarn docs:dev

# Production build (outputs to .vitepress/dist, then copies public/* into it)
yarn docs:build

# Preview the production build
yarn docs:preview
```

## Architecture

- `src/` — all documentation pages (`srcDir` in the VitePress config). Markdown
  only.
- `.vitepress/config.ts` — top-level VitePress config (title, search, social
  links, locales). `ignoreDeadLinks` is **on**, so broken links won't fail the
  build — double-check links yourself.
- `.vitepress/locales/` — per-locale config (`en.config.ts`, `fr.config.ts`,
  `pt.config.ts`). Only `en` (root) and `fr` are wired into `config.ts` today;
  `pt.config.ts` exists but is not currently mounted.
- `.vitepress/sidebar.ts` + `.vitepress/generate-sidebar.ts` — the sidebar is
  **auto-generated** from the `src/` tree (a vendored fork of
  `vitepress-sidebar`). You normally never edit the sidebar by hand.
- `.vitepress/theme/` — custom theme tweaks (`custom.css`, `index.js`).
- `public/` — static assets (logos, images) copied as-is to the site root
  (referenced as `/danet-logo.png`, etc.).
- `src/index.md` — the home page, using VitePress's `layout: home` hero.

### Content layout

Pages are grouped into top-level section directories under `src/`, each
becoming a collapsible sidebar group:

- `introduction/` — welcome / getting started.
- `overview/` — core building blocks (controllers, modules, injectables,
  guards, middlewares, exception filters, renderer, static files).
- `fundamentals/` — DI deep-dives (scopes, custom injectables, dynamic modules,
  execution context, lifecycle).
- `techniques/` — cross-cutting features (cors, sessions, events, sse,
  task-scheduling, kvQueue, compression, databases, rate-limiting, ...).
- `openapi/`, `recipes/`, `migration/`, `websockets/`, `zod/` — focused topics.
- `cli.md`, `deno-deploy.md`, `license.md` — standalone top-level pages.

## Conventions

### Page frontmatter

Every content page starts with YAML frontmatter that drives its sidebar entry:

```markdown
---
label: Rate Limiting   # text shown in the sidebar (falls back to the filename)
order: 70              # sort key WITHIN the section
---
```

**Ordering is descending**: a higher `order` appears *higher* in the sidebar.
When inserting a page, pick an `order` relative to its siblings (compare the
other files in the same directory). Existing `techniques/` orders, for example,
run from `databases: 90` down to `sse: 20`.

### Section (directory) config

Each section directory has an `index.yml` controlling the *group*:

```yaml
order: 90        # position of this whole section in the sidebar (descending)
expanded: false  # whether the group starts expanded
# label: Custom  # optional; defaults to a capitalized directory name
```

### Code blocks

The dominant convention is a language **plus a filename** on the fence info
string (the filename renders as a tab/label):

````markdown
```typescript app.module.ts
import { Module } from 'jsr:@danet/core';
```
````

A legacy `@@filename(name)` directive appears in one older page — don't add new
uses of it; prefer the fence-with-filename form. Import framework symbols from
`jsr:@danet/core` in examples (matching how users consume the published
package).

### Links

Use root-relative links to other pages, e.g. `/overview/guards`. Because
`ignoreDeadLinks` is enabled, verify links manually.

## Internationalization

English is the root locale (`src/*`). Translations live in a mirrored subtree —
currently `src/fr/` for French. `src/fr` is excluded from the English sidebar
(`excludeDir: ['fr']` in `sidebar.ts`) and surfaced through the `fr` locale.
When you add or restructure an English page, the French tree will drift out of
sync until a matching `src/fr/...` page is added — note this rather than
silently leaving it.

## Adding a new page (typical workflow)

1. Create `src/<section>/<page>.md`.
2. Add frontmatter with a `label` and an `order` chosen relative to the
   section's existing pages.
3. Write the content (fence-with-filename code blocks, `jsr:@danet/core`
   imports, root-relative links).
4. Run `yarn docs:dev` and confirm the page appears in the right sidebar group
   at the right position.
5. If the feature exists in the framework, keep terminology and the public API
   (decorator/module names, option shapes) consistent with the `@danet/core`
   source.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
