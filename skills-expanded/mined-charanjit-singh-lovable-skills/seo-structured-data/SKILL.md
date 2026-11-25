---
name: seo-structured-data
description: >-
  Use when adding Schema.org JSON-LD structured data to public pages: Organization,
  WebSite, Article, Product, FAQPage, BreadcrumbList, SoftwareApplication.
  Not for authenticated dashboards or non-public content.
---

# SEO structured data (JSON-LD)

Schema.org JSON-LD helps Google show rich results (FAQs, ratings, breadcrumbs) and improves AI-powered SERP features. Render it in the page `<head>` or just before `</body>`.

Companion skills: [`seo-meta-tags-spa`](../seo-meta-tags-spa/), [`seo-landing-page`](../seo-landing-page/), [`seo-ssr-and-prerendering`](../seo-ssr-and-prerendering/).

## Helper

```tsx
export function JsonLd({ data }: { data: object }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
```

Always `JSON.stringify` — never inline a JS object literal as text.

## Home / global (every public page or just `/`)

```tsx
<JsonLd
  data={{
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "Acme",
    url: "https://acme.com",
    logo: "https://acme.com/logo.png",
    sameAs: [
      "https://twitter.com/acme",
      "https://www.linkedin.com/company/acme",
      "https://github.com/acme",
    ],
  }}
/>

<JsonLd
  data={{
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "Acme",
    url: "https://acme.com",
    potentialAction: {
      "@type": "SearchAction",
      target: "https://acme.com/search?q={query}",
      "query-input": "required name=query",
    },
  }}
/>
```

## SaaS product / pricing page

```ts
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Acme",
  applicationCategory: "BusinessApplication",
  operatingSystem: "Web",
  offers: [
    { "@type": "Offer", price: "0", priceCurrency: "USD", name: "Free" },
    { "@type": "Offer", price: "29", priceCurrency: "USD", name: "Pro" },
  ],
  aggregateRating: {
    "@type": "AggregateRating",
    ratingValue: "4.8",
    reviewCount: "127",
  },
}
```

Only include `aggregateRating` if the ratings are real and verifiable on the page.

## Article / blog post

```ts
{
  "@context": "https://schema.org",
  "@type": "Article",
  headline: post.title,
  description: post.excerpt,
  image: [post.cover_url],
  datePublished: post.published_at,
  dateModified: post.updated_at,
  author: { "@type": "Person", name: post.author.name, url: `https://acme.com/authors/${post.author.slug}` },
  publisher: {
    "@type": "Organization",
    name: "Acme",
    logo: { "@type": "ImageObject", url: "https://acme.com/logo.png" },
  },
  mainEntityOfPage: { "@type": "WebPage", "@id": `https://acme.com/blog/${post.slug}` },
}
```

## FAQ page

```ts
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: faqs.map((f) => ({
    "@type": "Question",
    name: f.question,
    acceptedAnswer: { "@type": "Answer", text: f.answer },
  })),
}
```

Only mark up FAQs **visible on the same page**. Marking up hidden Q&A is against Google guidelines.

## Breadcrumbs

```ts
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  itemListElement: [
    { "@type": "ListItem", position: 1, name: "Home", item: "https://acme.com/" },
    { "@type": "ListItem", position: 2, name: "Blog", item: "https://acme.com/blog" },
    { "@type": "ListItem", position: 3, name: post.title, item: `https://acme.com/blog/${post.slug}` },
  ],
}
```

## Product (e-commerce)

```ts
{
  "@context": "https://schema.org",
  "@type": "Product",
  name: product.name,
  image: product.images,
  description: product.description,
  sku: product.sku,
  brand: { "@type": "Brand", name: "Acme" },
  offers: {
    "@type": "Offer",
    url: `https://acme.com/p/${product.slug}`,
    priceCurrency: "USD",
    price: (product.price_cents / 100).toFixed(2),
    availability: product.in_stock
      ? "https://schema.org/InStock"
      : "https://schema.org/OutOfStock",
  },
}
```

## HowTo, Review, Event

Use only when the page is **really about** the entity. Don't slap HowTo on every blog post — Google ignores or penalizes mismatched schema.

## Verify

- [Rich Results Test](https://search.google.com/test/rich-results)
- [Schema Markup Validator](https://validator.schema.org/)
- Search Console → Enhancements → check each schema type for errors.

## Avoid

- Marking up content not visible on the page.
- Fake ratings or counts.
- Multiple primary types (`Article` + `Product` on the same page) without a clear reason.
- Repeating the same Organization block on every page when one global instance is fine.
- Forgetting to update `dateModified` on edits.

## Checklist

- [ ] `Organization` + `WebSite` on home page.
- [ ] `Article` on every blog post with real author and dates.
- [ ] `BreadcrumbList` on nested pages.
- [ ] `FAQPage` only when FAQ is rendered and visible.
- [ ] Validated in Rich Results Test before deploy.
