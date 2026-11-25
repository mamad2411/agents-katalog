---
name: canon-seo
description: Use when auditing or implementing technical SEO — semantic HTML, meta tags, structured data, canonical URLs, sitemap, robots.txt, page speed as a ranking factor, and accessible content. Trigger when the user mentions SEO, search engine, meta tags, structured data, sitemap, or crawlability.
---

# CANON · SEO

Technical SEO is about making content findable and understandable by search engines. Not tricks — structure.

## Semantic HTML is SEO

Search engines understand semantic HTML natively. Every rule in `canon-accessibility` that improves screen reader experience also improves SEO.

- `<h1>` once per page, matching the page topic.
- Heading hierarchy (h1 → h2 → h3) reflects content structure.
- `<nav>`, `<main>`, `<article>`, `<aside>` help crawlers understand page layout.
- `<a href>` for links (not `<div onClick>`).
- `<img alt>` describes the image for image search.

## Essential meta tags

```html
<head>
  <title>Page Title — Site Name</title>
  <meta name="description" content="Concise summary under 155 characters.">
  <link rel="canonical" href="https://example.com/page">
  <meta name="robots" content="index, follow">
</head>
```

- `<title>`: 50–60 characters. Unique per page. Primary keyword near the front.
- `<meta description>`: 120–155 characters. Compelling summary. Unique per page.
- `<link rel="canonical">`: prevents duplicate content penalties.
- `<meta robots>`: `index, follow` is default. `noindex` for admin pages.

## Structured data (JSON-LD)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Page Title",
  "author": { "@type": "Person", "name": "Author" },
  "datePublished": "2026-04-18"
}
</script>
```

Use for: articles, products, FAQs, breadcrumbs, organizations, events. Google uses structured data for rich results (stars, prices, FAQ dropdowns).

## Page speed = ranking factor

Core Web Vitals are a Google ranking signal. See `canon-performance` for targets:
- LCP ≤ 2.5s
- INP ≤ 200ms
- CLS ≤ 0.1

## Crawlability

- `robots.txt`: allow crawlers access to important pages, block admin/API routes.
- `sitemap.xml`: list all public pages with `<lastmod>` dates.
- Internal linking: every important page reachable within 3 clicks from the homepage.
- No orphan pages (pages with no internal links pointing to them).

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Same `<title>` on every page | Search engines can't distinguish pages |
| No `<meta description>` | Search engine generates one (often badly) |
| Keyword stuffing | Penalized by modern search engines |
| Client-rendered content without SSR/SSG | Crawlers may not execute JS |
| No canonical URL | Duplicate content across www/non-www, http/https |
| Blocking CSS/JS in robots.txt | Crawlers can't render the page |

## Audit checklist

- [ ] Unique `<title>` per page, 50–60 characters
- [ ] Unique `<meta description>` per page, 120–155 characters
- [ ] `<link rel="canonical">` on every page
- [ ] One `<h1>` per page matching the topic
- [ ] Heading hierarchy is correct
- [ ] Images have descriptive `alt` text
- [ ] Structured data (JSON-LD) for content types
- [ ] `sitemap.xml` submitted to search consoles
- [ ] `robots.txt` allows crawling of public pages
- [ ] Core Web Vitals in "Good" range

## Sources

- Google Search Central · SEO starter guide
- Schema.org · structured data types
- `canon-performance` for Core Web Vitals
- `canon-accessibility` for semantic HTML
