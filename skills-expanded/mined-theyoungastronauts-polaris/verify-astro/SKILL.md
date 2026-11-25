---
name: verify-astro
description: "Astro verification checklist."
disable-model-invocation: true
---

# Skill: Verify Astro

## Purpose
Systematic verification checklist for Astro sites. Used by the reviewer agent after code execution.

## Verification Process

### 1. Zero-JS Budget
- [ ] No `client:*` directives on components that don't need interactivity
- [ ] Interactive islands use the least eager directive (`client:visible` > `client:idle` > `client:load`)
- [ ] No framework integration installed unless islands actually exist
- [ ] Build output shows zero or minimal JS bundles

### 2. Components
- [ ] Server logic stays in code fence (`---`), not in `<script>` tags
- [ ] Props are typed with `interface Props`
- [ ] Scoped `<style>` used (no `is:global` unless intentional)
- [ ] Components are reasonably sized (extract if >100 lines)
- [ ] `.astro` components preferred over framework components for non-interactive UI

### 3. Pages & Routing
- [ ] Every page has a `<title>` and `<meta name="description">`
- [ ] Dynamic routes have `getStaticPaths()` (static output)
- [ ] Layouts applied consistently (no orphan pages without layout)
- [ ] 404 page exists (`src/pages/404.astro`)

### 4. Content Collections
- [ ] Schema defined in `src/content.config.ts` with Zod validation
- [ ] Content queried with `getCollection()` / `getEntry()` (not raw file reads)
- [ ] Frontmatter matches schema (no runtime errors)
- [ ] `astro check` passes for content types

### 5. Styling
- [ ] DaisyUI semantic colors used (`base-100`, `primary`, etc.) — no hardcoded hex
- [ ] Responsive design works at mobile, tablet, desktop
- [ ] No unused global styles
- [ ] Font loading is optimal (self-hosted or `@fontsource`)

### 6. Performance
- [ ] Images use `<Image>` from `astro:assets` (not raw `<img>`)
- [ ] Above-fold images have `loading="eager"` or priority
- [ ] Below-fold images use `loading="lazy"`
- [ ] No unnecessary third-party scripts
- [ ] Build size is reasonable for content delivered

### 7. Accessibility
- [ ] Semantic HTML (`header`, `main`, `footer`, `nav`, `section`)
- [ ] Skip-to-content link present
- [ ] Images have alt text
- [ ] Interactive elements are keyboard accessible
- [ ] Color contrast meets WCAG AA

### 8. SEO
- [ ] Open Graph tags (`og:title`, `og:description`, `og:image`) on all pages
- [ ] Canonical URL set
- [ ] Sitemap generated (`@astrojs/sitemap` integration)
- [ ] `robots.txt` exists in `public/`

### 9. Code Quality
- [ ] No commented-out code
- [ ] No console.logs left in
- [ ] `astro check` passes
- [ ] TypeScript strict mode enabled
- [ ] Consistent naming conventions

### 10. Development Environment
- [ ] `Dockerfile.dev` exists and uses a supported LTS Node image (`node:22-alpine` or newer)
- [ ] `docker-compose.yml` exists with volume mounts
- [ ] `Makefile` exists and wraps all commands via `docker compose exec`
- [ ] No `npm run` / `npx` commands used directly on host

## Output
Produce a `verification-report.md` (same format as verify-django).
