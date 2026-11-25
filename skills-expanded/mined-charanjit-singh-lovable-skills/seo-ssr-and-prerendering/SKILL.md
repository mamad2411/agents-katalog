---
name: seo-ssr-and-prerendering
description: >-
  Use when a Lovable SPA needs Google or social crawlers to see populated HTML:
  SSR, prerendering, react-snap, prerender.io, vite-ssg, or migrating routes to
  static. Not for fully authenticated apps with no public surface.
---

# SEO SSR and prerendering

Lovable apps are Vite + React SPAs. Crawlers and link-preview bots see an empty `<div id="root"></div>` until JS runs. **Public marketing pages must ship populated HTML** — Google does run JS, but indexing is slower and less reliable than HTML-first; Twitter/LinkedIn/Slack/Discord bots do not run JS at all.

Companion skills: [`seo-meta-tags-spa`](../seo-meta-tags-spa/), [`seo-landing-page`](../seo-landing-page/), [`tanstack-prefetch-and-hydration`](../tanstack-prefetch-and-hydration/), [`programmatic-seo-pages`](../programmatic-seo-pages/).

## When to use what

| Site type | Recommended approach |
|-----------|----------------------|
| Marketing site + blog + a few public routes | **Build-time prerender** (vite-plugin-prerender, react-snap, or `vite-ssg`) |
| Hundreds/thousands of pages from data (locations, comparisons) | **Static generation** (`vite-ssg` with route iterator) |
| Truly dynamic public pages updated minute-to-minute | **SSR** via a Node server (Cloudflare Pages Functions, Vercel, Render) |
| Hybrid: SPA app + a few public marketing routes | **Prerender just the public routes** |

Start with prerendering; move to SSR only when content changes too fast for a rebuild.

## Build-time prerender (vite-ssg pattern)

```ts
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  // vite-ssg config in package.json or its own file
});
```

```ts
// src/main.tsx
import { ViteSSG } from "vite-ssg";
import App from "./App";
import { routes } from "./routes";

export const createApp = ViteSSG(App, { routes }, ({ app, router, isClient, initialState }) => {
  // hydrate or set up per-app state
});
```

For each public route, expose an `includedRoutes` generator that lists URLs (e.g. one per blog post slug, one per location).

## Prerender service (prerender.io / Browserless)

If you can't change the build pipeline:

1. Add a serverless function or middleware that detects bot User-Agents and proxies to prerender.io.
2. Prerender.io caches the rendered HTML and serves it to crawlers.

This is fine as a stopgap but slower and not free at scale.

## react-snap (alternative, low-effort)

```bash
npm i -D react-snap
```

```json
{
  "scripts": { "postbuild": "react-snap" }
}
```

Edit `index.html` to use `hydrateRoot` instead of `createRoot` so the prerendered HTML hydrates cleanly.

Caveats: react-snap is unmaintained but still works for static SPAs.

## Hydration with data

Don't prerender a "loading…" shell. Either:

- Fetch data at build time and pass it through, or
- Use [`tanstack-prefetch-and-hydration`](../tanstack-prefetch-and-hydration/) to embed a dehydrated cache and hydrate on the client without a refetch flash.

## Routes to prerender — checklist

- `/` (home)
- `/pricing`
- `/blog` and every `/blog/[slug]`
- `/about`, `/contact`, `/changelog`, `/legal/*`
- Programmatic templates (`/integrations/[tool]`, `/locations/[city]`) — see [`programmatic-seo-pages`](../programmatic-seo-pages/)
- 404 page (`/404.html`)

Do **not** prerender authenticated routes (`/app`, `/dashboard`, `/settings`) — they should redirect to login.

## Verify

For every public URL, raw HTML must include the title, meta, and main content:

```bash
curl -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" \
  https://your-domain.com/pricing | grep -iE '<title|<h1|og:title'
```

Also check Twitter card / Open Graph rendering: `https://cards-dev.twitter.com/validator`, `https://developers.facebook.com/tools/debug/`.

## Avoid

- Shipping a Lovable marketing site as a pure SPA and hoping Google figures it out.
- Prerendering authenticated routes and leaking dashboard chrome to crawlers.
- Different HTML for bots vs users (cloaking) — Google penalizes.
- Forgetting `hydrateRoot` after introducing prerender — causes a re-render flash.

## Checklist

- [ ] Every public route ships with title, meta, h1, and primary copy in raw HTML.
- [ ] OG image and Twitter card validated in third-party debuggers.
- [ ] Auth routes excluded from prerender.
- [ ] Sitemap and robots.txt in sync with prerendered URL list ([`seo-sitemap-generation`](../seo-sitemap-generation/)).
