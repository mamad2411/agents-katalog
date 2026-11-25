---
name: seo-standards
description: Technical SEO for Next.js and Shopify — metadata, canonical URLs, structured data, sitemaps/robots, redirects, crawlability, Core Web Vitals, and i18n. Use when building or reviewing public/indexable pages, changing routes, or auditing a site's SEO.
---

# SEO Standards

Apply these when authoring or reviewing any publicly indexable page (Next.js or Shopify). Search visibility is a product surface: treat SEO regressions like functional bugs. Cross-reference `frontend-performance` for Core Web Vitals work.

## Metadata (Next.js App Router)

- Every indexable route exports metadata. Use static `export const metadata` when values are fixed; use `generateMetadata` when they depend on params/data.
- Always set `title`, `description`, `alternates.canonical`, `openGraph`, and `twitter`. Set `metadataBase` once in the root layout so relative OG/image URLs resolve.
- Titles: unique per page, front-load the primary keyword, keep under ~60 chars. Descriptions ~150–160 chars, written for humans (they drive CTR, not ranking).

```tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const p = await getProduct(params.slug);
  return {
    title: `${p.name} — Brand`,
    description: p.summary,
    alternates: { canonical: `/products/${p.slug}` },
    openGraph: { title: p.name, images: [{ url: p.image, width: 1200, height: 630 }], type: 'website' },
    twitter: { card: 'summary_large_image', title: p.name, images: [p.image] },
  };
}
```

- OG images: 1200×630, absolute URL. Prefer `next/og` (`ImageResponse`) for dynamic cards over hand-maintained static images.

## Canonical URLs & duplicate content

- One canonical URL per piece of content. Set `alternates.canonical` explicitly — never let query params (`?sort=`, `?utm_`, `?page=`) mint duplicate indexable URLs.
- Faceted/filter/sort params must canonicalize to the clean URL (or be `noindex`). Paginated lists canonicalize to their own page, not to page 1.
- Enforce one host + one scheme (https, no `www`↔apex split). Redirect the rest 301.
- Trailing-slash policy must be consistent site-wide (config it once) and match canonicals.

## Structured data (JSON-LD)

- Emit JSON-LD as a `<script type="application/ld+json">` in the page. Match schema type to page: `Product` (+ `Offer`, `AggregateRating`) on PDPs, `Article` on posts, `BreadcrumbList` on any nested page, `Organization`/`WebSite` in the root layout.
- Only mark up content actually visible on the page. Keep prices/availability in sync with the real data or you risk manual penalties.
- Validate every schema change against Google's Rich Results Test and schema.org. Broken JSON-LD is a review finding.

## Sitemaps & robots

- Generate `sitemap.xml` from real data — a `sitemap.ts` route handler (or `next-sitemap`) that enumerates dynamic routes. Include `lastmod`; exclude `noindex`/redirected/auth-gated URLs. Split >50k URLs into a sitemap index.
- `robots.ts` sets crawl rules and points to the sitemap. Block admin/cart/checkout/search-result URLs; never block CSS/JS needed to render.
- Guard staging: staging must be `Disallow: /` + `noindex` and must never share a robots/sitemap with production.

## Redirect discipline

- **Every route removal or slug change needs a 301** to the closest live equivalent. A deleted URL that 404s (or worse, soft-404s) drops its rankings and backlinks.
- 301 = permanent (moved/renamed, passes signals). 302 = temporary only (A/B, geo, transient). Do not use 302 for real moves.
- Maintain a redirect map (in `next.config` `redirects()`, middleware, or a data-driven table) alongside the route change in the same PR. Avoid redirect chains and loops — collapse A→B→C to A→C.

## Rendering & crawlability

- Public, indexable content must be server-rendered (SSR or ISR) so crawlers see it in the initial HTML. **Client-only rendering of indexable content is a finding** — if the body text/product data only appears after hydration, it is at risk.
- ISR (`revalidate`) is the default for content that changes but not per-request; SSG for truly static; SSR for personalized/real-time.
- **Changing a page's rendering strategy** (e.g. SSG→SSR, or moving content client-side) affects crawlability and cost — that is a gated architecture decision (see `docs/02-approval-gates.md`), not a silent refactor.
- Ensure real `<a href>` links (crawlable) rather than click handlers for navigation.

## Core Web Vitals

CWV (LCP, INP, CLS) is a confirmed ranking factor. Treat regressions as SEO regressions. Reserve image/embed dimensions to protect CLS, prioritize the LCP image (`priority`), and keep field data (CrUX/RUM) green. Full technique lives in `frontend-performance`.

## Shopify specifics

- Set theme SEO defaults: title/meta templates, social image, and homepage title/description in theme settings.
- Product/collection templates must emit liquid-generated `<title>`, meta description, canonical, and Product/Breadcrumb JSON-LD. Don't duplicate Shopify's built-in canonical.
- Collection URLs with `?sort_by=` / tag filters create duplicate content — ensure Shopify's canonical points to the clean collection URL and don't link to param variants internally.
- Handle (slug) changes: Shopify keeps the old handle only sometimes — add a URL redirect in Navigation → URL Redirects for every changed handle.
- Blog/article pages: set the article excerpt as the meta description and Article JSON-LD.

## i18n / hreflang

- Localized pages need reciprocal `hreflang` (via `alternates.languages` in Next.js metadata, or theme hreflang tags in Shopify), including an `x-default`.
- Each locale gets its own canonical (self-referencing), not a canonical pointing at the default locale.
- Keep locale routing crawlable (path or subdomain, not JS-switched content).

## Audit checklist

1. Crawl (Screaming Frog / URL Inspection): status codes, redirect chains, orphan pages, duplicate titles/descriptions.
2. Index coverage (Search Console): excluded/soft-404/duplicate reports clean.
3. CWV: field data passing for the templates that matter (PDP, PLP, article, home).
4. Structured data: valid, no errors/warnings in Rich Results Test.
5. Sitemaps submitted, current, and matching live indexable URLs.

## PR-review checklist (SEO-affecting diffs)

- Route removed/renamed → 301 redirect added in the same PR.
- New indexable page → metadata (title/description/canonical/OG) present and unique.
- Indexable content rendered server-side, not client-only.
- Structured data added/changed → validated.
- No accidental `noindex`/`Disallow` on production pages; no staging config leaking to prod.
- Rendering-strategy change → ADR present (gated).
