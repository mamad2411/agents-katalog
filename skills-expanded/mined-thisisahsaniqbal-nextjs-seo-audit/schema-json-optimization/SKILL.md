---
name: schema-json-optimization
description: >
  Validates existing JSON-LD structured data and suggests relevant schemas based on
  auto-detected page type. Does NOT enforce all schema types — only checks what is
  applicable to the current page context. Use when auditing or generating structured
  data for search engine rich results.
license: MIT
metadata:
  author: Muhammad Ahsan Iqbal (https://muhammadahsaniqbal.com)
  linkedin: https://www.linkedin.com/in/ahsan-iqbal-digitalmarketingexpert/
  version: "1.0"
---

# Schema JSON Optimization

Validate existing JSON-LD and suggest **only relevant** schemas based on the detected page type.

> **Important**: Do NOT blindly check for all schema types. First detect what kind of page this is, then only validate/suggest schemas that are applicable.

## Step 1: Find and validate existing JSON-LD

Look for all `<script type="application/ld+json">` elements:

- None found → ⚠️ WARN "No JSON-LD schema markup found"
- Found → ✅ PASS "Found N JSON-LD block(s)" → validate each:

### Validation rules

- **Invalid JSON** → ❌ FAIL "Could not parse JSON-LD"
- **Missing `@context`** → ❌ FAIL
- **Missing `@type`** → ❌ FAIL
- Valid → ✅ PASS and check type-specific required fields (see Step 3)

## Step 2: Auto-detect page type

Scan the HTML for signals to determine what type of page this is. A page may match **zero, one, or multiple** types:

| Page type | Detection signals |
|---|---|
| **Article / Blog** | `<meta property="article:published_time">`, `<article>` tag, blog-like URL patterns (`/blog/`, `/post/`, `/news/`) |
| **LocalBusiness** | `<address>` tag, `<a href="tel:...">`, `[itemprop="telephone"]`, `[itemprop="address"]`, contact page patterns |
| **Product** | `<meta property="og:type" content="product">`, price elements (`[itemprop="price"]`), add-to-cart buttons |
| **FAQ** | Multiple `<details>/<summary>` or FAQ-patterned heading + paragraph pairs |
| **Organization** | About page with company info, `<meta property="og:type" content="website">` on homepage |
| **BreadcrumbList** | `<nav aria-label="breadcrumb">`, `.breadcrumb` class, `<ol>` with breadcrumb-like links |
| **WebSite** | Homepage with site-wide search form |

**If no type is detected** → only validate existing schemas, do not suggest new ones.

## Step 3: Validate and suggest ONLY for detected types

### Only if Article/Blog detected:

Check existing Article schema for:

| Field | Missing = |
|---|---|
| `headline` | ⚠️ WARN |
| `datePublished` | ⚠️ WARN |
| `author` | ⚠️ WARN |
| `image` | ⚠️ WARN |
| `description` | ⚠️ WARN |

If no Article schema exists, suggest generating one:

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[from og:title, <title>, or <h1>]",
  "datePublished": "[from article:published_time or <time datetime>]",
  "author": { "@type": "Person", "name": "[from meta author]" },
  "image": "[from og:image or first article img]",
  "description": "[from meta description]",
  "url": "[from canonical or og:url]"
}
```

### Only if LocalBusiness detected:

Check for:

| Field | Missing = |
|---|---|
| `name` | ❌ FAIL |
| `address` | ⚠️ WARN |
| `telephone` | ⚠️ WARN |

If no LocalBusiness schema exists, suggest generating one:

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[from og:site_name or <title>]",
  "address": "[from <address> or itemprop=address]",
  "telephone": "[from itemprop=telephone or tel: link]",
  "url": "[from canonical or og:url]",
  "image": "[from og:image]"
}
```

### Only if Product detected:

Check for:

| Field | Missing = |
|---|---|
| `name` | ❌ FAIL |
| `offers` (with `price` and `priceCurrency`) | ⚠️ WARN |
| `image` | ⚠️ WARN |
| `description` | ⚠️ WARN |

### Only if FAQ detected:

Suggest FAQPage schema with Question/Answer pairs extracted from the page.

### Only if BreadcrumbList detected:

Suggest BreadcrumbList schema from the breadcrumb navigation structure.

## Key principle

```
DO: "This page looks like a blog post → checking for Article schema"
DON'T: "Missing LocalBusiness schema" on a blog post page
```

The goal is **relevance, not completeness**. Only flag missing schemas that would actually benefit the detected page type.

## Edge cases

- A page may have multiple valid types (e.g. a product page with FAQ section → suggest both Product and FAQPage)
- A page may have existing schemas that are valid but don't match the detected type — that's fine, still validate them
- If detection is ambiguous, report what was detected and let the user decide
- Schema `@type` can be an array (e.g. `["Article", "NewsArticle"]`)
