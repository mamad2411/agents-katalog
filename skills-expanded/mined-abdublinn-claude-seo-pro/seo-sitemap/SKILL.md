---
name: seo-sitemap
description: "Analyze existing XML sitemaps or generate new ones. Validates format, URLs, lastmod, structure. Industry templates. Enforces 50k URL limit and quality gates for location pages."
triggers:
  - "sitemap"
  - "generate sitemap"
  - "sitemap issues"
  - "XML sitemap"
---

# Sitemap Analysis

You are a sitemap specialist.

## Input

```
/seo sitemap <url> [--generate] [--type=standard|ecommerce|local|publisher]
```

## Analysis

### Existing Sitemap
1. Fetch `<url>/sitemap.xml` and `<url>/sitemap_index.xml`
2. Check format: valid XML, proper namespace
3. Count URLs per sitemap
4. Check `<lastmod>` presence and accuracy
5. Check `<changefreq>` and `<priority>` (optional, mostly ignored by Google)
6. Verify: all sitemap URLs return 200
7. Cross-check: sitemap referenced in robots.txt?

### Quality Checks
- **Utility pages in sitemap**: `/cart/`, `/checkout/`, `/my-account/`, `/wp-admin/` → should NOT be in sitemap
- **Thin content pages**: Tag/filter pages with <100 words → consider excluding
- **Non-canonical pages**: Pages with canonical pointing elsewhere → remove from sitemap
- **Redirect URLs**: 301/302 URLs in sitemap → replace with final destination
- **4xx URLs**: Broken URLs in sitemap → remove immediately
- **Feed URLs**: `/feed/` pages → remove from sitemap
- **Parameter URLs**: `?pa_cvet=`, `?filter=` → typically exclude unless they have unique content

### Structure
- Index sitemap pointing to child sitemaps?
- Logical grouping (products, categories, blog, pages)?
- Under 50,000 URLs per sitemap?
- Under 50MB uncompressed per sitemap?
- Gzipped versions available?

## Generation (if --generate)

Create sitemap XML based on site structure with industry template.

## Output

```markdown
# Sitemap Report: {domain}

> Score: {}/100 | Date: {date}

## Current Sitemap Status
{exists/missing, format, URL count}

## URLs in Sitemap
| Sitemap | URLs | With lastmod | Issues |
|---------|------|-------------|--------|

## Problems Found
| Issue | URLs affected | Action |
|-------|--------------|--------|
| Broken URLs (4xx) in sitemap | N | Remove |
| Redirect URLs in sitemap | N | Update to final URL |
| Utility pages in sitemap | N | Remove |
| Thin content in sitemap | N | Noindex or remove |
| Non-canonical in sitemap | N | Remove |

## Recommendations
{prioritized list}

## Generated Sitemap (if requested)
\`\`\`xml
{sitemap code}
\`\`\`
```
