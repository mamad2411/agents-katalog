---
name: mobile-optimization
description: >
  Validates viewport meta configuration, responsive design, font sizes, touch target
  sizes, and mobile-hostile patterns. Use when checking mobile-friendliness or fixing
  mobile rendering issues.
license: MIT
metadata:
  author: Muhammad Ahsan Iqbal (https://muhammadahsaniqbal.com)
  linkedin: https://www.linkedin.com/in/ahsan-iqbal-digitalmarketingexpert/
  version: "1.0"
---

# Mobile Optimization

Audit the page for mobile-friendliness.

## 1. Viewport meta tag

| Check | Status |
|---|---|
| Missing `<meta name="viewport">` | ❌ FAIL "Page will not render correctly on mobile" |
| Present but missing `width=device-width` | ⚠️ WARN |
| Contains `user-scalable=no` or `maximum-scale=1` | ⚠️ WARN "Disabling zoom hurts accessibility" |
| Properly configured | ✅ PASS |

## 2. Fixed-width elements

Scan all elements with inline `style="..."` for `width: Npx`:

- If any element has `width > 500px` → ⚠️ WARN "May cause horizontal scrolling on mobile"
- Report the count of offending elements

## 3. Font sizes

Scan inline styles for `font-size: Npx`:

- If any element has `font-size < 12px` → ⚠️ WARN "Difficult to read on mobile"
- Report the count

## 4. Touch target sizes

Check interactive elements (`<a>`, `<button>`, `<input type="submit">`, `<input type="button">`) with inline `height` style:

- If `height < 48px` → ⚠️ WARN "Too small for touch targets"
- Minimum recommended: **48px × 48px** (per Google's mobile-friendly guidelines)

## 5. Overflow detection

- Elements with `overflow-x: hidden` or `overflow: hidden` → ⚠️ WARN "Verify content is not clipped on mobile"

## 6. Responsive stylesheets

- `<link rel="stylesheet" media="...">` found → ✅ PASS "Media-query-specific stylesheets found"

## 7. Tables

- If > 2 `<table>` elements → ⚠️ WARN "Tables can be difficult to read on mobile. Consider responsive table patterns"

## Edge cases

- If no inline styles are present, skip fixed-width and font-size checks
- CSS-in-JS frameworks (styled-components, Emotion) embed styles at runtime — these cannot be audited from static HTML alone; note this limitation
- Elements with `display: none` or `visibility: hidden` should be excluded from touch target checks
- AMP pages have their own viewport rules — flag but do not fail if AMP boilerplate is detected
- PWA splash screens and app-shell patterns may intentionally use `user-scalable=no` — flag as ⚠️ WARN but note context
