---
name: astro-core
description: "Shared reference for the Astro cluster: the rendering-mode decision (static / on-demand SSR / hybrid + server islands), hydration directives, the Content Layer & collections model, astro:env / sessions / actions conventions, and SSR adapter selection. USE WHEN deciding how an Astro page renders or where data comes from — the cross-cutting model the Astro spokes share. Implementation depth lives in astro-framework."
cluster: astro
version: 1.0.0
---

# Astro Core

Shared model for the `astro` cluster. The rendering and content decisions below shape every
page; keep them consistent. For full implementation, see `astro-framework`.

## 1. Rendering mode (decide first)

| Need | Mode |
|---|---|
| Content known at build time (marketing, docs, blog) | **Static (SSG)** — the default; fastest, cheapest |
| Per-request data (auth, personalization, form POST) | **On-demand (SSR)** — set `export const prerender = false` on that route |
| Mostly static with a few dynamic fragments | **Static page + server islands** (`server:defer`) — render the shell statically, stream the dynamic piece |
| Mixed across the site | **Hybrid** — static by default, opt specific routes into SSR |

**Ship static by default; opt into SSR only where required.** Server islands keep a page static
while deferring a dynamic fragment — prefer them over making the whole route SSR.

## 2. Islands & hydration

Astro ships zero JS by default. A framework component is static HTML unless you add a directive:

- `client:load` — hydrate immediately (above-the-fold interactivity).
- `client:idle` — when the browser is idle (non-urgent).
- `client:visible` — when scrolled into view (best default for below-the-fold).
- `client:media` — when a media query matches.
- `client:only` — skip SSR, render only on the client (for client-only libs).

Keep islands small and hydrate at the **latest** directive that works.

## 3. Content (Content Layer & collections)

- **Content collections** under `src/content/` (or configured) with a schema (`zod`) for typed, validated content.
- **Content Layer loaders**: `glob()` / `file()` for local content; **live loaders** for data fetched at request time; custom loaders for any source.
- Query with `getCollection` / `getEntry`; render Markdown/MDX via the entry's component.
- Docs/wiki publishing flows → `astro-wiki-publisher`.

## 4. Server conventions

- **`astro:env`** — typed, validated environment variables (declare `server`/`client`, secret/public). Use it instead of raw `import.meta.env` for anything sensitive or required.
- **Sessions** — server-side session storage (with an SSR adapter) for per-user state.
- **Actions** — typed server functions callable from the client with input validation; prefer over hand-rolled API routes for form/RPC.

## 5. SSR adapters

On-demand rendering needs an adapter matched to the host: `@astrojs/vercel`, `@astrojs/cloudflare`,
`@astrojs/node`, etc. Match the adapter to the deploy target; align its major with the Astro major.
Static-only sites need **no** adapter.

## 6. View transitions

`<ClientRouter />` enables SML-like cross-page transitions. Scripts don't re-run on client nav —
re-init on `astro:page-load`; `transition:persist` keeps element state across navigation. (Animation
specifics → creative-frontend's `astro-gsap-scrolltrigger`.)

## 7. Shared guardrails

- Static-first; SSR only where needed; server islands for dynamic fragments in static pages.
- Minimal islands, latest-working hydration directive.
- Typed content schemas; `astro:env` for secrets; actions over ad-hoc API routes.
- Adapter major aligned to Astro major; none for static.
- Re-init scripts across view transitions.
