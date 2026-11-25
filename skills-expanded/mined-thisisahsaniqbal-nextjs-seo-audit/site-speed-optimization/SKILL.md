---
name: site-speed-optimization
description: >
  Audits stylesheet loading, inline CSS volume, image alt text, image formats, and
  Next.js Image component usage. Use when checking page speed related to HTML structure.
  For render-blocking scripts, image dimensions, lazy loading, and resource hints, see
  the core-web-vitals skill.
license: MIT
metadata:
  author: Muhammad Ahsan Iqbal (https://muhammadahsaniqbal.com)
  linkedin: https://www.linkedin.com/in/ahsan-iqbal-digitalmarketingexpert/
  version: "1.0"
---

# Site Speed Optimization

Audit HTML-level factors that affect page load speed.

> **Note**: Render-blocking scripts, image dimensions/lazy loading, preconnect hints, and font loading are handled by the [core-web-vitals](../core-web-vitals/SKILL.md) skill. Do not duplicate those checks here.

## 1. Total script count

Count all `<script src="...">` elements:

- More than **10** external scripts → ⚠️ WARN "Consider bundling or removing unused scripts"
- 10 or fewer → ✅ PASS

## 2. Inline CSS volume

Measure total character count of all `style="..."` attributes + `<style>` element contents:

| Condition | Status |
|---|---|
| Total > **5000 characters** | ⚠️ WARN "Move styles to external stylesheet for caching" |
| Total ≤ 5000 | ✅ PASS |

## 3. Stylesheet loading

- Count `<link rel="stylesheet">` elements
- If stylesheets > 3 → ⚠️ WARN "Consider combining CSS files"

## 4. Image alt text

| Condition | Status |
|---|---|
| All images have `alt` attribute | ✅ PASS |
| Any image missing `alt` | ❌ FAIL "Critical for SEO and accessibility" |

## 5. Image formats

- Images with `.jpg`, `.jpeg`, `.png`, `.gif` extensions → ⚠️ WARN "Consider WebP or AVIF for smaller file sizes"

## 6. Next.js Image component

- Images not using `/_next/image` src → ⚠️ WARN "Consider using Next.js `<Image>` component for automatic optimization"
- Skip this check if the site is not a Next.js project

## Edge cases

- Inline `<script>` tags (no `src`) should be counted separately from external scripts — they contribute to page weight but not network requests
- `<style>` elements inside `<noscript>` blocks should be excluded from inline CSS volume
- Base64-encoded images (`src="data:image/..."`) bypass network loading but increase HTML size — flag as ⚠️ WARN if total base64 content exceeds 10KB
- SVG images (`<img src="*.svg">`) do not need WebP/AVIF conversion — exclude from image format checks
- Next.js `<Image>` component detection: look for `/_next/image` in `src` or `srcset` attributes, or `data-nimg` attribute
- Dynamically injected scripts (via JS) are not visible in static HTML — note this limitation
