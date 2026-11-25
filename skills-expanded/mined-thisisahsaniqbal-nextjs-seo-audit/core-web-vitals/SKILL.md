---
name: core-web-vitals
description: >
  Audits HTML patterns that affect Core Web Vitals (LCP, CLS, INP). Checks for layout
  shift causes, largest contentful paint blockers, and interaction responsiveness issues.
  Use when optimising page performance or fixing Google PageSpeed Insights warnings.
license: MIT
metadata:
  author: Muhammad Ahsan Iqbal (https://muhammadahsaniqbal.com)
  linkedin: https://www.linkedin.com/in/ahsan-iqbal-digitalmarketingexpert/
  version: "1.0"
---

# Core Web Vitals

Audit HTML for patterns that negatively impact Core Web Vitals — the performance metrics Google uses as a ranking signal.

## Overview

| Metric | Full name | Good threshold | What it measures |
|---|---|---|---|
| **LCP** | Largest Contentful Paint | ≤ 2.5s | Loading — time until the largest visible element renders |
| **CLS** | Cumulative Layout Shift | ≤ 0.1 | Visual stability — unexpected layout movement |
| **INP** | Interaction to Next Paint | ≤ 200ms | Responsiveness — delay between user input and visual update |

## 1. LCP (Largest Contentful Paint) checks

Identify the likely LCP element and check for blockers:

### Identify LCP candidate

The LCP element is typically the largest visible element above the fold:
- Hero image (`<img>` near top of `<body>`)
- Hero background image (CSS `background-image`)
- Large heading (`<h1>`) with significant text
- Video poster image

### LCP blockers to flag

| Check | Status |
|---|---|
| Hero/banner `<img>` missing `fetchpriority="high"` | ⚠️ WARN "Add fetchpriority=high to LCP image" |
| Hero image uses `loading="lazy"` | ❌ FAIL "Never lazy-load the LCP element" |
| LCP image not preloaded (`<link rel="preload" as="image">`) | ⚠️ WARN "Preload LCP image for faster rendering" |
| Render-blocking CSS in `<head>` (stylesheets without `media` attribute) | ⚠️ WARN |
| Render-blocking JS in `<head>` (scripts without `async`/`defer`) | ⚠️ WARN |
| LCP image served in legacy format (JPG/PNG instead of WebP/AVIF) | ⚠️ WARN |
| No render-blocking resources | ✅ PASS |

### Font loading

| Check | Status |
|---|---|
| Custom fonts without `<link rel="preload" as="font">` | ⚠️ WARN "Preload critical fonts" |
| No `font-display: swap` or `font-display: optional` in `@font-face` | ⚠️ WARN "Add font-display to prevent invisible text" |
| Fonts preloaded properly | ✅ PASS |

## 2. CLS (Cumulative Layout Shift) checks

Identify HTML patterns that cause layout shift:

| Check | Status |
|---|---|
| `<img>` without `width` and `height` attributes | ❌ FAIL "Missing dimensions cause layout shift" |
| `<video>` or `<iframe>` without `width`/`height` | ⚠️ WARN |
| Ads/embeds without reserved space (no explicit dimensions) | ⚠️ WARN "Reserve space for dynamic content" |
| Web fonts causing FOIT (Flash of Invisible Text) — no `font-display` | ⚠️ WARN |
| Content injected above existing content (banners, cookie notices without reserved space) | ⚠️ WARN |
| All images have dimensions | ✅ PASS "No layout shift from images" |

### CSS animation checks

| Check | Status |
|---|---|
| Animations using `top`, `left`, `width`, `height` (trigger layout) | ⚠️ WARN "Use `transform` instead for animations" |
| Animations using `transform` and `opacity` only | ✅ PASS "GPU-accelerated, no layout shift" |

## 3. INP (Interaction to Next Paint) checks

Identify patterns that block the main thread:

| Check | Status |
|---|---|
| `<script>` tags without `async` or `defer` | ⚠️ WARN "Blocks main thread during parsing" |
| Inline `<script>` with heavy computation (> 50 lines) | ⚠️ WARN "Move heavy JS to async external file" |
| Event handlers in HTML attributes (`onclick`, `onchange`, etc.) | ⚠️ WARN "Use addEventListener instead for better performance" |
| Third-party scripts loaded synchronously | ⚠️ WARN "Load third-party scripts with async" |
| All scripts properly deferred/async | ✅ PASS |

### Third-party impact

Count third-party scripts (different domain):
- 0–3 → ✅ PASS
- 4–8 → ⚠️ WARN "Consider reducing third-party scripts"
- 9+ → ❌ FAIL "Excessive third-party scripts severely impact INP"

## 4. General performance patterns

| Check | Status |
|---|---|
| `<link rel="preconnect">` for third-party origins | ✅ PASS if present, ⚠️ WARN if missing with 3rd-party resources |
| `<link rel="dns-prefetch">` for third-party origins | ✅ PASS if present |
| `<link rel="preload">` for critical resources | ✅ PASS if present |
| Excessive DOM size (> 1500 elements) | ⚠️ WARN "Large DOM slows rendering" |
| `<meta name="viewport">` with `width=device-width` | Required for mobile CWV (see [mobile-optimization](../mobile-optimization/SKILL.md) for full viewport checks) |

## Reporting format

```
Core Web Vitals Audit
─────────────────────
LCP Risk Factors:  X issues found
CLS Risk Factors:  Y issues found
INP Risk Factors:  Z issues found

Overall CWV Risk:  LOW / MEDIUM / HIGH
```

- 0 issues → LOW risk
- 1–3 issues → MEDIUM risk
- 4+ issues → HIGH risk

## Edge cases

- This skill audits HTML patterns that *correlate* with CWV issues — actual CWV scores require real-browser measurement (Lighthouse, CrUX data)
- Next.js automatically handles image optimization, code splitting, and font loading — check for Next.js-specific patterns before flagging generic issues
- Inline `<style>` for critical CSS is intentional and should NOT be flagged as a CLS risk — distinguish from injected layout-shifting styles
- `<script type="module">` is inherently deferred — do not flag as render-blocking
- Third-party scripts loaded inside `<iframe>` do not block the main thread — exclude from INP third-party count
- AMP pages have their own performance model — flag CWV patterns but note that AMP runtime handles many optimizations automatically
