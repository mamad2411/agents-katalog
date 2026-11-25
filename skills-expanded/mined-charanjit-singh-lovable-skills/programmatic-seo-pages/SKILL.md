---
name: programmatic-seo-pages
description: >-
  Use when generating SEO pages at scale from data: location pages, "X vs Y"
  comparison pages, "alternatives to X", integration pages, feature templates,
  or any pattern producing hundreds of pages from rows. Not for one-off
  marketing pages or thin/spammy content.
---

# Programmatic SEO pages

Generate many high-intent SEO pages from a single template + a dataset. Done right, this captures long-tail traffic the brand team would never write by hand. Done wrong, you ship thin doorway pages and tank the whole domain.

Companion skills: [`programmatic-seo-content-quality`](../programmatic-seo-content-quality/), [`seo-ssr-and-prerendering`](../seo-ssr-and-prerendering/), [`seo-meta-tags-spa`](../seo-meta-tags-spa/), [`seo-structured-data`](../seo-structured-data/), [`seo-sitemap-generation`](../seo-sitemap-generation/).

## Common patterns

| Pattern | Examples | Search intent |
|---------|----------|---------------|
| Location pages | `/locations/[city]`, `/dentist/[city]` | "dentist in austin" |
| Comparisons | `/compare/[a]-vs-[b]` | "notion vs evernote" |
| Alternatives | `/alternatives/[brand]` | "alternatives to mailchimp" |
| Integrations | `/integrations/[tool]` | "stripe integration" |
| Templates / use-cases | `/templates/[category]/[name]` | "marketing plan template" |
| Glossary / wiki | `/glossary/[term]` | "what is bounce rate" |

Pick **one or two patterns** first. Don't ship five at once.

## Data model

Each template needs a row per page with enough unique data to justify existence:

```sql
create table public.location_pages (
  slug text primary key,
  city text not null,
  state text not null,
  country text not null,
  lat numeric, lng numeric,
  service_areas text[],
  testimonials jsonb,
  avg_price_cents int,
  faqs jsonb,                  -- [{ q, a }]
  hero_image_url text,
  published boolean default false,
  noindex boolean default false,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create index location_pages_published_idx on public.location_pages (published) where published = true;
```

Rules:

- **`published` boolean** so drafts never leak into sitemap.
- **`noindex` flag** per row — kill underperformers without deleting.
- Enough unique fields per row to write 300+ words of real content (testimonials, FAQs, local stats, prices).

## Route + template

```tsx
// /locations/[slug]
export default function LocationPage() {
  const { slug } = useParams();
  const { data: page } = useLocationPage(slug);
  if (!page) return <NotFound />;

  return (
    <>
      <Seo
        title={`${page.service} in ${page.city}, ${page.state}`}
        description={`Find ${page.service} in ${page.city}. ${page.unique_hook}.`}
        path={`/locations/${page.slug}`}
        image={page.hero_image_url}
      />
      <JsonLd data={buildLocalBusinessSchema(page)} />
      <JsonLd data={buildFaqSchema(page.faqs)} />
      <JsonLd data={buildBreadcrumbSchema(page)} />

      <Hero city={page.city} state={page.state} hook={page.unique_hook} />
      <LocalStats data={page.stats} />
      <Testimonials items={page.testimonials} />
      <ServiceAreas items={page.service_areas} />
      <Faq items={page.faqs} />
      <RelatedLocations city={page.city} state={page.state} />
    </>
  );
}
```

Each section must take **page-specific data**. If your testimonials section says "Loved by customers" identically on every page, it's filler.

## Prerender at build

These pages must be in the **raw HTML** — Googlebot can render JS, but at scale you'll hit crawl-budget issues.

```ts
// vite-ssg includedRoutes
export async function includedRoutes() {
  const slugs = await fetchAllPublishedSlugs();
  return [
    "/",
    "/pricing",
    ...slugs.map((s) => `/locations/${s}`),
  ];
}
```

For thousands of pages: split into chunks and run prerender in parallel, or move to true SSR ([`seo-ssr-and-prerendering`](../seo-ssr-and-prerendering/)).

## URL structure

- Single segment when possible: `/alternatives/[brand]` not `/best/alternatives/to/[brand]/2026`.
- Hyphens, lowercase, no stop-words (`mailchimp-alternatives` not `the-best-mailchimp-alternatives`).
- One canonical URL per row — never multiple URLs leading to the same content.

## Internal linking

Programmatic pages need **internal links** to be discovered and ranked:

- Cross-link siblings: every location links to 5–10 nearby cities.
- Link from canonical hub pages: `/locations` lists all cities; `/integrations` lists all tools.
- Link contextually from blog content and the home page where natural.
- Use a small `RelatedX` component per template, deterministic per row (sorted by proximity, popularity, etc.).

## OG images per page

Generate dynamically — one PNG per row, cached.

- **Build-time**: render via Satori → store in Supabase Storage → reference in `og:image`.
- **Edge runtime**: Vercel OG (`@vercel/og`) or Cloudflare Workers — generate on first request, cache.

Cheap fallback: a single branded OG with the page title overlaid via CSS in a screenshot service.

## Avoid

- Generating 5,000 pages overnight from a CSV without unique content.
- Identical content with one swapped keyword (this is a doorway page; Google penalizes).
- Listing in sitemap before pages render with real data.
- Building pages for keywords that have zero search demand (use Search Console / Ahrefs to validate).
- Auto-publishing without a quality threshold ([`programmatic-seo-content-quality`](../programmatic-seo-content-quality/)).

## Checklist

- [ ] Data model rich enough for unique content per page.
- [ ] `published` + `noindex` flags so you can curate.
- [ ] Per-page meta, OG, JSON-LD (LocalBusiness/Product/SoftwareApp + FAQPage + BreadcrumbList).
- [ ] Internal linking between siblings and to a hub.
- [ ] Prerendered or SSR'd — populated HTML on first request.
- [ ] Included in `sitemap.xml` only when `published = true`.
