---
name: astro-orchestrator
description: "Route an Astro task to the right spoke — building the site (components, islands/hydration, content, SSR, actions, i18n) or publishing a docs/wiki/press-kit site. USE WHEN working on an Astro project but the specific concern isn't named, or when deciding the rendering mode (static vs on-demand vs hybrid). For scroll/animation/video on an Astro page, hand off to the creative-frontend cluster."
cluster: astro
version: 1.0.0
---

# Astro Orchestrator

Entry skill for **Astro** site work (the framework itself — not the animation layer). It picks
the rendering strategy and routes to the right spoke. The rendering-mode decision, content
model, and hydration rules live in `astro-core`; read it before choosing static vs SSR or
wiring content collections.

## Cluster map (routing targets)

- `astro-core` — rendering mode (static / on-demand SSR / hybrid + server islands), hydration directives, Content Layer & collections, `astro:env` + sessions + actions, SSR adapter selection, view transitions.
- `astro-framework` — *(shared with creative-frontend)* the deep implementation skill: components, islands, hydration, Content Layer (glob/file/live loaders), `server:defer`, actions, i18n, SSR adapters, view transitions, React/Vue/Svelte/Solid integration.
- `astro-wiki-publisher` — publishing/hardening a docs/wiki/press-kit site: Markdown/MDX content, generated routes, copy QA, browser verification, Vercel/Cloudflare deploy.

## Routing Rules by Intent

- **Build the site** (components, layouts, islands, content, actions, i18n, SSR) → `astro-framework` (+ `astro-core` for the mode/content decision).
- **Choose how it renders** (SSG vs on-demand SSR vs hybrid; should this piece be a server island?) → `astro-core`, then `astro-framework`.
- **Publish a docs / wiki / press-kit** → `astro-wiki-publisher`.
- **Add scroll effects / animation / embedded video** → **creative-frontend cluster** (`astro-gsap-scrolltrigger`, `creative-frontend-orchestrator`).

## Standard Operating Flow

1. Establish the rendering mode and content source from `astro-core` (it shapes everything else).
2. Delegate build work to `astro-framework`; publishing/QA to `astro-wiki-publisher`.
3. For motion on the page, redirect to the creative-frontend cluster.
4. Return: rendering mode chosen, adapter (if SSR), content strategy, next action.

## Guardrails

See `astro-core`. In short: **ship static by default**, opt into on-demand SSR only where you
need it (and add server islands for dynamic fragments inside static pages); keep islands minimal
and hydrate at the latest directive that works (`client:visible`/`idle` over `load`); validate
secrets through `astro:env` rather than raw `import.meta.env` on the server.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
