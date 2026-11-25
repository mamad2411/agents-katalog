---
name: tanstack-seo
description: "Complete SEO setup for TanStack Router/Start: OG image generation (Satori + Resvg), meta helpers, JSON-LD structured data, sitemap, robots.txt, llms.txt, canonical URLs, Twitter Cards, web manifest."
---

# TanStack SEO

Complete SEO implementation for TanStack Router / TanStack Start projects. Nine layers covering crawlability, social sharing, structured data, and AI discoverability.

## Dependencies

```bash
# OG image generation (server-side only)
bun add satori @resvg/resvg-js
```

No other SEO-specific dependencies. Everything uses TanStack Router's built-in `head()` API and server route handlers.

## Architecture

```
src/
├── lib/
│   ├── seo.ts              # Centralized config, meta helpers, JSON-LD generators
│   ├── og-image.tsx         # Satori + Resvg OG image generator (JSX → SVG → PNG)
│   └── brand/index.ts       # Brand constants (name, description, social, keywords)
├── routes/
│   ├── __root.tsx           # Base HTML: charset, viewport, favicons, default OG, site-wide JSON-LD
│   ├── og[.]png.ts          # Server handler: GET /og.png?title=...&description=...
│   ├── sitemap[.]xml.ts     # Dynamic XML sitemap
│   ├── llms[.]txt.ts        # Concise site summary for AI crawlers
│   ├── llms-full[.]txt.ts   # Full content dump for AI crawlers
│   └── (every route)        # Per-route head() with title, description, canonical, OG, JSON-LD
└── public/
    ├── robots.txt           # Crawl rules + sitemap reference
    ├── site.webmanifest     # PWA manifest
    ├── favicon.svg/.png/.ico
    └── apple-touch-icon.png
```

## Setup Workflow

### 1. Create Brand Config

Create `src/lib/brand/index.ts`:

```typescript
export const brand = {
  name: "Your App",
  shortName: "App",
  description: "Your app description for SEO.",
  author: { name: "Your Name", url: "https://yoursite.com" },
  social: { twitter: "@yourhandle", github: "https://github.com/you/repo" },
  keywords: ["keyword1", "keyword2", "keyword3"],
} as const;
```

### 2. Create SEO Utility

See [references/seo-utilities.md](references/seo-utilities.md) for the complete `src/lib/seo.ts`. Provides:

- `siteConfig` — centralized site metadata
- `getAbsoluteUrl()` / `getCanonicalUrl()` — URL helpers
- `getOGImageUrl(title, description?)` — builds dynamic OG image URLs
- `generateMetaTags(seo)` — OG + Twitter + robots + keywords meta array
- `generateHead(seo)` — meta + canonical link tags (used in every route)
- Six JSON-LD generators: Organization, WebSite, Article, Breadcrumb, FAQ, Software

### 3. Create OG Image Generator

See [references/og-image.md](references/og-image.md) for:

- `src/lib/og-image.tsx` — Satori + Resvg engine with Google Fonts
- `src/routes/og[.]png.ts` — server route handler

### 4. Create Server Routes + Static Files

See [references/server-routes.md](references/server-routes.md) for:

- Dynamic sitemap at `/sitemap.xml`
- `robots.txt` (static in `public/`)
- `llms.txt` and `llms-full.txt` for AI crawlers
- `site.webmanifest` for PWA

### 5. Wire Up Root Layout + Per-Route Heads

See [references/route-patterns.md](references/route-patterns.md) for:

- `__root.tsx` head: charset, viewport, favicons, manifest, default OG/Twitter, site-wide JSON-LD
- Three per-route patterns: static pages, pages with custom OG, dynamic pages (blog/docs)

## Key Conventions

- **Filename escaping**: `[.]` escapes dots. `og[.]png.ts` → `/og.png`, `sitemap[.]xml.ts` → `/sitemap.xml`.
- **Title suffixing**: `generateMetaTags()` auto-appends `| Site Name` to titles that don't already include it.
- **Cache headers**: OG images 24h, sitemaps 1h, llms.txt 24h.
- **Server handlers**: Non-HTML routes (PNG, XML, plaintext) use `server.handlers.GET` with no React component.
- **`<html lang="en">`**: Set in the root layout.
