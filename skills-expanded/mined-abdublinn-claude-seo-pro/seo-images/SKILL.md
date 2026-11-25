---
name: seo-images
description: "Image optimization analysis: alt text audit, file sizes via HEAD requests with distribution tiers, format recommendations (WebP/AVIF), responsive images, lazy loading, CLS prevention, filename audit (uppercase, cyrillic, transliteration). v2.1 — adds HEAD-request sizing strategy."
triggers:
  - "image optimization"
  - "alt text"
  - "image SEO"
  - "image size"
  - "image audit"
  - "WebP"
  - "image filenames"
---

# Image Optimization Analysis — v2.0

You are an image optimization specialist. Audit all images across the site for SEO, performance, and accessibility.

## Input

```
/seo images <url> [--pages=all|50|homepage] [--check-sizes]
```

## Analysis Sections

### 1. Alt Text Audit

Crawl pages and collect all `<img>` tags. Categorize:

```markdown
Total images found: N (across N pages)

Alt text status:
- With meaningful alt: N (X%)
- With short/generic alt (<5 chars or "image", "photo", "img"): N (X%)
- With empty alt (alt=""): N (X%) — acceptable for decorative
- WITHOUT alt attribute at all: N (X%) ← CRITICAL for accessibility
- With keyword-stuffed alt (>125 chars): N (X%)

Pages with most missing alt:
| Page URL | Images total | Missing alt | Examples |
```

**Scoring:**
- >95% meaningful alt = 100
- 90-95% = 80
- 80-90% = 60
- 60-80% = 40
- 40-60% = 20
- <40% = 0

**Fix recommendations:**
- For product images: `{product name} — {color/variant} — {brand}`
- For decorative images: add `alt=""` (empty, not missing)
- For informational images: describe what the image conveys

### 2. File Size Distribution (ENHANCED v2.1)

Use `Content-Length` from HEAD requests. The `crawl_site.py --check-image-sizes` flag does this automatically and saves results in crawl data. If crawl data is available at `/tmp/crawl_data.json`, read image sizes from there instead of re-fetching.

**HEAD-request strategy (v2.1):**
- Send HEAD requests (not GET) to avoid downloading full images
- Batch by domain, max 5 concurrent, 0.5s delay
- If Content-Length header is missing, estimate from Content-Type + typical sizes
- For external CDN images (wp-content/uploads on CDN), HEAD may return accurate sizes

```markdown
Total image files: N
Total size: {X} MB

Size distribution:
| Tier | Size range | Count | Percentage | Status |
|------|-----------|-------|------------|--------|
| Optimal | <50 KB | N | X% | Good |
| Acceptable | 50-100 KB | N | X% | OK |
| Large | 100 KB - 500 KB | N | X% | Optimize |
| Too large | 500 KB - 1 MB | N | X% | Compress |
| Critical | >1 MB | N | X% | MUST fix |

Top 10 heaviest images:
| URL | Size | Page used on | Dimensions (if detectable) |
```

**Scoring:**
- >90% under 100KB = 100
- >80% under 100KB = 80
- >60% under 100KB = 60
- >40% under 100KB = 40
- >20% under 100KB = 20
- <20% under 100KB = 0

### 3. Format Analysis

```markdown
Format distribution:
| Format | Count | Percentage | Modern? |
|--------|-------|------------|---------|
| JPEG | N | X% | Legacy |
| PNG | N | X% | Legacy (unless transparency needed) |
| WebP | N | X% | Modern |
| AVIF | N | X% | Modern |
| SVG | N | X% | Vector (OK) |
| GIF | N | X% | Legacy |
| BMP/TIFF | N | X% | Unacceptable |

Modern format adoption: X%
```

**Recommendation:** Serve WebP with JPEG fallback via `<picture>` element or server-side content negotiation.

### 4. Filename Audit (NEW v2.0)

Check all image URLs for naming issues:

```markdown
Filename issues:
| Issue | Count | Examples |
|-------|-------|---------|
| Uppercase letters in filename | N | /uploads/Photo_1.JPG |
| Cyrillic characters | N | /uploads/кресло-мешок.jpg |
| Spaces in filename | N | /uploads/my image.jpg |
| Generic names (1.jpg, img001.png) | N | /uploads/2023/08/1.jpg |
| Very long filenames (>80 chars) | N | /uploads/very-long-name....jpg |
| Underscores instead of hyphens | N | /uploads/product_image_1.jpg |
| Percent-encoded characters | N | /uploads/%D0%BA%D1%80%D0%B5%D1%81%D0%BB%D0%BE.jpg |
```

**Why this matters:**
- Uppercase: Can cause duplicate URLs on case-sensitive servers (Linux)
- Cyrillic: Breaks in some tools, APIs, CDNs; becomes long percent-encoded URLs
- Generic names: Miss keyword opportunity in Google Images
- Underscores: Google treats underscores as joiners, hyphens as separators

**Fix:** Rename files to lowercase-latin-hyphenated format: `kreslo-meshok-sinij-xl.webp`

### 5. Responsive Images

Check for:
- `srcset` attribute — multiple resolutions served?
- `sizes` attribute — viewport-appropriate size hints?
- `<picture>` element — format fallbacks?
- Oversized images (e.g., 2000px wide image in a 300px container)

```markdown
Responsive image adoption:
- Images with srcset: N (X%)
- Images with sizes: N (X%)
- Images in <picture>: N (X%)
- Potentially oversized: N (X%)
```

### 6. Lazy Loading

```markdown
- Images with loading="lazy": N (X%)
- Images with loading="eager": N (X%)
- Images without loading attribute: N (X%)
- Above-fold images with lazy (BAD): N ← should be eager or not set
- Below-fold images without lazy: N ← should have lazy
```

**Best practice:** First 2-3 images visible on load should be `loading="eager"` or have no attribute. All others should be `loading="lazy"`.

### 7. CLS Prevention

```markdown
- Images with explicit width+height: N (X%)
- Images with aspect-ratio CSS: N (X%)
- Images with neither (CLS risk): N (X%)
```

### 8. Performance Attributes (NEW v2.0)

```markdown
- Images with fetchpriority="high": N (hero/LCP images should have this)
- Images with decoding="async": N (X%)
```

### 9. Image Sitemap

- Does a dedicated image sitemap exist?
- Are images included in the main sitemap via `<image:image>` tags?
- Count of images in sitemap vs images on site

## Output Format

```markdown
# Image Optimization Report: {domain}

> Score: {}/100 | Date: {date}
> Total images: {N} | Total size: {X} MB
> Modern format adoption: {X}%

## Summary
{Key issues — lead with biggest impact items}

## Alt Text Audit
{table + scoring}

## File Size Distribution
{tiered table + top 10 heaviest}

## Format Analysis
{format table + recommendation}

## Filename Audit (NEW v2.0)
{issues table + fix recommendation}

## Responsive Images
{adoption stats}

## Lazy Loading
{stats + misconfigurations}

## CLS Prevention
{stats}

## Recommendations
| Priority | Action | Impact | Effort |
|----------|--------|--------|--------|
| CRITICAL | Convert {N} images >1MB to WebP | -X MB page weight | Medium |
| HIGH | Add alt to {N} images | Accessibility + SEO | Low |
| HIGH | Rename {N} files (uppercase/cyrillic) | URL consistency | Medium |
| MEDIUM | Add srcset to product images | Mobile performance | Medium |
| MEDIUM | Add lazy loading to below-fold | LCP improvement | Low |
| LOW | Create image sitemap | Google Images traffic | Low |
```
