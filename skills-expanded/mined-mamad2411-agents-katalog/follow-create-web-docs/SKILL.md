---
name: follow-create-web-docs
description: Single-page README + docs site with Comark Vue, deployed to Cloudflare Workers via GitHub CI
argument-hint: "[repo-path]"
related:
  - follow-create-web
  - follow-create-web-nuxt
  - follow-service-cloudflare
  - follow-lib-vue
  - run-docs
  - update-docs
  - follow-tool-github-actions
  - ship
  - report

---

## Goal

Build a single-page site that renders the repo's `README.md` (and `docs/` if present) with Comark Vue — nav shows the repo name, GitHub link, registry badges, theme toggle — deployed to Cloudflare Workers via GitHub Actions

## Scope

Use when you want a small docs site for a repo — not a heavyweight docs framework (use `/run-docs` for VitePress)

- Output: Vue + Vite app (single page), Comark renders markdown, deployed with `wrangler` + `cloudflare/wrangler-action`
- The source of truth is the files in the repo — `README.md` is required, `docs/` optional (glob `docs/**/*.md`)
- No router — every docs file renders in a single scroll, or a sidebar switcher within one page

## Execute

### 1. Detect Metadata

> Goal: Determine what the nav/docs must show

1. Repo name: from the git remote (`git remote get-url origin`) or the `package.json` name
2. Registries: publishable `package.json` → npm badge/link; `Cargo.toml` → crates.io; `pyproject.toml` → PyPI
3. Docs: if `docs/**/*.md` exists → enable the docs pane + sidebar TOC; if not → single README pane only

### 2. Scaffold App

> Goal: Vue + Vite app ready for Comark

1. Always prefer `create-docs` (the canonical generator) — `bunx create-docs` (or `npx create-docs`, repo: `wrikka/create-docs`) scaffolds the whole site per this spec; if the generator isn't usable (not published yet/network) → fall back to the manual steps below
2. Manual fallback: `bun create vite <name> --template vue-ts` (or add it to the existing repo as `site/` or `docs-site/`)
3. `bun add @comark/vue` plus plugins as needed (shiki for code highlight)
4. Comark Vue usage: `<Markdown>` must be inside `<Suspense>`, use `:value` or a slot
5. Bundle the markdown as strings via `import readme from '../README.md?raw'` (Vite raw imports) — no runtime fetching

### 3. Build Layout

> Goal: layout per spec — simple and clean

1. Nav: repo name on the left, right side = registry badges (npm/crates if present) + GitHub icon link + theme toggle icon (sun/moon)
2. Desktop (≥1024px): 2 columns — left README render with `position: sticky`, right docs with a sidebar TOC (if docs exist)
3. Mobile: README scrolls normally first — once scrolled to the end, the docs pane becomes an `h-screen` separate scroll
4. Keep the layout minimal — small CSS, system font, readable max-width

### 4. Deploy To Cloudflare Workers

> Goal: CI deploys on every push to main

1. `bun add -D wrangler` + `wrangler.toml` (assets point to `dist/`, SPA fallback)
2. GitHub Actions workflow: build then deploy assets with `cloudflare/wrangler-action@v3` + secrets `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`
3. Run `/run-docs` or `bun run build` + `wrangler deploy --dry-run` to verify before pushing

## Rules

### 1. Simplicity

- Single page only — don't add a router, don't add state management
- Minimal style: system font stack, one spacing scale, light/dark themes only
- Never hard-code the repo name/registry — detect from the actual repo

### 2. Content Integrity

- Render README/docs as-is — don't rewrite the content
- Internal links within the docs should work with the sidebar TOC

### 3. Safety

- Don't deploy for real without permission — build + dry-run only until the user confirms
- Use GitHub secrets for secrets only; never commit them

- Use /follow-lib-vue when needed
- Use /follow-service-cloudflare when needed
- Use /follow-tool-github-actions when needed
- Use /suggest-next-action when needed
- Use /follow-create-web when needed
- Use /follow-create-web-nuxt when needed
- Use /update-docs when needed
- Use /ship when needed
- Use /report when needed


## Expected Outcome

- Single-page site renders README (+docs) with Comark Vue per the layout spec
- Nav has the repo name, GitHub link, registry badges, and theme toggle
- GitHub Actions deploys to Cloudflare Workers and is ready to use
- Passes local build and `wrangler deploy --dry-run`
