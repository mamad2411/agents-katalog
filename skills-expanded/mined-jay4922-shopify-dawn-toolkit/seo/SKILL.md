---
name: seo
description: The team's authoritative SEO standard for Shopify Dawn-fork themes — heading hierarchy (one h1, configurable heading_tag), semantic HTML, structured data / JSON-LD (FAQPage, BreadcrumbList, Article, VideoObject, no duplicates), metadata and canonical URLs, internal linking and link rel rules, image SEO, and collection/product/page technical SEO. Use this skill whenever building or editing headings, links, meta output, structured data, or any content crawlers should rank, and whenever the user mentions SEO, schema.org, structured data, meta tags, rich results, canonicals, sitemaps, or redirects. BUILD-TIME guidance; the qa agent audits against this same file.
---

# SEO Standard (Shopify Dawn-fork)

Single source of truth for SEO. Build against it; the `qa` agent verifies rendered output against it.

## Headings & hierarchy

- **Never emit a second `<h1>`.** The page template owns the `<h1>`; sections normally start at `<h2>`, no skipped levels.
- **Recommended pattern (not yet adopted anywhere in this project — real sections currently hardcode `<h1>`/`<h2>` directly, e.g. `custom-content-banner.liquid`, `custom-page-hero.liquid`):** make a section's heading level configurable so merchants reordering sections can't break the outline:
  ```liquid
  {%- assign heading_tag = section.settings.heading_tag | default: 'h2' -%}
  <{{ heading_tag }}>{{ section.settings.heading | escape }}</{{ heading_tag }}>
  ```
  Add a `heading_tag` select (h2/h3) to the schema when a section can appear at varying page depths. Apply this going forward on new sections; retrofitting existing hardcoded headings is optional cleanup, not a blocker.
- The heading outline must make sense _in the rendered page_, not just within the section in isolation.

## Semantic HTML

Real semantic elements — `<section>`, `<article>`, `<nav>`, `<ul>`/`<ol>`, `<button>` vs `<a>`. No div soup, no headings faked with styled `<p>`/`<span>`. Content that should rank is server-rendered by Liquid in the initial HTML — never injected by JS, never hidden behind `display:none`.

## Structured data (JSON-LD)

- Add JSON-LD where the content type warrants it: FAQ/accordion → `FAQPage`, breadcrumbs → `BreadcrumbList` (greenfield in this project — no breadcrumb markup/JSON-LD exists yet anywhere), video → `VideoObject`, article → `Article`.
- **ALWAYS search the theme for existing `application/ld+json` first.** Never add schema the theme already emits. In this project specifically: `Organization`/`WebSite` JSON-LD is already emitted in `sections/header.liquid`, and `Product` JSON-LD is emitted independently by BOTH `sections/main-product.liquid` and `sections/featured-product.liquid` — check both before adding a third `Product` block anywhere those two could co-render on the same page (a featured-product section on a page also showing the main product).
- Build values with `{{ value | strip_html | json }}` and do NOT add your own quotes — `| json` emits them; double-quoting produces invalid JSON.
- Rendered JSON-LD must parse as valid JSON and match the visible content (QA verifies this on the rendered page).

## Metadata & canonicals (template-level)

- `layout/theme.liquid` outputs the title / meta-description pattern and `{{ canonical_url }}`.
- Paginated collections canonicalize correctly; no accidental `noindex`.
- `og:` / `twitter:` tags present with a fallback image and the correct `og:type` per template.

## Links & internal linking

- Descriptive anchor text — no bare "click here" / "read more".
- Real `<a href>`, never JS-`onclick` divs (crawlers only follow real links). All internal links crawlable.
- `rel="noopener"` on `target="_blank"`. `nofollow`/`sponsored`/`ugc` ONLY on paid/untrusted/user links — never on internal links.

## Image SEO

- Meaningful `alt` on informative images (describes content, not `IMG_2043.jpg`); empty `alt=""` only for decorative images (coordinated with the `ada-accessibility` skill).
- Real text stays HTML text — never baked into images.

## Collection / product / page SEO

- Collection pages: unique title/description, crawlable pagination, faceted-filter URLs that don't create infinite crawlable combinations.
- Product pages: `Product` JSON-LD (already emitted by `main-product.liquid`/`featured-product.liquid` — don't duplicate), one h1 (the product title), breadcrumbs only if/when Figma actually introduces them (greenfield today, not an existing pattern to extend).
- Content pages: clean heading outline, canonical set, internal links to related products/collections.

## Migration (when replacing an existing site)

Inventory old URLs → build a 301 redirect map; preserve top-traffic title patterns. If a TinySEO-style app covers some duties, audit only what remains theme-side and respect any briefed page-type scope.

## What counts as a blocker (for the qa gate)

Defects in the audited scope's OWN code: invalid/broken JSON-LD, duplicate schema introduced by this section, a second h1, uncrawlable links, JS-injected rankable content. Site-wide or app-caused issues outside scope are warnings.
