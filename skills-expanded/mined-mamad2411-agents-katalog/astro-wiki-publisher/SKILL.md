---
name: astro-wiki-publisher
description: Use when publishing or hardening an Astro docs/wiki/press-kit site with Markdown or MDX content, generated routes, artifact data, public copy QA, browser verification, Vercel or Cloudflare deploy checks, or README/docs media outputs.
cluster: astro
version: 1.0.0
---

# Astro Wiki Publisher

## Purpose

Coordinate the full publishing loop for content-driven Astro wikis: content collections, Markdown rendering, navigation, artifact data, public-copy quality, browser verification, media artifacts, and deploy truth.

## Required Skill Routing

- Use `astro-framework` for Astro 5+, content collections, routing, i18n, hydration, view transitions, adapters, images, and static/server output decisions.
- Use `markdown-rendering-regression` before claiming Markdown or public copy is fixed.
- Use `webapp-testing` or `browser` for local preview, console errors, failed requests, screenshots, and layout overflow checks.
- Use `site-architecture` for docs hierarchy, sidebars, route naming, breadcrumbs, and internal linking.
- Use `copywriting`, `copy-editing`, `seo-audit`, and `ai-seo` for public reader/press copy and metadata.
- Use `notebooklm` for live NotebookLM notebook/source/artifact verification.
- Use `r2-notebooklm-artifact-portal` for R2-backed public artifact URLs, MIME, cache, and playback validation.
- Use `cloudflare` or `wrangler` for Cloudflare platform operations only; do not duplicate platform syntax here.
- Use `mermaid-to-gif` for animated Mermaid process/architecture visuals.
- Use `hyperframes-cli` for launch trailer or video composition dev loop.
- Use `animejs` only for deterministic HyperFrames micro-animations, not for live Astro route scroll behavior.

## Workflow

1. Confirm repo truth: cwd, branch, remote, dirty state, package manager, Astro version, and deploy target.
2. Read `AGENTS.md`, `DESIGN.md`, `astro.config.*`, `package.json`, `src/content.config.*` or `src/content/**`, route files, and verification scripts.
3. Map public routes: expected routes, generated routes, sidebar/nav routes, artifact routes, and localized aliases.
4. Verify content: frontmatter descriptions, rendered Markdown, public copy, no placeholders, no local paths, no internal wave/build/run labels, no raw artifact wording.
5. Verify artifacts: local `src/data/artifacts.json`, public `href`/`thumbnail` URLs, R2 HEAD responses, MIME, cache headers, and audio/video playback affordances.
6. Verify browser behavior: local preview, console errors, failed network requests, keyboard-visible routes where applicable, and typography overflow at mobile/tablet/desktop widths.
7. Verify deploy truth: build output, pushed branch, remote head, hosting deployment state, and live URL behavior before claiming production status.

## Required Verification

Prefer a single repo script such as:

```bash
bun run verify:all
```

If unavailable, run the equivalent:

```bash
bun run verify:data
bun run build
bun run verify:routes
bun run verify:html
bun run verify:routes:inventory
bun run verify:browser
bun run verify:r2
```

Report any skipped command with the reason.
