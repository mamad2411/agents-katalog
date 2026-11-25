---
name: seo-sitemap-generation
description: >-
  Use when generating sitemap.xml, robots.txt, dynamic sitemaps from a database,
  sitemap index files, or fixing crawl coverage. Not for in-app navigation or
  internal link strategy (see programmatic-seo-pages).
---

# SEO sitemap and robots

Every public Lovable site needs `/sitemap.xml` and `/robots.txt` — generate dynamically when content lives in Supabase.

Companion skills: [`seo-ssr-and-prerendering`](../seo-ssr-and-prerendering/), [`programmatic-seo-pages`](../programmatic-seo-pages/), [`seo-landing-page`](../seo-landing-page/).

## robots.txt

Serve from the static root or via an edge function:

```
User-agent: *
Allow: /
Disallow: /app
Disallow: /api
Disallow: /auth
Disallow: /admin

Sitemap: https://acme.com/sitemap.xml
```

Rules:

- Disallow authenticated routes and webhooks.
- Always include the absolute `Sitemap:` URL.
- Don't `Disallow: /` and expect a deploy delay to "uncrawl" — it won't.

## Sitemap (static, small site)

For sites with < 100 public pages, generate at build time and place at `public/sitemap.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://acme.com/</loc><lastmod>2026-05-22</lastmod><priority>1.0</priority></url>
  <url><loc>https://acme.com/pricing</loc><lastmod>2026-05-22</lastmod></url>
  <url><loc>https://acme.com/about</loc></url>
</urlset>
```

Generate from a route list rather than hand-editing — keep one source of truth.

## Sitemap (dynamic from Supabase)

Edge function returning XML:

```ts
// supabase/functions/sitemap/index.ts
Deno.serve(async () => {
  const { data: posts } = await admin
    .from("posts")
    .select("slug, updated_at")
    .eq("status", "published")
    .is("deleted_at", null)
    .order("updated_at", { ascending: false });

  const { data: locations } = await admin
    .from("location_pages")
    .select("slug, updated_at")
    .eq("published", true);

  const staticUrls = ["/", "/pricing", "/about", "/contact", "/blog"];

  const urls = [
    ...staticUrls.map((p) => ({ loc: `https://acme.com${p}`, lastmod: today() })),
    ...(posts ?? []).map((p) => ({
      loc: `https://acme.com/blog/${p.slug}`,
      lastmod: p.updated_at,
    })),
    ...(locations ?? []).map((l) => ({
      loc: `https://acme.com/locations/${l.slug}`,
      lastmod: l.updated_at,
    })),
  ];

  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls
  .map(
    (u) => `  <url><loc>${u.loc}</loc><lastmod>${formatIso(u.lastmod)}</lastmod></url>`,
  )
  .join("\n")}
</urlset>`;

  return new Response(body, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
});
```

Route `/sitemap.xml` at your hosting layer to this function (or generate at build).

## Sitemap index (large sites)

If you have > 50,000 URLs or > 50 MB sitemap, split into multiple files and reference from a sitemap index:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://acme.com/sitemaps/posts.xml</loc><lastmod>2026-05-22</lastmod></sitemap>
  <sitemap><loc>https://acme.com/sitemaps/locations.xml</loc><lastmod>2026-05-22</lastmod></sitemap>
</sitemapindex>
```

Submit the index URL to Search Console.

## What goes in the sitemap

| Include | Exclude |
|---------|---------|
| Public, indexable pages | Login, signup, dashboard |
| Canonical URLs only | Paginated mirrors (`/blog?page=2`) |
| `200 OK` URLs | Redirected URLs (`301`, `302`) |
| Published content | Drafts, expired listings, soft-deleted rows |
| `noindex: false` pages | Pages with `noindex` meta |

## Submitting and monitoring

1. Verify the property in Google Search Console.
2. Submit `https://acme.com/sitemap.xml`.
3. Check **Coverage** weekly for the first month — fix excluded URLs, broken redirects.
4. Add Bing Webmaster Tools too — free, takes 10 minutes.

## Avoid

- Listing `/dashboard` or other auth-gated pages.
- Stale `lastmod` (use the actual `updated_at` from DB).
- Including URLs with `noindex` meta tag — pick one signal.
- Returning `200` HTML on `/sitemap.xml` (bots expect `application/xml`).
- Sitemaps > 50 MB or > 50,000 URLs in a single file.

## Checklist

- [ ] `/sitemap.xml` returns valid XML with correct `Content-Type`.
- [ ] `/robots.txt` references the sitemap.
- [ ] Authenticated routes excluded.
- [ ] Soft-deleted / unpublished content filtered out.
- [ ] Submitted to Google Search Console.
