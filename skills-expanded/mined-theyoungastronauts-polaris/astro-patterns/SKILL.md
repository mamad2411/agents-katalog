---
name: astro-patterns
description: "Astro project conventions: components, content collections, islands, and styling. Apply when writing or reviewing Astro code."
paths: ["**/*.astro"]
---

# Skill: Astro Patterns

## Purpose
Guide Claude Code when building Astro sites (landing pages, marketing, docs). Targets Astro 5.x. Follow these conventions unless the project's CLAUDE.md overrides them.

## Project Structure
- File-based routing from `src/pages/`
- Components in `src/components/` organized by section (`layout/`, `landing/`, `ui/`)
- Layout templates in `src/layouts/`
- Content collections in `src/content/` with schema in `src/content.config.ts`
- Global styles in `src/styles/`
- Static assets in `public/`
- `@/*` path alias via tsconfig

## Components (.astro files)
- Code fence (`---`) for server-only TypeScript — never sent to browser
- Define `Props` interface above usage, destructure from `Astro.props`
- PascalCase filenames matching component name (`Hero.astro`, `FeatureGrid.astro`)
- Scoped `<style>` by default — use `is:global` only when intentional
- Prefer `.astro` components over framework components unless interactivity is needed
- Use `<slot />` for child content; named slots with `<slot name="footer" />`

## Islands (Interactive Components)
- Only add `client:*` directives when JavaScript interactivity is truly required
- `client:load` — immediately interactive (nav menus, forms with validation)
- `client:idle` — hydrate when browser idle (carousels, counters)
- `client:visible` — hydrate when scrolled into view (comment sections, chat)
- `server:defer` — defer server rendering for personalized content
- Each island hydrates independently — keep them small and self-contained
- To add a framework: `npx astro add react` (or vue, svelte, solid) inside the container
- No framework integration is installed by default — add only when you need an island

## Pages & Routing
- Each `.astro` file in `src/pages/` = one route (`index.astro` → `/`, `about.astro` → `/about`)
- Wrap page content in a layout component: `<BaseLayout title="About">...</BaseLayout>`
- Dynamic routes use `[param].astro` or `[...slug].astro` with `getStaticPaths()`
- Set page metadata via layout props (`title`, `description`)
- Always create `src/pages/404.astro` for custom 404

## Content Collections
- Define schemas in `src/content.config.ts` using `defineCollection` with Zod
- Query with `getCollection('blog')` / `getEntry('blog', 'my-post')`
- Render markdown content with the `<Content />` component
- Frontmatter is type-safe and validated at build time

## Styling
- Tailwind v4 via `@tailwindcss/vite` plugin (Astro uses Vite natively)
- DaisyUI as `@plugin "daisyui"` in global CSS
- DaisyUI semantic colors: `base-100`, `base-content`, `primary` — never hardcoded hex
- Scoped `<style>` in `.astro` files for component-specific overrides
- Responsive-first: mobile breakpoints before desktop

## Naming
- Components: PascalCase (`Hero.astro`, `FeatureCard.astro`)
- Pages: kebab-case matching URL slugs (`about-us.astro`, `contact.astro`)
- Layouts: PascalCase with Layout suffix (`BaseLayout.astro`, `BlogLayout.astro`)
- Content collections: kebab-case directories and files
- CSS custom properties: `--color-*`, `--font-*`, `--spacing-*`

## Development Environment
- All commands run via `make` (Docker Compose under the hood) — never run `npm` directly on host
- Use `/astro-bootstrap` when setting up a new project from scratch
- `make dev` starts the dev server (default port 4321)
- `make astro-check` for TypeScript and template validation
- `make build` for production static build, `make preview` to test it locally

## SEO & Performance
- Set `<title>` and `<meta name="description">` on every page via layout props
- Use `<ViewTransitions />` from `astro:transitions` for smooth page navigation
- Images: use `<Image>` from `astro:assets` for automatic optimization
- Fonts: self-host via `@fontsource` packages — no external CDN requests
- Include OG tags (`og:title`, `og:description`, `og:image`) on all pages
- Add `@astrojs/sitemap` integration for automatic sitemap generation
- Place `robots.txt` and favicons in `public/`
