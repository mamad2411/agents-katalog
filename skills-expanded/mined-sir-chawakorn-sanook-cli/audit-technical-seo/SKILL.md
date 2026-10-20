---
name: audit-technical-seo
description: Audits and fixes technical/on-page SEO — meta tags, Open Graph/Twitter cards, JSON-LD structured data, canonicals, sitemap, robots.txt; used when improving discoverability or fixing crawlability.
when_to_use: When the user wants SEO improvements, mentions meta tags, Open Graph, schema.org/JSON-LD structured data, sitemap, robots.txt, canonical URLs, crawlability, or indexing.
---

## When to Use

Trigger this skill when the request involves: improving search discoverability/indexing, adding or fixing `<title>`/`<meta>` tags, Open Graph or Twitter Card previews, schema.org / JSON-LD structured data, canonical URLs, `sitemap.xml`, `robots.txt`, `hreflang`, or "why isn't this page showing up / previewing right on social". No API keys, crawler accounts, or paid tools required — this is static analysis + code fixes on the project's own source.

Skip if the ask is about off-page SEO (backlinks, content strategy, keyword research) or Core Web Vitals performance — those are different jobs (use a Lighthouse/perf pass for the latter).

## Steps

Detect the stack first, then audit head-out. Output a **missing-items report** with concrete diffs, don't just describe.

1. **Detect framework + render mode.** `grep -rl "next" package.json` etc. Branch:
   - Next.js App Router → `export const metadata` / `generateMetadata()` in `layout.tsx`/`page.tsx`. Do NOT hand-write `<head>` tags; they get stripped.
   - Next.js Pages Router → `next/head` `<Head>` component, or `_document.tsx` for site-wide.
   - Plain HTML / Vite / Astro → edit `<head>` directly or the framework's head API.
   Find existing tags: `grep -rniE "og:|twitter:|application/ld\+json|rel=.canonical|<title|name=.description" src/ app/ public/`.

2. **Title + meta description.** Every indexable page needs a unique `<title>` (aim ≤60 chars so it isn't truncated in SERP) and `<meta name="description">` (≤160 chars, written for click-through, not keyword-stuffed). Flag pages sharing the same title/description as duplicate-content risk. In Next: set `title` (string or `{ default, template }`) and `description` in the metadata object.

3. **Open Graph + Twitter Card.** Required for correct social previews:
   - OG: `og:title`, `og:description`, `og:type` (`website`/`article`), `og:url` (absolute), `og:image` (absolute URL, 1200×630, <5MB), `og:site_name`.
   - Twitter: `twitter:card` = `summary_large_image`, `twitter:title`, `twitter:description`, `twitter:image`.
   In Next, use the `openGraph` and `twitter` keys (Next auto-emits the `<meta>` tags). Images must be absolute — set `metadataBase: new URL("https://example.com")` so relative image paths resolve, otherwise OG images silently 404 for crawlers.

4. **JSON-LD structured data.** Pick the type that matches the page: `Article`/`BlogPosting` (blog), `Product` + `Offer` (commerce), `BreadcrumbList` (nav trail), `FAQPage` (Q&A), `Organization`/`WebSite` (site-wide, in root layout). Emit as `<script type="application/ld+json">` with `JSON.stringify` — in React use `dangerouslySetInnerHTML`, never `{JSON.stringify(...)}` as a text child (React escapes the quotes and breaks parsing). Include all required props for the type (e.g. `Article` needs `headline`, `image`, `datePublished`, `author`). Validate the shape against schema.org before declaring done.

5. **Canonical URLs.** Each page must self-reference a single absolute canonical (`<link rel="canonical">` / Next `alternates.canonical`). Audit for conflicts: trailing-slash variants, `?utm_`/query params, `http` vs `https`, `www` vs apex all resolving to the same content without one canonical winner. Paginated/filtered list pages each canonical to themselves, not page 1.

6. **sitemap.xml + robots.txt.**
   - `sitemap.xml`: lists only indexable, canonical, 200-status URLs (no redirects, no `noindex` pages, no admin/auth routes). Next: `app/sitemap.ts`. Verify `<loc>` URLs are absolute and match canonicals exactly.
   - `robots.txt`: must NOT `Disallow` paths you also list in the sitemap or want indexed. Confirm it points to the sitemap (`Sitemap: https://example.com/sitemap.xml`). Check no stray `Disallow: /` left from a staging config.

7. **Heading + semantic HTML.** Exactly one `<h1>` per page, no skipped levels (h1→h3), descriptive not styling-driven. Use `<main>`, `<nav>`, `<article>`, `<header>`; `alt` on content images. This is the crawler's content map — don't leave it as `<div>` soup.

8. **hreflang (only if i18n).** For multi-locale sites, every locale variant lists reciprocal `hreflang` tags including a self-reference and `x-default`. Skip entirely for single-locale sites — wrong/partial hreflang is worse than none.

9. **Report.** Produce a table: page · issue · severity · concrete fix (with the diff). Apply the fixes, then re-audit.

## Common Errors

- **Hand-writing `<head>` in Next App Router** — React strips it on the server. Must go through the metadata API.
- **Relative OG/canonical image URLs without `metadataBase`** — crawlers and social scrapers can't resolve them; previews break and canonicals get ignored. Always absolute, or set `metadataBase`.
- **JSON-LD as a React text child** — `<script>{JSON.stringify(data)}</script>` HTML-escapes the quotes (`&quot;`) and the data won't parse. Use `dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}`.
- **Sitemap listing `noindex`/redirected/non-canonical URLs** — sends mixed signals; sitemap must only contain final indexable canonicals.
- **`robots.txt` Disallow vs sitemap conflict** — disallowing a URL that's in the sitemap (or carries `noindex`) wastes crawl budget and confuses indexing.
- **Multiple or zero `<h1>`** — common with component-based layouts where a shared header and the page both render an h1, or neither does.
- **Duplicate title/description across pages** — usually a layout-level default never overridden per-page; treat as a real bug, not cosmetic.
- **`noindex` left in from staging** — grep for `noindex` / `robots: { index: false }` before shipping; a single leftover tag silently de-indexes the page.

## Verify

- **Render the head:** build + serve, then `curl -s <url> | grep -iE "og:|twitter:|canonical|<title|ld\+json"` (or DevTools → Elements). Tags must exist in the **server-rendered HTML**, not injected client-side after load — crawlers read the initial response.
- **Structured data:** extract each JSON-LD block and confirm it's valid JSON and includes every required field for its `@type` per schema.org (Google Rich Results Test / Schema Markup Validator for a live check).
- **Social preview:** scrape with the platforms' validators (Facebook Sharing Debugger, Twitter/X Card Validator) — confirm image, title, description resolve from absolute URLs.
- **Sitemap/robots:** fetch `/sitemap.xml` (well-formed XML, absolute `<loc>`, no 404/redirect/noindex entries) and `/robots.txt` (references sitemap, doesn't block indexable paths).
- **Canonicals:** each page's canonical is absolute and self-consistent; no two pages claim the same canonical unless intended.
- **Done = the missing-items report has zero open high-severity items** and the above checks pass against the actually-served output, not the source file.
