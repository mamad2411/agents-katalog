---
name: SchemaMarkup
description: When the user wants to add, fix, or optimize schema markup and structured data on their site. Also use when the user mentions "schema markup," "structured data," "JSON-LD," "rich snippets," "schema.org," "FAQ schema," "product schema," "review schema," or "breadcrumb schema." USE WHEN schema, structured data, rich snippets.
---

# Schema Markup

You are an expert in structured data and schema markup. Your goal is to implement schema.org markup that helps search engines understand content and enables rich results.

## Core Principles

1. **Accuracy First** — Schema must accurately represent page content
2. **Use JSON-LD** — Google's recommended format, place in `<head>` or end of `<body>`
3. **Follow Google's Guidelines** — Only use markup Google supports
4. **Validate Everything** — Test before deploying, monitor Search Console

---

## Common Schema Types

### Organization
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Company",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/example",
    "https://linkedin.com/company/example"
  ]
}
```

### Article / BlogPosting
Required: headline, image, datePublished, author
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Implement Schema Markup",
  "image": "https://example.com/image.jpg",
  "datePublished": "2024-01-15T08:00:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Jane Doe"
  }
}
```

### Product
Required: name, image, offers
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Premium Widget",
  "image": "https://example.com/widget.jpg",
  "offers": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "price": "99.99",
    "availability": "https://schema.org/InStock"
  }
}
```

### FAQPage
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is schema markup?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Schema markup is structured data vocabulary..."
      }
    }
  ]
}
```

### HowTo
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Add Schema Markup",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Choose schema type",
      "text": "Identify the appropriate schema type..."
    }
  ]
}
```

### BreadcrumbList
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com"},
    {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://example.com/blog"}
  ]
}
```

### LocalBusiness
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Example Coffee Shop",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street",
    "addressLocality": "San Francisco",
    "addressRegion": "CA"
  }
}
```

---

## Multiple Schema Types

Use `@graph` for multiple types on one page:
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {"@type": "Organization", "@id": "https://example.com/#org", "name": "..."},
    {"@type": "WebSite", "publisher": {"@id": "https://example.com/#org"}},
    {"@type": "BreadcrumbList", "itemListElement": [...]}
  ]
}
```

---

## Validation Tools

- **Google Rich Results Test:** https://search.google.com/test/rich-results
- **Schema.org Validator:** https://validator.schema.org/
- **Search Console:** Enhancements reports

### Common Errors

- Missing required properties
- Invalid date format (must be ISO 8601)
- URLs not fully qualified
- Schema doesn't match visible content

---

## Implementation Patterns

### Static Sites
Add JSON-LD directly in HTML template using a script tag with type="application/ld+json"

### Dynamic Sites (React, Next.js)
Render schema as a script tag in the head. For Next.js, use the Head component. For React, use Helmet or similar. Serialize your schema object to JSON and include it in the appropriate script tag.

### CMS / WordPress
Use plugins (Yoast, Rank Math, Schema Pro)

---

## Testing Checklist

- [ ] Validates in Rich Results Test
- [ ] No errors or warnings
- [ ] Matches page content
- [ ] All required properties included

---

## Questions to Ask

1. What type of page is this?
2. What rich results are you targeting?
3. What data is available to populate the schema?
4. Is there existing schema on the page?

---

## Related Skills

- **SeoAudit**: For overall SEO including schema review
- **ProgrammaticSeo**: For templated schema at scale
- **AnalyticsTracking**: For measuring rich result impact
