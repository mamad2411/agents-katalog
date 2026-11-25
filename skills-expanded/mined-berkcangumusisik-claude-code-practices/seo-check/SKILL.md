---
name: seo-check
description: Audits Next.js/React app for SEO issues - metadata, Open Graph, structured data
argument-hint: [page-path]
user-invocable: true
allowed-tools: Read Grep Glob Edit
effort: medium
---

## SEO Audit

Target: **$1** (or all pages if not specified)

### 1. Metadata
```bash
grep -rn "title\|description\|metadata\|<head" src/app/ src/pages/ --include="*.tsx" | head -20
```

For Next.js App Router, check each `layout.tsx` and `page.tsx`:
- `export const metadata` defined?
- Title is unique per page (not just app name)?
- Description 120-160 chars?
- `robots` config correct?

### 2. Open Graph & Twitter Cards
- `og:title`, `og:description`, `og:image` set?
- `og:image` is 1200×630px?
- Twitter card type set?

### 3. Structured Data
- Homepage: Organization/WebSite schema?
- Blog posts: Article schema?
- Products: Product schema?

### 4. Technical SEO
- Canonical URLs set?
- `sitemap.xml` exists and is registered?
- `robots.txt` not blocking important paths?
- Images have `alt` text?

### 5. Performance (Core Web Vitals)
- Images using `next/image` or `loading="lazy"`?
- Fonts using `font-display: swap`?

Generate missing metadata and structured data. Apply on confirmation.
