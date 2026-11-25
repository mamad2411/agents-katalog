---
name: seo-meta-tags-spa
description: >-
  Use when adding per-route titles, meta descriptions, Open Graph, Twitter card,
  or canonical tags in a Lovable SPA (React + Vite). Not for static HTML edits
  or content-only changes.
---

# SEO meta tags for SPAs

SPAs need **per-route** title + meta tags, but `index.html` only has one. Use one of these mechanisms consistently — never mix.

Companion skills: [`seo-ssr-and-prerendering`](../seo-ssr-and-prerendering/), [`seo-structured-data`](../seo-structured-data/), [`seo-landing-page`](../seo-landing-page/).

## Choose one approach

| Option | When | Notes |
|--------|------|-------|
| **React 19 native** (`<title>`, `<meta>` in JSX) | React 19+ projects | Built-in, no library, hoisted to `<head>` |
| **`react-helmet-async`** | React 18 and earlier, or you need SSR with collected tags | Battle-tested, SSR-friendly |
| **`@unhead/react`** | Modern alternative, smaller than helmet | Works for SSR + SPA |

For Lovable's current default React version, prefer **React 19 native tags** if available, otherwise `react-helmet-async`.

## React 19 native (preferred)

```tsx
function PricingPage() {
  return (
    <>
      <title>Pricing — Acme</title>
      <meta name="description" content="Simple per-seat pricing. Start free." />
      <link rel="canonical" href="https://acme.com/pricing" />
      <meta property="og:title" content="Acme Pricing" />
      <meta property="og:description" content="Simple per-seat pricing. Start free." />
      <meta property="og:image" content="https://acme.com/og/pricing.png" />
      <meta property="og:url" content="https://acme.com/pricing" />
      <meta name="twitter:card" content="summary_large_image" />

      <main>{/* ... */}</main>
    </>
  );
}
```

React lifts these to `<head>` automatically; SSR/prerendering captures them.

## react-helmet-async (React 18)

```tsx
import { HelmetProvider, Helmet } from "react-helmet-async";

// once at the root
<HelmetProvider>
  <App />
</HelmetProvider>

// per page
function PricingPage() {
  return (
    <>
      <Helmet>
        <title>Pricing — Acme</title>
        <meta name="description" content="Simple per-seat pricing. Start free." />
        <link rel="canonical" href="https://acme.com/pricing" />
        <meta property="og:title" content="Acme Pricing" />
        <meta property="og:image" content="https://acme.com/og/pricing.png" />
      </Helmet>
      <main>{/* ... */}</main>
    </>
  );
}
```

## Per-page contract

Every public route MUST set:

| Tag | Length | Notes |
|-----|--------|-------|
| `<title>` | 50–60 chars | Format: "Page — Brand" |
| `<meta name="description">` | 140–160 chars | One sentence, action-oriented |
| `<link rel="canonical">` | absolute URL | Even when there are no obvious duplicates |
| `og:title`, `og:description`, `og:image`, `og:url` | OG image 1200×630 | Required for LinkedIn/Slack previews |
| `twitter:card` | `summary_large_image` | Required for Twitter/X |

## Helper component

Centralize defaults so every page only overrides what's unique:

```tsx
type SeoProps = {
  title: string;
  description: string;
  path: string;
  image?: string;
  type?: "website" | "article";
};

export function Seo({ title, description, path, image, type = "website" }: SeoProps) {
  const url = `https://acme.com${path}`;
  const ogImage = image ?? "https://acme.com/og/default.png";

  return (
    <>
      <title>{`${title} — Acme`}</title>
      <meta name="description" content={description} />
      <link rel="canonical" href={url} />
      <meta property="og:type" content={type} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:url" content={url} />
      <meta property="og:image" content={ogImage} />
      <meta name="twitter:card" content="summary_large_image" />
    </>
  );
}
```

Use at the top of every page:

```tsx
<Seo title="Pricing" description="Simple per-seat pricing. Start free." path="/pricing" />
```

## Canonicals

- Self-referencing canonical on every page (yes, even the home page).
- For paginated pages, canonical to the **first** page or self-canonical per page; do not canonical all pages to `/blog`.
- For UTM-tagged URLs, canonical to the clean URL.

## Open Graph images

- 1200×630 PNG/JPG, < 1 MB, no transparency.
- Programmatic images: see [`programmatic-seo-pages`](../programmatic-seo-pages/) — generate per-page OG via Satori or an edge function.

## Verify

- View source of the rendered HTML — tags must be present (matters when prerendering / SSR).
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)

## Avoid

- Identical `<title>` on every route.
- Description duplicated across pages.
- OG image missing or > 5 MB.
- Mixing `react-helmet-async` and React 19 native tags — one wins, the other is dropped silently.
- Canonical pointing to `/` from every page.

## Checklist

- [ ] One `Seo` helper used everywhere.
- [ ] Each public route has unique title and description.
- [ ] Canonical set absolute, per-page.
- [ ] OG image generated and validated in three external debuggers.
