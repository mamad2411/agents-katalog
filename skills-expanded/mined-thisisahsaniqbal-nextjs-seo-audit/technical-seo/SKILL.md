---
name: technical-seo
description: >
  Audits sitemap references, robots.txt directives, canonical tags, crawlability,
  URL structure, redirect chains, and indexability. Use when checking technical SEO
  foundations or fixing crawl/index issues.
license: MIT
metadata:
  author: Muhammad Ahsan Iqbal (https://muhammadahsaniqbal.com)
  linkedin: https://www.linkedin.com/in/ahsan-iqbal-digitalmarketingexpert/
  version: "1.0"
---

# Technical SEO

Audit fundamental technical SEO factors that affect crawlability and indexability.

## 1. Canonical URL

| Check | Status |
|---|---|
| `<link rel="canonical">` missing | ⚠️ WARN "Add canonical to prevent duplicate content" |
| Canonical present but empty `href` | ❌ FAIL |
| Canonical points to a different domain | ⚠️ WARN "Cross-domain canonical — verify this is intentional" |
| Canonical is relative (not absolute URL) | ⚠️ WARN "Use absolute URLs for canonical tags" |
| Canonical present and valid | ✅ PASS |
| Multiple canonical tags | ❌ FAIL "Only one canonical allowed per page" |
| Canonical is self-referencing | ✅ PASS (best practice) |

## 2. Robots meta

| Check | Status |
|---|---|
| `<meta name="robots" content="noindex">` | ⚠️ WARN "Page will not appear in search results" |
| `<meta name="robots" content="nofollow">` | ⚠️ WARN "Links on this page will not be followed" |
| `<meta name="robots" content="noindex, nofollow">` | ⚠️ WARN "Page excluded from search entirely" |
| `<meta name="robots" content="index, follow">` or absent | ✅ PASS "Page is indexable" |
| `<meta name="googlebot">` present | ✅ PASS — report its content |

## 3. Robots.txt references

Check if the page references or is affected by robots.txt:

- Look for `<meta name="robots">` directives
- If analysing a full site, check `robots.txt` at site root for:
  - `Disallow` rules that block the current page
  - `Sitemap` directive pointing to sitemap location
  - `Crawl-delay` directives (may slow indexing)

## 4. Sitemap references

| Check | Status |
|---|---|
| `<link rel="sitemap">` present | ✅ PASS |
| No sitemap reference found | ⚠️ WARN "Consider adding sitemap reference" |

If sitemap URL is available, verify:
- Valid XML format
- Contains the current page URL
- No URLs returning 4xx/5xx status codes

## 5. URL structure

Analyse the page URL (from `<link rel="canonical">` or `<meta property="og:url">`):

| Check | Status |
|---|---|
| URL contains uppercase letters | ⚠️ WARN "Use lowercase-only URLs" |
| URL contains underscores | ⚠️ WARN "Use hyphens instead of underscores" |
| URL contains special characters or spaces (encoded `%20`) | ⚠️ WARN "Simplify URL structure" |
| URL exceeds 100 characters | ⚠️ WARN "Keep URLs concise" |
| URL has double slashes (`//path`) | ❌ FAIL "Fix double slashes" |
| URL has trailing slash inconsistency | ⚠️ WARN "Be consistent with trailing slashes" |
| Clean, descriptive, lowercase with hyphens | ✅ PASS |

## 6. HTTP status hints

| Check | Status |
|---|---|
| `<meta http-equiv="refresh" content="0;url=...">` present | ⚠️ WARN "Use 301 redirects instead of meta refresh" |
| Page contains `window.location` redirect in inline script | ⚠️ WARN "JS redirects are not SEO-friendly" |

## 7. Indexability checklist

| Check | Status |
|---|---|
| Has `<title>` tag | Required for indexing |
| Has `<meta name="description">` | Required for SERP snippets |
| Has unique content (not empty `<body>`) | Required |
| Not blocked by `noindex` | Required |
| Has canonical URL | Recommended |
| Is HTTPS (check canonical/og:url) | ⚠️ WARN if HTTP |

## 8. Pagination

| Check | Status |
|---|---|
| `<link rel="prev">` / `<link rel="next">` present | ✅ PASS "Pagination properly marked" |
| Paginated content without prev/next | ⚠️ WARN "Add for multi-page content" |

## 9. Duplicate content signals

| Check | Status |
|---|---|
| Same `<title>` as canonical page but different URL | ⚠️ WARN |
| No canonical + URL has query parameters | ⚠️ WARN "URL parameters may create duplicate pages" |
| Multiple pages with identical meta description | ⚠️ WARN |

## Edge cases

- Next.js app router generates canonical tags automatically via the `metadata` export — audit the rendered HTML output
- `robots.txt` may not be accessible if auditing a single HTML file — note this limitation and skip robots.txt checks
- Pages behind authentication (login walls) may intentionally use `noindex` — flag as ⚠️ WARN but note context
- Single-page applications with client-side routing may have a single canonical URL for all "pages" — flag as ⚠️ WARN
- Staging/preview environments often have `noindex` — distinguish between intentional and accidental noindex when possible
- Pages with `rel="prev"` / `rel="next"` are deprecated by Google (since 2019) but still supported by Bing — note as informational, not FAIL
