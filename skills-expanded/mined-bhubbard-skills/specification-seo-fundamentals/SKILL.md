---
name: specification-seo-fundamentals
description: "Guidelines from The Website Specification on SEO fundamentals including semantic HTML, Sitemaps, and robots.txt."
---

# SEO Fundamentals Specification

According to [The Website Specification](https://specification.website/spec/seo/), a good website implements technical SEO flawlessly to ensure discoverability.

## Core Requirements

### 1. `robots.txt` and Sitemaps
*   A valid `robots.txt` must exist at the root, clearly defining crawl permissions (including specific rules for AI crawlers like `CCBot` or `GPTBot` if desired).
*   It must declare the `Sitemap: https://example.com/sitemap.xml` directive.
*   The XML Sitemap must be kept up-to-date, containing only canonical, `200 OK` URLs (no redirects or 404s).

### 2. Semantic HTML and Metadata
*   Every page must have a unique, descriptive `<title>` and `<meta name="description">`.
*   Pages must define a canonical URL via `<link rel="canonical" href="...">` to prevent duplicate content indexing.
*   Use proper semantic headings (`<h1>` through `<h6>`) chronologically without skipping levels. The `<h1>` should uniquely identify the page content.

### 3. Open Graph & Twitter Cards
*   Implement `og:title`, `og:description`, `og:image`, and `og:url` on all public pages so links unfurl beautifully on social media and messaging platforms.
