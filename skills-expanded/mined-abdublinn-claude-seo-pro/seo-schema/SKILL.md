---
name: seo-schema
description: "Detect, validate, and generate Schema.org structured data in JSON-LD format. Supports all Google-supported types. Enforces deprecation rules (HowTo removed Dec 2023, FAQ restricted to gov/health)."
triggers:
  - "schema"
  - "structured data"
  - "rich results"
  - "JSON-LD"
  - "markup"
---

# Schema / Structured Data Analysis

You are a structured data specialist. Detect, validate, and generate Schema.org markup.

## Input

```
/seo schema <url> [--generate] [--type=Product|LocalBusiness|Article|...]
```

## Process

### 1. Detection
Fetch the page and find all structured data:
- JSON-LD blocks (`<script type="application/ld+json">`)
- Microdata (`itemscope`, `itemprop`)
- RDFa (`typeof`, `property`)

### 2. Validation
For each detected schema:
- Valid JSON syntax?
- Required properties present? (per Google's docs)
- Recommended properties present?
- Deprecated types used? (HowTo: removed Dec 2023, FAQ: restricted to gov/health since Aug 2023)
- Logo dimensions valid? (min 112x112px, flag 1x1px bugs)
- URLs resolve? (logo URL, image URL, sameAs URLs)

### 3. Gap Analysis
Based on page type, what schema is MISSING:
- **Homepage**: Organization or LocalBusiness, SearchAction, WebSite
- **Product pages**: Product with Offer, AggregateRating, Review, Brand
- **Category pages**: CollectionPage, BreadcrumbList, ItemList
- **Blog/article**: Article or BlogPosting, BreadcrumbList, author Person
- **About page**: Organization, Person (founders)
- **Contact page**: Organization with contactPoint
- **FAQ page**: FAQPage (only if gov/health site)
- **Local business**: LocalBusiness subtype, OpeningHoursSpecification, GeoCoordinates

### 4. Generation
Generate ready-to-paste JSON-LD code for all missing schemas. Use the site's actual data (name, address, products).

Load reference `seo/references/schema-types.md` for type details.

## Output

```markdown
# Schema Report: {domain}

> Score: {}/100 | Date: {date}

## Detected Schema
| Type | Format | Valid | Issues |
|------|--------|-------|--------|

## Missing Schema (by page type)
| Page type | Pages | Missing schema | Impact |
|-----------|-------|---------------|--------|

## Generated JSON-LD

### Organization / LocalBusiness
\`\`\`json
{ready code}
\`\`\`

### Product (template for product pages)
\`\`\`json
{ready code}
\`\`\`

### BreadcrumbList
\`\`\`json
{ready code}
\`\`\`

### WebSite + SearchAction
\`\`\`json
{ready code}
\`\`\`

## Implementation Guide
{where to add each schema, CMS-specific instructions}
```
