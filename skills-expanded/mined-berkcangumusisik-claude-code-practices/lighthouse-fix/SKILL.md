---
name: lighthouse-fix
description: Analyzes and fixes common Lighthouse performance score issues
argument-hint: [page-url-or-file]
user-invocable: true
allowed-tools: Read Grep Glob Edit Bash
effort: medium
---

## Lighthouse Performance Fixes

Target: **$1**

Since we can't run Lighthouse directly, audit the code for common score killers:

### Performance (LCP, FID, CLS)

**Largest Contentful Paint (LCP):**
```bash
grep -rn "img\|Image\|hero\|banner" src/ --include="*.tsx" | head -10
```
- Hero images not preloaded (`<link rel="preload">` or `priority` prop)
- No explicit `width`/`height` on images (causes layout shift)
- Render-blocking scripts/fonts

**Cumulative Layout Shift (CLS):**
- Images without dimensions
- Dynamic content inserted above existing content
- Fonts causing FOUT (missing `font-display: swap`)

**First Input Delay (FID) / INP:**
- Long tasks on main thread
- Heavy JS in `<head>` without `defer`/`async`

### Accessibility Score
```bash
grep -rn "<img" src/ --include="*.tsx" | grep -v "alt=" | head -10
```
- Missing `alt` on images
- Low color contrast
- Missing form labels

### Best Practices
- Mixed content (HTTP resources on HTTPS page)
- Console errors
- Deprecated APIs

For each finding: show the fix and estimated score improvement.
